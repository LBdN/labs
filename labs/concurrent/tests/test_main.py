from labs.concurrent import main as m
from labs.data_structure import tree
#from pprint import pprint as pp
import random

def gen_el(i):
    o = tree.Node(cargo=i)
    return o

def setup_graph(nb, nb_cnx):
    elements = map(gen_el, range(nb))
    root     = elements[0]
    for idx, el in enumerate(elements):
        rst = elements[:idx]
        if not rst:
            continue
        ii  = min(nb_cnx, len(rst))
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
    return root, elements

def test_tarjan(nb, nb_cnx):
    r, elements = setup_graph(nb, nb_cnx)
    task_list   = m.tarjan(r, elements)
    done        = set([])
    for el in task_list:
        for p in el.parents:
            assert p in done
        done.add(el)
    assert set(elements) == set(task_list)
    return task_list

def test_tarjan2(nb, nb_cnx):
    r, elements = setup_graph(nb, nb_cnx)
    task_list   = m.tarjan_par(r, elements)
    done        = set([])
    for group in task_list:
        for el in group:
            for p in el.parents:
                assert p in done
            done.add(el)
    assert set(elements) == set(sum(task_list, []))
    return task_list


def prof(nb, nb_cnx):
    import time
    import cProfile
    cProfile.runctx("test_tarjan2(%s, %s)" %(nb, nb_cnx), globals(), locals(), \
                    "prf_bfs::%s-%s::%s" %(nb, nb_cnx, time.asctime()))
