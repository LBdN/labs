import _base as b
from ..data_structure import tree

class Transaction(object):
    def __init__(self, new, old=None, sender=None):
        self.new    = new
        self.old    = old
        self.sender = sender
        assert self.sender
        assert self.old is not None or isinstance(self, (AppendItem, Init))
        #==
        self.applied_on = None
        self.vnames     = None

    def __repr__(self):
        return "%s(new:%s old:%s sender:%s)" \
                %( str(type(self)), self.new, self.old, self.sender)

class Init(Transaction):

    def affect(self, listener):
        listener.tr_replace(self)

class Replace(Transaction):
    def reverse(self):
        new, old = self.old, self.new
        return Replace(self.old, old=self.new, sender=self.sender)

    def proposed_value(self, naked_instance):
        assert naked_instance == self.old
        return self.new

    def do(self, rvalue):
        for c in rvalue.children[:]:
            tree.disconnect(c, rvalue)
        rvalue.naked_instance = self.new
        for c in rvalue.rtype.children:
            vIndexes = b.wrap(c, self.new)
            for vIndex in vIndexes:
                tree.connect(vIndex, rvalue)
        #==
        if isinstance(rvalue.naked_instance, list):
            assert len(rvalue.children)==len(rvalue.naked_instance)

    def affect(self, listener):
        listener.tr_replace(self)

class InsertItem(Transaction):
    def reverse(self):
        idx, val = self.new
        new_old  = self.old[:]
        new_old.insert(idx, val)
        new      = idx
        return RemoveItem(new, new_old, sender= self.sender)

    def proposed_value(self, naked_instance):
        idx, val = self.new
        proposed_value = naked_instance[:]
        proposed_value.insert(idx, val)
        return proposed_value

    def do(self, rvalue):
        #==
        assert rvalue.rtype.is_multi_list()
        tIndex   = rvalue.rtype.children[0]
        idx, val = self.new
        vIndexes = b.wrap(tIndex, [val])
        rvalue.naked_instance.insert(idx, val) #modification in place
        assert len(vIndexes) == 1
        vIndex     = vIndexes[0]
        vIndex.idx = idx
        for c in rvalue.children[idx:]:
            c.idx += 1
        tree.connect(vIndex, rvalue)
        #==
        assert len(rvalue.children)==len(rvalue.naked_instance)

    def affect(self, listener):
        listener.tr_insert(self)

class AppendItem(Transaction):
    def reverse(self):
        new_old  = self.old[:]
        new_old.append(self.new)
        new =  -1
        return RemoveItem(new, old=new_old, sender=self.sender)

    def proposed_value(self, naked_instance):
        assert naked_instance == self.old
        proposed_value = naked_instance[:]
        proposed_value.append(self.new)
        return proposed_value

    def do(self, rvalue):
        #==
        assert rvalue.rtype.is_multi_list()
        n        = len(rvalue.naked_instance)
        tIndex   = rvalue.rtype.children[0]
        vIndexes = b.wrap(tIndex, [self.new])
        rvalue.naked_instance.append(self.new) #modification in place
        for vIndex in vIndexes:
            vIndex.idx = vIndex.idx + n
            tree.connect(vIndex, rvalue)
        #==
        assert len(rvalue.children)==len(rvalue.naked_instance)

    def affect(self, listener):
        listener.tr_append(self)

class RemoveItem(Transaction):
    def reverse(self):
        new_old  = self.old[:]
        new      = new_old.pop(self.new)
        return InsertItem((self.new, new), old=new_old, sender=self.sender)

    def proposed_value(self, naked_instance):
        assert naked_instance == self.old
        proposed_value = naked_instance[:]
        del proposed_value[self.new]
        return proposed_value

    def do(self, rvalue):
        assert rvalue.rtype.is_multi_list()
        c = rvalue.children[self.new]
        #tree.disconnect(c.get_only_child(), c) #not necessary
        tree.disconnect(c, rvalue)
        del rvalue.naked_instance[self.new]
        rvalue.reorder_indexes()
        #==
        assert len(rvalue.children)==len(rvalue.naked_instance)

    def affect(self, listener):
        listener.tr_remove(self)

class Error(object):
    def __init__(self, transaction):
        self.transaction = transaction

    def __nonzero__(self):
        return False

    def __repr__(self):
        return repr(self.transaction)

    def do(self, rvalue):
        pass

    def affect(self, listener):
        listener.tr_error(self)
