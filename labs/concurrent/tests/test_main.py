from labs.concurrent import main as m
from labs.data_structure import tree
#from pprint import pprint as pp
import random

def gen_el(i):
    o = m.Operation('', str(i),  {})
    return o

def setup_el():
    elements = map(lambda i : gen_el(i), range(5))
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

def test_topo():
    r = setup_el()
    l = m.topo_sort(r)
    print l
    #m.


