import time
import requests
from task_base import TaskBase
from db_access import WorkshopDb
from ir_services import IrSerialServices


class Task08_TvControl(TaskBase):
    during_run = False

    def __init__(self):
        TaskBase.__init__(self, 'TV Control')
        self.db = WorkshopDb()
        self.subnet = self.db.get_config_item("subnet_ip")
        self.static_ip_start = int(self.db.get_config_item("base_ip"))
        self.response_keys = ['name',
                              'number',
                              'temperature',
                              'time',
                              'lights',
                              'tv_state']
        self.port = self.db.get_config_item('serial1')
        self.ser_connection = IrSerialServices.try_open_serial_connection(self.port)
        print('init serial connection 1')

    def try_to_parse_response(self, group_number, response, req_state):
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
                                        tv=response_data['tv_state'])
            if req_state == response_data['tv_state']:
                return 'success'
            return 'Wrong TV state in response'
        return 'Wrong group number'

    def test(self, group_number, points):
        """
        Send HTTP multiple requests to http://IP/television and attempts to parse expected keys
        each request has a different parameter to verify execution
        :return: True if response is valid and all keys were parsed successfully
        """
        if self.during_run:
            self.group_failed(group_number, 'Could not allocate IR receiver')
            return False
        self.during_run = True
        sequences = [
            '?state=on',
            '?state=off',
        ]
        verification_sequences = [
            1,
            0,
        ]
        url_base = 'http://' + self.subnet + str(self.static_ip_start + group_number) + '/television'
        dbg_msg = 'Starting sequence - \n'
        try:
            # check serial connection
            if self.ser_connection is None:
                self.ser_connection = IrSerialServices.try_open_serial_connection(self.port)
            for i in range(0, 2):
                IrSerialServices.try_move_and_start_capture(self.ser_connection, self.db.get_group_degrees(group_number))
                url = url_base + sequences[i]
                dbg_msg += url + '\n'
                response = requests.get(url)
                if response.status_code == 200:
                    message = self.try_to_parse_response(group_number, response, verification_sequences[i])
                    if message != 'success':
                        self.group_failed(group_number, message)
                        self.during_run = False
                        return False
                else:
                    self.group_failed(group_number, 'Could not get a response from ' + url)
                    self.during_run = False
                    return False
                time.sleep(0.5)  # give it a little time...
                dbg_msg += 'got JSON response - checking IR device\n'
                if not IrSerialServices.try_stop_and_search_response(self.ser_connection,
                                                                     group_number,
                                                                     device=1,
                                                                     state=verification_sequences[i]):
                    self.group_failed(group_number, 'IR verification failed')
                    self.during_run = False
                    return False
                dbg_msg += 'success\n'
            dbg_msg += 'TV IR sequence completed'
            self.group_completed(group_number, points, dbg_msg)
            self.during_run = False
            return True
        # true - this is bad practice but everything other than 200 here - is a failure.
        except Exception:
            pass
        self.group_failed(group_number, 'Could not get valid json response from ' + url_base)
        self.during_run = False
        return False


if __name__ == '__main__':
    t = Task08_TvControl()
    print(t.test(11, 5))