import numpy
from pygame import Rect
from operator import itemgetter
import itertools

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

class Color:
    RED   = (255, 51, 153, 220)
    DARK_RED   = (255, 15, 63, 220)
    GREEN = (0, 204, 0, 220)
    BRONZE = (205, 127, 50, 128)
    BLUE  = (10, 102, 240, 220)
    GRAY  = (200, 200, 200, 128)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BACKGROUND = BLACK

# Calc the gradient 'm' of a line between p1 and p2
def calculateGradient(p1, p2):
  
    # Ensure that the line is not vertical
    if (p1[0] != p2[0]):
        m = (p1[1] - p2[1]) / (p1[0] - p2[0])
        return m
    else:
        return None
 
# Calc the point 'b' where line crosses the Y axis
def calculateYAxisIntersect(p, m):
    return p[1] - (m * p[0])
 
# Calc the point where two infinitely long lines (p1 to p2 and p3 to p4) intersect.
# Handle parallel lines and vertical lines (the later has infinate 'm').
# Returns a point tuple of points like this ((x,y),...)  or None
# In non parallel cases the tuple will contain just one point.
# For parallel lines that lay on top of one another the tuple will contain
# all four points of the two lines
def getIntersectPoint(p1, p2, p3, p4):
    m1 = calculateGradient(p1, p2)
    m2 = calculateGradient(p3, p4)
      
    # See if the the lines are parallel
    if (m1 != m2):
        # See if either line is vertical
        if (m1 is not None and m2 is not None):
            # Neither line vertical           
            b1 = calculateYAxisIntersect(p1, m1)
            b2 = calculateYAxisIntersect(p3, m2)   
            x = (b2 - b1) / (m1 - m2)       
            y = (m1 * x) + b1           
        else:
            # Line 1 is vertical so use line 2's values
            if (m1 is None):
                b2 = calculateYAxisIntersect(p3, m2)   
                x = p1[0]
                y = (m2 * x) + b2
            # Line 2 is vertical so use line 1's values               
            elif (m2 is None):
                b1 = calculateYAxisIntersect(p1, m1)
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
            b1 = calculateYAxisIntersect(p1, m1)
           
        if m2 is not None:   
            b2 = calculateYAxisIntersect(p3, m2)
       
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
def calculateIntersectPoint(p1, p2, p3, p4):
    p = getIntersectPoint(p1, p2, p3, p4)
    if p is not None:
        for point in p:
            l1 = calculateParameterOfPointOnSegment(p1, p2, point)
            l2 = calculateParameterOfPointOnSegment(p3, p4, point)
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

def calculateParameterOfPointOnSegment(start, end, pt):
    if start[0] != end[0]:
        return (pt[0] - start[0])/(end[0] - start[0])
    elif start[1] != end[1]:
        return (pt[1] - start[1])/(end[1] - start[1])
    else:
        return 0.0

def getNearestPointAndDistanceToPath(start, end, point):
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
def getExtremePointsOnSegmentIntersectingCircle(segment_start, segment_end, circle_center, circle_radius):
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

def getUnitVector(orientation_vector, angle):
    rotmat = numpy.array([
        [numpy.cos(angle), numpy.sin(angle)],
        [-numpy.sin(angle), numpy.cos(angle)]
    ])
    return numpy.matmul(rotmat, orientation_vector)

def getPointInfo(position, orientation, point):
    dx = point[0] - position[0]
    dy = point[1] - position[1]
    distance = numpy.sqrt(dx ** 2 + dy ** 2)
    angle = numpy.rad2deg(numpy.arctan2(dx, -dy))
    angle = _valid_angle(angle - orientation)
    return angle, distance, point

