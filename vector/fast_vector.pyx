import itertools

cdef extern from "math.h":
 double sqrt(double)
 double fabs(double)

cdef inline float _max(float a, float b): return a if a >= b else b
cdef inline float _min(float a, float b): return a if a <= b else b


cdef class Vector:
    cdef readonly float x, y, z

    def __init__(self, float x, float y, float z):
        self.x = x
        self.y = y
        self.z = z

    def __richcmp__(self, Vector vec, op):
        if op == 2:
            if self.x != vec.x : return False
            if self.z != vec.z : return False
            if self.y != vec.y : return False
            return True
        elif op == 3:
            if self.x != vec.x : return True
            if self.z != vec.z : return True
            if self.y != vec.y : return True
            return False

    def __neg__(self) :
        return Vector(- self.x, - self.y, -self.z)

    def __add__(Vector self, Vector vec):
        return Vector(self.x+vec.x, self.y+vec.y, self.z+vec.z)

    def __sub__(Vector self, Vector vec):
        return Vector(self.x-vec.x, self.y-vec.y, self.z-vec.z)

    def __mul__(Vector self, float scalar) :
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)

    def __imul__(Vector self, float scalar) :
        self.x = self.x * scalar
        self.y = self.y * scalar
        self.z = self.z * scalar
        return self

    cpdef float dot_product(self, Vector vec) :
        return (self.x * vec.x) + (self.y * vec.y) + (self.z * vec.z)

    cpdef Vector cross_product3D(self, Vector vec) :
        cdef float x, y, z
        x = self.y * vec.z - self.z * vec.y
        y = self.z * vec.x - self.x * vec.z
        z = self.x * vec.y - self.y * vec.x
        return Vector(x, y, z)

    cpdef float cross_product(self, Vector vec):
        return (self.x * vec.y) - (vec.x * self.y)
    
    cpdef float sq_magnitude(self):
        return self.dot_product(self)

    cpdef float magnitude(self):
        return sqrt(self.dot_product(self))

    cpdef Vector unit(self) :
        cdef float sq_magnitude
        magnitude = sqrt(self.sq_magnitude())
        if magnitude != 0 : return self * (1./magnitude)
        else              : return self

    cpdef Vector iunit(self):
        cdef float sq_magnitude
        magnitude = sqrt(self.sq_magnitude())
        if magnitude != 0 : 
            self.x = self.x / magnitude
            self.y = self.y / magnitude
            self.z = self.z / magnitude

    def __repr__(self) :
        return "Vector ( x:%s y:%s z:%s ) "%(self.x, self.y, self.z)

    def __str__(self) :
        return "Vector ( x:%s y:%s z:%s ) "%(self.x, self.y, self.z)

cdef class Line:
    cdef readonly Vector origin
    cdef readonly Vector direction
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

cdef connect(Segment before, Segment after):
    before.after = after
    after.before = before
    #==
    before.invariant()
    after.invariant()

cdef class Segment:
    cdef readonly Vector start, end
    cdef readonly Segment before, after
    def __init__(self, start, end, before=None, after=None):
        self.start = start
        self.end   = end
        self.before = None
        self.after  = None

    def invariant(self):
        #==
        assert not before or self.start  == before.end
        assert not after  or after.start == self.end

    cpdef Line to_line(self):
        return Line(self.start, self.end - self.start)

    cpdef bool in_bbox(self, Vector v):
        bl, tr = bbox([self.start, self.end])
        return (v.x >= bl.x and v.x =< tr.x) and \
               (v.y >= bl.y and v.y =< tr.y) 

    cpdef tuple split(self, Vector v):
        until_v = Segment(self.start, v) 
        after_v = Segment(v, self.end) 
        #==
        if self.before:
            connect(self.before, until_v)
        if self.after:
            connect(after_v, self.after)
        connect(until_v, after_v)
        #==
        return until_v, after_v

    cpdef bool ends_of(self, Vector v):
        if self.start == v : return True
        if self.end   == v : return True
        #==
        return False

cpdef Vector segm_intersect(Segment s1, Segment s2):
    cdef Line l1  = s1.to_line()
    cdef Line l2  = s2.to_line()
    cdef Vector p = line_intersect(l1, l2)
    if s1.in_bbox(p):
        return p

