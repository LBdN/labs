from gamr7_lib.basic_calcul import cross_product, points_diff, normalize 
import random
import math

def random_nb(_max):
    return range(random.randint(3,_max))

def random_point(_max):
    return random.random()*_max, random.random()*_max

def random_polygon(max_side, max_dist):
    nb_side = random_nb(max_side)
    ps      = []
    for side in nb_side:
        p = random_point(max_dist)
        ps.append(p)
    return ps

def random_point2(_max, angle):
    d = random.random()*_max
    return math.cos(angle)*d, math.sin(angle)*d

def random_polygon2(max_side, max_dist):
    nb_side = random_nb(max_side)
    ps      = []
    for side in nb_side:
        angle = side*2*math.pi/len(nb_side)
        p = random_point2(max_dist, angle)
        ps.append(p)
    return ps

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

def is_trigo(ps):
    for p, n, nn in tri_gen(ps):
        cp = xcross(n, p, nn)
        return cp > 0


def xcross(center, point, next_point):
    return cross_product(normalize(points_diff(center, point)), normalize(points_diff(center, next_point)))
