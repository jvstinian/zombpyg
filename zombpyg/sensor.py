import numpy, pygame
from zombpyg.utils import Color, calculate_distance


class Sensor:
    def __init__(self, center, angle, length, walls, owner):
        self.owner = owner
        self.center = center
        self.length = length
        self.angle = angle
        self.orientation = 0

        self.end_point = None
        self.distance_to_wall = None
        self.collide_point = None
        self.walls = walls
        
        # initialize
        self.adjust_endpoint_for_wall()
    
    def set_center(self, x, y):
        self.center = (x, y)
        self.adjust_endpoint_for_wall()
    
    def set_orientation(self, orient):
        self.orientation = orient
        self.adjust_endpoint_for_wall()
    
    def restore_end_point(self):
        angle = self.angle + self.orientation
        dx = int(self.length * numpy.sin(numpy.deg2rad(angle)))
        dy = int(-self.length * numpy.cos(numpy.deg2rad(angle)))
        self.end_point = (self.center[0]+dx, self.center[1]+dy)
                
    def adjust_endpoint_for_wall(self):
        self.restore_end_point()
        self.collide_point = None
        self.distance_to_wall = None
        
        for wall in self.walls:
            point = wall.collide(self.center, self.end_point)
            if point is not None:
                distance = calculate_distance(self.center, point)
                if (self.distance_to_wall is None) or (distance < self.distance_to_wall):
                    self.distance_to_wall = distance
                    self.collide_point = point
 
    def detect_wall(self, default_length_multiplier=2):
        default = default_length_multiplier * self.length
        return self.distance_to_wall or default
                
    def detect_objective(self, objectives):
        minimum_distance = self.length * 2
        
        for objective in objectives:
            points = objective.collide(self.center, self.end_point)
            for point in points:
                distance = calculate_distance(self.center, point)
                if distance < minimum_distance:
                    minimum_distance = distance
        
        return minimum_distance
                
    def draw(self, game):
        if self.collide_point is None:
            self.restore_end_point()
            pygame.draw.line(game.DISPLAYSURF, Color.GRAY, self.center, self.end_point, 1)
        else:
            pygame.draw.line(game.DISPLAYSURF, Color.GRAY, self.center, self.collide_point, 1)
