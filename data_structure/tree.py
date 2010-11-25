def connect(child, parent):
    if parent in child.parents  : return
    if child in parent.children : return
    #==
    assert not parent in child.parents
    assert not child in parent.children
    #==
    child.parents.append(parent)
    parent.children.append(child)
    #==
    child.invariant()
    parent.invariant()

def disconnect(child, parent):
    if parent not in child.parents  : return
    if child not in parent.children : return
    #==
    assert parent in child.parents
    assert child in parent.children
    #==
    child.parents.remove(parent)
    parent.children.remove(child)
    #==
    child.invariant()
    parent.invariant()

class Node(object):
    def __init__(self, cargo = None):
        self.children = []
        self.parents  = []
        self.cargo    = cargo

    def invariant(self):
        pass

class OneChildMixin(object):
    def invariant(self):
        assert len(self.children) <= 1
        #assert len(self.parents)  == 1

    def get_only_child(self):
        return self.children[0]
