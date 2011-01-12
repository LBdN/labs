def connect(child, parent):
    if parent in child.parents  : return
    if child in parent.children : return
    #==
    assert not parent in child.parents
    assert not child in parent.children
    #==
    child.pre_connect(None, parent)
    parent.pre_connect(child, None)
    #==
    child.parents.append(parent)
    parent.children.append(child)
    #==
    child.post_connect(None, parent)
    parent.post_connect(child, None)

def disconnect(child, parent):
    if parent not in child.parents  : return
    if child not in parent.children : return
    #==
    assert parent in child.parents
    assert child in parent.children
    #==
    child.pre_disconnect(None, parent)
    parent.pre_disconnect(child, None)
    #==
    child.parents.remove(parent)
    parent.children.remove(child)
    #==
    child.post_disconnect(None, parent)
    parent.post_disconnect(child, None)

class Node(object):
    def __init__(self, cargo = None, children=None):
        self.children = []
        self.parents  = []
        self.cargo    = cargo
        #==
        print self, children
        if children:
            for c in children:
                connect(c, self)

    def pre_disconnect(self, child, parent):
        self.invariant()

    def post_disconnect(self, child, parent):
        self.invariant()

    def pre_connect(self, child, parent):
        self.invariant()

    def post_connect(self, child, parent):
        self.invariant()

    def invariant(self):
        pass

    def __repr__(self):
        return repr(self.cargo) if self.cargo else str(self.__class__.__name__.lower())

class OneChildMixin(object):
    def invariant(self):
        assert len(self.children) <= 1

    def get_only_child(self):
        return self.children[0]


def prettyprint(node, inc, _str=None):
    _str = '  '*inc+ str(node)+'\n'
    for child in node.children:
        _str += ''.join(prettyprint(child, inc+1))
    return _str
