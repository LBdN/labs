from labs.reactive import _type as t

def test_list_int():
    a = range(5)
    #==
    tl  = t.List()
    tl.add_idx('multi', t._Type(int))
    #==
    return tl.validate(a)


def test_list_mixed():
    a = [1, 1.0, 'aaa']
    #==
    tl  = t.List()
    #==
    tl.add_idx(0, t._Type(int))
    tl.add_idx(1, t._Type(float))
    tl.add_idx(2, t._Type(str))
    #==
    return tl.validate(a)

def test_class():
    #==
    class Test(object):
        def __init__(self, first=None, second=None):
            self.first = first
            self.second = second
    #==
    a = Test(1, "t")
    #==
    tc = t._Class(Test)
    tc.add_attr("first", t._Type(int))
    tc.add_attr("second", t._Type(str))
    #==
    return tc.validate(a)


