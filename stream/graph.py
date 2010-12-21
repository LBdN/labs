from labs.data_structure import tree
from base                import broadcast, zzip, index

class TNode(tree.Node):

    def post_connect(self, child, parent):
        self.invariant()

    def invariant(self):
        assert all(isinstance(p, ISlot) for p in self.parents)
        assert all(isinstance(p, OSlot) for p in self.children)

    def get_target(self, parent=None):
        target = self.children[0].get_target(self) if self.children else None
        return self.cargo.resolve(target)


class OSlot(tree.Node):

    def post_connect(self, child, parent):
        self.invariant()

    def invariant(self):
        assert all(isinstance(p, TNode) for p in self.parents)
        assert all(isinstance(p, ISlot) for p in self.children)

    def get_target(self, parent):
        if len(self.children)==1:
            target = self.children[0].get_target(self)
        else:
            target = broadcast([child.get_target(parent) for child in self.children])
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
        real_target = self.children[0].get_target(self)
        if len(self.parents) == 1:
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
