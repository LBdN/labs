import types
import collections
#==
import labs.data_structure.tree as tree

class GeneratorProto(object):
    def __init__(self, gen, params=None):
        self.gen     = gen
        self.params  = params

    def resolve(self, target):
        coroutine = self.gen(target, self.params)
        coroutine.next() #to start it
        return coroutine

    def __repr__(self):
        return "%s ( %s ) " %(_str(self.gen), _str(self.params))

def _str(obj):
    if isinstance(obj, types.FunctionType):
        return obj.func_name
    else:
        return str(obj)


def GenTreeDrawer(g, inc):
    _str = '  '*inc + g.__name__+ '\n'
    if g.__name__ == 'broadcast':
        for child in g.gi_frame.f_locals['targets']:
            _str += ''.join(GenTreeDrawer(child, inc+1))
    elif g.__name__ == 'sink':
        pass
    else:
        child = g.gi_frame.f_locals['target']
        _str += ''.join(GenTreeDrawer(child, inc+1))
    return _str

def gen_to_tree(g):
    n = tree.Node(cargo=g)
    #==
    if   g.__name__ == 'broadcast' : children = g.gi_frame.f_locals['targets']
    elif g.__name__ == 'sink'      : children = []
    else                           : children = [g.gi_frame.f_locals['target']]
    #==
    for child in children:
        tree.connect(gen_to_tree(child), n)
    return n

def value(target, x):
    start = (yield)
    target.send(x)
    while True:
        end = (yield)

def broadcast(targets):
    while True:
        new_val = (yield)
        if new_val is not None:
            for t in targets:
                #print 'broadcasting to %s' %t.__name__
                t.send(new_val)

def transformer(target, func):
    while True:
        val = (yield)
        if isinstance(val, collections.Sequence) : target.send(func(*val))
        else                                     : target.send(func(val))

def index(idx, target):
    while True:
        val = (yield)
        #print 'index forwarding to %s' %target.__name__
        target.send((idx, val))

def zzip(length, target):
    _list = [None for i in range(length)]
    while True:
        _val = (yield)
        if _val is not None:
            #print "getting partial result"
            idx, val   = _val
            _list[idx] = val
        if None not in _list:
            #print 'zipping and sending to %s' %target.__name__
            target.send(_list)

def sink(target, func):
    assert target is None
    while True:
        val = (yield)
        func(val)

