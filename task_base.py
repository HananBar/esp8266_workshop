import time
from db_access import WorkshopDb


class TaskBase:
    def __init__(self, task_name):
        self.db = WorkshopDb()
        self._task_name_in_db = self.db.get_task_name(task_name)
        self._task_number = int(self._task_name_in_db.split('.')[0])
        self.start_time = time.time()

    def group_completed(self, group_number, points, dbg_msg=''):
        if group_number in self.db.get_groups_in_task(self._task_number):
            # advance and don't remove
            self.db.advance_group_task(group_number,
                                       self._task_number,
                                       self._task_name_in_db,
                                       int(round(time.time() - self.start_time, 0)),
                                       points,
                                       dbg_msg)
            print(f'task {self._task_name_in_db}, completed by group {group_number}')
        else:
            self.db.update_group_debug(group_number, dbg_msg)
            print(f'task {self._task_name_in_db}, completed by group {group_number} - db not updated - debug mode?')

    def group_failed(self, group_number, dbg_msg):
        self.db.update_group_debug(group_number, dbg_msg)
        print(f'task {self._task_name_in_db}, group {group_number} failed - {dbg_msg}')