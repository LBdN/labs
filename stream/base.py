class GeneratorProto(object):
    def __init__(self, gen, params=None):
        self.gen     = gen
        self.params  = params

    def resolve(self, target):
        coroutine = self.gen(target, self.params)
        coroutine.next() #to start it
        return coroutine

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
                t.send(new_val)

def transformer(target, func):
    while True:
        val = (yield)
        target.send(func(val))

def index(idx, target):
    while True:
        val = (yield)
        target.send((idx, val))

def zzip(length, target):
    _list = [None for i in range(length)]
    while True:
        _val = (yield)
        if _val is not None:
            idx, val = _val
            _list.insert(idx, val)
        if None not in _list:
            target.send(_list)

def sink(target, func):
    assert target is None
    while True:
        val = (yield)
        func(val)

