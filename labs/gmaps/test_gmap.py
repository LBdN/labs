
import numpy as np

import context
import gamr7_lib.g_maps.dart as dart
import gamr7_lib.g_maps.g_maps_operations as g_ops


gmap = np.fromfile('gmap_2011.08.16_15:12.np')
gmap = gmap.reshape(100000, 3)

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
            idxs = map(lambda x : x.idx, g_ops.get_0_orbit(ddd))
            idxs.reverse()
            idxs2 = map(lambda x : x.idx, g_ops.generic_get_orbit(ddd, 0 ,''))
            assert idxs ==  idxs2
        if 1 in dims:
            idxs = map(lambda x : x.idx, g_ops.get_1_orbit(ddd))
            idxs.reverse()
            idxs2 = map(lambda x : x.idx, g_ops.generic_get_orbit(ddd, 1 ,''))
            assert idxs ==  idxs2
        if 2 in dims:
            idxs = map(lambda x : x.idx, g_ops.get_2_orbit(ddd))
            idxs.reverse()
            idxs2 = map(lambda x : x.idx, g_ops.generic_get_orbit(ddd, 2 ,''))
            assert idxs ==  idxs2

def traverse(dart_idx, gmap, dims):
    cur  = 0
    seen = np.zeros(gmap.shape[0])
    seen.fill(-1)
    stack = np.zeros(gmap.shape[0])
    stack.fill(-1)
    stack[0] = dart_idx
    while stack[cur] != -1:
        idx = stack[cur]
        for i, d in enumerate(dims):
            t = gmap[idx][d]
            if t != -1 and seen[t] == -1 :
                seen[t] = 1
                stack[cur+i+1] = t
        cur = cur + 1
    return np.nonzero(seen > -1)

def main():
    gmap = np.fromfile('gmap_2011.08.16_15:12.np')
    gmap = gmap.reshape(100000, 3)
    darts = create_darts(gmap)
    connect_darts(gmap, darts)
    return gmap, darts

if __name__ == '__main__':
    main()
