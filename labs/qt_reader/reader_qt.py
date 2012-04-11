
from PyQt4.QtGui  import *
from PyQt4.QtCore import *

from reader import MetaReader


class Terminal(object):
    def match(self, obj):
        return True

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
        print "%s registering on %s" %(widget, source.full_name())
        #==
        #if not source.rvalue().is_union() :
            #source.lock()
        #==
        ctx['layout'].addWidget(widget)
        #==
        if source.rvalue().is_union() :
            rvalue = source.rvalue().children[0]
        else :
            rvalue = source.rvalue()
        #==
        if rvalue.is_container():
            new_ctx                  = ctx.copy()
            new_ctx['layout']        = widget.value_layout
            return rvalue.children, new_ctx
        else:
            return None, None

class DeleteEvent(object):
    def __init__(self, widget):
        self.widget = widget
    def __call__(self, transaction):
        self.widget.setParent(None)

class MultiEvent(object):

    def __init__(self, widget):
        self.widget    = widget
        self.callables = []

    def __call__(self, transaction):
        if transaction.sender is self.widget:
            return
        for c in self.callables:
            res = c(transaction)

    def __iadd__(self, callable):
        self.callables.append(callable)
        return self

    def clear(self):
        self.callables = []

class UnionReplace(object):
    def __init__(self, widget):
        self.widget = widget

    def __call__(self, transaction):
        self.widget.clear()
        #==
        ctx       = {'layout' : self.widget.value_layout}
        union_val = transaction.target.rvalue()
        if union_val.is_container():
            next_vals = union_val.children[0].children
            self.widget.meta.read_all([(next_vals, ctx)])
        else:
            # the union is send as if it was a name, 
            # it supports the methods that creates transaction
            value_parse(self.widget, union_val) 

class BaseWidget(QWidget):
    def __init__(self, meta):
        self.meta = meta
        super(BaseWidget, self).__init__()
        self.name_layout  = None
        self.value_layout = None
        self.tr_replace     = MultiEvent(self)
        self.tr_delete      = MultiEvent(self)
        self.tr_remove      = MultiEvent(self)
        self.tr_append      = MultiEvent(self)
        self.tr_change_type = MultiEvent(self)
        #==
        self.name = ''

    def clear(self):
        widgets = [self.value_layout.itemAt(i).widget() for i in range(0, self.value_layout.count())]
        for w in widgets :
            w.setParent(None)
        self.tr_replace.clear()
        self.tr_delete.clear()
        self.tr_remove.clear()
        self.tr_append.clear()
        self.tr_change_type.clear()

    def __repr__(self):
        return "%s:%s (id:%s)" %(self.__class__.__name__, self.name, id(self))


def container_parse(widget, source):
    if source.rvalue().is_container() : 
        layout    = QVBoxLayout(widget)
        #==
        groupbox  = QGroupBox(widget)
        if source.rvalue().is_list() and not source.rvalue().is_multi_list() :
            gb_layout = QHBoxLayout()
        else:
            gb_layout = QVBoxLayout()
        groupbox.setLayout(gb_layout)
        layout.addWidget(groupbox)
        widget.value_layout = gb_layout
        #==
        name               = QWidget(widget)
        name_layout        = QHBoxLayout(name)
        widget.name_layout = name_layout
    else:
        layout             = QHBoxLayout(widget)
        widget.name_layout = QHBoxLayout()
        layout.addLayout(widget.name_layout)
        widget.value_layout = QHBoxLayout()
        layout.addLayout(widget.value_layout, 1)
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
    widget.tr_delete += DeleteEvent(widget) #lambda x,w=widget : widget.setParent(None)
    return widget, source

def name_parse(widget, source):
    if source.rvalue().is_container() : title = "%s :: %s" %(source.as_key(), source.rvalue().rtype)
    else                              : title = str(source.as_key())
    label = QLabel(title, parent = widget)
    widget.name_layout.addWidget(label,2)
    return widget, source

def pprint(tr, widget):
    #print type(tr), tr
    #if tr.old is None:
        #return
    #elif tr.sender is widget:
        #return
    #else:
        #debug_func()
    #print tr, widget
    pass

