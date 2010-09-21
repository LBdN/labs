import p_base

from PyQt4.QtGui         import *
from PyQt4.QtCore        import *

class Reader(object):
    def read(self, obj):
        if isinstance(obj, self._type):
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

class ActionReader(Reader):
    _type = p_base.FakeAction

    def __init__(self, container, connect):
        self.container = container
        self.connect   = connect

    def _read(self, action):
        btn = QPushButton()
        self.container.addWidget(btn)
        self.connect(btn, SIGNAL("clicked()"), action.execute)
            

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
            if res and res != el : to_read.append(res)
            else                 : break
        max -= 1
