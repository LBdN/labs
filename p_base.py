class Action(object):
    def __init__(self):
        pass

    def execute(self):
        pass

class FakeAction(Action):
    def execute(self):
        print "hello"

from math import cos, sin, radians

class SpinCamera(object):
    def __init__(self, taskMgr, camera):
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

from collections import defaultdict

class Data(object):
    def __init__(self):
        self.views = defaultdict(list)
        pass

    def update(self, old, new, sender, transaction)
            for view in views.values():
                view.notify(old_v, self.v, sender, transaction)

class Int(Data):
    def __init__(self, v):
        Data.__init__(self)
        self.v = v

    def set_value(self, new_v, sender, transaction):
        if new_v != self.v :
            old_v  = self.v
            self.v = new_v
            self.update(old_v, self.v, sender, transaction)



class Mesh3d(object):
    def __init__(self, path, scale, pos):
        self.scale = scale
        self.path  = path
        self.pos   = pos


def default():
        d = [ Mesh3d("models/environment", (0.25,0.25,0.25), (-8,42,0)),
              7, 
              FakeAction()]
        return d

