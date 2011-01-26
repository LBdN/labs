cdef extern from "math.h":
 double sqrt(double)
 double abs(double)


cdef class Vector:
    cdef readonly float x, y, z

    def __init__(self, float x, float y, float z):
        self.x = x
        self.y = y
        self.z = z

    #def __eq__(self, Vector vec):
        #if self.x != vec.x : return False
        #if self.z != vec.z : return False
        #if self.y != vec.y : return False
        #return True

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

    #def is_orthogonal(self, vector) :
        #return is_same(self.unit().dot_product(vector.unit()), 0)

    #def is_colinear(self, vector) :
        #return is_same(self.unit().cross_product(vector.unit()), 0)
        #return self.opposite()

    #def __str__(self) :
        #string = '('
        #for i in xrange(len(self)):
            #string += str(self[i])+','
        #return string[:-1] + ')'

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
        p  = ps[i]        #current point
        n  = ps[(i+1)%l]  #next point
        nn = ps[(i+2)%l]  #next next point
        #==
        z  = (n.x - p.x) * (nn.y - n.y)
        z -= (n.y - p.y) * (nn.x - n.x)
        if   z < 0  : flag |= 1
        elif z > 0  : flag |= 2
        if flag == 3: return False
    return True

PRECISION = 0.01

cdef inline float pseudo_prod(Vector p, Vector n): 
    return (p.x*n.y) - (n.x*p.y)

cpdef float area(list ps):
    return abs(_area(ps))

cdef float _area(list ps):
    cdef int i, l
    cdef float s
    cdef Vector p, n
    l = len(ps)
    for i in range(l):
        p = ps[i]        #current point
        n = ps[(i+1)%l]  #next point
        #==
        s += pseudo_prod(p, n)
    return 0.5*s

cpdef bint is_ccw(list ps):
    return area(ps)> 0
