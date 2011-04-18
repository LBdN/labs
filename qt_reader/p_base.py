from labs.reactive import _base as b
from labs.reactive import _type as t

class Rect(b.Reactive):
    width  = t._Type(int)
    height = t._Type(int)

class Circle(b.Reactive):
    radius = t._Type(int)

class Node(b.Reactive):
    name = t._Type(str)
    shape = t.Union(children=[t.Rtype(Circle), t.Rtype(Rect)])

class Mesh(b.Reactive):
    path  = t._Type(str)
    scale = t._Type(float)
    pos   = t.List().add_idxs([t._Type(float), t._Type(float), t._Type(float)])

def default_obj(*args):
    m = Mesh.create()
    m.rnode['path'].replace("models/environment", True)
    m.rnode['scale'].replace(0.25, True)
    m.rnode['pos'].replace([-8.0,42.0,0.0], True)
    n = Node.create()
    n.rnode['shape']['radius'].replace(10, True)
    return [(m.rnode, {}), (n.rnode, {})]

