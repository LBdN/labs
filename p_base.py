from data_structure import tree
import utils
#==
from collections import defaultdict
from math        import cos, sin, radians


class Name(tree.Node, tree.OneChildMixin):
    def __init__(self, name, _type):
        tree.Node.__init__(self)
        self.inactive_views = defaultdict(list)
        self.active_views   = defaultdict(list)
        self.name           = name

    def get_inactive_views(self, key):
        views =  self.inactive_views[key]
        return views.pop() if views else None

    def set_active_view(self, key, view):
        self.active_views[key].append(view)

    def clear_views(self):
        for key in self.active_views:
            actives = self.active_views[key]
            for a in actives :
                a.deactivate()
            self.inactive_views[key].extend(actives)
            self.active_views[key] = []

    def update(self, old, new, sender, transaction):
        for view in sum(self.active_views.values(), []):
            view.notify(old, new, sender, transaction)


class Data(tree.Node):
    def __init__(self, value, _type=None):
        tree.Node.__init__(self)
        self.value = value
        self._type = _type or utils.identity

    def update(self, old, new, sender, transaction):
        for parent in self.parents:
            parent.update(old, new, sender, transaction)

    def set_value(self, new_v, sender, transaction):
        if new_v == self.value:
            return True
        if not self._type(new_v):
            return False
        #==
        old_v      = self.value
        self.value = new_v
        self.update(old_v, self.value, sender, transaction)

    def execute(self):
        print "test"

class List(Data):
    def add_value(self, new_v, sender, transaction):
        if not self._type(new_v):
            return False
        #==
        old_v      = self.value
        self.value = old_v + [new_v]
        self.update(old_v, self.value, sender, transaction)

    def remove_value(self, new_v, sender, transaction):
        pass

    def set_value(self, new_v, sender, transaction):
        pass


class FakeAction(Data):
    def execute(self):
        print "hello"

class Action(tree.Node):
    def execute(self):
        pass

class SpinCamera(Data):
    def __init__(self, taskMgr, camera, Task):
        Data.__init__(self, None)
        self.taskMgr = taskMgr
        self.camera  = camera
        self.started = False
        self.first   = True
        self.Task    = Task

    def execute(self):
        if self.first:
            self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
            self.first = False
        self.started = not self.started
        
    def spinCameraTask(self, task):
        if not self.started:
            return self.Task.cont
        else:
            angle_deg = task.time * 6.0
            angle_rad = radians(angle_deg)
            self.camera.setPos(20 * sin(angle_rad), -20.0 * cos(angle_rad), 3)
            self.camera.setHpr(angle_deg, 0, 0)
            return self.Task.cont


class Int(Data):
    def __init__(self, v):
        Data.__init__(self, v)


class Mesh3d(Data):
    def __init__(self, path, scale, pos):
        Data.__init__(self,(path, scale, pos)) 


def default(taskMgr, camera, Task):
        d = [ Mesh3d("models/environment", (0.25,0.25,0.25), (-8,42,0)),
               #Int(7), 
              FakeAction(None), 
              SpinCamera(taskMgr, camera, Task)]
        return d
