
import numpy      as np
import dart       as dart
import operations as ops


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
            idxs = map(lambda x : x.idx, ops.get_0_orbit(ddd))
            idxs.reverse()
            idxs2 = map(lambda x : x.idx, ops.generic_get_orbit(ddd, 0 ,''))
            assert idxs ==  idxs2
        if 1 in dims:
            idxs = map(lambda x : x.idx, ops.get_1_orbit(ddd))
            idxs.reverse()
            idxs2 = map(lambda x : x.idx, ops.generic_get_orbit(ddd, 1 ,''))
            assert idxs ==  idxs2
        if 2 in dims:
            idxs = map(lambda x : x.idx, ops.get_2_orbit(ddd))
            idxs.reverse()
            idxs2 = map(lambda x : x.idx, ops.generic_get_orbit(ddd, 2 ,''))
            assert idxs ==  idxs2

def check2(darts, dims):
    cycle01 = gen_cycle(0,1)
    cycle02 = gen_cycle(0,2)
    cycle12 = gen_cycle(1,2)
    for ddd in darts.values():
        if 0 in dims:
            idxs = map(lambda x : x.idx, orbit_path(ddd, cycle12))
            idxs2 = map(lambda x : x.idx, ops.generic_get_orbit(ddd, 0 ,''))
            assert set(idxs) ==  set(idxs2)
        if 1 in dims:
            idxs = map(lambda x : x.idx, orbit_path(ddd, cycle02))
            idxs2 = map(lambda x : x.idx, ops.generic_get_orbit(ddd, 1 ,''))
            assert set(idxs) ==  set(idxs2)
        if 2 in dims:
            idxs = map(lambda x : x.idx, orbit_path(ddd, cycle01))
            idxs2 = map(lambda x : x.idx, ops.generic_get_orbit(ddd, 2 ,''))
            assert set(idxs) ==  set(idxs2)

def generic_all(darts):
    for ddd in darts.values():
        ops.generic_get_orbit(ddd, 0 ,'')
        ops.generic_get_orbit(ddd, 1 ,'')
        ops.generic_get_orbit(ddd, 2 ,'')

def orbit_path_all(darts):
    cycle01 = gen_cycle(0,1)
    cycle02 = gen_cycle(0,2)
    cycle12 = gen_cycle(1,2)
    for ddd in darts.values():
        orbit_path(ddd, cycle12)
        orbit_path(ddd, cycle02)
        orbit_path(ddd, cycle01)

def gen_cycle(i,j):
    while True:
        yield i
        yield j

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
            # break
            scnd_path = True
            _idx = cycle.next()
            start_idx = _idx if _idx != start_idx else cycle.next()
            cur = dart.alphas[start_idx]
        else           : 
            cur = ncur
    return orbit

def traverse(dart_idx, gmap, dims):
    cur  = 0
    seen = np.zeros(gmap.shape[0])
    seen.fill(-1)
    stack = np.zeros(gmap.shape[0])
    stack.fill(-1)
    stack[0] = dart_idx
    seen[dart_idx] = 1
    while stack[cur] != -1:
        idx = stack[cur]
        for i, d in enumerate(dims):
            t = gmap[idx][d]
            if t != -1 and seen[t] == -1 :
                seen[t] = 1
                stack[cur+i+1] = t
        cur = cur + 1
    return np.nonzero(seen > -1)

def main(path=None):
    path = path or './data/gmap_2011.08.16_15:12.np'
    gmap = np.fromfile(path)
   
    gmap = gmap.reshape( gmap.shape[0]/3, 3)
    darts = create_darts(gmap)
    connect_darts(gmap, darts)
    return gmap, darts

if __name__ == '__main__':
    main()
