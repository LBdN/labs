from .. import _value as v
from .. import _type as t
from .. import _base as b

def test_meta1():
    class Rect(object):
        __metaclass__ = b.ReactiveMeta
        width  = t._Type(int)
        height = t._Type(int)
        def __init__(self, width=None, height=None):
            self.width  = width  or 0
            self.height = height or 0
    r  = Rect.rtype.get_default()
    assert isinstance(r, Rect)
    assert hasattr(r, 'width')
    assert hasattr(r, 'height')
    
def test_meta2():
    class Rect(b.Reactive):
        width  = t._Type(int)
        height = t._Type(int)
    r = Rect.create()
    assert isinstance(r, Rect)
    assert hasattr(r, 'width')
    assert hasattr(r, 'height')

def test_meta3():
    class Polygon(b.Reactive):
        points  = t.List().add_idx('multi', t._Type(int))
    p = Polygon.create()
    assert isinstance(p, Polygon)
    assert hasattr(p, 'points')
    assert isinstance(p.points, list)
    assert all( isinstance(el, int) for el in p.points)

def test_meta4():
    class Shape(b.Reactive):
        ttype = t.Union(children=[t._Type(int), t._Type(float), t._Type(str)])
    s = Shape.create()
    assert isinstance(s, Shape)
    assert hasattr(s, 'ttype')
    assert isinstance(s.ttype, (int,float,str))

def test_meta5():
    class Rect(b.Reactive):
        width  = t._Type(int)
        height = t._Type(int)
    class Circle(b.Reactive):
        radius = t._Type(int)
    class Shape(b.Reactive):
        kind = t.Union(children=[t._Type(Rect), t._Type(Circle)])
    s = Shape.create()


def test_meta6():
    class Polygon(b.Reactive):
        points  = t.List().add_idx('multi', t._Type(int))
        def __repr__(self):
            return str(self.points)
    p = Polygon.create()
    p.rnode.children[0].set_value(v.Transaction([1,2,3], old=v.Nothing))
    p.rnode.children[0].set_value(v.Transaction([1], old=[1,2,3]))
    p.rnode.children[0].set_value(v.Transaction([5], old=[1], _type=v.AddItem))
    assert isinstance(p, Polygon)
    assert hasattr(p, 'points')
    assert isinstance(p.points, list)
    assert all( isinstance(el, int) for el in p.points)

