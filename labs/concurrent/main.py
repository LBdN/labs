import labs.data_structure.tree as tree
from collections import deque
# from multiprocessing import Process, Queue, current_process, freeze_support
context  ={}

# any new connection imply recomputation of the graph topo sort
# any params change imply an update of the task linked to the operation
# any select might change the tas


class Operation(tree.Node):
    """ """
    def __init__(self, func, params, payload):
        super(Operation, self).__init__( cargo = (func, params, payload))
        self.task    = None


def bfs(root):
    todo = [(0, [root])]
    while todo:
        node = todo.pop()
        yield node
        idx = node[0] + 1
        todo.append((idx, node.children))

def indexize(node, idx, visited):
    t = visited.get(node)
    #==
    if t:
        idx =  max(t[0], idx)
    #==
    visited[node] = (idx, node)

def topo_sort(root):
    visited = {}
    for tupl in bfs(root):
        idx, nodes = tupl
        for n in nodes:
            indexize(n, idx, visited)
    #==
    task_list = sorted(visited.values(), key=lambda n : n[0]) 
    return task_list


class Worker(object):
    """object that does the real work"""
    def __init__(self, tasklist):
        super(Worker, self).__init__()
        self.tasklist = tasklist

    def run(self):
        t = self.tasklist.get()
        q = Queue()

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
        self.done     = False

