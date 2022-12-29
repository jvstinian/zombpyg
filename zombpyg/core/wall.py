import pygame
from zombpyg.utils.geometry import calculate_intersect_point
from zombpyg.utils.surroundings import Color


class Wall(object):
    def __init__(self, start, end, width=2):
        self.start = start
        self.end = end
        self.width = width
        
    def draw(self, game):
        pygame.draw.line(game.DISPLAYSURF, Color.WHITE, self.start, self.end, self.width)

    def collide(self, p1, p2):
        point = calculate_intersect_point(p1, p2, self.start, self.end)
        if point is None:
            return None
        else:
            return (int(point[0]), int(point[1]))
