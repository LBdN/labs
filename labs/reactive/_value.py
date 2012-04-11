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
            debug_func()
            tr = t.Error(tr); assert False, tr
        tr.do(self)
        assert self.rtype.validate(self.naked_instance)
        assert self.naked_instance == proposed_value
        #==
        for p in self.parents:
            p.post_set_value(tr)

    def replaceT(self, new, sender, target):
        return t.Replace(new, self.naked_instance, sender, target)

    def get_value(self):
        return self.naked_instance

    def is_name(self):
        return False

    def is_list(self):
        return False

    def is_multi_list(self):
        return False

    def is_container(self):
        return self.children != [] 

    def is_union(self):
        return False

    def __repr__(self):
        return repr(self.rtype)

    def init_notification(self):
        for c in self.children:
            c.init_notification()

class UnionValue(Value):
    def __getitem__(self, key):
        return self.children[0][key]

    def rvalue(self):
        return self.children[0]

    def is_container(self):
        return self.children[0].is_container()

    def is_union(self):
        return True

    #def is_index(self):
        #return False

    def change_typeT(self, new, sender, target):
        return t.ChangeType(new, old=self.naked_instance, sender=sender, target=target)

    def replace(self, new, sender):
        return self.parents[0].replace(new, sender)

    def insert(self, idx, val, sender):
        return self.parents[0].insert(idx, val, sender)

    def append(self, new, sender):
        return self.parents[0].append(new, sender)

    def remove(self, new, sender):
        return self.parents[0].remove(new, sender)

    def change_type(self, new, sender):
        return self.parents[0].change_type(new, sender)

    def register(self, listener):
        self.parents[0].register(listener)

class List(Value):

    def __getitem__(self, key):
        if not self.rtype.is_multi_list():
            return Value.__getitem__(self, key)
        #==
        c = self.children[key]
        return c

    def replaceT(self, new, sender, target):
        return t.Replace(new, old=self.naked_instance[:], sender=sender, target=target)

    def appendT(self, new, sender, target):
        return t.AppendItem(new, old=self.naked_instance[:], sender=sender, target=target)

    def removeT(self, idx, sender, target):
        return t.RemoveItem(idx, old=self.naked_instance[:], sender=sender, target=target)

    def insertT(self, idx, val, sender, target):
        return t.InsertItem((idx, val), old=self.naked_instance[:], sender=sender, target=target)

    def reorder_indexes(self):
        assert self.rtype.is_multi_list()
        for idx, el in enumerate(self.children):
            el.idx = idx

    def get_new_item(self):
        assert self.rtype.is_multi_list()
        return self.rtype.children[0].get_default()

    def is_container(self):
        return True

    def is_list(self):
        return True

    def is_multi_list(self):
        return self.rtype.is_multi_list()


class Name(tree.Node, tree.OneChildMixin):
    def __init__(self, name):
        self.name        = name
        self.listeners   = []
        tree.Node.__init__(self)
        self.locked      = False

    def __repr__(self):
        return "value.Name: %s" %repr(self.name)

    def __getitem__(self, key):
        return self.get_only_child()[key]

    def replace(self, new, sender):
        value = self.get_only_child()
        t = value.replaceT(new, sender, self)
        self.set_value(t)
        return t

    def insert(self, idx, val, sender):
        value = self.get_only_child()
        t = value.insertT(idx, val, sender, self)
        self.set_value(t)
        return t

    def append(self, new, sender):
        value = self.get_only_child()
        t = value.appendT(new, sender, self)
        self.set_value(t)
        return t

    def remove(self, new, sender):
        value = self.get_only_child()
        t = value.removeT(new, sender, self)
        self.set_value(t)
        return t

    def change_type(self, new, sender):
        value = self.get_only_child()
        t = value.change_typeT(new, sender, self)
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
        assert_( not self.locked)
        #print self,  listener
        if listener not in self.listeners:
            self.listeners.append(listener)

    def lock(self):
        self.locked = True

    def init_notification(self):
        tr = t.Init(self.get_value(), sender=self, target=self)
        self.fire_notification(tr)
        for c in self.children:
            c.init_notification()

    def fire_notification(self, transaction):
        for l in self.listeners:
            #print self, transaction, l
            transaction.affect(l)

    def set_value(self, transaction):
        assert self.invariant()
        child = self.get_only_child()
        child.set_value(transaction)
        
    def post_set_value(self, transaction):
        if not isinstance(transaction, t.Error):
            self.set(transaction)
        assert self.invariant() # no warranty once we call notify
        #==
        self.fire_notification(transaction)
        if isinstance(transaction, t.AppendItem):
            self.rvalue().children[-1].init_notification()
        if isinstance(transaction, t.InsertItem):
            self.rvalue().children[transaction.new[0]].init_notification()
        if isinstance(transaction, t.ChangeType):
            self.rvalue().children[0].init_notification()
        #==

    def get_value(self):
        child     = self.get_only_child()
        result    = child.get_value()
        assert self.invariant()
        return result

    def rvalue(self):
        return self.get_only_child()

    def is_name(self):
        return True

    def is_index(self):
        return False

    def as_key(self):
        return self.name.name

    def full_name(self):
        parents = [str(p.as_key()) for p in tree.walk_up(self, []) if p.is_name()]
        return '/'.join(parents)

class Index(Name):
    def __init__(self, name, idx):
        Name.__init__(self, name)
        self.idx = idx

    def as_key(self):
        return self.idx

    def set(self, transaction):
        if not isinstance(self.get_only_child(), List):
            self.name.set(self.parents[0].naked_instance, transaction.new, idx=self.idx)
        assert self.invariant() # no warranty once we call notify

    def extract(self):
        return self.name.extract(self.parents[0].naked_instance, idx=self.idx)

    def is_index(self):
        return True

    def delete(self, sender=True):
        vlist = self.parents[0]
        name  = vlist.parents[0]
        assert vlist.is_multi_list()
        tr = name.remove( self.idx, sender)
        del_tr = t.Delete(self.idx, tr)
        self.fire_notification(del_tr)
