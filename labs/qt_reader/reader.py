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

class NameReader(Reader):
    def create_scope(self, obj):
        pass

    def _create_scope(self, obj):
        pass

class IndexReader(NameReader):
    def _create_scope(self, obj):
        pass


class MeshReader(Reader):
    _type = p_base.Mesh

    def __init__(self, ctx_panda):
        self.ctx_panda = ctx_panda

    def _read(self, mesh_node, ctx):
        mesh = mesh_node.get_value()
        am   = AbstractMesh(self.ctx_panda)
        Wrapper(mesh_node['scale'], am.notify_scale)
        Wrapper(mesh_node['path'], am.notify_path)
        #obj = self.ctx_panda.load(mesh.path)
        #obj.setScale((mesh.scale, mesh.scale,mesh.scale))
        #obj.setPos(*mesh.pos)
        #Scaler(obj, mesh_node['scale'])
        for idx, c in enumerate(mesh_node['pos'].children[0].children):
            Wrapper(c, am.notify_pos, {'idx':idx})
            #Mover(obj, c, idx)
        mesh_node.init_notification()
        return make_scope(mesh_node, ctx)

class AbstractMesh(object):
    def __init__(self, loader):
        self.loader = loader
        self.mesh   = None

    def notify_path(self, transaction, d=None):
        if self.mesh:
            scale = self.mesh.getScale()
            pos   = self.mesh.getPos()
            self.mesh.removeNode()
        #==
        new_mesh = self.loader.load(transaction.new)
        if self.mesh:
            new_mesh.setScale(scale)
            new_mesh.setPos(pos)
        #==
        self.mesh = new_mesh

    def notify_scale(self, transaction, d=None):
        if not self.mesh:
            pass
        scale = [transaction.new]*3
        self.mesh.setScale(*scale)

    def notify_pos(self, transaction, d=None):
        if not self.mesh:
            pass
        pos = self.mesh.getPos()
        print transaction.new
        pos[d['idx']] = transaction.new
        self.mesh.setPos(pos)

class Wrapper(object):
    def __init__(self, node, func, _dict=None):
        node.register(self)
        self.func  = func
        self._dict = _dict

    def notify(self, transaction):
        self.func(transaction, d=self._dict)

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
        label    = QLabel(str(int_value))
        spin_box = QDoubleSpinBox()
        layout   = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(spin_box)
        #==
        spin_box.setValue(int_value.get_value())
        spin_box.valueChanged.connect(lambda x: int_value.replace(x, True))
        #==
        ctx['layout'].addLayout(layout)
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
        fp = FileProp()
        fp.connect(str_name)
        ctx['layout'].addLayout(fp.layout)
        #==
        return None, None

class FileProp(object):
    def __init__(self):
        self.layout   = QHBoxLayout()
        self.label    = QLabel()
        self.button   = QPushButton("...")
        self.button.clicked.connect(self.choose_path)
        self.layout.addWidget(self.label, 5)
        self.layout.addWidget(self.button, 1)

    def connect(self, v):
        self.target = v
        self.target.register(self)
        self.set_value(str(self.target.get_value()))

    def notify(self, transaction):
        self.set_value(transaction.new)

    def set_value(self, v):
        self.label.setText(v)

    def choose_path(self):
        path = QFileDialog.getOpenFileName( None,
                                        "Open Mesh",
                                        "~",
                                        self.label.tr("Panda Mesh Files (*.egg *.egg.pz *.bam)"))
        if path:
            self.target.replace(str(path), True)


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
