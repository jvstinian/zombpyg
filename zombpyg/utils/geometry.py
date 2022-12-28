import numpy


def _valid_angle(angle):
    if angle > 180:
        angle -= 360
    elif angle <= -180:
        angle += 360
    return angle
    
def calculate_distance(position, point):
    dx = point[0] - position[0]
    dy = point[1] - position[1]
    return numpy.sqrt(dx ** 2 + dy ** 2)

# The methods 
# _valid_angle, 
# calculateGradient, and 
# calculateYAxisIntersect
# were taken (and renamed) from 
# https://github.com/PacktPublishing/Python-Reinforcement-Learning-Projects/tree/master/Chapter03/demo

# Calc the gradient 'm' of a line between p1 and p2
def calculate_gradient(p1, p2):
    # Ensure that the line is not vertical
    if (p1[0] != p2[0]):
        m = (p1[1] - p2[1]) / (p1[0] - p2[0])
        return m
    else:
        return None
 
# Calc the point 'b' where line crosses the Y axis
def calculate_yaxis_intersect(p, m):
    return p[1] - (m * p[0])
 
# Calc the point where two infinitely long lines (p1 to p2 and p3 to p4) intersect.
# Handle parallel lines and vertical lines (the later has infinate 'm').
# Returns a point tuple of points like this ((x,y),...)  or None
# In non parallel cases the tuple will contain just one point.
# For parallel lines that lay on top of one another the tuple will contain
# all four points of the two lines
def get_intersect_point(p1, p2, p3, p4):
    m1 = calculate_gradient(p1, p2)
    m2 = calculate_gradient(p3, p4)
      
    # See if the the lines are parallel
    if (m1 != m2):
        # See if either line is vertical
        if (m1 is not None and m2 is not None):
            # Neither line vertical           
            b1 = calculate_yaxis_intersect(p1, m1)
            b2 = calculate_yaxis_intersect(p3, m2)   
            x = (b2 - b1) / (m1 - m2)       
            y = (m1 * x) + b1           
        else:
            # Line 1 is vertical so use line 2's values
            if (m1 is None):
                b2 = calculate_yaxis_intersect(p3, m2)   
                x = p1[0]
                y = (m2 * x) + b2
            # Line 2 is vertical so use line 1's values               
            elif (m2 is None):
                b1 = calculate_yaxis_intersect(p1, m1)
                x = p3[0]
                y = (m1 * x) + b1           
            else:
                assert False
               
        return ((x,y),)
    else:
        # Parallel lines with same 'b' value must be the same line so they intersect
        # everywhere in this case we return the start and end points of both lines
        # the calculateIntersectPoint method will sort out which of these points
        # lays on both line segments
        b1, b2 = None, None # vertical lines have no b value
        if m1 is not None:
            b1 = calculate_yaxis_intersect(p1, m1)
           
        if m2 is not None:   
            b2 = calculate_yaxis_intersect(p3, m2)
       
        # If these parallel lines lay on one another   
        if b1 == b2:
            return p1,p2,p3,p4
        else:
            return None
 
