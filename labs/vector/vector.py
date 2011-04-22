from math                    import sqrt, radians, cos, sin, acos, degrees, pi, atan

from itertools         import izip

PRECISION = 1e-2
def is_same(x,y):
    return abs(x-y) <= PRECISION

def create_vector_from_points(start, end) :
    return Vector([e2-e1 for e1,e2 in zip(start, end)])

class Vector(tuple) :
    def __init__(self, *args):
        self._magnitude        = None
        self._square_magnitude = None
        self._unit             = None

    def angle(self) :
        """
        Return the angle of a vector in degrees.
        """
        x,y = float(self[0]),float(self[1])
        r   = sqrt(x*x+y*y)
        if   r == 0           : return 0.0
        elif y == 0 and x < 0 : return 180.0
        else                  :
            try                      : return degrees(2 * atan(y / (r + x)) + 2*pi) % 360
            except ZeroDivisionError :
                if is_same(y, 0) and x < 0 : return 180.
                else                       : return 0.

    def angle_with(self, vec) :
        """
        Return the angle between two vectors in degrees.
        Convention : angle_between(x,y) = - angle_between(y,x) and angles in [-360, 360]
        """
        return self.angle() - vec.angle()

    def oriented_angle_with(self, vec) :
        """
        Convention : angle_between(x,y) = - angle_between(y,x) and angles in [-180, 180]
        """
        angle = self.unoriented_angle_with(vec)
        if self.cross_product(vec) > 0 : return -angle
        else                           : return angle

    def oriented_angle_with_convention(self, vec) :
        """
        Convention : angle_between(x,y) = - angle_between(y,x) and angles in [-180, 180], convention is for Math Convention
        """
        angle = self.unoriented_angle_with(vec)
        if self.cross_product(vec) > 0 : return angle
        else                           : return -angle

    def unoriented_angle_with(self, vec, precision=None) :
        """
        Convention : angle_between(x,y) = angle_between(y,x) and angles in [0, 180]
        """
        unit_self = self.unit()
        vec_unit  = vec.unit()
        dot_prod  = unit_self.dot_product(vec_unit)
        # ==
        if not precision: precision = PRECISION
        if   abs( 1.0 - dot_prod) < precision :dot_prod = 1.
        elif abs(-1.0 - dot_prod) < precision :dot_prod = -1.
        return degrees(acos(dot_prod))

    def dot_product(self, vec) :
        assert len(self) == len(vec), "Vectors must have same length"
        return sum([s*v for s, v in izip(self, vec)])

    def cross_product(self, vec) :
        # det(self, vec) = -det(vec, self)
        assert len(self) == len(vec) >= 2, "Vectors must have same length"
        return self[0] * vec[1] - vec[0] * self[1]

    def cross_product3D(self, vec) :
        assert len(self) == len(vec) == 3, "Vectors must have same length"
        x = self[1] * vec[2] - self[2] * vec[1]
        y = self[2] * vec[0] - self[0] * vec[2]
        z = self[0] * vec[1] - self[1] * vec[0]
        return Vector((x, y, z))

    def multiply(self, scalar) :
        return Vector([i*scalar for i in self])

    def magnitude(self) :
        if self._magnitude is None:
            self._magnitude = sqrt(self.square_magnitude())
        return self._magnitude

    def square_magnitude(self) :
        if self._square_magnitude is None:
            self._square_magnitude = sum([i**2 for i in self])
        return self._square_magnitude

    def unit(self) :
        if self._unit is None:
            magnitude = self.magnitude()
            if magnitude != 0 : self._unit = self.multiply(1./magnitude)
            else              : self._unit = self
        # ==
        return self._unit

    def normal(self, trigo_rotation = None) :
        # cw == clock_wise
        cw_normal  = Vector((self[1], -self[0]))
        ccw_normal = Vector((-self[1], self[0]))
        if trigo_rotation is None : return cw_normal, ccw_normal
        else                      : return ccw_normal if trigo_rotation else cw_normal

    def opposite(self) :
        return Vector([-x for x in self])

    def is_orthogonal(self, vector) :
        return is_same(self.unit().dot_product(vector.unit()), 0)

    def is_colinear(self, vector) :
        return is_same(self.unit().cross_product(vector.unit()), 0)

    def radians_rotate(self, angle) :
        x     = cos(angle) * self[0] - sin(angle) * self[1]
        y     = sin(angle) * self[0] + cos(angle) * self[1]
        return Vector((x,y))

    def rotate(self, angle) :
        theta = radians(angle)
        x     = cos(theta) * self[0] - sin(theta) * self[1]
        y     = sin(theta) * self[0] + cos(theta) * self[1]
        return Vector((x,y))

    def add(self, vect) :
        assert len(self) == len(vect), "Vectors must have same length : %s  ----   %s" %(str(self), str(vect))
        return Vector([el_self + el_vect for el_self, el_vect in izip(self, vect)])

    def sub(self, vect) :
        assert len(self) == len(vect), "Vectors must have same length : %s  ----   %s" %(str(self), str(vect))
        return Vector([el_self - el_vect for el_self, el_vect in izip(self, vect)])

    # == Surcharge des operateurs :

    def __sub__(self, vect) :
        return self.sub(vect)

    def __add__(self, vect) :
        return self.add(vect)

    def __mul__(self, scalar) :
        return self.multiply(scalar)

    __rmul__ = __mul__

    def __neg__(self) :
        return self.opposite()

    def __str__(self) :
        string = '('
        for i in xrange(len(self)):
            string += str(self[i])+','
        return string[:-1] + ')'

    def __eq__(self, vect)    :
        if len(self) != len(vect) : return False
        # ==
        self_is_equal_to_vect = True
        for i, coord in enumerate(self) : self_is_equal_to_vect = self_is_equal_to_vect and (coord == vect[i])
        # ==
        return self_is_equal_to_vect

    def convert_to_vec3D_ifn(self, val = 0) :
        if len(self) == 2 : return Vector((self[0], self[1], val))
        else              : return self
