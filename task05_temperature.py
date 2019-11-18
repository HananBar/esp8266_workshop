import time
import requests
from task_base import TaskBase
from db_access import WorkshopDb


class Task05_ApiResponse(TaskBase):
    def __init__(self):
        TaskBase.__init__(self, 'Temperature')
        self.db = WorkshopDb()
        self.subnet = self.db.get_config_item("subnet_ip")
        self.static_ip_start = int(self.db.get_config_item("base_ip"))
        self.response_keys = ['name',
                              'number',
                              'temperature',
                              'time']

    def try_to_parse_response(self, group_number, response):
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
        if int(response_data['number']) == group_number:
            self.db.update_group_fields(group_number,
                                        True,
                                        group_name=response_data['name'],
                                        temp=response_data['temperature'],
                                        group_time=response_data['time'])
            return 'success'
        return 'Wrong group number'

    def test(self, group_number, points):
        """
        Send HTTP request to http://IP/json and attempts to parse expected keys
        :return: True if response is valid and all keys were parsed successfully
        """
        url = 'http://' + self.subnet + str(self.static_ip_start + group_number) + '/json'
        temperature = 0
        try:
            for i in range(1, 4):
                response = requests.get(url)
                if response.status_code == 200:
                    message = self.try_to_parse_response(group_number, response)
                    if message == 'success':
                        temperature += self.db.get_group_temp(group_number)
                    else:
                        self.group_failed(group_number, message)
                        return False
                    time.sleep(0.5)
                else:
                    self.group_failed(group_number, 'Could not get a response from ' + url)
                    return False
            avg_temp = temperature / 3
            temperature = int(temperature / 3)
            if avg_temp != temperature:
                if 15 <= temperature <= 35:
                    self.group_completed(group_number, points,
                                         dbg_msg=f'Valid temperature was received from group {group_number} - ' +
                                                 f'{response.json()["temperature"]}.\nTask 5 completed')
                    return True
                else:
                    self.group_failed(group_number, 'Temperature ' + str(temperature) + ' is not in range 15-35')
                    return False
            else:
                self.group_failed(group_number, 'All temperatures are the same ' + str(temperature) +
                                  '. Try touching sensor while running the test')
                return False
        # true - this is bad practice but everything other than 200 here - is a failure.
        except Exception:
            pass
        self.group_failed(group_number, 'Could not get valid json response from ' + url)
        return False


if __name__ == '__main__':
    t = Task05_ApiResponse()
    print(t.test(11, 5))