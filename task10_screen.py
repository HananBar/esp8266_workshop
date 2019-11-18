from task_base import TaskBase


class Task10_Screen(TaskBase):

    def __init__(self):
        TaskBase.__init__(self, 'Screen')

    def test(self, group_number, points):
        self.group_failed(group_number, 'Manual task - use skip?')
        return False


if __name__ == '__main__':
    t = Task10_Screen()
    print(t.test(10, 5))
