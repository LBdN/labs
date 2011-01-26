from gamr7_lib.basic_calcul import PRECISION, normalize, is_same, points_diff, tuple_float_mult, tuple_sum, dot_product, cross_product, magnitude, square_magnitude
import math

def segments_are_intersecting_in_polygon(points) :
    segments = [(points[i-1], point) for i, point in enumerate(points)]
    for i, segment in enumerate(segments) :
        for j, other_segment in enumerate(segments) :
            #i-1=>two following segments=>not test needed
            if j >= i-1                                                           : break
            #elif segment[0] == other_segment[1] or segment[1] == other_segment[0] : continue
            elif segments_are_intersecting(segment, other_segment):
                if actual_intersection(segments, i, j):
                    return True
    # ==
    return False

#check if intersection point is an acutal intersection
#wich means wether the two lines actually cross or are parallel or are tangent
def actual_intersection(segments, i,j):
    segment = segments[i]
    other_segment = segments[j]
    if is_same(dot_product(points_diff(*segment), points_diff(*other_segment)), 0.): 
        return False

    for index1, p1 in enumerate(segment):
        for index2, p2 in enumerate(other_segment):
            if is_same(p1, p2):
                segment1 = segments[i-1][index1], segments[(i+1)%len(segments)][index1]
                segment2 = segments[j-1][index2], segments[(j+1)%len(segments)][index2]
                if have_common_point(segment1, segment2):
                    return False
                if not segments_are_intersecting(segment1, segment2):
                    return False
                # ==
                if index1==0 : connected_segment1 = segments[i-1]
                else         : connected_segment1 = segments[(i+1)%len(segments)]  
                if index2==0 : connected_segment2 = segments[j-1]
                else         : connected_segment2 = segments[(j+1)%len(segments)]
                if is_same(cross_product(points_diff(*connected_segment1), points_diff(*other_segment)), 0.) or \
                   is_same(cross_product(points_diff(*connected_segment2), points_diff(*segment)), 0.): 
                    return False      
                center = p1
                if _is_in_angle(segment1[0], center, segment1[1], segment2[0])==_is_in_angle(segment1[0], center, segment1[1], segment2[1]):
                    return False

    for index1, p1 in enumerate(segment):
        if is_on_segment(other_segment[0], other_segment[1], p1):
            full_segment = (segments[i-1][index1], segments[(i+1)%len(segments)][index1])
            if have_common_point(other_segment, full_segment):
                return False
            if not segments_are_intersecting(full_segment, other_segment):
                return False
            
    for index2, p2 in enumerate(other_segment):
        if is_on_segment(segment[0], segment[1], p2):
            full_segment = (segments[j-1][index2], segments[(j+1)%len(segments)][index2])
            if have_common_point(segment, full_segment):
                return False
            if not segments_are_intersecting(full_segment, segment):
                return False
                             
    return True


    
def _is_in_angle(p1, center, p2, point_to_check):
    v1 = normalize(points_diff(center, p1))
    v2 = normalize(points_diff(center, p2))
    v = normalize(points_diff(center, point_to_check))
    return cross_product(v1, v)<=PRECISION and cross_product(v2, v)>=PRECISION

def have_common_point(segment1, segment2):
    for _p1 in segment1:
            for _p2 in segment2:
                if is_same(_p1, _p2):
                    return True
    return False
    
def segments_are_intersecting(first_segment, second_segment) :
    return optimized_get_collision_between_segments(first_segment, second_segment) is not None

def get_collision_between_segments(line1, line2, precision=PRECISION) :
    """ returns collision between 2 segments defined by 2 points """
    point_d1, point_d2 = line1
    point_l1, point_l2 = line2
    # ==
    collision_point = get_collision_between_lines_with_points((point_d1, point_d2), (point_l1, point_l2), precision=precision)
    return collision_point if collision_point is not None and in_between(point_d1, collision_point, point_d2, precision=precision) and in_between(point_l1, collision_point, point_l2, precision=precision) and is_on_line(point_d1, point_d2, collision_point) and is_on_line(point_l1, point_l2, collision_point) else None

