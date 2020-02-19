import time
import random
import requests
from task_base import TaskBase
from db_access import WorkshopDb
from ir_services import IrWebServices, IrNecParser


class Task09_AcControl(TaskBase):

    def __init__(self):
        TaskBase.__init__(self, 'AC Control')
        self.db = WorkshopDb()
        self.subnet = self.db.get_config_item("subnet_ip")
        self.static_ip_start = int(self.db.get_config_item("base_ip"))
        self.response_keys = ['name',
                              'number',
                              'temperature',
                              'time',
                              'lights',
                              'tv_state',
                              'ac_state',
                              'ac_temp']

    def try_to_parse_response(self, group_number, response, req_state, req_temp):
        response_data = {k: '' for k in self.response_keys}
        try:
            json_data = response.json()
        except Exception:  # json parsing exception
            return 'Could not parse JSON response'
        # make sure all keys are here
        for k in self.response_keys:
            try:
                response_data[k] = json_data[k]
            except Exception:
                return 'Could not find key ' + k
        try:
            resp_lights = [
                int(response_data['lights'][0]),
                int(response_data['lights'][1]),
                int(response_data['lights'][2])
            ]
        except:
            return 'Could not parse lights array'
        if int(response_data['number']) == group_number:
            self.db.update_group_fields(group_number,
                                        True,
                                        group_name=response_data['name'],
                                        temp=response_data['temperature'],
                                        group_time=response_data['time'],
                                        light1=resp_lights[0],
                                        light2=resp_lights[1],
                                        light3=resp_lights[2],
                                        tv=response_data['tv_state'],
                                        ac=response_data['ac_state'],
                                        ac_temp=response_data['ac_temp'])
            # in state off - allow any temp
            if (req_state == response_data['ac_state'] and req_state == 0) or \
               (req_state == response_data['ac_state'] and req_temp == int(response_data['ac_temp'])):
                return 'success'
            return 'Wrong AC parameters in response'
        return 'Wrong group number'

    def test(self, group_number, points):
        """
        Send HTTP multiple requests to http://IP/ac and attempts to parse expected keys
        each request has a different parameter to verify execution
        :return: True if response is valid and all keys were parsed successfully
        """
        # since we only get the group number from the server -
        # we use the variable to overload it with the IR capture device number as well
        ir_dev_number = (group_number & 0xff00) >> 8
        group_number = group_number & 0xff
        req_temp = random.randint(16, 25)
        sequences = [
            '?state=on&temperature=' + str(req_temp),
            '?state=off&temperature=' + str(req_temp),
        ]
        verification_sequences = [
            1,
            0,
        ]
        url_base = 'http://' + self.subnet + str(self.static_ip_start + group_number) + '/ac'
        dbg_msg = 'Starting sequence - \n'
        try:
            for i in range(0, 2):
                if not IrWebServices.start_capture(self.subnet + str(ir_dev_number), group_number):
                    self.group_failed(group_number, 'Could not allocate ' + self.subnet + str(ir_dev_number))
                    return False
                url = url_base + sequences[i]
                dbg_msg += url + '\n'
                response = requests.get(url)
                if response.status_code == 200:
                    message = self.try_to_parse_response(group_number, response, verification_sequences[i], req_temp)
                    if message != 'success':
                        self.group_failed(group_number, message)
                        self.during_run = False
                        IrWebServices.release(self.subnet + str(ir_dev_number))
                        return False
                else:
                    self.group_failed(group_number, 'Could not get a response from ' + url)
                    self.during_run = False
                    IrWebServices.release(self.subnet + str(ir_dev_number))
                    return False
                time.sleep(0.5)  # give it a little time...
                dbg_msg += 'got JSON response - checking IR device\n'
                ir_capture = IrWebServices.stop_and_get_capture(self.subnet + str(ir_dev_number))
                inp = IrNecParser()
                if not inp.is_ir_match(ir_capture,
                                       group_number,
                                       device=2,
                                       state=verification_sequences[i],
                                       temperature=req_temp):
                    self.group_failed(group_number, 'IR verification failed')
                    self.during_run = False
                    return False
                dbg_msg += 'success\n'
            dbg_msg += 'AC IR sequence completed'
            self.group_completed(group_number, points, dbg_msg)
            self.during_run = False
            return True
        # true - this is bad practice but everything other than 200 here - is a failure.
        except Exception:
            # in case of exception - release IR device
            IrWebServices.release(self.subnet + str(ir_dev_number))
        self.group_failed(group_number, 'Could not get valid json response from ' + url_base)
        self.during_run = False
        return False


if __name__ == '__main__':
    t = Task09_AcControl()
    group_number = 11
    ir_number = 21
    print(t.test((ir_number << 8) + group_number, 5))