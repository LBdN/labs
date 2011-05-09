import labs.data_structure.tree as tree

# from multiprocessing import Process, Queue, current_process, freeze_support
# any new connection imply recomputation of the graph topo sort
# any params change imply an update of the task linked to the operation
# any select might change the tas

class Operation(tree.Node):
    """ """
    def __init__(self, type_id, params):
        super(Operation, self).__init__( cargo = params)
        self.done    = False
        self.payload = None
        self.type_id = type_id

    def send_result(self, result):
        self.done = True
        self.payload = result

    def get_target(self):
        return [p.payload for p in self.parents]

    def as_task(self):
        return Task(self)


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

class Chief(object):
    def __init__(self, tasklist, workers):
        self.tasklist = tasklist
        self.workers  = workers
        self.active   = False

    def next(self):
        if not self.active:
            return
        if not self.workers:
            return
        task = self.tasklist.get()
        if not task:
            return
        for w in self.workers:
            if w.match(task):
                w.do_task(task)
                break

    def done(self, worker, task):
        self.tasklist.done(task)


class TaskSystem(object):
    def __init__(self, tasklists, chiefs):
        self.tasklists = tasklists
        self.chiefs = chiefs

    def pause(self):
        for c in self.chiefs:
            c.active = False

    def clear(self):
        pass


class Tasklist(object):
    def __init__(self):
        self.tasks       = []
        self.in_progress = []

    def get(self):
        if not self.tasks:
            return None
        #==
        task = self.tasks.pop(0)
        self.in_progress.apprend(task)
        task.on_start()
        return task

    def done(self, task):
        assert task in self.in_progress
        self.in_progress.remove(task)
        task.on_done()

class Task(object):
    def __init__(self, creator, params):
        self.creator   = creator
        self.params   = params
        self.target   = None
        self.result   = None

    def on_start(self):
        self.target = self.creator.get_target()

    def on_done(self):
        assert self.result
        self.creator.send_result(self.result)
