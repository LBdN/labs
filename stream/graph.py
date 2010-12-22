from labs.data_structure import tree
from base                import broadcast, zzip, index

class TNode(tree.Node):
    def __init__(self, *args, **kw): 
        tree.Node.__init__(self, *args, **kw)
        self.zipper = None

    def post_connect(self, child, parent):
        self.invariant()

    def invariant(self):
        assert all(isinstance(p, ISlot) for p in self.parents)
        assert all(isinstance(p, OSlot) for p in self.children)

    def get_target(self, parent=None):
        assert self.parents or self.children
        target = self.children[0].get_target(self) if self.children else None
        real_target = self.cargo.resolve(target)
        if len(self.parents) <= 1:
            return real_target
        else:
            if not self.zipper:
                self.zipper = zzip(len(self.parents), real_target)
                self.zipper.next() #to start it
            #==
            idx    = self.parents.index(parent)
            target = index(idx, self.zipper)
            target.next() # to start it
            return target


class OSlot(tree.Node):

    def post_connect(self, child, parent):
        self.invariant()

    def invariant(self):
        assert all(isinstance(p, TNode) for p in self.parents)
        assert all(isinstance(p, ISlot) for p in self.children)

    def get_target(self, parent):
        assert self.parents
        assert self.children
        #==
        if len(self.children)==1:
            target = self.children[0].get_target(self)
        else:
            target = broadcast([child.get_target(self) for child in self.children])
            target.next() # to start it
        return target


class ISlot(tree.Node):
    def __init__(self, *args, **kw): 
        tree.Node.__init__(self, *args, **kw)
        self.zipper = None

    def post_connect(self, child, parent):
        self.invariant()

    def invariant(self):
        assert all(isinstance(p, OSlot) for p in self.parents)
        assert all(isinstance(p, TNode) for p in self.children)

    def get_target(self, parent):
        assert self.parents
        assert self.children
        #==
        real_target = self.children[0].get_target(self)
        return real_target
        #if len(self.parents) == 1:
            #return real_target
        #else:
            #if not self.zipper:
                #self.zipper = zzip(len(self.parents), real_target)
                #self.zipper.next() #to start it
            ##==
            #idx    = self.parents.index(parent)
            #target = index(idx, self.zipper)
            #target.next() # to start it
            #return target

def next_TNodes(node):
    if isinstance(node, ISlot):
        assert len(node.children) == 1
        return node.children[0]
    elif isinstance(node, OSlot):
        return [next_TNodes(child) for child in node.children]
    elif isinstance(node, TNode):
        _list = []
        for child in node.children:
            _list.extend(next_TNodes(child))
        return _list
    else:
        assert False

