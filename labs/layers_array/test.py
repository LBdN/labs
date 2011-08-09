import itertools

class Layers(object):
    def __init__(self, mat, l, p, idx, vtx):
        self.mat = mat
        self.vtx = vtx
        self.idx = idx
        self.p   = p
        self.l   = l

def quad(w, h, mat):
    vtx = list(itertools.product((-w, +w), (-h, +h)))
    idx = [i for i,v in enumerate(vtx)]
    p   = [(0, len(idx))]
    l   = [[0, 0]]
    m   = [mat]
    return Layers(m, l, p, idx, vtx)

def add_layers(l1, l2):
    vtxs = l1.vtx + l2.vtx
    #==
    idx2 = [i+len(l1.vtx) for i in l2.idx]
    idxs = l1.idx + idx2
    #==
    p2   = [(i[0]+len(l1.idx), i[1]+len(l1.idx)) for i in l2.p]
    ps   = l1.p + p2
    #==
    ll2   = [ (i[0]+len(l1.p), i[1]+len(l1.p)) for i in l2.l]
    ls   = l1.l + ll2
    #==
    ms   = l1.mat + l2.mat
    return Layers(ms, ls, ps, idxs, vtxs)

# generate convex polys
# merge them into a numpy structure
# run shrink

def test1():
    return add_layers(quad(10,10, (10,01), quad(15,21, (5,5)))

