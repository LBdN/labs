from ..data_structure import tree
from transaction import Error, ReplaceItem


class Value(tree.Node):
    def __init__(self, rtype, naked_instance):
        self.rtype = rtype
        self.naked_instance = naked_instance
        tree.Node.__init__(self)

    def set_value(self, tr):
        assert (self.naked_instance == tr.old)
        proposed_value = tr.proposed_value()
        if not self.rtype.validate(proposed_value) : 
            tr = Error(tr); assert False
        tr.do(self)
        assert self.rtype.validate(self.naked_instance)
        #==
        for p in self.parents:
            p.post_set_value(tr)

    def get_value(self):
        return self.naked_instance

class List(Value):
    def reorder_indexes(self):
        assert self.rtype.is_multi_list()
        for idx, el in enumerate(self.children):
            el.idx = idx

class Name(tree.Node, tree.OneChildMixin):
    def __init__(self, name):
        self.name        = name
        self.listeners   = []
        tree.Node.__init__(self)

    def invariant(self):
        if not self.children or not self.parents:
            return True
        #==
        assert len(self.parents)==1 
        assert isinstance(self.parents[0], Value)
        assert all(isinstance(c, Value) for c in self.children)
        assert self.get_only_child().get_value() is self.extract()
        return True
    
    def extract(self):
        return self.name.extract(self.parents[0].naked_instance)

    def register(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def notify(self, transaction):
        for l in self.listeners:
            l.notify(transaction)

    def set_value(self, transaction):
        assert self.invariant()
        child = self.get_only_child()
        child.set_value(transaction)
        
    def post_set_value(self, transaction):
        if transaction and isinstance(transaction, ReplaceItem):
            self.name.set(self.parents[0].naked_instance, transaction.new)
            # no need for the other case because list are shared via reference.
        assert self.invariant() # no warranty once we call notify
        self.notify(transaction)

    def get_value(self):
        child     = self.get_only_child()
        result    = child.get_value()
        assert self.invariant()
        return result

class Index(Name):
    def __init__(self, name, idx):
        Name.__init__(self, name)
        self.idx = idx

    def extract(self):
        return self.name.extract(self.parents[0].naked_instance, idx=self.idx)
