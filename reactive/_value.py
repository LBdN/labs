from ..data_structure import tree

create_types()

def error(obj):
    assert False

def create(inst, **kw):
    inst.rtype.get_default()


class ReactiveMeta(type):
    def __init__(cls, name, bases, dct):
        #==
        factory = attrs.get('factory_name')
        if factory : r = RType(factory)
        else       : r = RType(cls)
        #==
        r_types = {}
        attrs   = {}
        for k, v in dct.iteritems():
            if isinstance(v, RType) : r_types[k] = v
            else                    : attrs[k]   = v
        #==
        for k, v in r_types.iteritems():
            r.add_attr(k, v)
        attrs['rtype'] = r
        #==
        super(ReactiveMeta, cls).__init__(name, bases, attrs)
        #setattr(cls, '__init__', lambda self : )

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

    def get_value(self):
