import numpy
from pygame import Rect
from operator import itemgetter
import itertools

from zombpyg.utils.geometry import (
    _valid_angle, 
    get_intersect_point,
    get_nearest_point_and_distance_to_path,
    get_extreme_points_on_segment_intersecting_circle,
    rotate_vector,
    get_angle_and_distance_to_point,
)


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

    def __simple_move_distance_to_point__(self, center, radius, wallpoint):
        dx = wallpoint[0] - center[0]
        dy = wallpoint[1] - center[1]
        distance = numpy.sqrt(dx ** 2 + dy ** 2)
        return max(distance - radius, 0)

    def simple_maximum_move_distance(self, center, radius, orientation, default_max_distance):
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
                    self.__simple_move_distance_to_point__(center, radius, self.left_point)
                )
            if (self.right_angle > -90) and (self.right_angle < 90):
                distances.append(
                    self.__simple_move_distance_to_point__(center, radius, self.right_point)
                )
            # if len(distances) > 0:
            #     return min(distances)
            # else:
            #     return 10 * radius
            return min(distances)

    def contains_angle(self, angle):
        return (self.left_angle <= angle) and (angle <= self.right_angle)
    
    def contains_angle_in_interior(self, angle):
        return (self.left_angle < angle) and (angle < self.right_angle)
 
# Find the gap to the right
def get_angle_to_gap_on_right(target_gap_width, surroundings):
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
        while any([vws.contains_angle(right_angle) and (vws.right_angle > right_angle) for vws in surroundings]):
            # adjust right endpoint
            # Get the maximum right endpoint of intervals containing right_angle.
            right_angle, right_point = next(
                iter(sorted(
                    map(
                        lambda vws: (vws.right_angle, vws.right_point),
                        filter(
                            lambda vws: vws.contains_angle(right_angle) and (vws.right_angle > right_angle),
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
def get_angle_to_gap_on_left(target_gap_width, surroundings):
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
        while any([vws.contains_angle(left_angle) and (vws.left_angle < left_angle) for vws in surroundings]):
            # adjust left endpoint
            # Get the minimum left endpoint of intervals containing left_angle.
            left_angle, left_point = next(
                iter(sorted(
                    map(
                        lambda vws: (vws.left_angle, vws.left_point),
                        filter(
                            lambda vws: vws.contains_angle(left_angle) and (vws.left_angle < left_angle),
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
def identify_visible_point_extremes_in_subinterval(
    lower_visible_point, upper_visible_point, 
    lower_bound, upper_bound,
    cpt, is_nearest_point_to_line,
    position, orientation_vector, wall
):
    lower_angle, lower_distance, lower_point = lower_visible_point
    upper_angle, upper_distance, upper_point = upper_visible_point

    if lower_angle < lower_bound:
        lower_bound_rad = numpy.deg2rad(lower_bound)
        visend = tuple(numpy.array(position) + rotate_vector(orientation_vector, lower_bound_rad))
        adj_intersection_points = get_intersect_point(position, visend, wall.start, wall.end)
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
        visend = tuple(numpy.array(position) + rotate_vector(orientation_vector, upper_bound_rad))
        adj_intersection_points = get_intersect_point(position, visend, wall.start, wall.end)
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

def identify_visible_point_extremes(visiblepts, cpt, is_nearest_point_to_line, position, orientation_vector, wall):
    # visiblepts are expected to be ordered by angle
    if len(visiblepts) == 2:
        left_angle, left_distance, left_point = visiblepts[0]
        right_angle, right_distance, right_point = visiblepts[1]
        if right_angle - left_angle > 180:
            left_angle, right_angle = right_angle, (left_angle + 360.0)
            left_distance, right_distance = right_distance, left_distance
            left_point, right_point = right_point, left_point

        if max(left_angle, -90) <= min(right_angle, 90):
            return identify_visible_point_extremes_in_subinterval(
                (left_angle, left_distance, left_point), (right_angle, right_distance, right_point),
                -90, 90, 
                cpt, is_nearest_point_to_line, position, orientation_vector, wall
            )
        elif max(left_angle, 270) <= min(right_angle, 360):
            return identify_visible_point_extremes_in_subinterval(
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

def get_movement_estimates(position, radius, orientation, walls, obstacle_distance):
    surroundings = []
    orientation_vector = (
        numpy.sin(numpy.deg2rad(orientation)),
        -numpy.cos(numpy.deg2rad(orientation))
    )
    for wall in walls:
        cpt, dist, is_nearest_point_to_line = get_nearest_point_and_distance_to_path(wall.start, wall.end, position)
        if dist < obstacle_distance:
            wallpts = list(get_extreme_points_on_segment_intersecting_circle(wall.start, wall.end, position, obstacle_distance))
            wallpts = list(filter(lambda pt: pt is not None, wallpts))
            visiblepts = list(map(lambda wallpt: get_angle_and_distance_to_point(position, orientation, wallpt), wallpts))
            visiblepts = sorted(visiblepts, key=itemgetter(0, 1))
            vwso = identify_visible_point_extremes(visiblepts, cpt, is_nearest_point_to_line, position, orientation_vector, wall)
            if vwso is not None:
                surroundings.append(vwso)
    distanceForward = min(list(map(lambda vws: vws.simple_maximum_move_distance(position, radius, orientation, obstacle_distance), surroundings)), default=obstacle_distance)
    hasGapAhead = not any(map(lambda vws: vws.contains_angle(0.0), surroundings))
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
    angle_left_gap = get_angle_to_gap_on_left(target_gap_width, surroundings)
    angle_right_gap = get_angle_to_gap_on_right(target_gap_width, surroundings)

    return distanceForward, hasGapAhead, gapAheadWidth, gapAheadLeftAngle, gapAheadRightAngle, angle_left_gap, angle_right_gap, surroundings
