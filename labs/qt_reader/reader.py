import p_base
import qtgraph

import random

from PyQt4.QtGui  import *
from PyQt4.QtCore import *


class Terminal(object):
    def match(self, obj):
        return True
        return not obj.rvalue().is_container() 

    def read(self, obj, ctx):
        if not self.match(obj):
            return obj, ctx
        #==
        view, new_ctx = self._read(obj, ctx)
        return view, new_ctx

    def _read(self, source, ctx):
        widget = BaseWidget(self.meta)
        widget, source = container_parse(widget, source)
        widget, source = index_parse(widget, source)
        widget, source = name_parse(widget, source)
        widget, source = union_parse(widget, source)
        widget, source = value_parse(widget, source)
        widget, source = list_parse(widget, source)
        #==
        source.register(widget)
        source.init_notification()
        #==
        ctx['layout'].addWidget(widget)
        if not source.rvalue().is_container():
            return None, None
        if source.rvalue().is_container():
            new_ctx                  = ctx.copy()
            new_ctx['layout']        = widget.value_layout
            return source.rvalue().children, new_ctx
        if not source.rvalue().is_union():
            return source.children[0], ctx

class DeleteEvent(object):
    def __init__(self, widget):
        self.widget = widget
    def __call__(self, transaction):
        print "Here"
        self.widget.setParent(None)

class Event(object):
    def __call__(self, transaction):
        print "do nothing"


class BaseWidget(QWidget):
    def __init__(self, meta):
        self.meta = meta
        super(BaseWidget, self).__init__()
        self.name_layout  = None
        self.value_layout = None
        self.tr_replace   = Event()
        self.tr_delete    = Event()
        self.tr_remove    = Event()
        self.tr_append    = Event()

def container_parse(widget, source):
    if source.rvalue().is_container() : 
        layout    = QVBoxLayout(widget)
        #==
        groupbox  = QGroupBox(widget)
        gb_layout = QVBoxLayout()
        groupbox.setLayout(gb_layout)
        layout.addWidget(groupbox)
        widget.value_layout = gb_layout
        #==
        name = QWidget(widget)
        name_layout = QHBoxLayout(name)
        widget.name_layout = name_layout
    else:
        layout    = QHBoxLayout(widget)
        widget.name_layout  = layout
        widget.value_layout = layout
    return widget, source


def index_parse(widget, source):
    #==
    if not source.is_index():
        return widget, source
    #==
    button = QPushButton("-")
    button.setMaximumSize(20, 20)
    button.clicked.connect(lambda x : source.delete(sender=widget))
    widget.name_layout.addWidget(button,1)
    widget.tr_delete = DeleteEvent(widget) #lambda x,w=widget : widget.setParent(None)
    return widget, source

def name_parse(widget, source):
    if source.rvalue().is_container() : title = "%s :: %s" %(source.as_key(), source.rvalue().rtype)
    else                              : title = str(source.as_key())
    label = QLabel(title, parent = widget)
    widget.name_layout.addWidget(label,2)
    return widget, source

def value_parse(widget, source):
    rvalue = source.get_value()
    if isinstance(rvalue, (int, float)):
        spin_box = QDoubleSpinBox(widget)
        spin_box.valueChanged.connect(lambda x: source.replace(x, True))
        widget.value_layout.addWidget(spin_box,7)
        widget.tr_replace = lambda x : spin_box.setValue(x.new)
    elif isinstance(rvalue, str):
        path_widget = PathProp(source)
        widget.value_layout.addWidget(path_widget, 7)
        widget.tr_replace = lambda x : path_widget.path_label.setText(x.new)
    else:
        label = QLabel(str(source.get_value()))
        widget.value_layout.addWidget(label, 7)
    return widget, source

def union_parse(widget, source):
    return widget, source
    #if not source.rvalue().is_union():
        #return widget, source
    #button = QPushButton(">")
    #button.setMaximumSize(20, 20)
    #button.clicked.connect(lambda x : self.change_type(source))
    #widget.tr_replace = lambda x :  x # clear layout, reinspect #widget.setParent(None)
    #widget.name_layout.addWidget(button,1)
        #==

