import random
import math
import fvector

import context
import gamr7_lib.geometry.shape_operation as so 
import gamr7_lib.intersections as it

def random_nb(_max):
    return range(random.randint(3,_max))

def random_point(_max, angle):
    d = random.random()*_max
    return math.cos(angle)*d, math.sin(angle)*d

def random_polygon(max_side, max_dist):
    nb_side = random_nb(max_side)
    ps      = []
    for side in nb_side:
        angle = side*2*math.pi/len(nb_side)
        p = random_point(max_dist, angle)
        ps.append(p)
    return ps

def random_line(max_dist):
    return random_point(max_dist, random.random()*math.pi), \
           random_point(max_dist, random.random()*math.pi)

def fvline(origin, direction):
    return fvector.Line(fvector.Vector(origin[0], origin[1], 0), \
                        fvector.Vector(direction[0], direction[1], 0))

# for plot(ting) polygon in ipython
def separate_coord(ps):
    xs = []
    ys = []
    for p in ps:
        xs.append(p[0])
        ys.append(p[1])
    xs.append(ps[0][0])
    ys.append(ps[0][1])
    return (xs, ys)


def bi_gen(ps):
    for i, p in enumerate(ps):
        n  = ps[(i+1)%len(ps)]
        yield p, n

def tri_gen(ps):
    for i, p in enumerate(ps):
        n  = ps[(i+1)%len(ps)]
        nn = ps[(i+2)%len(ps)]
        yield p, n, nn

def test_trigo(_max_pol, _max_side, _max_dist):
    # generate polys
    rp = (random_polygon2(_max_side, _max_dist) for i in range(_max_pol))
    return all(fvector.is_ccw(fvector.convert_vec(p)) == so.is_a_trigo_shape(p) for p in rp)

def test_convex(_max_pol, _max_side, _max_dist):
    # generate polys
    rp = (random_polygon2(_max_side, _max_dist) for i in range(_max_pol))
    return all(fvector.is_convex(fvector.convert_vec(p)) == so.is_a_convex_shape(p) for p in rp)

def test_area(): #todo
    pass

def test_center(): #todo
    pass

def test_intersection_line(_max_line, _max_dist):
    rl = ((random_line(_max_dist), random_line(_max_dist)) for i in range(_max_line))
    return [(fvector.get_intersection(fvline(*l1), fvline(*l2)), \
            it.get_collision_between_lines(l1, l2)) for l1, l2 in rl]

def test_is_online(_max_line, _max_dist):
    rl = ((random_line(_max_dist), random_line(_max_dist)) for i in range(_max_line))