class VisibleWallSegment(object):
    def __init__(
        self, 
        left_angle, left_distance, left_point,
        right_angle, right_distance, right_point,
        nearest_point_on_segment, 
        is_nearest_point_to_line
    ):
        self.left_angle = left_angle
        self.left_distance = left_distance 
        self.left_point = left_point
        self.right_angle = right_angle
        self.right_distance = right_distance
        self.right_point = right_point
        self.nearest_point_on_segment = nearest_point_on_segment
        self.is_nearest_point_to_line = is_nearest_point_to_line

    def __repr__(self):
        return ("VisibleWallSegment("
               f"left_angle={self.left_angle}, "
               f"left_distance={self.left_distance}, "
               f"left_point={self.left_point}, "
               f"right_angle={self.right_angle}, "
               f"right_distance={self.right_distance}, "
               f"right_point={self.right_point}, "
               f"nearest_point_on_segment={self.nearest_point_on_segment}, "
               f"is_nearest_point_to_line={self.is_nearest_point_to_line}"
               ")")

    def __simpleMoveDistanceToPoint(self, center, radius, wallpoint):
        dx = wallpoint[0] - center[0]
        dy = wallpoint[1] - center[1]
        distance = numpy.sqrt(dx ** 2 + dy ** 2)
        return max(distance - radius, 0)

    def simpleMaximumMoveDistance(self, center, radius, orientation, default_max_distance):
        if self.is_nearest_point_to_line:
            orientation_vector = (
                numpy.sin(numpy.deg2rad(orientation)),
                -numpy.cos(numpy.deg2rad(orientation))
            )
            dx = self.nearest_point_on_segment[0] - center[0]
            dy = self.nearest_point_on_segment[1] - center[1]
            distance2 = dx ** 2 + dy ** 2
            distance = numpy.sqrt(distance2)
            a = numpy.inner(
                numpy.array(orientation_vector),
                numpy.array((dx, dy))
            )
            if a > 0:
                # maxmove = distance2 / a # TODO: Check this
                # return max(maxmove - radius, 0)
                maxmove = (distance2 - distance * radius) / a
                return max(maxmove, 0.0)
            else:
                return default_max_distance
        else:
            distances=[default_max_distance]
            if (self.left_angle > -90) and (self.left_angle < 90):
                distances.append(
                    self.__simpleMoveDistanceToPoint(center, radius, self.left_point)
                )
            if (self.right_angle > -90) and (self.right_angle < 90):
                distances.append(
                    self.__simpleMoveDistanceToPoint(center, radius, self.right_point)
                )
            # if len(distances) > 0:
            #     return min(distances)
            # else:
            #     return 10 * radius
            return min(distances)

    def containsAngle(self, angle):
        return (self.left_angle <= angle) and (angle <= self.right_angle)
    
    def containsAngleInInterior(self, angle):
        return (self.left_angle < angle) and (angle < self.right_angle)
        
# Find the gap to the right
def getAngleToGapOnRight(target_gap_width, surroundings):
    # Start with the minimum right-endpoint angle that is >= 0.0
    right_angle, right_point = next(
        iter(sorted(
            map(
                lambda vws: (vws.right_angle, vws.right_point),
                filter(
                    lambda vws: vws.right_angle >= 0.0,
                    surroundings
                )
            ),
            key=itemgetter(0),
            reverse=False
        )),
        (0.0, None)
    )
    while right_angle < 90.0:
        while any([vws.containsAngle(right_angle) and (vws.right_angle > right_angle) for vws in surroundings]):
            # adjust right endpoint
            # Get the maximum right endpoint of intervals containing right_angle.
            right_angle, right_point = next(
                iter(sorted(
                    map(
                        lambda vws: (vws.right_angle, vws.right_point),
                        filter(
                            lambda vws: vws.containsAngle(right_angle) and (vws.right_angle > right_angle),
                            surroundings
                        )
                    ),
                    key=itemgetter(0),
                    reverse=True
                )),
                (right_angle, right_point) # this should not be needed
            )
        
        if right_angle >= 90.0:
            return 90.0
            
        # Find the next interval to the right (higher left angle)
        next_vws = next(
            iter(sorted(
                filter(
                    lambda vws: vws.left_angle > right_angle,
                    surroundings
                ),
                key=lambda vws: vws.left_angle,
                reverse=False
            )),
            None
        )

        if next_vws is None:
            return right_angle
        else:
            gap_width = numpy.linalg.norm(
                numpy.array(right_point) - numpy.array(next_vws.left_point)
            )
            # if gap_width > some specified value, break
            if gap_width > target_gap_width:
                return right_angle
            else:
                # keep going
                right_angle = next_vws.right_angle
                right_point = next_vws.right_point

    return min(right_angle, 90.0)

