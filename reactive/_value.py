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
        assert self.old is not None or self.type is not ReplaceItem

    def reverse(self):
        if self.type is RemoveItem:
            new_type = AddItem
            new_old  = self.old[:]
            new_old.remove(self.new)
            return Transaction(self.new, old=new_old, sender=self.sender, _type=new_type)
        if self.type is AddItem:
            new_type = RemoveItem
            new_old  = self.old[:]
            new_old.append(self.new)
            return Transaction(self.new, old=new_old, sender=self.sender, _type=new_type)
        if self.type is ReplaceItem:
            new_type = ReplaceItem
            new, old = self.old, self.new
            return Transaction(self.old, old=self.new, sender=self.sender, _type=new_type)


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
        if   tr.type is ReplaceItem : 
            proposed_value = tr.new
        elif tr.type is AddItem     : 
            proposed_value = self.naked_instance[:]
            proposed_value.append(tr.new)
        elif tr.type is RemoveItem  : 
            proposed_value = self.naked_instance[:]
            proposed_value.remove(tr.new)
        if self.rtype.validate(proposed_value) : self.modify(tr) 
        else                                   : tr = Error(tr); assert False
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
            for c in self.children[:]:
                tree.disconnect(c, self)
            self.naked_instance = tr.new
            for c in self.rtype.children:
                vIndexes = b.wrap(c, tr.new)
                for vIndex in vIndexes:
                    tree.connect(vIndex, self)
        #==
        elif tr.type is AddItem:
            assert self.rtype.is_multi_list()
            n        = len(self.naked_instance)
            tIndex   = self.rtype.children[0]
            vIndexes = b.wrap(tIndex, [tr.new])
            self.naked_instance.append(tr.new) #modification in place
            for vIndex in vIndexes:
                vIndex.idx = vIndex.idx + n
                tree.connect(vIndex, self)
        elif tr.type is RemoveItem:
            assert self.rtype.is_multi_list()
            for c in self.children[:]:
                if c.get_value() == tr.new:
                    tree.disconnect(c.get_only_child(), c)
                    tree.disconnect(c, self)
            self.naked_instance.remove(tr.new)
            self.reorder_indexes()
        else:
            assert False
        #==
        assert len(self.children)==len(self.naked_instance)

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
        if transaction and transaction.type is ReplaceItem:
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
