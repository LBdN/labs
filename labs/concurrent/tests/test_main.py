from labs.concurrent import main as m
from labs.data_structure import tree
#from pprint import pprint as pp
import random

def gen_el(i):
    o = tree.Node(cargo=i)
    #o = m.Operation('', str(i),  '')
    return o

def setup_el(nb):
    elements = map(lambda i : gen_el(i), range(nb))
    root     = elements[0]
    for idx, el in enumerate(elements):
        rst = elements[:idx]
        if not rst:
            continue
        ii  = random.randint(1, len(rst))
        els = random.sample(rst, ii)
        for e in els:
            if el in e.children:
                continue
            tree.connect(el, e)
    #==
    for el in elements:
        if el != root:
            assert el.parents 
    assert root.children
    #==
    return root

def test_topo(nb):
    r = setup_el(nb)
    #print tree.prettyprint(r, 4)
    l = m.topo_sort(r)
    #print l
    #m.


