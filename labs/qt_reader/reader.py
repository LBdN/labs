import p_base
import qtgraph

import random

from PyQt4.QtGui  import *
from PyQt4.QtCore import *


class Reader(object):
    def match(self, obj):
        return isinstance(obj.get_value(), self._type)

    def read(self, obj, ctx):
        assert obj.is_name() or obj.parents == []
        if not self.match(obj):
            return obj, ctx
        #==
        #print "catching %s" %(self._type)
        view, new_ctx = self._read(obj, ctx)
        return view, new_ctx

class MeshReader(Reader):
    _type = p_base.Mesh

    def __init__(self, ctx_panda):
        self.ctx_panda = ctx_panda

    def _read(self, mesh_node, ctx):
        mesh = mesh_node.get_value()
        obj = self.ctx_panda.load(mesh.path)
        obj.setScale((mesh.scale, mesh.scale,mesh.scale))
        obj.setPos(*mesh.pos)
        Scaler(obj, mesh_node['scale'])
        for idx, c in enumerate(mesh_node['pos'].children[0].children):
            Mover(obj, c, idx)
        return make_scope(mesh_node, ctx)

class Scaler(object):
    def __init__(self, mesh, scale_node):
        self.mesh = mesh
        scale_node.register(self)

    def notify(self, transaction):
        scale = [transaction.new]*3
        self.mesh.setScale(*scale)

class Mover(object):
    def __init__(self, mesh, pos_node, idx):
        self.mesh = mesh
        pos_node.register(self)
        self.idx = idx

    def notify(self, transaction):
        pos = self.mesh.getPos()
        pos[self.idx] = transaction.new
        self.mesh.setPos(pos)

class ListReader(Reader):
    _type = list

    def _read(self, list_node, ctx):
        assert list_node.is_name()
        return make_scope(list_node, ctx)

def make_scope(node, ctx):
    hGroupBox = QGroupBox(str(node))
    layout    = QVBoxLayout()
    hGroupBox.setLayout(layout)
    ctx['layout'].addWidget(hGroupBox)
    if node.is_name(): children = node.children[0].children
    else             : children = node.children
    #==
    return children, {'layout' : layout}

class IntReader(Reader):
    _type = float

    def __init__(self, ctx_qt):
        self.ctx_qt = ctx_qt

    def _read(self, int_value, ctx):
        assert int_value.is_name()
        #==
        #hGroupBox = QGroupBox(str(int_value))
        layout = QHBoxLayout()
        #hGroupBox.setLayout(layout)
        #==
        ctx['layout'].addLayout(layout)
        #==
        label    = QLabel(str(int_value))
        spin_box = QDoubleSpinBox()
        layout.addWidget(label)
        layout.addWidget(spin_box)
        #==
        spin_box.setValue(int_value.get_value())
        spin_box.valueChanged.connect(lambda x: int_value.replace(x, True))
        #==
        return None, None

class StrReader(Reader):
    _type = str

    def __init__(self, ctx_qt):
        self.ctx_qt = ctx_qt

    def _read(self, str_name, ctx):
        assert str_name.is_name()
        #==
        layout = QHBoxLayout()
        #==
        label    = QLabel(str(str_name.get_value()))
        ctx['layout'].addWidget(label)
        #==
        return None, None

class NodeReader(Reader):
    _type = p_base.Node

    def __init__(self, ctx_qt):
        self.ctx_qt = ctx_qt
        self.graph  = qtgraph.Graph(ctx_qt.view)
        self.done   = False
        self.nodes  = []

    def _read(self, any_val, ctx):
        n = self.graph.drawNode(any_val, 50, ( len(self.nodes)*50, len(self.nodes)*50))
        self.nodes.append(n)
        return make_scope(any_val, ctx)
        #if self.done :
            #return any_val, ctx
        #else:
            #self.done = True
        #size  = 50
        #nodes = []
        #for i in range(0,500,100):
            #for j in range(0,500,100):
                #n  = self.graph.drawNode(any_val, size, (i,j))
                #if nodes:
                    #start = random.choice(nodes)
                    #e = self.graph.drawEgde(start, n, size)
                    #n.edgeList.append(e)
                    #start.edgeList.append(e)
                #nodes.append(n)
        ##r = qtgraph.getRect(nodes)
        ##self.graph.centerScene(r)
        #return None, ctx

class SelectionReader(Reader):
    _type = (p_base.Selection, p_base.World)

    def __init__(self, ctx_qt):
        self.ctx_qt = ctx_qt

    def prepare(self, meta_reader):
        self.meta_reader = meta_reader

    def _read(self, val, ctx):
        return make_scope(val, ctx)
        

def reader_prepare(ctx_panda, ctx_qt):
    r = []
    r.append(MeshReader(ctx_panda))
    r.append(ListReader())
    r.append(IntReader(ctx_qt))
    r.append(StrReader(ctx_qt))
    r.append(NodeReader(ctx_qt))
    r.append(SelectionReader(ctx_qt))
    return r


class MetaReader(object):
    def __init__(self, readers):
        self.readers = readers
        for r in self.readers:
            r.meta = self

    def read_all(self, to_read):
        max = 100
        while to_read and max :
            el, ctx = to_read.pop()
            if isinstance(el, list):
                for sub_el in el :
                    r= self.read_one(sub_el, ctx)
                    if r is not None :
                        to_read.append(r)
            else:
                r= self.read_one(el, ctx)
                if r is not None :
                    to_read.append(r)

    def read_one(self, el, ctx):
        new_els = []
        for r in self.readers:
            res, nctx = r.read(el, ctx)
            print "%s :: %s -> %s" %(r, el, res)
            if   res is None : return None 
            elif res != el   : return res, nctx
