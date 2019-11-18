from db_access import WorkshopDb
from task_base import TaskBase


class Task02_StaticIp(TaskBase):

    def __init__(self):
        TaskBase.__init__(self, 'Static IP')
        self.db = WorkshopDb()
        self.static_ip_start = int(self.db.get_config_item('base_ip'))

    def test(self, group_number, points):
        mac = self.db.get_group_mac(group_number)
        ip = self.db.get_ip_from_mac(mac)
        if ip != '':
            ip_arr = ip.split('.')
            if int(ip_arr[3]) == (self.static_ip_start + group_number):
                self.db.update_group_fields(group_number, 'Connected - Static IP')
                self.group_completed(group_number, points,
                                     dbg_msg=f'MAC address {mac} found with static IP {ip}\nTask 2 completed')
                return True
        self.group_failed(group_number, 'MAC address does not have the correct IP')
        return False


if __name__ == '__main__':
    t = Task02_StaticIp()
    print(t.test(10, 5))
    print(t.test(11, 5))