def get_collision_between_lines(line1, line2, precision=PRECISION) : # get_line_vector_collision_point
    """ returns collision between 2 lines defined by a point and the direction vector """
    point_1, director_1 = line1
    point_2, director_2 = line2
    # ==
    if not is_same(det(director_1, director_2), 0, precision=precision) : return tuple_sum(point_1, tuple_float_mult(director_1, det(points_diff(point_1, point_2), director_2) / float( det(director_1, director_2) ) ))
    if is_same(det( points_diff(point_1, point_2), director_1 ), 0, precision=precision) : return point_1 # ou point_2, c'est la meme chose : les droites sont confondues
    return None

def get_collision_between_lines_with_points(line1, line2, precision=PRECISION) : # get_line_collision_point
    """ returns collision between 2 lines defined by 2 points """
    point_d1, point_d2 = line1
    point_l1, point_l2 = line2
    # ==
    return get_collision_between_lines( (point_d1, points_diff(point_d1, point_d2)),(point_l1, points_diff(point_l1, point_l2)), precision=precision )


# ====

def get_line_vector_collision_point(line1, line2):
    """ returns collision between 2 lines defined by a point and the direction vector """
    (p1, v1) = line1
    (p2, v2) = line2
    return get_line_collision_point( (p1, tuple_sum(p1, v1)), (p2, tuple_sum(p2, v2)) )


def optimized_get_collision_between_segments(line1, line2, precision=PRECISION) :
    point_d1, point_d2 = line1
    point_l1, point_l2 = line2
    x1_max = max(point_d1[0], point_d2[0])
    x2_min = min(point_l1[0], point_l2[0])
    if x2_min-PRECISION>x1_max: return
    # ==
    x1_min = min(point_d1[0], point_d2[0])
    x2_max = max(point_l1[0], point_l2[0])
    if x1_min-PRECISION>x2_max: return
    # ==
    y1_max = max(point_d1[1], point_d2[1])
    y2_min = min(point_l1[1], point_l2[1])
    if y2_min-PRECISION>y1_max: return
    # ==
    y1_min = min(point_d1[1], point_d2[1])
    y2_max = max(point_l1[1], point_l2[1])
    if y1_min-PRECISION>y2_max: return
    """ returns collision between 2 segments defined by 2 points """
    # ==
    return get_collision_between_segments((point_d1, point_d2), (point_l1, point_l2), precision=precision)

def broken_line_intersections(first_broken_line, second_broken_line, precision=PRECISION):
    collision_list = []
    for index1, point1 in enumerate(first_broken_line):
        if index1==0 : continue
        segment1 = [first_broken_line[index1-1], point1]
        for index2, point2 in enumerate(second_broken_line):
            if index2==0 : continue
            segment2 = [second_broken_line[index2-1], point2]
            collision_point = optimized_get_collision_between_segments(segment1, segment2, precision=precision)
            if collision_point:collision_list.append((collision_point, segment1, segment2))
    return collision_list

def get_collision_point(l1, l2) :  
    """collision points between 2 segments"""
    p1, p2 = l1
    p3, p4 = l2
    collision_point = get_line_collision_point((p1, p2), (p3, p4))
    # all the wrong situations imply returning None
    if   collision_point is None                    : return None
    elif not is_on_segment(p1, p2, collision_point) : return None
    elif not is_on_segment(p3, p4, collision_point) : return None
    # if we are here, should be good 
    return collision_point

def get_line_segment_collision_point(line, segment) :
    collision_point = get_line_collision_point(line, segment)
    # ==
    if collision_point is None                                  : return None
    elif is_on_segment(segment[0], segment[1], collision_point) : return collision_point
    else                                                        : return None

def self_intersect_line(points, precision=PRECISION):
    for index in range(len(points))[:-2]:
        first_segment = (points[index], points[index+1])
        for index2 in range(len(points))[index+1:-1]:
            second_segment = (points[index2], points[index2+1])
            collision_point = get_collision_between_segments(first_segment, second_segment, precision=precision)
            if collision_point and not is_same(collision_point, points[index2]) : 
                return True
    return False    
    

def get_collision_point_between_broken_lines(first_line,second_line):
    for first_line_index in xrange(len(first_line)-1):
        for second_line_index in xrange(len(second_line)-1):
            first_segment   = ( first_line[first_line_index]   , first_line[first_line_index+1]   )
            second_segment  = ( second_line[second_line_index] , second_line[second_line_index+1] )
            collision_point = get_collision_point(  first_segment, second_segment  )
            if collision_point : return collision_point
    return None

