import p_base
import qtgraph

import random

from PyQt4.QtGui  import *
from PyQt4.QtCore import *


class Terminal(object):
    def match(self, obj):
        return not obj.rvalue().is_container() 

    def read(self, obj, ctx):
        if not self.match(obj):
            return obj, ctx
        #==
        view, new_ctx = self._read(obj, ctx)
        return view, new_ctx

    def _read(self, obj, ctx):
        rvalue = obj.get_value()
        if isinstance(rvalue, (int, float)):
            prop = NumberProp(obj)
        elif isinstance(rvalue, str):
            prop = PathProp(obj)
        else:
            prop = TerminalProp(obj)
        ctx['layout'].addWidget(prop)
        return None, None

class TerminalProp(QWidget):

    def __init__(self, source, parent=None):
        super(TerminalProp, self).__init__(parent=parent)
        self.layout  = QHBoxLayout(self)
        #==
        if source.is_index():
            button   = QPushButton("-")
            button.setMaximumSize(20, 20)
            self.layout.addWidget(button,1)
        #==
        label    = QLabel(str(source.name))
        self.layout.addWidget(label,2)
        #==
        self.right_part(source, self.layout)
        #==
        source.register(self)
        source.init_notification()

    def right_part(self, source, layout):
        self.label = QLabel(str(source.get_value()))
        layout.addWidget(self.label, 7)

    def notify(self, transaction):
        transaction.affect(self)

    def tr_replace(self, transaction):
        self.set_value(transaction.new)

    def set_value(self, v):
        self.label.setText(str(v))

class NumberProp(TerminalProp):

    def right_part(self, source, layout):
        self.spin_box = QDoubleSpinBox()
        self.spin_box.valueChanged.connect(lambda x: source.replace(x, True))
        layout.addWidget(self.spin_box,7)

    def set_value(self, new_val):
        self.spin_box.setValue(new_val)

class PathProp(TerminalProp):
    def right_part(self, source, layout):
        self.path_label = QLineEdit()
        self.path_label.setReadOnly(True)
        self.path_label.textChanged.connect(lambda x: source.replace(str(x), True))
        self.button      = QPushButton("...")
        self.button.clicked.connect(self.choose_path)
        layout.addWidget(self.path_label, 6)
        layout.addWidget(self.button, 1)

    def set_value(self, v):
        self.path_label.setText(v)

    def choose_path(self):
        path = QFileDialog.getOpenFileName( None,
                                        "Open Mesh",
                                        "~",
                                        self.path_label.tr("Panda Mesh Files (*.egg *.egg.pz *.bam)"))
        if path:
            self.path_label.setText(path)


class ScopeProp(QWidget):

    def __init__(self, source, meta):
        self.meta = meta
        super(ScopeProp, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,10,0,0)
        #==
        self.groupbox  = QGroupBox(self)
        self.gb_layout = QVBoxLayout()
        self.groupbox.setLayout(self.gb_layout)
        self.layout.addWidget(self.groupbox)
        #==
        if source.is_index():
            self.button  = QPushButton("-", parent = self)
            self.button.setMaximumSize(20, 17)
            self.button.move(10, 5) 
        if source.rvalue().is_multilist():
            button = QPushButton("+")
            button.clicked.connect(lambda : self.add_item(source))
            self.layout.addWidget(button)
            #source.register(self)
        #==
        title        = "%s::%s" %(source.name, source.rvalue().rtype)
        self.label   = QLabel(title, parent = self)
        self.label.move(40, 0) 

    def notify(self, tr):
        tr.affect(self)

    def tr_remove(self, transaction):
        self.setParent(None)

    def add_item(self, obj):
        new_item = obj.rvalue().get_new_item()
        obj.append(new_item, True)
        ctx           = {}
        ctx['layout'] = self.gb_layout
        self.meta.read_all([(obj, ctx)])
        #==
        #==
        #widget = ctx['widget']
        #parent = widget.parentWidget()
        #layout = parent.layout()
        #idx    = layout.indexOf(widget)
        #widget.setParent(None)
        ##==
        #new_ctx                  = ctx.copy()
        #new_ctx['layout']        = layout
        #new_ctx['widget']        = parent
        #new_ctx['index']         = idx
        #self.meta.read_all([(obj, new_ctx)])


