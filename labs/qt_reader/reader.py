


class Reader(object):
    def match(self, obj):
        return isinstance(obj.get_value(), self._type)

    def read(self, obj, ctx):
        if not obj.is_name() and obj.parents and not obj.is_union():
            debug_func()
        if not self.match(obj):
            return self.not_match(obj, ctx)
        #==
        view, new_ctx = self._read(obj, ctx)
        return view, new_ctx

    def not_match(self, obj, ctx):
        return obj, ctx

#import p_base
#import qtgraph
#class NodeReader(Reader):
    #_type = p_base.Node

    #def __init__(self, ctx_qt):
        #self.ctx_qt = ctx_qt
        #self.graph  = qtgraph.Graph(ctx_qt.view)
        #self.done   = False
        #self.nodes  = []

    #def _read(self, any_val, ctx):
        #n = self.graph.drawNode(any_val, 50, ( len(self.nodes)*50, len(self.nodes)*50))
        #self.nodes.append(n)
        #return make_scope(any_val, ctx)

class MetaReader(object):
    def __init__(self, readers):
        self.readers = readers
        for r in self.readers:
            r.meta = self
        self.seen = set([])

    def read_all(self, to_read, seen=None):
        max = 100
        seen = seen if seen is not None else self.seen
        while to_read and max :
            el, ctx = to_read.pop()
            if not isinstance(el, list):
                el = [el]
            for sub_el in el :
                r= self.read_one(sub_el, ctx, seen)
                if r is not None :
                    to_read.append(r)

    def read_one(self, el, ctx, seen):
        assert_( el not in seen )
        seen.add(el)
        for r in self.readers:
            res, nctx = r.read(el, ctx)
            print "%s :: %s -> %s" %(r, el, res)
            el.init_notification()
            if   res is None : 
                return None 
            elif res != el   : 
                if not isinstance(res, list):
                    res = [res]
                for rr in res:
                    assert_( rr not in seen)
                return res, nctx
