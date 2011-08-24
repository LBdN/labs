
import numpy      as np
import dart       as dart
from operations import generic_get_orbit, get_0_orbit, get_1_orbit, get_2_orbit


def create_darts(gmap, darts=None):
    if darts is None:
        darts = {}
    for idx, row in enumerate(gmap):
        ddd        = dart.Dart(None, 3)
        ddd.idx    = idx
        darts[idx] = ddd
    return darts

def connect_darts(gmap, darts):
    for i, row in enumerate(gmap):
        if np.any(row > -1): 
            ddd = darts[i]
            for j, idx in enumerate(row):
                if idx > -1:
                    ddd.alphas[j] = darts[idx]

def check(darts, dims):
    for ddd in darts.values():
        if 0 in dims:
            idxs = map(lambda x : x.idx, get_0_orbit(ddd))
            idxs.reverse()
            idxs2 = map(lambda x : x.idx, generic_get_orbit(ddd, 0 ))
            assert idxs ==  idxs2
        if 1 in dims:
            idxs = map(lambda x : x.idx, get_1_orbit(ddd))
            idxs.reverse()
            idxs2 = map(lambda x : x.idx, generic_get_orbit(ddd, 1 ))
            assert idxs ==  idxs2
        if 2 in dims:
            idxs = map(lambda x : x.idx, get_2_orbit(ddd))
            idxs.reverse()
            idxs2 = map(lambda x : x.idx, generic_get_orbit(ddd, 2 ))
            assert idxs ==  idxs2

def check2(darts, dims):
    cycle10 = gen_cycle2(1,0)
    cycle20 = gen_cycle2(2,0)
    cycle21 = gen_cycle2(2,1)
    for ddd in darts.values():
        if 0 in dims:
            idxs = map(lambda x : x.idx, orbit_path(ddd, cycle21))
            idxs2 = map(lambda x : x.idx, generic_get_orbit(ddd, 0 ))
            assert idxs ==  idxs2
            cycle21.send((2,1))
        if 1 in dims:
            idxs = map(lambda x : x.idx, orbit_path(ddd, cycle20))
            idxs2 = map(lambda x : x.idx, generic_get_orbit(ddd, 1 ))
            assert idxs ==  idxs2
            cycle20.send((2,0))
        if 2 in dims:
            idxs = map(lambda x : x.idx, orbit_path(ddd, cycle10))
            idxs2 = map(lambda x : x.idx, generic_get_orbit(ddd, 2 ))
            assert idxs ==  idxs2
            cycle10.send((1,0))

def get_X_orbit_all(darts):
    for ddd in darts.values():
         get_0_orbit(ddd)
         get_1_orbit(ddd)
         get_2_orbit(ddd)

def generic_all(darts):
    for ddd in darts.values():
        generic_get_orbit(ddd, 0 )
        generic_get_orbit(ddd, 1 )
        generic_get_orbit(ddd, 2 )

def orbit_path_all(darts):
    cycle10 = gen_cycle2(1,0)
    cycle20 = gen_cycle2(2,0)
    cycle21 = gen_cycle2(2,1)

    for ddd in darts.values():
        orbit_path(ddd, cycle21)
        orbit_path(ddd, cycle20)
        orbit_path(ddd, cycle10)
        cycle21.send((2,1))
        cycle20.send((2,0))
        cycle10.send((1,0))


def gen_cycle(i,j):
    while True:
        yield i
        yield j

def gen_cycle2(i,j):
    while True:
        nv = (yield i)
        if nv :
            i,j = nv
        nv = (yield j)
        if nv :
            j,i = nv


def orbit_path(dart, cycle):
    scnd_path = False
    orbit     = [dart]
    start_idx = cycle.next()
    cur       = dart.alphas[start_idx]
    while cur != dart:
        orbit.append(cur)
        ncur = cur.alphas[cycle.next()]
        if ncur == cur :
            if scnd_path : 
                break
            scnd_path = True
            _idx = cycle.next()
            start_idx = _idx if _idx != start_idx else cycle.next()
            cur = dart.alphas[start_idx]
        else           : 
            cur = ncur
    return orbit 

class Traverser(object):
    def __init__(self, gmap):
        self.seen = np.zeros(gmap.shape[0])
        self.seen.fill(-1)
        self.stack = np.zeros(gmap.shape[0])
        self.stack.fill(-1)

    def traverse(self, dart_idx, gmap, dims):
        cur = 0
        self.stack[0] = dart_idx
        self.seen[dart_idx] = 1
        while self.stack[cur] != -1:
            idx = self.stack[cur]
            for i, d in enumerate(dims):
                t = gmap[idx][d]
                if t != -1 and self.seen[t] == -1 :
                    self.seen[t] = 1
                    self.stack[cur+i+1] = t
            cur = cur + 1
        return self.seen, self.stack #np.nonzero(self.seen > -1)

def main(path=None):
    path = path or './data/gmap_2011.08.16_15:12.np'
    gmap = np.fromfile(path)
    gmap = gmap.reshape( gmap.shape[0]/3, 3)
    darts = create_darts(gmap)
    connect_darts(gmap, darts)
    return gmap, darts

if __name__ == '__main__':
    main()
