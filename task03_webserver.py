import requests
from task_base import TaskBase
from db_access import WorkshopDb


class Task03_WebServer(TaskBase):
    def __init__(self):
        TaskBase.__init__(self, 'Web Server')
        self.db = WorkshopDb()
        self.subnet = self.db.get_config_item("subnet_ip")
        self.static_ip_start = int(self.db.get_config_item("base_ip"))

    def test(self, group_number, points):
        """
        Send HTTP request to IP - check for status 200
        Meaning - server is up and running.
        """
        url = 'http://' + self.subnet + str(self.static_ip_start + group_number) + '/'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.db.update_group_fields(group_number, 'Web Server is up')
                self.group_completed(group_number, points,
                                     dbg_msg=f'HTTP request was responded successfully\n{response.text}\nTask 3 completed')
                return True
        # true - this is bad practice but everything other than 200 here - is a failure.
        except Exception:
            pass
        self.group_failed(group_number, 'Could not get valid HTTP response from ' + url)
        return False


if __name__ == '__main__':
    t = Task03_WebServer()
    print(t.test(11, 5))