#def change_type(widget, source):
    #union_type  = source.rvalue().rtype
    #active_type = union_type.get_active(source.get_value())
    #idx         = union_type.children.index(active_type)
    #items = map(str, union_type.children)
    #item  = QInputDialog.getItem(widget, "Alternative Types", "choose", items, current=idx)
    #if item:
        #i = items.index(item)
        #new_active_type = union_type.children[i]
        #new_inst = new_active_type.get_default()
        #source.replace(new_inst, widget)


def list_parse(widget, source):
    if not source.rvalue().is_multi_list():
        return widget, source
    #==
    button = QPushButton("+")
    button.clicked.connect(lambda : add_item(source, widget.meta, widget.value_layout))
    widget.value_layout.addWidget(button)
    #==
    return widget, source

def add_item(obj, meta, layout):
    new_item = obj.rvalue().get_new_item()
    obj.append(new_item, True)
    new_wrapped_item = obj.rvalue().children[-1]
    ctx           = {}
    ctx['layout'] = layout
    meta.read_all([(new_wrapped_item, ctx)])

#class TerminalProp(QWidget):

    #def __init__(self, source, parent=None):
        #assert False
        #super(TerminalProp, self).__init__(parent=parent)
        #self.layout  = QHBoxLayout(self)
        #self.name_layout 
        ##==
        #self, source = index_parse(self, source)
        #self, source = name_parse(self, source)
        #self, source = union_parse(self, source)
        #self, source = value_parse(self, source)
        ##==
        #label = QLabel(str(source.as_key()))
        #self.layout.addWidget(label,2)
        ##==
        #if source.rvalue().is_union():
            #stacked = QStackedWidget(self)
            #self.layout.addWidget(stacked)
            #layout = stacked
        #else:
            #layout = self.layout
        #self.right_part(source, layout)
        ##==
        #if source.rvalue().is_union():
            #button = QPushButton(">")
            #button.setMaximumSize(20, 20)
            #button.clicked.connect(lambda x : self.change_type(source))
            #self.layout.addWidget(button,1)
        ##==
        #source.register(self)
        #source.init_notification()

    #def change_type(self, source):
        #union_type  = source.rvalue().rtype
        #active_type = union_type.get_active(source.get_value())
        #idx         = union_type.children.index(active_type)
        #items = map(str, union_type.children)
        #item  = QInputDialog.getItem(self, "Alternative Types", "choose", items, current=idx)
        #if item:
            #i = items.index(item)
            #new_active_type = union_type.children[i]
            #new_inst = new_active_type.get_default()
            #source.replace(new_inst, self)

            #textLabel.setText(text)

    #def right_part(self, source, layout):
        #self.label = QLabel(str(source.get_value()))
        #layout.addWidget(self.label, 7)

    #def tr_replace(self, transaction):
        #self.set_value(transaction.new)

    #def tr_delete(self, transaction):
        #self.setParent(None)

    #def set_value(self, v):
        #self.label.setText(str(v))

#class NumberProp(TerminalProp):

    #def right_part(self, source, layout):
        #self.spin_box = QDoubleSpinBox()
        #self.spin_box.valueChanged.connect(lambda x: source.replace(x, True))
        #layout.addWidget(self.spin_box,7)

    #def set_value(self, new_val):
        #self.spin_box.setValue(new_val)

class PathProp(QWidget):
    def __init__(self, source):
        super(PathProp, self).__init__()
        layout = QHBoxLayout(self)
        self.path_label = QLineEdit(self)
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
            button  = QPushButton("-", parent = self)
            button.setMaximumSize(20, 17)
            button.move(10, 5) 
            button.clicked.connect(lambda x : source.delete(sender=self))
        if source.rvalue().is_multi_list():
            button = QPushButton("+")
            button.clicked.connect(lambda : self.add_item(source))
            self.layout.addWidget(button)
        source.register(self)
        #==
        title        = "%s::%s" %(source.as_key(), source.rvalue().rtype)
        self.label   = QLabel(title, parent = self)
        self.label.move(40, 0) 

    def tr_delete(self, transaction):
        self.setParent(None)

    def tr_append(self, transaction):
        pass

    def tr_remove(self, transaction):
        pass

    def add_item(self, obj):
        new_item = obj.rvalue().get_new_item()
        obj.append(new_item, True)
        new_wrapped_item = obj.rvalue().children[-1]
        ctx           = {}
        ctx['layout'] = self.gb_layout
        self.meta.read_all([(new_wrapped_item, ctx)])
        #==