# Find the gap to the left
def getAngleToGapOnLeft(target_gap_width, surroundings):
    # Start with the maximum left-endpoint angle that is <= 0.0
    left_angle, left_point = next(
        iter(sorted(
            map(
                lambda vws: (vws.left_angle, vws.left_point),
                filter(
                    lambda vws: vws.left_angle <= 0.0,
                    surroundings
                )
            ),
            key=itemgetter(0),
            reverse=True
        )),
        (0.0, None)
    )
    while left_angle > -90.0:
        while any([vws.containsAngle(left_angle) and (vws.left_angle < left_angle) for vws in surroundings]):
            # adjust left endpoint
            # Get the minimum left endpoint of intervals containing left_angle.
            left_angle, left_point = next(
                iter(sorted(
                    map(
                        lambda vws: (vws.left_angle, vws.left_point),
                        filter(
                            lambda vws: vws.containsAngle(left_angle) and (vws.left_angle < left_angle),
                            surroundings
                        )
                    ),
                    key=itemgetter(0),
                    reverse=False
                )),
                (left_angle, left_point) # this should not be needed
            )
        
        if left_angle <= -90.0:
            return -90.0
            
        # Find the next interval to the left (lower right-endpoint angle)
        next_vws = next(
            iter(sorted(
                filter(
                    lambda vws: vws.right_angle < left_angle,
                    surroundings
                ),
                key=lambda vws: vws.right_angle,
                reverse=True
            )),
            None
        )

        if next_vws is None:
            return left_angle
        else:
            gap_width = numpy.linalg.norm(
                numpy.array(left_point) - numpy.array(next_vws.right_point)
            )
            # if gap_width > some specified value, break
            if gap_width > target_gap_width:
                return left_angle
            else:
                # keep going
                left_angle = next_vws.left_angle
                left_point = next_vws.left_point

    return max(left_angle, -90.0)

# The following assumes the visible points have already been 
# processed and that the visible region is between 
# (the angles defined in)
# lower_visible_point and upper_visible_point.
# Also, this interval should intersect the interval 
# [lower_bound, upper_bound].
def identifyVisiblePointExtremesInSubinterval(
    lower_visible_point, upper_visible_point, 
    lower_bound, upper_bound,
    cpt, is_nearest_point_to_line,
    position, orientation_vector, wall
):
    lower_angle, lower_distance, lower_point = lower_visible_point
    upper_angle, upper_distance, upper_point = upper_visible_point

    if lower_angle < lower_bound:
        lower_bound_rad = numpy.deg2rad(lower_bound)
        visend = tuple(numpy.array(position) + getUnitVector(orientation_vector, lower_bound_rad))
        adj_intersection_points = getIntersectPoint(position, visend, wall.start, wall.end)
        if adj_intersection_points is not None: 
            adj_lower_point = adj_intersection_points[0]
            # This should be the case
            lower_angle = _valid_angle(lower_bound)
            dx = adj_lower_point[0] - position[0]
            dy = adj_lower_point[1] - position[1]
            lower_distance = numpy.sqrt(dx ** 2 + dy ** 2)
            lower_point = adj_lower_point
    else:
        # adjust lower angle as it might be outside [-180, 180)
        lower_angle = _valid_angle(lower_angle)


    if upper_bound < upper_angle:
        upper_bound_rad = numpy.deg2rad(upper_bound)
        visend = tuple(numpy.array(position) + getUnitVector(orientation_vector, upper_bound_rad))
        adj_intersection_points = getIntersectPoint(position, visend, wall.start, wall.end)
        if adj_intersection_points is not None: 
            adj_upper_point = adj_intersection_points[0]
            # This should be the case
            dx = adj_upper_point[0] - position[0]
            dy = adj_upper_point[1] - position[1]
            upper_angle = _valid_angle(upper_bound)
            upper_distance = numpy.sqrt(dx ** 2 + dy ** 2)
            upper_point = adj_upper_point
    else:
        # adjust upper angle as it might be outside [-180, 180)
        upper_angle = _valid_angle(upper_angle)

    if lower_angle == upper_angle:
        return VisibleWallSegment(
                lower_angle,
                lower_distance,
                lower_point,
                lower_angle,
                lower_distance,
                lower_point,
                cpt,
                is_nearest_point_to_line 
            )
    else:
        return VisibleWallSegment(
                lower_angle,
                lower_distance,
                lower_point,
                upper_angle,
                upper_distance,
                upper_point,
                cpt,
                is_nearest_point_to_line 
            )