def get_collision_points_between_broken_lines(first_line,second_line):
    collisions =[]
    for first_line_index in xrange(len(first_line)-1):
        for second_line_index in xrange(len(second_line)-1):
            first_segment   = ( first_line[first_line_index]   , first_line[first_line_index+1]   )
            second_segment  = ( second_line[second_line_index] , second_line[second_line_index+1] )
            collision_point = get_collision_point(  first_segment, second_segment  )
            collisions.append(collision_point)
    return collisions

# ====

def det(u,v) :
    return u[0] * v[1] - u[1] * v[0]


def in_between_on_x(p1, p, p2, precision = PRECISION) :
    return ( (p1[0] - p[0] < precision ) and (p[0] - p2[0] < precision) ) or ( (p2[0] - p[0] < precision ) and (p[0] - p1[0] < precision) )

def in_between_on_y(p1, p, p2, precision = PRECISION) :
    return ( (p1[1] - p[1] < precision ) and (p[1] - p2[1] < precision) ) or ( (p2[1] - p[1] < precision ) and (p[1] - p1[1] < precision) )

def in_between(p1, p, p2, precision = PRECISION) : # p dans le carre de diagonale de p1 a p2
    return in_between_on_x(p1, p, p2, precision=precision) and in_between_on_y(p1, p, p2, precision=precision)
  
def is_on_line(seg_start, seg_end, point, precision=PRECISION) :
    if is_same(seg_start, point, precision=precision) or is_same(seg_end, point, precision=precision) : return True
    if is_same(seg_start, seg_end, precision=precision)                                               : return False
    vector_from_start_to_end   = points_diff(seg_start, seg_end)
    vector_from_start_to_point = points_diff(seg_start, point)
    angle = math.degrees(math.acos(min(1.0, max(-1.0, dot_product( vector_from_start_to_end, vector_from_start_to_point)/(magnitude(vector_from_start_to_end)*magnitude(vector_from_start_to_point))))))
    # ==
    return is_same(angle, 0, precision=precision) or is_same(angle, 360.0, precision=precision) or is_same(angle, -360.0, precision=precision)


def get_line_collision_point(line1, line2) :
    p1, p2 = line1
    p3, p4 = line2
    """ returns collision between 2 lines defined by 2 points """
    a1, b1, d1 = line_eq_calculus(p1, p2)
    a2, b2, d2 = line_eq_calculus(p3, p4)
    # ==
    a, b, c, d = (a1, a2), (b1, b2), p3, (d1, d2)
    det_a_b    = float(det(a,b))
    # ==
    if is_same(abs(det_a_b),0.) :
#    if abs(det_a_b) == 0. :
        if is_same(a1 * p3[0] + b1 * p3[1], d1) : # Tous les cas qui suivent sont equivalents :
            if   is_on_segment(p3, p4, p1) : return p1
            elif is_on_segment(p3, p4, p2) : return p2
            elif is_on_segment(p1, p2, p3) : return p3
            elif is_on_segment(p1, p2, p4) : return p4
        return None
    else :
        x = det(d, b) / det_a_b
        y = det(a, d) / det_a_b
        return ((x,y))
    
def is_on_segment(seg_start, seg_end, point, precision=PRECISION) :
#    vector_from_start_to_end   = create_vector_from_points(seg_start, seg_end)
#    vector_from_start_to_point = create_vector_from_points(seg_start, point)
#    # ==
#    return 0 <= vector_from_start_to_point.dot_product(vector_from_start_to_end) / float(vector_from_start_to_end.square_magnitude()) <= 1 and is_same(vector_from_start_to_end.unit().cross_product(vector_from_start_to_point.unit()), 0.)
    return in_between(seg_start, point, seg_end, precision=PRECISION) and is_on_line(seg_start, seg_end, point)

    
def line_eq_calculus(p1, p2) :
    a = float(p2[1] - p1[1])
    b = float(p1[0] - p2[0])
    d = float(p1[0] * a + p1[1] * b)
    return a,b,d

