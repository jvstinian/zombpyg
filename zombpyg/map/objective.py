from abc import ABC, abstractmethod
from zombpyg.utils import calculate_distance, Color
from zombpyg.core import RectangularThing, CircularThing
from zombpyg.object import Wall

class Objective(ABC):
    @abstractmethod
    def contains(point):
        pass
    
    @abstractmethod
    def collide(self, start, end):
        pass

class ObjectiveLocation(RectangularThing, Objective):
    """Objective location."""
    def __init__(self, left, top, width, height):
        color = Color.GRAY
        super(ObjectiveLocation, self).__init__(
            left, top, width, height,
            'objective', color, 0, 
        )
    
    def contains(self, point):
        x = point[0]
        y = point[1]
        return (
            (x >= self.left) and
            (x <= self.left + self.width) and
            (y >= self.top) and
            (y <= self.top + self.height)
        )
    
    def collide(self, start, end):
        # we get the boundary of the rectangle as a set of walls
        topleft = (self.left, self.top)
        bottomleft = (self.left, self.top + self.height)
        bottomright = (self.left + self.width, self.top + self.height)
        topright = (self.left + self.width, self.top)
        walls = [
            Wall(topleft, bottomleft),
            Wall(bottomleft, bottomright),
            Wall(bottomright, topright),
            Wall(topright, topleft),
        ]

        points = []
        for wall in walls:
            point = wall.collide(start, end)
            if point is not None:
                points.append(point)

        return points

class CircularObjectiveLocation(CircularThing, Objective):
    def __init__(
        self, x, y, r
    ):
        super(CircularObjectiveLocation, self).__init__(
            x, y, r,
            'objective', 'blue', 0, 
        )
    
    def contains(point):
        return calculate_distance(self.center, point) < self.r

    def collide(self, start, end):
        potential_points = getExtremePointsOnSegmentIntersectingCircle(
            start, end, 
            self.get_position(),
            self.r
        )
        return list(filter(lambda pt: pt is not None, potential_points))
