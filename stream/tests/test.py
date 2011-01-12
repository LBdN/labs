import random
#==
from labs.stream         import base
from labs.stream         import graph
from labs.data_structure import tree

def func_to_node(f):
    sink =  f.__dict__.get('sink')
    if sink: gen = base.sink
    else   : gen = base.transformer
    gp = base.GeneratorProto(gen, f)
    tn = graph.TNode(cargo=gp)
    #==
    if not sink:
        os = graph.OSlot()
        tree.connect(os, tn)
    else:
        os = None
    #==
    if f.__code__.co_varnames: nb_arg = 1
    else                     : nb_arg = f.__code__.co_argcount
    islots = []
    for i in range(nb_arg):
        islot = graph.ISlot()
        islots.append(islot)
        tree.connect(tn, islot)
    #==
    return islots, tn, os

def add(a, b):
    return a+b

def minus(a, b):
    return a-b

def inc(a):
    return a + 2

def decr(a):
    return a - 1

def sink(f):
    f.__dict__['sink'] = True
    return f

@sink
def pprint(*args):
    print args

def test():
    gp = base.GeneratorProto(base.value, 5)
    tn = graph.TNode(cargo=gp)
    os = graph.OSlot()
    tree.connect(os, tn)
    #==
    oss = [os]
    for i in range(100):
        op         = random.choice([add, minus, inc, decr])
        iss, _, os = func_to_node(op)
        for i in iss:
            tree.connect(i, random.choice(oss))
        oss.append(os)
    #==
    op         = pprint
    iss, _, os = func_to_node(op)
    while oss:
        tree.connect(random.choice(iss), oss.pop())
    assert not oss
    return tn