# For line segments (ie not infinitely long lines) the intersect point
# may not lay on both lines.
#   
# If the point where two lines intersect is inside both line's bounding
# rectangles then the lines intersect. Returns intersect point if the line
# intesect o None if not
def calculate_intersect_point(p1, p2, p3, p4):
    p = get_intersect_point(p1, p2, p3, p4)
    if p is not None:
        for point in p:
            l1 = calculate_parameter_of_point_on_segment(p1, p2, point)
            l2 = calculate_parameter_of_point_on_segment(p3, p4, point)
            if (0 <= l1) and (l1 <= 1) and (0 <= l2) and (l2 <= 1):
                return point
        return None            
    else:
        return None

    # p = getIntersectPoint(p1, p2, p3, p4)
  
    # if p is not None:               
    #     width = p2[0] - p1[0]
    #     height = p2[1] - p1[1]       
    #     r1 = Rect(p1, (width , height))
    #     r1.normalize()
       
    #     width = p4[0] - p3[0]
    #     height = p4[1] - p3[1]
    #     r2 = Rect(p3, (width, height))
    #     r2.normalize()              
    
    #     # Ensure both rects have a width and height of at least 'tolerance' else the
    #     # collidepoint check of the Rect class will fail as it doesn't include the bottom
    #     # and right hand side 'pixels' of the rectangle
    #     tolerance = 1
    #     if r1.width < tolerance:
    #         r1.width = tolerance
                    
    #     if r1.height < tolerance:
    #         r1.height = tolerance
        
    #     if r2.width < tolerance:
    #         r2.width = tolerance
                    
    #     if r2.height < tolerance:
    #         r2.height = tolerance
    
    #     for point in p:                 
    #         try:
    #             point = [numpy.rint(pp) for pp in point] 
    #             res1 = r1.collidepoint(point)
    #             res2 = r2.collidepoint(point)
    #             if res1 and res2:
    #                 point = [int(pp) for pp in point]                       
    #                 return point
    #         except:         
    #             print("point was invalid {}".format(point))
                
    #     # This is the case where the infinately long lines crossed but 
    #     # the line segments didn't
    #     return None            
    
    # else:
    #     return None

def calculate_parameter_of_point_on_segment(start, end, pt):
    if start[0] != end[0]:
        return (pt[0] - start[0])/(end[0] - start[0])
    elif start[1] != end[1]:
        return (pt[1] - start[1])/(end[1] - start[1])
    else:
        return 0.0

def get_nearest_point_and_distance_to_path(start, end, point):
    np_start = numpy.array(start)
    np_end = numpy.array(end)
    np_pt = numpy.array(point)
    d = np_end - np_start
    a = numpy.inner(np_pt - np_start, d)/ numpy.power(numpy.linalg.norm(d), 2.0)
    cpt = None
    is_nearest_point_to_line = None
    if a < 0:
        cpt = np_start
        is_nearest_point_to_line = False
    elif a > 1:
        cpt = np_end
        is_nearest_point_to_line = False
    else: 
        cpt = np_start + a * d
        is_nearest_point_to_line = True
    dist = numpy.linalg.norm(np_pt - cpt)
    return cpt, dist, is_nearest_point_to_line 

# The following identifies the extreme points on a line segment where 
# the line segment meets the closed ball.  For the following method to work, 
# the line segment must meet the interior of the ball.
def get_extreme_points_on_segment_intersecting_circle(segment_start, segment_end, circle_center, circle_radius):
    if segment_start == segment_end: 
        return segment_start, None
    diff1 = numpy.array(segment_end) - numpy.array(segment_start)
    diff2 = numpy.array(segment_start) - numpy.array(circle_center)
    a = numpy.linalg.norm(diff1) ** 2
    b = 2.0 * numpy.inner(diff1, diff2)
    c = (numpy.linalg.norm(diff2) ** 2) - (circle_radius ** 2)
    d = b ** 2 - 4*a*c
    if d > 0.0:
        lmin = (-b - numpy.sqrt(d))/(2*a)
        lmin = max(lmin, 0.0)
        lmax = (-b + numpy.sqrt(d))/(2*a)
        lmax = min(lmax, 1.0)
        smin = tuple(numpy.array(segment_start) + lmin*diff1)
        smax = tuple(numpy.array(segment_start) + lmax*diff1)
        return smin, smax
    elif d == 0.0:
        l = (-b - numpy.sqrt(d))/(2*a)
        s = tuple(numpy.array(segment_start) + l*diff1)
        return s, None
    else:
        # d < 0
        return None, None

def rotate_vector(orientation_vector, angle):
    rotmat = numpy.array([
        [numpy.cos(angle), numpy.sin(angle)],
        [-numpy.sin(angle), numpy.cos(angle)]
    ])
    return numpy.matmul(rotmat, orientation_vector)

def get_angle_and_distance_to_point(position, orientation, point):
    dx = point[0] - position[0]
    dy = point[1] - position[1]
    distance = numpy.sqrt(dx ** 2 + dy ** 2)
    angle = numpy.rad2deg(numpy.arctan2(dx, -dy))
    angle = _valid_angle(angle - orientation)
    return angle, distance, point
