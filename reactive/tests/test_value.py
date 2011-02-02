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
        #color = t.Promise('color.ColorRGB')
    s = Shape.create()


def test_meta6():
    class Polygon(b.Reactive):
        points  = t.List().add_idx('multi', t._Type(int))
        #matrix  = t.Interface(t.List().add_idx('16x', t._Type(float))) matrix = implements
        def __repr__(self):
            return str(self.points)
    p = Polygon.create()
    name_node = p.rnode.children[0]
    trs       = []
    #==
    trs.append(name_node.replace([1,2,3], True))
    trs.append(name_node.replace([1], True))
    trs.append(name_node.append(5, True))
    trs.append(name_node.remove(1, True))
    trs.append(name_node.insert(1,6, True))
    #==
    assert isinstance(p, Polygon)
    assert hasattr(p, 'points')
    assert isinstance(p.points, list)
    assert all( isinstance(el, int) for el in p.points)

def test_meta7():
    class Polygon(b.Reactive):
        points  = t.List().add_idx('multi', t._Type(int))
        def __repr__(self):
            return str(self.points)
    p   = Polygon.create()
    assert isinstance(p, Polygon)
    assert hasattr(p, 'points')
    assert isinstance(p.points, list)
    assert all( isinstance(el, int) for el in p.points)
    #==
    name_node = p.rnode.children[0]
    trs       = []
    #==
    trs.append(name_node.replace([1,2,3], True))
    trs.append(name_node.replace([1], True))
    trs.append(name_node.append(5, True))
    trs.append(name_node.remove(1, True))
    trs.append(name_node.insert(1,6, True))
    #==
    assert p.points == [1,6]
    for tr in reversed(trs):
        name_node.set_value(tr.reverse())
    assert p.points == [0]

def test_meta8():
    class Rect(b.Reactive):
        width  = t._Type(int)
        height = t._Type(int)
    class Circle(b.Reactive):
        radius = t._Type(int)
    class Polygon(b.Reactive):
        points  = t.List().add_idx('multi', t.Union(children=[t._Type(Rect), t._Type(Circle)]))
        #matrix  = t.Interface(t.List().add_idx('16x', t._Type(float))) matrix = implements
        def __repr__(self):
            return str(self.points)
    p   = Polygon.create()
    assert isinstance(p, Polygon)
    assert hasattr(p, 'points')
    assert isinstance(p.points, list)
    assert all( isinstance(el, (Rect, Circle)) for el in p.points)
    #==
    start = p.points[0]
    r     = Rect.create()
    c     = Circle.create()
    c2    = Circle.create()
    #==
    trs         = []
    points_node = p.rnode['points']
    #==
    trs.append(points_node.replace([r], True))
    trs.append(points_node.replace([c], True))
    trs.append(points_node.append(c2, True))
    trs.append(points_node.remove(1, True))
    trs.append(points_node.insert(1,c2, True))
    #==
    assert len(p.points) == 2 and all( isinstance(c, Circle) for c in p.points)
    for tr in reversed(trs):
        p.rnode.children[0].set_value(tr.reverse())
    assert p.points == [start]

def test_meta9():
    class Rect(b.Reactive):
        width  = t._Type(int)
        height = t._Type(int)
    class Circle(b.Reactive):
        radius = t._Type(int)
    class Polygon(b.Reactive):
        points  = t.List().add_idx('multi', t.Union(children=[t._Type(Rect), t._Type(Circle)]))
        def __repr__(self):
            return str(self.points)
    p   = Polygon.create()
    assert isinstance(p, Polygon)
    assert hasattr(p, 'points')
    assert isinstance(p.points, list)
    assert all( isinstance(el, (Rect, Circle)) for el in p.points)
    #==
    start = p.points[0]
    r     = Rect.create()
    c     = Circle.create()
    c2    = Circle.create()
    #==
    trs         = []
    points_node = p.rnode['points']
    #==
    trs.append(points_node.replace([c], True))
    #==
    radius_node = points_node[0]['radius']
    tr_radius = radius_node.replace(10, True)
    trs.append(tr_radius)
    trs.append(points_node.replace([r], True))
    trs.append(points_node.remove(0, True))
    #==
    assert len(p.points) == 0 and all( isinstance(c, Circle) for c in p.points)
    for tr in reversed(trs):
        if tr is tr_radius: target = radius_node
        else              : target = points_node
        target.set_value(tr.reverse())
    assert p.points == [start]
