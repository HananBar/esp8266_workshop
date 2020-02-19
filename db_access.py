from pymongo import MongoClient
from config_manager import ConfigManager


class WorkshopDb:
    _group_keys = [
        'number',
        'name',
        'current_task',
        'points',
        'is_online',
        'is_light_1_on',
        'is_light_2_on',
        'is_light_3_on',
        'is_ac_on',
        'ac_temp',
        'is_tv_on',
        'current_temp',
        'current_time',
        'acc_time',
        'dgb_msg',
        'degrees',
        'mac'
    ]

    _tasks = [
        {'name': '01. Connect',       'mode': 'MODE_AUTO'},
        {'name': '02. Static IP',     'mode': 'MODE_AUTO'},
        {'name': '03. Web Server',    'mode': 'MODE_AUTO'},
        {'name': '04. API response',  'mode': 'MODE_AUTO'},
        {'name': '05. Temperature',   'mode': 'MODE_AUTO'},
        {'name': '06. Time',          'mode': 'MODE_AUTO'},
        {'name': '07. Light Control', 'mode': 'MODE_SEMI'},
        {'name': '08. TV Control',    'mode': 'MODE_AUTO'},
        {'name': '09. AC Control',    'mode': 'MODE_AUTO'},
        {'name': '10. Screen',        'mode': 'MODE_MANUAL'},
    ]

    _config = [
        'serial1',
        'serial2',
        'base_ip',
        'subnet_ip',
        'dynamic_ip',
        'groups_number',
    ]

    _number_of_groups = 20

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')

    def reset(self):
        # remove db collection
        self.client.drop_database('esp8266_workshop')
        # create a new db
        db_handle = self.client['esp8266_workshop']
        # create rooms collection and init values
        config = ConfigManager()
        groups_collection = db_handle['groups']
        group_list = []
        for group in range(1, self._number_of_groups + 1):
            new_group = {key: 0 for key in self._group_keys}
            new_group['number'] = group
            new_group['current_task'] = 1
            new_group['name'] = ''
            new_group['dbg_msg'] = ''
            new_group['degrees'] = config.get_group_degrees(group)
            new_group['mac'] = config.get_group_mac_address(group)
            group_list.append(new_group)
        groups_collection.insert_many(group_list)
        # create tasks collection and init values
        tasks_collection = db_handle['tasks']
        for task in self._tasks:
            new_task = {'name': task['name'],
                        'mode': task['mode'],
                        'completed_by': ''}
            tasks_collection.insert_one(new_task)
        # create config collection and init values
        config_collection = db_handle['config']
        for config_item in self._config:
            new_config = {'name': config_item,
                          'value': config.get_item(config_item)}
            config_collection.insert_one(new_config)
        devices_ip_collection = db_handle['devices_ip']
        devices_ip_list = []
        for group in range(1,self._number_of_groups + 1):
            devices_ip_list.append({'mac': config.get_group_mac_address(group),
                                    'ip': ''})
        devices_ip_collection.insert_many(devices_ip_list)

    def advance_group_task(self, group_number, current_task, task_name, task_time, points, dbg_msg=''):
        db_handle = self.client['esp8266_workshop']
        groups_collection = db_handle['groups']
        group_query = {'number': group_number}
        groups = []
        if dbg_msg == '':
            dbg_msg = f'Task {task_name} completed'
        for g in groups_collection.find(group_query, {'_id': 0}):
            groups.append(g)
        if len(groups) > 0:
            if groups[0]['current_task'] == current_task:
                # update db
                new_values = {'$set': {'current_task': groups[0]['current_task'] + 1,
                                       'points': groups[0]['points'] + points,
                                       'acc_time': groups[0]['acc_time'] + task_time,
                                       'dbg_msg': dbg_msg}}
                groups_collection.update_one(group_query, new_values)
                # check if this is the first group to complete - save its' number
                tasks_collection = db_handle['tasks']
                task_query = {'name': task_name}
                tasks = []
                for t in tasks_collection.find(task_query, {'_id': 0}):
                    tasks.append(t)
                if len(tasks) > 0:
                    if tasks[0]['completed_by'] == '':
                        new_values = {'$set': {'completed_by': group_number}}
                        tasks_collection.update_one(task_query, new_values)

    def group_add_bonus(self, group_number, points, dbg_msg=''):
        db_handle = self.client['esp8266_workshop']
        groups_collection = db_handle['groups']
        group_query = {'number': group_number}
        groups = []
        if dbg_msg == '':
            dbg_msg = f'{points} bonus points awarded'
        for g in groups_collection.find(group_query, {'_id': 0}):
            groups.append(g)
        if len(groups) > 0:
            # update db
            new_values = {'$set': {'points': groups[0]['points'] + points,
                                   'dbg_msg': dbg_msg}}
            groups_collection.update_one(group_query, new_values)

    def update_group_debug(self, group_number, dbg_msg):
        db_handle = self.client['esp8266_workshop']
        groups_collection = db_handle['groups']
        group_query = {'number': group_number}
        groups = []
        for g in groups_collection.find(group_query, {'_id': 0}):
            groups.append(g)
        if len(groups) > 0:
            new_values = {'$set': {'dbg_msg': dbg_msg}}
            groups_collection.update_one(group_query, new_values)

    def get_group_mac(self, group_number):
        db_handle = self.client['esp8266_workshop']
        groups_collection = db_handle['groups']
        group_query = {'number': group_number}
        groups = []
        for g in groups_collection.find(group_query, {'_id': 0}):
            groups.append(g)
        mac = ''
        if len(groups) > 0:
            mac = groups[0]['mac']
        return mac

    def get_group_temp(self, group_number):
        db_handle = self.client['esp8266_workshop']
        groups_collection = db_handle['groups']
        group_query = {'number': group_number}
        groups = []
        for g in groups_collection.find(group_query, {'_id': 0}):
            groups.append(g)
        mac = ''
        if len(groups) > 0:
            mac = groups[0]['current_temp']
        return mac

    def get_group_degrees(self, group_number):
        db_handle = self.client['esp8266_workshop']
        groups_collection = db_handle['groups']
        group_query = {'number': group_number}
        groups = []
        for g in groups_collection.find(group_query, {'_id': 0}):
            groups.append(g)
        degrees = 90
        if len(groups) > 0:
            degrees = groups[0]['degrees']
        return degrees

    def get_ip_from_mac(self, mac):
        db_handle = self.client['esp8266_workshop']
        devices_ip_collection = db_handle['devices_ip']
        device_query = {'mac': mac}
        devices_ip_list = []
        for d in devices_ip_collection.find(device_query, {'_id': 0}):
            devices_ip_list.append(d)
        ip = ''
        if len(devices_ip_list) > 0:
            ip = devices_ip_list[0]['ip']
        return ip

    def update_mac_ip(self, mac, ip):
        db_handle = self.client['esp8266_workshop']
        devices_ip_collection = db_handle['devices_ip']
        device_query = {'mac': mac}
        devices_ip_list = []
        for d in devices_ip_collection.find(device_query, {'_id': 0}):
            devices_ip_list.append(d)
        if len(devices_ip_list) > 0:
            new_values = {'$set': {'ip': ip}}
            devices_ip_collection.update_one(device_query, new_values)

    def update_group_fields(self, group_number, online, group_name='', light1=-1, light2=-1, light3=-1,
                            tv=-1, ac=-1, ac_temp=-1, temp=-1, group_time='00:00'):
        db_handle = self.client['esp8266_workshop']
        groups_collection = db_handle['groups']
        group_query = {'number': group_number}
        groups = []
        for g in groups_collection.find(group_query, {'_id': 0}):
            groups.append(g)
        if len(groups) > 0:
            if light1 == -1:
                light1 = groups[0]['is_light_1_on']
            if light2 == -1:
                light2 = groups[0]['is_light_2_on']
            if light3 == -1:
                light3 = groups[0]['is_light_3_on']
            if tv == -1:
                tv = groups[0]['is_tv_on']
            if ac == -1:
                ac = groups[0]['is_ac_on']
            if ac_temp == -1:
                ac_temp = groups[0]['ac_temp']
            if temp == -1:
                temp = groups[0]['current_temp']
            if group_name == '':
                group_name = groups[0]['name']

            new_values = {'$set': {'is_online': online,
                                   'name': group_name,
                                   'is_light_1_on': light1,
                                   'is_light_2_on': light2,
                                   'is_light_3_on': light3,
                                   'is_tv_on': tv,
                                   'is_ac_on': ac,
                                   'ac_temp': ac_temp,
                                   'current_temp': temp,
                                   'current_time': group_time}}
            groups_collection.update_one(group_query, new_values)

    def get_current_tasks(self):
        db_handle = self.client['esp8266_workshop']
        groups_collection = db_handle['groups']
        tasks = []
        for g in groups_collection.find({}, {'_id': 0}):
            task = g['current_task']
            if task not in tasks:
                tasks.append(task)
        return tasks

    def get_groups_in_task(self, task_number):
        db_handle = self.client['esp8266_workshop']
        groups_collection = db_handle['groups']
        groups = []
        for g in groups_collection.find({'current_task': task_number}, {'_id': 0}):
            groups.append(g['number'])
        return groups

    def get_task_name(self, task_short_name):
        db_handle = self.client['esp8266_workshop']
        tasks_collection = db_handle['tasks']
        tasks = []
        for t in tasks_collection.find({}, {'_id': 0}):
            tasks.append(t)
        for task in tasks:
            if task['name'].find(task_short_name) != -1:
                return task['name']
        return '00. Unknown'

    def get_config_item(self, config_item_name):
        db_handle = self.client['esp8266_workshop']
        config_collection = db_handle['config']
        configs = []
        for c in config_collection.find({}, {'_id': 0}):
            configs.append(c)
        for config_item in configs:
            if config_item['name'] == config_item_name:
                return config_item['value']
        return ''

    def reload_yaml(self):
        config = ConfigManager()
        config.reload_yaml()
        db_handle = self.client['esp8266_workshop']
        # update all groups mac address and degrees
        groups_collection = db_handle['groups']
        for group in range(1, self._number_of_groups + 1):
            group_query = {'number': group}
            groups = []
            for g in groups_collection.find(group_query, {'_id': 0}):
                groups.append(g)
            if len(groups) > 0:
                new_values = {'$set': {'mac': config.get_group_mac_address(group),
                                       'degrees': config.get_group_degrees(group)}}
                groups_collection.update_one(group_query, new_values)
        db_handle.drop_collection('config')
        config_collection = db_handle['config']
        for config_item in self._config:
            new_config = {'name': config_item,
                          'value': config.get_item(config_item)}
            config_collection.insert_one(new_config)
        db_handle.drop_collection('devices_ip')
        devices_ip_collection = db_handle['devices_ip']
        devices_ip_list = []
        for group in range(1,self._number_of_groups + 1):
            devices_ip_list.append({'mac': config.get_group_mac_address(group),
                                    'ip': ''})
        devices_ip_collection.insert_many(devices_ip_list)


if __name__ == '__main__':
    db = WorkshopDb()
    db.reset()
    print(db.get_current_tasks())
