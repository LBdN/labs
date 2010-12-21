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
    nb_arg = f.__code__.co_argcount
    islots = []
    for i in range(nb_arg):
        islot = graph.ISlot()
        islots.append(islot)
        tree.connect(tn, islot)
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
def pprint(a):
    print a

def test():
    gp = base.GeneratorProto(base.value, 5)
    tn = graph.TNode(cargo=gp)
    os = graph.OSlot()
    tree.connect(os, tn)
    #==
    oss = [os]
    i   = 0
    while oss and i<100:
        op = random.choice([add, minus, inc, decr, pprint])
        i  = i + 1
        iss, _, os = func_to_node(op)
        for i in iss:
            tree.connect(i, random.choice(oss))
        if os:
            oss.append(os)
    #==
    while oss:
        op = pprint
        iss, _, os = func_to_node(op)
        for i in iss:
            tree.connect(i, oss.pop())
    assert not oss
    return tn
