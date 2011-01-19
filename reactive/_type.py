from ..data_structure import tree

class TypeValidator(object):
    def validate(self, naked_instance):
        raise NotImplementedError

class BaseValidator(TypeValidator):
    def __init__(self, _class):
        self._class = _class
    def validate(self, naked_instance):
        return isinstance(naked_instance, self._class)

class _Type(tree.Node):
    def __init__(self, factory, type_validator=None, tname=None, children=None):
        self.factory        = factory
        self.type_validator = type_validator or BaseValidator(factory)
        self.tname          = tname or str(type(factory))
        tree.Node.__init__(self, children=children)

    def validate(self, naked_instance):
        return self.type_validator.validate(naked_instance)

    def get_default(self):
        v = self._get_default()
        assert self.validate(v)
        return v

    def _get_default(self):
        return self.factory()

class _Class(_Type):
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


class Name(tree.Node, tree.OneChildMixin):
    def __init__(self, name='anonymous'):
        self.name = name
        tree.Node.__init__(self)
    
    def extract(self, inst):
        return getattr(inst, self.name, None)

    def set(self, inst, value):
        setattr(inst, self.name, value)

    def get_default(self):
        ttype = self.get_only_child()
        return ttype.get_default()

    def validate(self, naked_instance):
        v = self.extract(naked_instance)
        return self.get_only_child().validate(v)


class List(_Type):
    def invariant(self):
        return all(isinstance(child, Index) for child in self.children)

    def __init__(self, factory=None):
        factory = factory or list
        _Type.__init__(self, factory)

    def _get_default(self):
        sorted_children = sorted(self.children, key = lambda c : c.name)
        return self.factory((c.get_default() for c in sorted_children))

    def add_idx(self, idx, rtype):
        i = Index(idx)
        tree.connect(rtype, i) 
        tree.connect(i, self) 
        return self

class Index(Name):
    def __init__(self, idx):
        assert (isinstance(idx, int) and idx>=0) or idx == "multi"
        self.multi = idx == 'multi'
        Name.__init__(self, idx) 

    def extract(self, inst, idx=None):
        assert (self.multi and idx is not None) or \
               (idx and not self.multi) 
        #==
        if self.multi : return inst[idx]
        else          : return inst[self.name]

    def validate(self, naked_instance):
        if self.multi:
            child = self.get_only_child()
            return all(child.validate(el) for el in naked_instance)
        else:
            return Name.validate(self, naked_instance)


class Union(_Type):
    def __init__(self, children=None):
        _Type.__init__(self, None, children=children)

    def validate(self, naked_instance):
        return any( s.validate(naked_instance) for s in self.children)

    def _get_default(self):
        return self.children[0].get_default()

    def get_active(self, naked_instance):
        for s in enumerate(self.children):
            if s.validate(naked_instance):
                return s

def _type(_type):
    rtype =  getattr(_type, "rtype")
    print "warning : not reactive type"
    return rtype if rtype else _Type(_type)
