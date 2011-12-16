cdef class Gmap:

    cdef int counter
    cdef public list darts

    def __init__(self):
        self.counter = 0
        self.darts   = []

    def new_dart(self, embedding):
        d = Dart(self.counter, embedding)
        self.counter += 1
        self.darts.append(d)
        return d

cdef class Cycle:

    cdef int start, end, current

    def __cinit__(self, int start, int end):
        self.start   = start
        self.end     = end
        self.current = start

    cpdef int next(self):
        res          = self.current
        self.current = self.end if self.current == self.start else self.start
        return res

    cpdef reset(self):
        self.current = self.start

cycle21 = Cycle(2,1)
cycle20 = Cycle(2,0)
cycle10 = Cycle(1,0)

cdef class Dart:

    cdef readonly int idx
    cdef dict embedding
    cdef Dart alpha0
    cdef Dart alpha1
    cdef Dart alpha2

    def __init__(self, int idx, dict embedding):
        self.idx       = idx
        self.embedding = embedding
        self.alpha0    = self
        self.alpha1    = self
        self.alpha2    = self

    property alphas:
        def __get__(self):
            return [self.alpha0, self.alpha1, self.alpha2]

    cpdef Dart get_alpha(self, int idx):
        if idx == 0 : return self.alpha0
        if idx == 1 : return self.alpha1
        if idx == 2 : return self.alpha2

    cpdef set_alpha(self, int idx, Dart d):
        if idx == 0 : self.alpha0 = d
        if idx == 1 : self.alpha1 = d
        if idx == 2 : self.alpha2 = d
        
    def orbit(self, int dim):
        cdef Cycle cycle
        cdef list orbit
        cdef bint scnd_path 
        cdef Dart cur, ncur
        #==
        if   dim == 0 : cycle = cycle21
        elif dim == 1 : cycle = cycle20
        else          : cycle = cycle10
        #==
        scnd_path = False
        orbit     = [self]
        cur       = self.get_alpha(cycle.next())
        while cur != self:
            orbit.append(cur)
            ncur = cur.get_alpha(cycle.next())
            if ncur == cur :
                if scnd_path : 
                    break
                scnd_path = True
                cycle.reset()
                cycle.next() #to use end
                cur = self.get_alpha(cycle.next())
            else           : 
                cur = ncur
        return orbit 
