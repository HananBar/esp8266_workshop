from db_access import WorkshopDb
from task_base import TaskBase


class Task01_Connect(TaskBase):

    def __init__(self):
        TaskBase.__init__(self, 'Connect')
        self.db = WorkshopDb()

    def test(self, group_number, points):
        self.db = WorkshopDb()
        mac = self.db.get_group_mac(group_number)
        ip = self.db.get_ip_from_mac(mac)
        if ip != '':
            self.db.update_group_fields(group_number, 'Connected')
            self.group_completed(group_number, points,
                                 dbg_msg=f'MAC address {mac} found (IP {ip})\nTask 1 completed')
            return True
        self.group_failed(group_number, 'Could not find MAC address in connected devices list')
        return False


if __name__ == '__main__':
    t = Task01_Connect()
    print(t.test(10, 5))
    print(t.test(11, 5))
