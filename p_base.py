import tree
#==
from collections import defaultdict
from math        import cos, sin, radians

class Action(tree.Node):
    def execute(self):
        pass

class Name(tree.Node, tree.OneChildMixin):
    def __init__(self, name, _type):
        tree.Node.__init__(self)
        self.name  = name
        self._type = _type

    def get_data(self):
        return self.children[0] if self.children else None


class Data(tree.Node):
    def __init__(self, value):
        tree.Node.__init__(self)
        self.inactive_views = defaultdict(list)
        self.active_views   = defaultdict(list)
        self.value          = value

    def get_inactive_views(self, key):
        views =  self.inactive_views[key]
        return views.pop() if views else None

    def set_active_view(self, key, view):
        self.active_views[key].append(view)

    def update(self, old, new, sender, transaction):
        for view in sum(self.active_views.values(), []):
            view.notify(old, new, sender, transaction)

    def set_value(self, new_v, sender, transaction):
        if new_v != self.v :
            old_v  = self.v
            self.v = new_v
            self.update(old_v, self.v, sender, transaction)

    def execute(self):
        print "test"

class FakeAction(Data):
    def execute(self):
        print "hello"


class SpinCamera(Action):
    def __init__(self, taskMgr, camera):
        Action.__init__(self)
        self.taskMgr = taskMgr
        self.camera  = camera
        self.started = False

    def execute(self):
        if not self.started:
            self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.started = not self.started
        
    def spinCameraTask(self, task):
        if not started:
            return Task.done
        angle_deg = task.time * 6.0
        angle_rad = radians(angle_deg)
        self.camera.setPos(20 * sin(angle_rad), -20.0 * cos(angle_rad), 3)
        self.camera.setHpr(angle_deg, 0, 0)
        return Task.cont



class Int(Data):
    def __init__(self, v):
        Data.__init__(self, v)


class Mesh3d(Data):
    def __init__(self, path, scale, pos):
        Data.__init__(self,(path, scale, pos)) 


def default():
        d = [ Mesh3d("models/environment", (0.25,0.25,0.25), (-8,42,0)),
              Int(7), 
              FakeAction(None)]
        return d
