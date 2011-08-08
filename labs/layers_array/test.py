import itertools

class Layers(object):
    def __init__(self, l, p, idx, vtx):
        self.vtx = vtx
        self.idx = idx
        self.p   = p
        self.l   = l

def quad(w, h):
    vtx = list(itertools.product((-w, +w), (-h, +h)))
    idx = [i for i,v in enumerate(vtx)]
    p   = [(0, len(idx))]
    l   = [[0, 0]]
    return Layers(l, p, idx, vtx)

def add_layers(l1, l2):
    vtxs = l1.vtx + l2.vtx
    #==
    idx2 = [i+len(l1.vtx) for i in l2.idx]
    idxs = l1.idx + idx2
    #==
    p2   = [(i[0]+len(l1.idx), i[1]+len(l1.idx)) for i in l2.p]
    ps   = l1.p + p2
    #==
    l2   = [ (i[0]+len(l1.p), i[1]+len(l1.p)) for i in l2.l]
    ls   = l1.l + l2
    #==
    return Layers(ls, ps, idxs, vtxs)

