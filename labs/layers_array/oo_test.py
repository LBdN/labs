class Transaction(object):
    def __init__(self, sources, vtx_buffer=None):
        self.sources    = sources
        self.vtx_buffer = vtx_buffer or VertexBuffer()

    def as_vtx(self):
        for s in self.sources:
            for layer in s.layers:
                for polygon in layer.polygons:
                    for idx in polygon.idxs:
                        yield self.vtx_buffer[idx]

    def fusion(self, other):
        idx_delta      = len(self.vtx_buffer)
        new_vtx_buffer = VertexBuffer(self.vtx_buffer + other.vtx_buffer)
        new_transaction = Transaction([], new_vtx_buffer)
        for source in other.sources:
            new_source = Source(source.name, [])
            new_transaction.sources.append(new_source)
            for layer in source.layers:
                new_layer = Layer([], layer.matrix)
                new_source.layers.append(new_layer)
                for polygon in layer.polygons:
                    nidx = [idx+idx_delta for idx in polygon.idxs]
                    new_polygon = Polygon(nidx, polygon.is_hole)
                    new_layer.polygons.append(new_polygon)
        return new_transaction
                        

class VertexBuffer(list):
    def append(self, item):
        idx = len(self)
        list.append(self, item)
        assert self[idx] == item
        return idx

    def add_quad(self, w, h):
        vtxs = [(1,1), (1,-1), (-1,-1), (-1,1)]
        idxs = [self.append((v[0]*w, v[1]*h)) for v in vtxs]
        return idxs

class Source(object):
    def __init__(self, name, layers):
        self.name   = name
        self.layers = layers

class Layer(object):
    def __init__(self, polygons, matrix):
        self.matrix   = matrix
        self.polygons = polygons

class Polygon(object):
    def __init__(self, idxs, is_hole):
        self.idxs    = idxs
        self.is_hole = is_hole



def from_vertex(idx, mat=(0,0)):
    return Layer([Polygon(idx, False)])


# generate convex polys
# merge them into a numpy structure
# run shrink

def test1():
    t = Transaction([])
    #==
    s = Source('test1',[])
    t.sources.append(s)
    #==
    for w in range(0,30,5):
        for h in range(0,30,5):
            idxs = t.vtx_buffer.add_quad(w, h)
            l    = Layer([Polygon(idxs, False)], (w,h))
            s.layers.append(l)
    return t
