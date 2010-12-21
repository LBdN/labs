from .. import base
from .. import graph
#from ..data_structure import tree

def func_to_node(f):
    gp = base.GeneratorProto(base.transformer, f)
    tn = graph.TNode(cargo=gp)
    #==
    os = graph.OSlot()
    graph.connect(os, tn)
    #==
    nb_arg = f.__code__.co_argcount
    islots = []
    for i in range(nb_arg):
        islot = graph.ISlot()
        islots.append(islot)
        graph.connect(tn, islot)
    return islots

def add(a, b):
    return a+b

def minus(a, b):
    return a-b

def inc(a):
    return a + 2

def decr(a):
    return a - 1

def test():
    gp = base.GeneratorProto(base.value, 5)
    tn = graph.TNode(cargo=gp)
    os = graph.OSlot()
    graph.connect(os, tn)
    #==
    iss = func_to_node(inc)
    graph.connect(iss[0],os)
    iss = func_to_node(decr)
    graph.connect(iss[0],os)
    #==
    return tn
