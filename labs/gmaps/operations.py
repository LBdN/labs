from dart import Dart
import traverser as t
from itertools import izip

def new_dart(embedding, cell_dimension):
    return Dart(embedding, cell_dimension)

#def traverse(dart, dimensions, func):
    #traversed_dart = set([dart])
    #stack = [dart]
    #while stack:
        #current_dart = stack.pop()
        #func(current_dart)
        #for i in dimensions:
            #other_dart = current_dart.alphas[i]
            #if not other_dart in traversed_dart:
                #traversed_dart.add(other_dart)
                #stack.append(other_dart)

def _get_n_orbit_in_dim_2(dart, n):
    if   n==0 : i, j = 1, 2
    elif n==1 : i, j = 0, 2
    elif n==2 : i, j = 0, 1
    #==
    orbit = []
    current_dart = dart.alphas[i]
    while current_dart!=dart:
        if current_dart.alphas[i]==current_dart:
            return [dart]
        if current_dart == dart:
            break
        else:
            orbit.append(current_dart)
        #==
        current_dart=current_dart.alphas[j]
        if current_dart.alphas[j]==current_dart:
            return [dart]
        if current_dart == dart:
            break
        else:
            orbit.append(current_dart)
        #==
        current_dart=current_dart.alphas[i]
    orbit.append(dart)
    return orbit
                
def get_0_orbit(dart):
    return _get_n_orbit_in_dim_2(dart, 0)
        
def get_1_orbit(dart):
    return _get_n_orbit_in_dim_2(dart, 1)
        
def get_2_orbit(dart):
    return _get_n_orbit_in_dim_2(dart, 2)
        
def generic_get_orbit(dart, dimension, ffrom):
    orbit = []
    dimensions = range(dimension)+range(dimension+1, dart.get_dimension())
    t.traverse(dart, dimensions, orbit.append, ffrom)
    return orbit               

def get_orbit(dart, dimension):
    assert dimension<=dart.get_dimension()
    ffrom= "from failed get_orbit"
    if dimension==0:
        return get_0_orbit(dart) or generic_get_orbit(dart, dimension, ffrom)
    elif dimension==1:
        return get_1_orbit(dart) or generic_get_orbit(dart, dimension, ffrom)
    elif dimension==2:
        return get_2_orbit(dart) or generic_get_orbit(dart, dimension, ffrom)
    return generic_get_orbit(dart, dimension, ffrom)


def get_orbit_under(dart, dimension):
    assert dimension<=dart.get_dimension()
    orbit = []
    ffrom= "from get_orbit_under"
    t.traverse(dart, range(dimension), orbit.append, ffrom)
    return orbit

def sew(dart1, dart2, dimension, embedding_update_func=None, **kw):
    assert dart1.alphas[dimension]==dart1
    assert dart2.alphas[dimension]==dart2
    dart1.alphas[dimension] = dart2
    dart2.alphas[dimension] = dart1
    if embedding_update_func:
        embedding_update_func(dart1, dart2, dimension, **kw)
    for d1, d2 in izip(get_orbit(dart1, dimension-1), get_orbit(dart2, dimension-1)):
        if d1==dart1:
            continue
        for dim in xrange(dimension): 
            d1.alphas[dimension] = d2
            d2.alphas[dimension] = d1
            if embedding_update_func:
                embedding_update_func(d1, d2, dimension, **kw)
    assert check_g_maps_validity(dart1, advanced_check=False)
                       

def unsew(dart1, dimension, embedding_update_func=None):
    sub_dim = dimension-1 
    if sub_dim == 0:
        d1 = dart1
        d2 = d1.alphas[dimension]
        d2.alphas[dimension] = d2
        d1.alphas[dimension] = d1
        if embedding_update_func:
            embedding_update_func(d1, d2, dimension)
    else:
        for d1 in get_orbit_under(dart1, sub_dim):
            d2 = d1.alphas[dimension]
            d2.alphas[dimension] = d2
            d1.alphas[dimension] = d1
            if embedding_update_func:
                embedding_update_func(d1, d2, dimension)