class NonTerminal(object):
    def match(self, obj):
        return obj.rvalue().is_container()

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
        assert obj.is_name() or not obj.parents
        if not self.match(obj):
            return obj, ctx
        #==
        view, new_ctx = self._read(obj, ctx)
        return view, new_ctx


class Mesh(Reader):
    _type = p_base.Node

    def _read(self, node, ctx):
        mesh_node = node['mesh']
        am   = MeshView(self.meta.panda)
        node.register(am)
        Wrapper(mesh_node['scale'], am.notify_scale)
        Wrapper(mesh_node['path'], am.notify_path)
        for idx, c in enumerate(mesh_node['pos'].children[0].children):
            Wrapper(c, am.notify_pos, {'idx':idx})
        mesh_node.init_notification()
        return node, ctx

class MeshView(object):
    def __init__(self, loader):
        self.loader = loader
        self.mesh   = None

    def tr_delete(self, transaction):
        print "deleted"
        self.mesh.removeNode()

    def tr_replace(self, transaction):
        #managed via the wrappers
        pass

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

    def tr_replace(self, transaction):
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

def io_readers():
    r = [IOReader()]
    return r

class IOReader(Reader):
    def __init__(self, *args):
        Reader.__init__(self, *args)
        self.io_listener = None

    def match(self, obj):
        return obj.is_name() or not obj.parents

    def _read(self, obj, ctx):
        if self.io_listener is None:
            self.io_listener = IOListener(self.meta)
        if not obj.parents:
            self.meta.root = obj
            return obj.children, ctx
        else:
            obj.register(self.io_listener)
            return obj.rvalue().children, ctx

class IOListener(object):
    def __init__(self, meta):
        self.meta = meta

    def tr_delete(self, transaction):
        self.meta.changed()

    def tr_replace(self, transaction):
        self.meta.changed()

    def tr_append(self, transaction):
        self.meta.changed()

    def tr_remove(self, transaction):
        pass

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
        for r in self.readers:
            res, nctx = r.read(el, ctx)
            print "%s :: %s -> %s" %(r, el, res)
            if   res is None : return None 
            elif res != el   : return res, nctx

class IOMetaReader(MetaReader):
    def __init__(self, readers, filepath):
        MetaReader.__init__(self, readers)
        self.filepath = filepath
        self.root     = None
        self.dirty    = True

    def changed(self):
        self.dirty = True

    def write(self):
        if not self.dirty:
            return
        if not self.root:
            return
        _str = to_json(self.root)
        print "%s writing" %_str
        f = open(self.filepath, "w")
        f.write(_str)
        #==
        self.dirty    = False

def to_json(obj):
    import json
    k, v = _to_json(obj)
    return json.dumps(v)

def _to_json(obj):
    if not obj.parents:
        k = 'root'
        v = {}
        for c in obj.children:
            k2, v2 = _to_json(c)
            v[k2] = v2
        return k, v
    #==
    k = obj.as_key()
    if obj.rvalue().is_list():
        v = {}
        v['_type'] = 'multilist' if obj.rvalue().is_multi_list() else 'list'
    elif obj.rvalue().is_container():
        v = {}
        v['_type'] = str(obj.rvalue().rtype)
    else:
        v = obj.get_value()
    #==
    for c in obj.rvalue().children:
        k2, v2 = _to_json(c)
        v[k2] = v2
    #==
    return k, v

class QTMetaReader(MetaReader):
    def __init__(self, readers, panda):
        MetaReader.__init__(self, readers)
        self.panda = panda

