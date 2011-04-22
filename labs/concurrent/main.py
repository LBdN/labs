import labs.data_structure.tree as tree
from collections import deque
context  ={}

class Operation(tree.Node):

    pass

def order_task(operation_node, acc=None):
    if acc is None : acc = []
    #==
    acc.append(operation_node)
    #==
    nacc = []
    for p in operation_node.parents:
        order_task(p, nacc)
    #==
    return acc


class Tasklist(object):
    def __init__(self):
        self.tasks = []
        self.paused = []

    def add(self, task):
        assert task not in self.tasks
        self.tasks[task.priority] = task

    def update(self, task):
        assert task in self.tasks
        self.tasks[task.priority] = task

    def get(self):
        return self.tasks.pop(0) if self.tasks else None

    def pause(self):
        self.tasks  = []
        self.paused = self.tasks

    def resume(self):
        self.tasks  = self.paused
        self.paused = []

class Task(object):
    def __init__(self, priority, func, params):
        self.func     = func
        self.params   = params
        self.priority = priority