def is_deletable(input_dart, dimension):
    if input_dart.get_dimension()-1<dimension+2:
        return True
    orbit = get_orbit(input_dart, dimension)
    for dart in orbit:
        if not dart.alphas[dimension+1].alphas[dimension+2]==dart.alphas[dimension+2].alphas[dimension+1]:
            return False
    return True


def insert(input_darts1, input_darts2, dart_to_associate_tuples, dimension, embedding_update_func=None):
    #in fact we can't use sew/unsew
    # _ _ A _ _
    #|   | |   |
    #|   | |   |
    # _ _   _ _  B
    # _ _   _ _
    #|   | |   |
    #|   | |   |
    # _ _   _ _
    #inserting a line between A and B doesn't work with sew/unsew
    #for dart_couple in dart_to_associate_tuples:
        #for dart in dart_couple:
            #if not dart.alphas[dimension]==dart:
                #unsew(dart, dimension)
    #for dart1, dart2 in dart_to_associate_tuples:
        #sew(dart1, dart2, dimension)
        
    for index, (dart1, dart2) in enumerate(dart_to_associate_tuples):
        unsew(dart1, dimension, embedding_update_func=embedding_update_func)
        unsew(dart2, dimension, embedding_update_func=embedding_update_func)
        
    for dart1, dart2 in dart_to_associate_tuples:
        dart1.alphas[dimension]=dart2
        dart2.alphas[dimension]=dart1

    for dart1, dart2 in dart_to_associate_tuples:
        if embedding_update_func:
            embedding_update_func(dart1, dart2, dimension)
            
    assert check_g_maps_validity(input_darts1[0], advanced_check=False)


def is_insertion_possible(darts1, darts2, dart_to_associate_tuples, dimension):
    association = {}
    for dart1, dart2 in dart_to_associate_tuples:
        if dart1 in association or dart2 in association:
            return False
        association[dart1] = dart2
        association[dart2] = dart1        
    # ==
    if any(dart.alphas[dimension]!=dart for _, dart in dart_to_associate_tuples):
        return False
    if not all(is_deletable(dart, dimension) for dart in darts2):
        return False

    for dart_couple in dart_to_associate_tuples:
        for dart in dart_couple:
            for j in xrange(dart.get_dimension()):
                if abs(dimension-j)>=2 and dart.alphas[j] in association and association[dart.alphas[j]]!=association[dart].alphas[j]:
                    return False
    # ==             
    associated_darts_2 = [dart2 for _, dart2 in dart_to_associate_tuples]
    for dart, _ in dart_to_associate_tuples:
        temp_dart = association[dart].alphas[dimension+1]
        while (temp_dart not in associated_darts_2 ):
            temp_dart = temp_dart.alphas[dimension].alphas[dimension+1]
        if not association[temp_dart]==dart.alphas[dimension]:
            return False
    # ==
    return True
            
    
def check_dart_validity(dart, advanced_check=True):
    all_alpha_i_involutions = all( dart.alphas[i].alphas[i] == dart for i in xrange(dart.get_dimension()))
    all_ai_ai_plus_2_involutions = True
    for i in xrange(dart.get_dimension()):
        if i>=2 and not dart.alphas[i-2].alphas[i].alphas[i-2].alphas[i] == dart:
            all_ai_ai_plus_2_involutions = False
    assert all_alpha_i_involutions
    assert all_ai_ai_plus_2_involutions
    no_fixed_points = check_no_fixed_point(dart)
    no_dangling_edge = check_dangling_edge(dart)
    #to check if correct:
    #fixed points are forbidden in the N-g-map under dimension N, but during construction can be accepted?
    if advanced_check:
        assert no_fixed_points
        assert no_dangling_edge
    return True
        
def check_g_maps_validity(dart, advanced_check=True):
    def func(dart):
        assert check_dart_validity(dart, advanced_check)
    t.traverse(dart, range(dart.get_dimension()), func)
    return True
    
def check_no_fixed_point(dart):
    return not any(dart.alphas[i] == dart for i in xrange(dart.get_dimension()))
                
def check_dangling_edge(dart):
    return not any(i>=2 and dart.alphas[i-2].alphas[i] == dart for i in xrange(dart.get_dimension()))
                

