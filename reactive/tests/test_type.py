from .. import _type as t

def test_list_int():
    a = range(5)
    #==
    tl  = t.RList()
    tl.add_idx('multi', t.RType(int))
    #==
    tl.validate(a)


def test_list_mixed():
    a = [1, 1.0, 'aaa']
    #==
    tl  = t.RList()
    #==
    tl.add_idx(0, t.RType(int))
    tl.add_idx(1, t.RType(float))
    tl.add_idx(2, t.RType(str))
    #==
    tl.validate(a)

def test_class():
    #==
    class Test(object):
        def __init__(self, first=None, second=None):
            self.first = first
            self.second = second
    #==
    a = Test(1, "t")
    #==
    tc = t.RClass(Test)
    tc.add_attr("first", t.RType(int))
    tc.add_attr("second", t.RType(str))
    #==
    tc.validate(a)

