from ..data_structure import tree

class TypeValidator(object):
    def validate(self, naked_instance):
        raise NotImplementedError

class BaseValidator(TypeValidator):
    def __init__(self, _class):
        self._class = _class
    def validate(self, naked_instance):
        return isinstance(self, self._class)

class RType(tree.Node):
    def __init__(self, factory, type_validator=None, tname=None):
        self.factory        = factory
        self.type_validator = type_validator or BaseValidator(factory)
        self.tname          = tname or str(type(factory))
        tree.Node.__init__(self)

    def validate(self, naked_instance):
        self.type_validator.validate(naked_instance)

    def get_default(self):
        v = self._get_default()
        assert self.validate(v)
        return v

class RClass(RType):
    def invariant(self):
        return all(isinstance(child, Name) for child in self.children)

    def _get_default(self):
        assert self.invariant()
        kw = {}
        for child in self.children:
            kw[child.name] = child.get_default()
        return self.factory(**kw)

    def validate(self, naked_instance):
        assert self.invariant()
        return self.type_validator.validate(naked_instance) and \
               all(child.validate(naked_instance) for child in self.children)

    def add_attr(self, name, rtype):
        n = Name(name)
        tree.connect(rtype, n) 
        tree.connect(n, self) 


class Name(tree.Node):
    def __init__(self, name='anonymous'):
        self.name = name
        tree.Node.__init__(self)
    
    def extract(self, inst):
        return getattr(inst, self.name, None)

    def get_default(self):
        ttype = self.get_only_child()
        return ttype.get_default()

    def validate(self, naked_instance):
        v = self.extract(naked_instance)
        return self.get_only_child().validate(v)


class RList(RType):
    def invariant(self):
        return all(isinstance(child, Index) for child in self.children)

    def __init__(self, factory=None):
        factory = factory or list
        RType.__init__(self, factory)

    def _get_default(self):
        sorted_children = sorted(self.children, key = lambda c : c.name)
        return self.factory((c.get_default() for c in sorted_children))

    def add_idx(self, idx, rtype):
        i = Index(idx)
        tree.connect(rtype, i) 
        tree.connect(i, self) 


class Index(Name):
    def __init__(self, idx):
        assert (isinstance(idx, int) and idx>=0) or idx == "multi"
        self.multi = idx == 'multi'
        Name.__init__(self, idx) 

    def extract(self, inst):
        assert not self.multi
        return inst[self.name]

    def validate(self, naked_instance):
        if self.multi:
            child = self.get_only_child()
            return all(child.validate(el) for el in naked_instance)
        else:
            return Name.validate(self, naked_instance)


class RUnion(RType):
    def __init__(self, subtypes):
        self.subtypes = subtypes

    def validate(self, naked_instance):
        return any( s.validate(naked_instance) for s in self.subtypes)

    def _get_default(self):
        return self.subtypes[0].get_default()

    def get_active(self, naked_instance):
        for s in enumerate(self.subtypes):
            if s.validate(naked_instance):
                return s

def rtype(_type):
    rtype =  getattr(_type, "rtype")
    print "warning : not reactive type"
    return rtype if rtype else RType(_type)
