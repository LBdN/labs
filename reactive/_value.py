from ..data_structure import tree
from _type import RType, RClass

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
        #return type.__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(ReactiveMeta, cls).__init__(name, bases, dct)

#def ReactiveMeta( name, bases, dct):
    ##super(ReactiveMeta, cls).__init__(name, bases, attrs)
    #return type( name, bases, attrs)
        ##setattr(cls, '__init__', lambda self : )

class Reactive(object):
    def __init__(self, **kw):
        self.rtype.get_default()

class IName(tree.Node):
    def __init__(self, name, annotations):
        self.name        = name
        self.annotations = annotations
        self.listeners   = []

    def notify(self, old_val, new_val, sender, transaction):
        for l in self.listeners:
            l.notify(old_val, new_val, sender, transaction)

class RValue(tree.Node):
    def __init__(self, rtype):
        self.rtype = rtype

    def set_value(self, sender, old, new):
        pass

    def get_value(self):
        pass
