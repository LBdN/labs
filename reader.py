import p_base

from PyQt4.QtGui         import *
from PyQt4.QtCore        import *

class Reader(object):
    def read(self, obj):
        if isinstance(obj, self._type):
            print "catching %s" %self._type
            view = obj.views.get(self)
            if not view : 
                view = self._read(obj)
                obj.views[self] = view
            return self._read(obj)
        print self._type, type(obj)
        return obj

class MeshReader(Reader):
    _type = p_base.Mesh3d

    def __init__(self, loader, parent):
        self.loader = loader
        self.parent = parent

    def _read(self, mesh):
        obj = self.loader.loadModel(mesh.path)
        obj.reparentTo(self.parent)
        obj.setScale(*mesh.scale)
        obj.setPos(*mesh.pos)

class IntReader(Reader):
    _type = p_base.Int

    def __init__(self, container, connect):
        self.container = container
        self.connect   = connect

    def _read(self, IntValue):
        view = int_value.views.get(self)
        if not view:
            btn = MyQPushButton()
            self.container.addWidget(btn)
            self.connect(btn, SIGNAL("clicked()"), int_value.set_value())






class ActionReader(Reader):
    _type = p_base.FakeAction

    def __init__(self, container, connect):
        self.container = container
        self.connect   = connect

    def _read(self, action):
        btn = MyQPushButton()
        btn.setMouseTracking(1)
        self.container.addWidget(btn)
        self.connect(btn, SIGNAL("clicked()"), action.execute)

class MyQPushButton(QPushButton):
    def mouseMoveEvent(self, event): 
        print "on Hover", event.pos().x(), event.pos().y(), event.buttons()
            

def reader_prepare(loader, parent, container, connect):
    r = []
    r.append(MeshReader(loader, parent))
    r.append(ActionReader(container, connect))
    return r

def read_all(to_read, readers):
    max = 100
    while to_read and max :
        el = to_read.pop()
        for r in readers:
            res = r.read(el)
            if   res is None : break 
            elif res != el   : to_read.append(res)
            else             : pass
        max -= 1