def value_parse(widget, source):
    if source.rvalue().is_container():
        return widget, source
    #==
    print source.full_name()
    rvalue = source.get_value()
    if isinstance(rvalue, float):
        spin_box = QDoubleSpinBox(widget)
        spin_box.valueChanged.connect(lambda x, widget=widget: source.replace(x, widget))
        widget.value_layout.addWidget(spin_box,7)
        widget.tr_replace += lambda x, widget=widget : pprint(x, widget)
        widget.tr_replace += lambda x : spin_box.setValue(x.new)
    elif isinstance(rvalue, int):
        spin_box = QSpinBox(widget)
        spin_box.valueChanged.connect(lambda x: source.replace(int(x), widget))
        widget.value_layout.addWidget(spin_box,7)
        widget.tr_replace += lambda x : spin_box.setValue(x.new)
    elif isinstance(rvalue, str):
        path_widget = PathProp(source)
        widget.value_layout.addWidget(path_widget, 7)
        widget.tr_replace += lambda x : path_widget.path_label.setText(x.new)
    else:
        label = QLabel(str(rvalue))
        widget.value_layout.addWidget(label, 7)
    return widget, source

def union_parse(widget, source):
    if not source.rvalue().is_union():
        return widget, source
    button = QPushButton(">")
    button.setMaximumSize(20, 20)
    button.clicked.connect(lambda x : change_type(widget, source))
    widget.tr_change_type += UnionReplace(widget)
    widget.name_layout.addWidget(button,1)
    return widget, source

def change_type(widget, source):
    union_type  = source.rvalue().rtype
    active_type = union_type.get_active(source.get_value())
    idx         = union_type.children.index(active_type)
    items       = map(str, union_type.children)
    item, ok    = QInputDialog.getItem(widget, "Alternative Types", "choose", items, current = idx)
    if ok and item:
        i               = items.index(str(item))
        new_active_type = union_type.children[i]
        new_inst        = new_active_type.get_default()
        tr              = source.change_type(new_inst, widget)


def list_parse(widget, source):
    if not source.rvalue().is_multi_list():
        return widget, source
    #==
    button = QPushButton("+")
    button.clicked.connect(lambda : add_item(source, widget.meta, widget.value_layout))
    widget.tr_append  += AddItem(widget)
    widget.tr_replace += Replace(widget)
    widget.value_layout.addWidget(button)
    #==
    return widget, source

class Replace(object):

    def __init__(self, widget):
        self.widget = widget

    def __call__(self, tr):
        if tr.old is None:
            # to avoid the Init case
            # as Init is a replace, the element in the list that wre already visited
            # because there were already there, were visited again.
            return
        self.widget.clear()
        list_parse(self.widget, tr.target)
        ctx     = {'layout' : self.widget.value_layout}
        new_wrapped_item = tr.target.rvalue().children
        self.widget.meta.read_all([(new_wrapped_item, ctx)], seen=set([]))

class AddItem(object):
    def __init__(self, widget):
        self.widget = widget

    def __call__(self, tr):
        new_wrapped_item = tr.target.rvalue().children[-1]
        ctx           = {}
        ctx['layout'] = self.widget.value_layout
        self.widget.meta.read_all([(new_wrapped_item, ctx)])

def add_item(obj, meta, layout):
    new_item = obj.rvalue().get_new_item()
    obj.append(new_item, True)

class PathProp(QWidget):
    def __init__(self, source):
        super(PathProp, self).__init__()
        layout = QHBoxLayout(self)
        self.path_label = QLineEdit(self)
        self.path_label.setReadOnly(True)
        self.path_label.textChanged.connect(lambda x: source.replace(str(x), True))
        self.button     = QPushButton("...")
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
        new_ctx['layout'] = layout
        new_ctx['widget'] = groupbox
        return obj.children, new_ctx


def make_scope(scope_name):
    groupbox  = QGroupBox(scope_name)
    layout    = QVBoxLayout()
    groupbox.setLayout(layout)
    groupbox.setStyleSheet("QGroupBox {border:1px solid #dddddd; padding: 5px 3px 5px 5px; margin-top:5px}\
                            QGroupBox::title {subcontrol-position: left top; color: #333; top: -6px; left:-5px; padding:2px}\ ")
    #==
    return groupbox, layout

def reader_prepare():
    r = [Root(), Terminal()]
    return r

class QTMetaReader(MetaReader):
    pass
