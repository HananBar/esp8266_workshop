import requests
from task_base import TaskBase
from db_access import WorkshopDb


class Task07_Lights(TaskBase):
    def __init__(self):
        TaskBase.__init__(self, 'Light Control')
        self.db = WorkshopDb()
        self.subnet = self.db.get_config_item("subnet_ip")
        self.static_ip_start = int(self.db.get_config_item("base_ip"))
        self.response_keys = ['name',
                              'number',
                              'temperature',
                              'time',
                              'lights']

    def try_to_parse_response(self, group_number, response, req_lights):
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
                                        light3=resp_lights[2])
            if (req_lights[0] == resp_lights[0] or req_lights[0] == 2) and \
               (req_lights[1] == resp_lights[1] or req_lights[1] == 2) and \
               (req_lights[2] == resp_lights[2] or req_lights[2] == 2):
                return 'success'
            return 'Wrong lights in response'
        return 'Wrong group number'

    def test(self, group_number, points):
        """
        Send HTTP multiple requests to http://IP/light and attempts to parse expected keys
        each request has a different parameter to verify execution
        :return: True if response is valid and all keys were parsed successfully
        """
        sequences = [
            '?number=1&state=on',
            '?number=2&state=on',
            '?number=3&state=on',
            '?number=3&state=off',
            '?number=2&state=off',
            '?number=1&state=off'
        ]
        # 2 is don't care (we don't know what the LED value was before we set it)
        verification_sequences = [
            [1, 2, 2],
            [1, 1, 2],
            [1, 1, 1],
            [1, 1, 0],
            [1, 0, 0],
            [0, 0, 0]
        ]
        url_base = 'http://' + self.subnet + str(self.static_ip_start + group_number) + '/light'
        dbg_msg = 'Starting sequence - \n'
        try:
            for i in range(0, 6):
                url = url_base + sequences[i]
                dbg_msg += url + '\n'
                response = requests.get(url)
                if response.status_code == 200:
                    message = self.try_to_parse_response(group_number, response, verification_sequences[i])
                    if message != 'success':
                        self.group_failed(group_number, message)
                        return False
                    dbg_msg += 'success\n'
                else:
                    self.group_failed(group_number, 'Could not get a response from ' + url)
                    return False
            dbg_msg += 'Lights sequence completed'
            self.group_completed(group_number, points, dbg_msg)
            return True
        # true - this is bad practice but everything other than 200 here - is a failure.
        except Exception:
            pass
        self.group_failed(group_number, 'Could not get valid json response from ' + url_base)
        return False


if __name__ == '__main__':
    t = Task07_Lights()
    print(t.test(11, 5))