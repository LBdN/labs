import numpy as np
adjency_matrix = np.zeros(3000000)
adjency_matrix.fill(-1)
adjency_matrix = adjency_matrix.reshape(1000000,3)
counter = 0

class Alpha(list):
    def __init__(self, val, parent):
        list.__init__(self, val)
        self.parent = parent

    def __setitem__(self, key, value):
        list.__setitem__(self, key, value)
        adjency_matrix[self.parent.idx][key] = value.idx

class Dart(object):
    __slots__ =['alphas','embedding','_spline','_polygon', 'idx']
    def __init__(self, embedding, cell_dimension):
        global counter
        self.idx = counter
        counter +=1

        #HACK for optim
        #self.alphas      = [self for i in xrange(cell_dimension)]
        assert cell_dimension==3
        self.alphas = Alpha([self, self, self], self)
        self.embedding   = embedding
        # ==
        #HACK for optim
        self._spline     = None
        self._polygon    = None
        # ==
        
    def delete(self):
        self.alphas = None
        self.embedding.delete()
        
    def get_dimension(self):
        return len(self.alphas)
    
    def __repr__(self):
        res = str(self.__class__)+ ' : '+str(id(self))
        return res+'\n'+str(self.embedding)
        
    def get_discretized_curv(self):
        return self.embedding.curv_generator.get_discretized_curv(self.embedding.pos, self.alphas[0].embedding.pos)
    
    def is_dead_end(self):
        return self.alphas[1]==self.alphas[2]
        
