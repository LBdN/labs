from labs.reactive import _base as b
from labs.reactive import _type as t
import random

class Rect(b.Reactive):
    width  = t._Type(int)
    height = t._Type(int)

class Circle(b.Reactive):
    radius = t._Type(int)

class Polygon(b.Reactive):
    radius  = t._Type(int)
    side_nb = t._Type(int)

class Mesh(b.Reactive):
    path  = t._Type(lambda : "models/environment", type_validator=lambda x: isinstance(x, str))
    position = t.List().add_idxs([t._Type(float), t._Type(float), t._Type(float)])
    rotation = t.List().add_idxs([t._Type(float), t._Type(float), t._Type(float)])
    scale    = t.List(lambda x: [1.0,1.0,1.0], type_validator=lambda x: isinstance(x, list)).add_idxs([t._Type(float), t._Type(float), t._Type(float)])

class Slot(b.Reactive):
    pass

class Slot(b.Reactive):
    name   = t._Type(str)
    parent = t.Rtype(Slot)


class Node(b.Reactive):
    name  = t._Type(str)
    slots = t.List().add_idx('multi', t._Type(str))
    mesh  = t.Rtype(Mesh)
    shape = t.List().add_idx('multi',t.Union(children=[t.Rtype(Circle), t.Rtype(Rect), t.Rtype(Polygon)]))

class Selection(b.Reactive):
    nodes = t.List().add_idx('multi', t.Rtype(Node))

class World(b.Reactive):
    
    selection = t.Rtype(Selection)
    nodes     = t.List().add_idx('multi', t.Rtype(Node))
    numbers   = t.List().add_idx('multi', t.Union(children=[t._Type(float), t._Type(str)]))


def default_obj():
    #==
    n = Node.create()
    m = n.rnode['mesh']
    m['path'].replace("models/environment", True)
    #m['scale'].replace(0.25, True)
    m['position'].replace([-8.0,42.0,0.0], True)
    #==
    n2 = Node.create()
    m2 = n2.rnode['mesh']
    m2['path'].replace("models/teapot", True)
    #m2['scale'].replace(0.25, True)
    m2['position'].replace([-8.0,42.0,0.0], True)
    m2['rotation'].replace([-8.0,42.0,0.0], True)
    #==
    w = World.create()
    #w.rnode['nodes'].append(n, True)
    #w.rnode['nodes'].append(n2, True)
    w.rnode['numbers'].replace(map(float, range(5)), True)
    #==
    for i in range( 1 ):
        n3 = Node.create()
        m3 = n3.rnode['mesh']
        m3['path'].replace("smiley", True)
        #m3['scale'].replace(10.0, True)
        m3['position'].replace([ float(random.randint( -30, 30 ) * 2), float(random.randint( -30, 30 ) * 2), float(random.randint( -30, 30 ) * 2)], True)
        #ball = loader.loadModel( 'smiley' )
        w.rnode['nodes'].append(n3, True)
        ##ball.setTag( PICK_TAG, '1' )
        ##ball.reparentTo( self.rootNp )
        #ball.setPos()
        #ball.setScale( 10, 10, 10 )
    return w.rnode