cdef Vector line_intersect(Line l0, Line l2):
    cdef float d = det(l1.direction, l2.direction)
    cdef float d2
    cdef Vector o1o2
    if d != 0:
        o1o2 = l2.origin - l1.origin
        d2   = det(o1o2, l2.direction)
        return l1.origin + (l1.direction * (d2/d))
    #==
    o1o2 = l2.origin - l1.origin
    d2   = det(o1o2, l1.direction)
    if d2 == 0 :
        return l1.origin

def bool poly_self_intersect(list ps)
    cdef Vector p
    for p1, p2 in itertools.combinations(ps, 2):
        p = segm_intersect(p1, p2):
        if not p : continue
        #==
        if not p1.ends_of(p) and not p2.ends_of(p)
            return True
    return False

cpdef Vector from_points(tuple p1, tuple p2):
    return Vector(p1[0]-p2[0], p1[1] - p2 [1], 0)

cpdef float xcross(tuple p1, tuple p2, tuple p3): 
    cdef Vector v1, v2
    v1 = from_points(p1, p2)
    v1.iunit()
    v2 = from_points(p1, p3)
    v2.iunit()
    return v1.cross_product(v2)

cpdef float xcross2(Vector v1, Vector v2, Vector v3):
    cdef Vector v5, v4
    v4 = v1 - v2
    v5 = v2 - v3
    v4.iunit()
    v5.iunit()
    return v4.cross_product(v5)


cpdef bool is_convex(list ps):
    cdef int i, l, flag
    cdef float z
    cdef Vector p, n, nn
    l = len(ps)
    for i in range(l):
        p  = <Vector>ps[i]        #current point
        n  = <Vector>ps[(i+1)%l]  #next point
        nn = <Vector>ps[(i+2)%l]  #next next point
        #==
        z  = (n.x - p.x) * (nn.y - n.y)
        z -= (n.y - p.y) * (nn.x - n.x)
        if   z < 0  : flag |= 1
        elif z > 0  : flag |= 2
        if flag == 3: return False
    return True

def convert_vec(list pol):
    cdef list result = []
    cdef tuple pt
    for pt in pol:
        result.append(Vector(pt[0], pt[1], 0))
    return result

cpdef bool is_on_line(Line l1, Vector p):
    if is_same(p, l1.origin, PRECISION)              : return True
    if is_same(p, l1.origin+l1.direction, PRECISION) : return True
    #==
    cdef Vector v =  p - l1.origin
    cdef float dp = l1.direction.dot_product(v)
    cdef float angle =  dp / (v.magnitude() * l1.direction.magnitude())
    #==
    if   is_same(angle, 0.0, PRECISION)   : return True
    elif is_same(angle, 360.0, PRECISION) : return True
    else                                  : return False

cpdef bool is_on_segment(Segment s, Vector v):
    return is_on_line(s.toLine(), v) and \
           s.in_bbox(v)

cdef float PRECISION = 0.0001

cdef inline bint is_same(float value, float target, float precision):
    return fabs(value-target) < precision

cdef inline float det(Vector p, Vector n): 
    return (p.x*n.y) - (n.x*p.y)

cpdef float area(list ps):
    return fabs(_area(ps))

cdef float _area(list ps):
    cdef int i, l
    cdef float s = 0.0
    cdef Vector p, n
    l = len(ps)
    for i in range(l):
        p = <Vector>ps[i]        #current point
        n = <Vector>ps[(i+1)%l]  #next point
        #==
        s += det(p, n)
    return 0.5*s

cpdef Vector center(list ps):
    cdef int i, l
    cdef float cx, cy, area
    cdef Vector p, n
    l = len(ps)
    for i in range(l):
        p = <Vector>ps[i]        #current point
        n = <Vector>ps[(i+1)%l]  #next point
        cx += (p.x + n.x)* (p.x*n.y - n.x*p.y)
        cy += (p.y + n.y)* (p.x*n.y - n.x*p.y)
    area = _area(ps)
    cx /= 6 * area
    cy /= 6 * area
    return Vector(cx, cy, 0) 

cpdef tuple bbox(list ps):
    cdef int i, l
    cdef float max_x, max_y, min_x, min_y
    cdef Vector p
    l = len(ps)
    for i in range(l):
        p = <Vector>ps[i]        #current point
        max_x = _max(p.x, max_x)
        max_y = _max(p.y, max_y)
        min_x = _min(p.x, min_x)
        min_y = _min(p.y, min_y)
    return Vector(min_x, min_y, 0), Vector(max_x, max_y, 0)

cpdef bint is_ccw(list ps):
    return _area(ps)> 0