class NonTerminal(object):
    def match(self, obj):
        return obj.is_container()
        #return not obj.parents or obj.is_container()

    def read(self, obj, ctx):
        if not self.match(obj):
            return obj, ctx
        #==
        view, new_ctx = self._read(obj, ctx)
        return view, new_ctx

    def _read(self, obj, ctx):
        prop = ScopeProp(obj, self.meta)
        ctx['layout'].addWidget(prop)
        new_ctx                  = ctx.copy()
        new_ctx['layout']        = prop.gb_layout
        return obj.rvalue().children, new_ctx

        #if obj.parents[0].is_list():
            #bgb = ScopeProp()
            #groupbox, layout = bgb, bgb.gb_layout
        #else:
            #groupbox, layout = make_scope(str(obj.name) + "::" + str(obj.get_only_child().rtype))
        ##==
        #if 'index' in ctx:
            #ctx['layout'].insertWidget(ctx['index'], groupbox)
        #else:
            #ctx['layout'].addWidget(groupbox)
        ##==
        #new_ctx                  = ctx.copy()
        #new_ctx['layout']        = layout
        #new_ctx['widget']        = groupbox
        #self.for_list(obj, new_ctx)
        #return obj.get_only_child().children, new_ctx

#    def for_list(self, obj, ctx):
        #if obj.rvalue().is_multilist():
            #button = QPushButton("+")
            #button.clicked.connect(lambda : self.add_item(obj, ctx))
            #ctx['layout'].addWidget(button)

    #def add_item(self, obj, ctx):
        #new_item = obj.get_only_child().get_new_item()
        #obj.append(new_item, True)
        #widget = ctx['widget']
        #parent = widget.parentWidget()
        #layout = parent.layout()
        #idx    = layout.indexOf(widget)
        #widget.setParent(None)
        ##==
        #new_ctx                  = ctx.copy()
        #new_ctx['layout']        = layout
        #new_ctx['widget']        = parent
        #new_ctx['index']         = idx
        #self.meta.read_all([(obj, new_ctx)])

class Root(object):
    def match(self, obj):
        return not obj.parents and not obj.is_name() 

    def read(self, obj, ctx):
        if not self.match(obj):
            return obj, ctx
        #==
        view, new_ctx = self._read(obj, ctx)
        return view, new_ctx

    def _read(self, obj, ctx):
        groupbox, layout = make_scope('root' + "::" + str(obj.rtype))
        ctx['layout'].addWidget(groupbox)
        new_ctx           = ctx.copy()
        new_ctx['layout']        = layout
        new_ctx['widget']        = groupbox
        return obj.children, new_ctx


def make_scope(scope_name):
    groupbox  = QGroupBox(scope_name)
    layout    = QVBoxLayout()
    groupbox.setLayout(layout)
    groupbox.setStyleSheet("QGroupBox {border:1px solid #dddddd; padding: 5px 3px 5px 5px; margin-top:5px}\
                            QGroupBox::title {subcontrol-position: left top; color: #333; top: -6px; left:-5px; padding:2px}\ ")
    #==
    return groupbox, layout

class Reader(object):
    def match(self, obj):
        return isinstance(obj.get_value(), self._type)

    def read(self, obj, ctx):
        assert obj.is_name() 
        if not self.match(obj):
            return obj, ctx
        #==
        view, new_ctx = self._read(obj, ctx)
        return view, new_ctx


class Mesh(Reader):
    _type = p_base.Mesh

    def _read(self, mesh_node, ctx):
        mesh = mesh_node.get_value()
        am   = MeshView(self.meta.panda)
        Wrapper(mesh_node['scale'], am.notify_scale)
        Wrapper(mesh_node['path'], am.notify_path)
        for idx, c in enumerate(mesh_node['pos'].children[0].children):
            Wrapper(c, am.notify_pos, {'idx':idx})
        mesh_node.init_notification()
        return mesh_node, ctx

class MeshView(object):
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
        pos[d['idx']] = transaction.new
        self.mesh.setPos(pos)

class Wrapper(object):
    def __init__(self, node, func, _dict=None):
        node.register(self)
        self.func  = func
        self._dict = _dict

    def notify(self, transaction):
        self.func(transaction, d=self._dict)

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

def reader_prepare():
    r = [Root(), Terminal(), Mesh(), NonTerminal()]
    return r

class MetaReader(object):
    def __init__(self, readers, panda):
        self.panda = panda
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