def identifyVisiblePointExtremes(visiblepts, cpt, is_nearest_point_to_line, position, orientation_vector, wall):
    # visiblepts are expected to be ordered by angle
    if len(visiblepts) == 2:
        left_angle, left_distance, left_point = visiblepts[0]
        right_angle, right_distance, right_point = visiblepts[1]
        if right_angle - left_angle > 180:
            left_angle, right_angle = right_angle, (left_angle + 360.0)
            left_distance, right_distance = right_distance, left_distance
            left_point, right_point = right_point, left_point

        if max(left_angle, -90) <= min(right_angle, 90):
            return identifyVisiblePointExtremesInSubinterval(
                (left_angle, left_distance, left_point), (right_angle, right_distance, right_point),
                -90, 90, 
                cpt, is_nearest_point_to_line, position, orientation_vector, wall
            )
        elif max(left_angle, 270) <= min(right_angle, 360):
            return identifyVisiblePointExtremesInSubinterval(
                (left_angle, left_distance, left_point), (right_angle, right_distance, right_point),
                270, 360,
                cpt, is_nearest_point_to_line, position, orientation_vector, wall
            )
        else:
            return None
    elif len(visiblepts) == 1:
        left_angle, left_distance, left_point = visiblepts[0]
        if -90 <= left_angle <= 90:
            return VisibleWallSegment(
                    left_angle,
                    left_distance,
                    left_point,
                    left_angle,
                    left_distance,
                    left_point,
                    cpt,
                    is_nearest_point_to_line 
                )
        else:
            return None

def getMovementEstimates(position, radius, orientation, walls, obstacle_distance):
    surroundings = []
    orientation_vector = (
        numpy.sin(numpy.deg2rad(orientation)),
        -numpy.cos(numpy.deg2rad(orientation))
    )
    for wall in walls:
        cpt, dist, is_nearest_point_to_line = getNearestPointAndDistanceToPath(wall.start, wall.end, position)
        if dist < obstacle_distance:
            wallpts = list(getExtremePointsOnSegmentIntersectingCircle(wall.start, wall.end, position, obstacle_distance))
            wallpts = list(filter(lambda pt: pt is not None, wallpts))
            visiblepts = list(map(lambda wallpt: getPointInfo(position, orientation, wallpt), wallpts))
            visiblepts = sorted(visiblepts, key=itemgetter(0, 1))
            vwso = identifyVisiblePointExtremes(visiblepts, cpt, is_nearest_point_to_line, position, orientation_vector, wall)
            if vwso is not None:
                surroundings.append(vwso)
    distanceForward = min(list(map(lambda vws: vws.simpleMaximumMoveDistance(position, radius, orientation, obstacle_distance), surroundings)), default=obstacle_distance)
    hasGapAhead = not any(map(lambda vws: vws.containsAngle(0.0), surroundings))
    gapAheadWidth = 0
    gapAheadLeftAngle = None
    gapAheadRightAngle = None
    if hasGapAhead:
        right_vector = (
            -orientation_vector[1],
            orientation_vector[0]
        )
        left_vector = (
            -right_vector[0],
            -right_vector[1]
        )
        extreme_right = (90.0, tuple(obstacle_distance*numpy.array(right_vector)))
        extreme_left = (-90.0, tuple(obstacle_distance*numpy.array(left_vector)))
        gapAheadLeft = next(
            iter(sorted(
                filter(
                    lambda tpl: tpl[0] < 0.0,
                    map(lambda vws: (vws.right_angle, vws.right_point), surroundings)
                ), 
                key=itemgetter(0),
                reverse=True
            )),
            extreme_left
        )
        gapAheadRight = next(
            iter(sorted(
                filter(
                    lambda tpl: tpl[0] > 0.0,
                    map(lambda vws: (vws.left_angle, vws.left_point), surroundings)
                ),
                key=itemgetter(0),
                reverse=False
            )),
            extreme_right
        )
        gapAheadLeftAngle = gapAheadLeft[0]
        gapAheadRightAngle = gapAheadRight[0]
        gapAheadWidth = numpy.linalg.norm(
            numpy.array(gapAheadLeft[1]) - numpy.array(gapAheadRight[1])
        )

    target_gap_width = 3 * radius
    angle_left_gap = getAngleToGapOnLeft(target_gap_width, surroundings)
    angle_right_gap = getAngleToGapOnRight(target_gap_width, surroundings)

    return distanceForward, hasGapAhead, gapAheadWidth, gapAheadLeftAngle, gapAheadRightAngle, angle_left_gap, angle_right_gap, surroundings
