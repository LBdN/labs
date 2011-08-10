import itertools

class Layers(object):
    def __init__(self, mat, l, p, idx, vtx):
        assert isinstance(mat, list)
        self.mat = mat
        self.vtx = vtx
        self.idx = idx
        self.p   = p
        self.l   = l

    def as_vtx(self):
        vtx = []
        for layer, mat in zip(self.l, self.mat):
            for poly in self.p[layer[0]:layer[1]]:
                print "poly", poly
                for idx in self.idx[poly[0]: poly[1]]:
                    print "idx", idx
                    v = self.vtx[idx]
                    vtx.append((v[0]+mat[0], v[1]+mat[1]))
        return vtx

def quad(w, h, mat):
    vtx = list(itertools.product((+w, -w), (h, -h)))
    return from_vertex(vtx, mat)

def from_vertex(vtx, mat=(0,0)):
    idx = [i for i,v in enumerate(vtx)]
    idx.append(0)
    p   = [(0, len(idx))]
    l   = [[0, 1]]
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
    return add_layers(quad(10,10, (10,01)), quad(15,21, (5,5)))
