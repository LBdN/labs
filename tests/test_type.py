from . import tree
from . import _type as t

def test_list_int():
    a = range(5)
    #==
    tl  = t.TList()
    idx = t.Index('multi')
    ti  = t.TType(int)
    tree.connect(ti, idx)
    tree.connect(idx, tl)
    #==
    tl.validate(a)


