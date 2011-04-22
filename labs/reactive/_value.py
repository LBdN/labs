from ..data_structure import tree
import transaction  as t 


class Value(tree.Node):
    def __init__(self, rtype, naked_instance):
        self.rtype = rtype
        self.naked_instance = naked_instance
        assert naked_instance is not None
        tree.Node.__init__(self)

    def __getitem__(self, key):
        for c in self.children:
            if c.name.name == key:
                return c

    def set_value(self, tr):
        assert (self.naked_instance == tr.old)
        proposed_value = tr.proposed_value(self.naked_instance)
        if not self.rtype.validate(proposed_value) : 
            tr = t.Error(tr); assert False, tr
        tr.do(self)
        assert self.rtype.validate(self.naked_instance)
        assert self.naked_instance == proposed_value
        #==
        for p in self.parents:
            p.post_set_value(tr)

    def replaceT(self, new, sender):
        return t.Replace(new, self.naked_instance, sender)

    def get_value(self):
        return self.naked_instance

    def is_name(self):
        return False

    def __repr__(self):
        return repr(self.rtype)

class List(Value):

    def __getitem__(self, key):
        if not self.rtype.is_multi_list():
            return Value.__getitem__(self, key)
        #==
        c = self.children[key]
        return c

    def replaceT(self, new, sender):
        return t.Replace(new, old=self.naked_instance[:], sender=sender)

    def appendT(self, new, sender):
        return t.AppendItem(new, old=self.naked_instance[:], sender=sender)

    def removeT(self, idx, sender):
        return t.RemoveItem(idx, old=self.naked_instance[:], sender=sender)

    def insertT(self, idx, val, sender):
        return t.InsertItem((idx, val), old=self.naked_instance[:], sender=sender)

    def reorder_indexes(self):
        assert self.rtype.is_multi_list()
        for idx, el in enumerate(self.children):
            el.idx = idx

class Name(tree.Node, tree.OneChildMixin):
    def __init__(self, name):
        self.name        = name
        self.listeners   = []
        tree.Node.__init__(self)

    def __repr__(self):
        return "value.Name: %s" %repr(self.name)

    def __getitem__(self, key):
        return self.get_only_child()[key]

    def replace(self, new, sender):
        value = self.get_only_child()
        t = value.replaceT(new, sender)
        self.set_value(t)
        return t

    def insert(self, *args):
        value = self.get_only_child()
        t = value.insertT(*args)
        self.set_value(t)
        return t

    def append(self, *args):
        value = self.get_only_child()
        t = value.appendT(*args)
        self.set_value(t)
        return t

    def remove(self, *args):
        value = self.get_only_child()
        t = value.removeT(*args)
        self.set_value(t)
        return t

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

    def set(self, transaction):
        if isinstance(transaction, t.Replace):
            self.name.set(self.parents[0].naked_instance, transaction.new)
        else:
            pass
            # !!! Tricky !!!
            # no need for the other case 
            # because list are shared via reference.
            # hence processed by the value (aka children[0])

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
        if not isinstance(transaction, t.Error):
            self.set(transaction)
        assert self.invariant() # no warranty once we call notify
        self.notify(transaction)

    def get_value(self):
        child     = self.get_only_child()
        result    = child.get_value()
        assert self.invariant()
        return result

    def is_name(self):
        return True

class Index(Name):
    def __init__(self, name, idx):
        Name.__init__(self, name)
        self.idx = idx

    def set(self, transaction):
        if not isinstance(self.get_only_child(), List):
            self.name.set(self.parents[0].naked_instance, transaction.new, idx=self.idx)
        assert self.invariant() # no warranty once we call notify

    def extract(self):
        return self.name.extract(self.parents[0].naked_instance, idx=self.idx)
