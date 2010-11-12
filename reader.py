import p_base
import qtgraph

import random

from PyQt4.QtGui  import *
from PyQt4.QtCore import *


class Reader(object):
    def match(self, obj):
        return isinstance(obj, self._type)

    def read(self, obj):
        if self.match(obj):
            print "catching %s" %self._type
            view = obj.get_inactive_views(self)
            if not view : 
                view = self._read(obj)
            obj.set_active_view(self, view)
            return view
        return obj

class MeshReader(Reader):
    _type = p_base.Mesh3d

    def __init__(self, ctx_panda):
        self.ctx_panda = ctx_panda

    def _read(self, mesh):
        path, scale, pos = mesh.value
        obj = self.ctx_panda.load(path)
        obj.setScale(*scale)
        obj.setPos(*pos)
        return obj

class IntReader(Reader):
    _type = p_base.Int

    def __init__(self, ctx_qt):
        self.ctx_qt = ctx_qt

    def _read(self, int_value):
        btn = MyQSpinBox(int_value, self.ctx_qt)
        self.ctx_qt.layout.addWidget(btn)
        btn.valueChanged.connect(btn._value_changed)
        return btn

class MyQSpinBox(QSpinBox):
    def __init__(self, v, parent):
        QSpinBox.__init__(self, parent)
        self.in_change = False
        self.v = v

    def _value_changed(self, new_int):
        if self.in_change:
            return
        self.v.set_value(new_int, self, None)

    def notify(self, old, new, sender, transaction):
        if sender is self:
            return
        #==
        self.in_change = True
        self.setValue(new)
        self.in_change = False

class ActionReader(Reader):
    _type = p_base.SpinCamera

    def __init__(self, ctx_qt):
        self.ctx_qt = ctx_qt

    def _read(self, int_value):
        btn = MyQPushButton(int_value, self.ctx_qt)
        self.ctx_qt.layout.addWidget(btn)
        btn.clicked.connect(btn._clicked)

class MyQPushButton(QPushButton):
    def __init__(self, v, parent):
        QPushButton.__init__(self, parent)
        self.v = v

    def _clicked(self):
        self.v.execute()

class NodeReader(Reader):

    _type = p_base.Data
    def __init__(self, ctx_qt):
        self.ctx_qt = ctx_qt
        self.graph  = qtgraph.Graph(ctx_qt.view)
        self.done   = False

    def _read(self, any_val):
        if self.done :
            return any_val
        else:
            self.done = True
        size  = 50
        nodes = []
        for i in range(0,500,100):
            for j in range(0,500,100):
                n  = self.graph.drawNode(any_val, size, (i,j))
                if nodes:
                    start = random.choice(nodes)
                    e = self.graph.drawEgde(start, n, size)
                    n.edgeList.append(e)
                    start.edgeList.append(e)
                nodes.append(n)
        #r = qtgraph.getRect(nodes)
        #self.graph.centerScene(r)
        return any_val

def reader_prepare(ctx_panda, ctx_qt):
    r = []
    r.append(MeshReader(ctx_panda))
    r.append(ActionReader(ctx_qt))
    r.append(IntReader(ctx_qt))
    r.append(NodeReader(ctx_qt))
    return r

def read_all(to_read, readers):
    max = 100
    while to_read and max :
        el = to_read.pop()
        for r in readers:
            res = r.read(el)
            if   res is None : break 
            elif res != el   : to_read.append(res)
        max -= 1
