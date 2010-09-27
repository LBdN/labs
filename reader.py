import p_base

from PyQt4.QtGui         import *
from PyQt4.QtCore        import *


class Reader(object):
    def read(self, obj):
        if isinstance(obj, self._type):
            print "catching %s" %self._type
            view = obj.get_inactive_views(self)
            if not view : 
                view = self._read(obj)
            obj.set_active_view(self, view)
            return view
        return obj


class MeshReader(Reader):
    _type = p_base.Mesh3d

    def __init__(self, loader, parent):
        self.loader = loader
        self.parent = parent

    def _read(self, mesh):
        path, scale, pos = mesh.value
        obj = self.loader.loadModel(path)
        obj.reparentTo(self.parent)
        obj.setScale(*scale)
        obj.setPos(*pos)


class IntReader(Reader):
    _type = p_base.Int

    def __init__(self, container, connect):
        self.container = container
        self.connect   = connect

    def _read(self, int_value):
        btn = MyQPushButton(int_value)
        self.container.addWidget(btn)
        #self.connect(btn, SIGNAL("clicked()"), btn.execute)
        #self.connect(btn, SIGNAL("clicked()"), btn, SLOT('execute2()'))
        self.connect(btn, SIGNAL("clicked()"), RAction(int_value, btn), SLOT('execute()'))


class ActionReader(Reader):
    _type = p_base.FakeAction

    def __init__(self, container, connect):
        self.container = container
        self.connect   = connect

    def _read(self, action):
        btn = MyQPushButton(action)
        #btn.setMouseTracking(1)
        self.container.addWidget(btn)
        self.connect(btn, SIGNAL("clicked()"), RAction(action, btn), SLOT('execute()'))

class RAction(QObject):
    def __init__(self, v, parent):
        QObject.__init__(self)
        #QObject.__init__(self, parent)
        self.v = v

    @pyqtSlot()
    def execute(self):
        self.v.execute()


class MyQPushButton(QPushButton):
    def __init__(self, v):
        QPushButton.__init__(self)
        self.v = v

    def mouseMoveEvent(self, event): 
        print "on Hover", event.pos().x(), event.pos().y(), event.buttons()

    #@pyqtSlot()
    #def execute(self):
        #self.v.execute()
            

def reader_prepare(loader, parent, container, connect):
    r = []
    r.append(MeshReader(loader, parent))
    r.append(ActionReader(container, connect))
    r.append(IntReader(container, connect))
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
