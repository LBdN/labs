from ..data_structure import tree
import _base as b

class __Symbol():
    pass

Nothing     = __Symbol()
RemoveItem  = __Symbol()
AddItem     = __Symbol()
ReplaceItem = __Symbol()

del __Symbol

class Transaction(object):
    def __init__(self, new, old=None, sender=None, _type=ReplaceItem):
        self.new    = new
        self.old    = old
        self.sender = sender
        self.type   = _type

class Error(object):
    def __init__(self, transaction):
        self.transaction = transaction

    def __nonzero__(self):
        return False

class Value(tree.Node):
    def __init__(self, rtype, naked_instance):
        self.rtype = rtype
        self.naked_instance = naked_instance
        tree.Node.__init__(self)

    def set_value(self, tr):
        assert (tr.old is Nothing) or (self.naked_instance == tr.old)
        if self.rtype.validate(tr.new) : self.modify(tr) #bug on the validate if tr.type is AddItem and rtype not multi
        else                           : tr = Error(tr); assert False
        #==
        for p in self.parents:
            p.post_set_value(tr)

    def modify(self, tr):
        assert tr.type is ReplaceItem
        self.naked_instance = tr.new

    def get_value(self):
        return self.naked_instance


class List(Value):
    def modify(self, tr):
        if tr.type is ReplaceItem:
            #if not self.rtype.validate(tr.new):
                #return Error(tr)
            for c in self.children:
                tree.disconnect(c, self)
            for c in self.rtype.children:
                vIndexes = b.wrap(c, tr.new)
                for vIndex in vIndexes:
                    tree.connect(vIndex, self)
            self.naked_instance += tr.new
        #==
        elif tr.type is AddItem:
            assert self.rtype.is_multi_list()
            #if not self.rtype.validate(self.naked_instance+tr.new):
                #return Error(tr)
            n        = len(self.naked_instance)
            tIndex   = self.rtype.children[0]
            vIndexes = b.wrap(tIndex, tr.new)
            for vIndex in vIndexes:
                tree.connect(vIndex, self)
                vIndex.idx = vIndex + n
            self.naked_instance += tr.new
        else:
            assert False

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
        if transaction:
            self.name.set(self.parents[0].naked_instance, transaction.new)
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

    def set_value(self, transaction):
        if transaction.type is RemoveItem:
            tree.disconnect(self.get_only_child(), self)
            tree.disconnect(self, self.parents[0])
            self.parents[0].reorder_indexes()
        else:
            Name.set_value(self, transaction)

    def extract(self):
        return self.name.extract(self.parents[0].naked_instance, idx=self.idx)
