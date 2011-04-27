import labs.data_structure.tree as tree

# from multiprocessing import Process, Queue, current_process, freeze_support
# any new connection imply recomputation of the graph topo sort
# any params change imply an update of the task linked to the operation
# any select might change the tas

class UserOperation(tree.Node):
    def __init__(self, func, params, payload):
        pass

    def as_Operation(self):
        in_op = Operation()
        out_op = Operation()
        return in_op, out_op

class Operation(tree.Node):
    """ """
    def __init__(self, func, params, payload):
        super(Operation, self).__init__( cargo = (func, params, payload))

    def do(self):
        #merge parent payload
        pass


def tarjan(root, elements):
    nb_parents = {}
    for el in elements:
        nb_parents[el] = len(el.parents)
    #==
    roots     = [[root]]
    task_list = []
    while roots:
        root = roots.pop(0)
        task_list.append(root)
        for node in root.children:
            nb_parents[node] = nb_parents[node] - 1
            if nb_parents[node] == 0:
                roots.append(node)
    return task_list

def tarjan_par(root, elements):
    nb_parents = {}
    for el in elements:
        nb_parents[el] = len(el.parents)
    #==
    all_roots = [[root]]
    task_list = []
    while all_roots:
        roots = all_roots.pop(0)
        task_list.append(roots)
        new_roots = []
        for root in roots:
            for node in root.children:
                nb_parents[node] = nb_parents[node] - 1
                if nb_parents[node] == 0:
                    new_roots.append(node)
        if new_roots:
            all_roots.append(new_roots)
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

