from ..data_structure import tree
from _type import RType, RClass, Name, Index

def error(obj):
    assert False

def create(inst, **kw):
    inst.rtype.get_default()


class ReactiveMeta(type):
    def __new__(cls, name, bases, dct):
        print "Allocating", name
        r_types = {}
        attrs   = {}
        for k, v in dct.iteritems():
            if isinstance(v, RType) : r_types[k] = v
            else                    : attrs[k]   = v
        #==
        T = type.__new__(cls, name, bases, attrs)
        #==
        factory = dct.get('factory_name')
        if factory : r = RClass(factory)
        else       : r = RClass(T)
        #==
        for k, v in r_types.iteritems():
            r.add_attr(k, v)
        T.rtype = r
        #==
        return T


    def __init__(cls, name, bases, dct):
        super(ReactiveMeta, cls).__init__(name, bases, dct)


class Reactive(object):
    __metaclass__ = ReactiveMeta
    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.rnode = self.wrap(self.rtype, self)

    def wrap(self, rtype, naked_instance):
        if isinstance(rtype, Index) and rtype.multi  : 
            assert(len(rtype.children) == 1)
            for idx, el in enumerate(naked_instance):
                node = vIndex(rtype, idx)
                tree.connect(self.wrap(rtype.children[0], el), node)
        elif isinstance(rtype, Name)  : 
            node = vName(rtype)
            assert(len(rtype.children) == 1)
            naked_instance = rtype.extract(naked_instance)
            tree.connect(self.wrap(rtype.children[0], naked_instance), node)
        elif isinstance(rtype, RType) : 
            node = vValue(rtype, naked_instance)
            for c in rtype.children:
                tree.connect(self.wrap(c, naked_instance), node)
        #==
        return node

    @classmethod
    def create(cls, **kw):
        return cls.rtype.get_default()

class Transaction(object):
    def __init__(self, new, old=None, sender=None, _type=None):
        self.new    = new
        self.old    = old
        self.sender = sender
        self.type   = _type


class vValue(tree.Node):
    def __init__(self, rtype, naked_instance):
        self.rtype = rtype
        self.naked_instance = naked_instance
        tree.Node.__init__(self)

    def set_value(self, new, old, sender):
        assert self.naked_instance is old
        if self.rtype.validate(new):
            self.naked_instance = new
        for p in self.parents:
            p.post_set_value(new, old, sender)

    def get_value(self):
        return self.naked_instance

    def reorder_indexes(self):
        for idx, el in enumerate(self.children):
            el.idx = idx


class vName(tree.Node, tree.OneChildMixin):
    def __init__(self, name):
        self.name        = name
        self.listeners   = []
        tree.Node.__init__(self)

    def invariant(self):
        if not self.children or not self.parents:
            return True
        #==
        assert len(self.parents)==1 
        assert isinstance(self.parents[0], vValue)
        assert all(isinstance(c, vValue) for c in self.children)
        assert self.get_only_child().get_value() is self.extract()
        return True
    
    def extract(self):
        return self.name.extract(self.parents[0].naked_instance)

    def notify(self, transaction):
        for l in self.listeners:
            l.notify(transaction)

    def set_value(self, transaction):
        assert self.invariant()
        child = self.get_only_child()
        child.set_value(transaction)
        
    def post_set_value(self, transaction):
        self.name.set(self.parents[0].naked_instance, transaction.new)
        assert self.invariant() # no warranty once we call notify
        self.notify(transaction)

    def get_value(self):
        child     = self.get_only_child()
        result    = child.get_value()
        assert self.invariant()
        return result


class __Symbol():
    pass

Nothing = __Symbol()
RemoveItem = __Symbol()

del __Symbol


class vIndex(vName):
    def __init__(self, name, idx):
        vName.__init__(self, name)
        self.idx = idx

    def set_value(self, transaction):
        if transaction.type is RemoveItem:
            tree.disconnect(self.get_only_child(), self)
            tree.disconnect(self, self.parents[0])
            self.parents[0].reorder_indexes()
        else:
            vName.set_value(self, transaction)

    def extract(self):
        return self.name.extract(self.parents[0].naked_instance, idx=self.idx)
