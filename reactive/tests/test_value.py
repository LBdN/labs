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
    assert isinstance(r, Rect)
    assert hasattr(r, 'width')
    assert hasattr(r, 'height')
    
def test_meta2():
    class Rect(v.Reactive):
        width  = t.RType(int)
        height = t.RType(int)
    r = Rect.create()
    assert isinstance(r, Rect)
    assert hasattr(r, 'width')
    assert hasattr(r, 'height')

def test_meta3():
    class Polygon(v.Reactive):
        points  = t.RList().add_idx('multi', t.RType(int))
    p = Polygon.create()
    assert isinstance(p, Polygon)
    assert hasattr(p, 'points')
    assert isinstance(p.points, list)
    assert all( isinstance(el, int) for el in p.points)

def test_meta4():
    class Shape(v.Reactive):
        ttype = t.RUnion(children=[t.RType(int), t.RType(float), t.RType(str)])
    s = Shape.create()
    assert isinstance(s, Shape)
    assert hasattr(s, 'ttype')
    assert isinstance(s.ttype, (int,float,str))

def test_meta5():
    class Rect(v.Reactive):
        width  = t.RType(int)
        height = t.RType(int)
    class Circle(v.Reactive):
        radius = t.RType(int)
    class Shape(v.Reactive):
        kind = t.RUnion(children=[t.RType(Rect), t.RType(Circle)])
    s = Shape.create()



