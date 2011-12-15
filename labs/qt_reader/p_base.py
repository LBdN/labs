from labs.reactive import _base as b
from labs.reactive import _type as t

class Rect(b.Reactive):
    width  = t._Type(int)
    height = t._Type(int)

class Circle(b.Reactive):
    radius = t._Type(int)

class Mesh(b.Reactive):
    path  = t._Type(str)
    scale = t._Type(float)
    pos   = t.List().add_idxs([t._Type(float), t._Type(float), t._Type(float)])

class Node(b.Reactive):
    name  = t._Type(str)
    #shape = t.Union(children=[t.Rtype(Circle), t.Rtype(Rect)])
    mesh  = t.Rtype(Mesh)

class Selection(b.Reactive):
    nodes = t.List().add_idx('multi', t.Rtype(Node))

class World(b.Reactive):
    selection = t.Rtype(Selection)
    nodes     = t.List().add_idx('multi', t.Rtype(Node))
    


def default_obj(*args):
    #==
    n = Node.create()
    m = n.rnode['mesh']
    m['path'].replace("models/environment", True)
    m['scale'].replace(0.25, True)
    m['pos'].replace([-8.0,42.0,0.0], True)
    #==
    n2 = Node.create()
    m2 = n2.rnode['mesh']
    m2['path'].replace("models/teapot", True)
    m2['scale'].replace(0.25, True)
    m2['pos'].replace([-8.0,42.0,0.0], True)
    #==
    w = World.create()
    w.rnode['nodes'].append(n, True)
    w.rnode['nodes'].append(n2, True)
    #==
    #return [(m.rnode, {}), (m2.rnode, {}), (n.rnode, {}), (s.rnode, {})]
    return [(w.rnode, {}),]

