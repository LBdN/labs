from .. import _value as v
from .. import _type as t

def test_meta1():
    class Rect(object):
        __metaclass__ = v.ReactiveMeta
        width  = t.RType(int)
        height = t.RType(int)
        def __init__(self, width=None, height=None):
            self.width  = width  or 0
            self.height = height or 0
    r  = Rect.rtype.get_default()
    




