import _value 
import _type 
from ..data_structure import tree

class ReactiveMeta(type):
    def __new__(cls, name, bases, dct):
        print "Allocating", name
        r_types = {}
        attrs   = {}
        for k, v in dct.iteritems():
            if isinstance(v, _type._Type) : r_types[k] = v
            else                    : attrs[k]   = v
        #==
        T = type.__new__(cls, name, bases, attrs)
        #==
        factory = dct.get('factory_name')
        if factory : r = _type._Class(factory)
        else       : r = _type._Class(T)
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
        nodes = wrap(self.rtype, self)
        assert len(nodes) == 1
        self.rnode = nodes[0]

    @classmethod
    def create(cls, **kw):
        return cls.rtype.get_default()

def wrap(rtype, naked_instance):
    if hasattr(naked_instance,"rnode"):
        return [naked_instance.rnode]
    #==
    if isinstance(rtype, _type.Index) and rtype.multi  : 
        assert(len(rtype.children) == 1)
        nodes = []
        for idx, el in enumerate(naked_instance):
            node = _value.Index(rtype, idx)
            nodes.append(node)
            vValues = wrap(rtype.children[0], el)
            for v in vValues:
                tree.connect(v, node)
    elif isinstance(rtype, _type.Name): 
        nodes = [_value.Name(rtype)]
        assert(len(rtype.children) == 1)
        sub_instance = rtype.extract(naked_instance)
        vNames = wrap(rtype.children[0], sub_instance)
        for vName in vNames:
            tree.connect(vName, nodes[0])
    elif isinstance(rtype, _type.List) : 
        nodes = [_value.List(rtype, naked_instance)]
        for c in rtype.children:
            vNames = wrap(c, naked_instance)
            for vName in vNames:
                tree.connect(vName, nodes[0])
    elif isinstance(rtype, _type._Type) : 
        nodes = [_value.Value(rtype, naked_instance)]
        for c in rtype.children:
            vNames = wrap(c, naked_instance)
            for vName in vNames:
                tree.connect(vName, nodes[0])
    #==
    return nodes
