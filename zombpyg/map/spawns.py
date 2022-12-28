import numpy
from zombpyg.core import RectangularThing


class SpawnLocation(RectangularThing):
    def __init__(self, left, top, width, height):
        super(SpawnLocation, self).__init__(
            left, top, width, height,
            'objective', 'green', 0, 
        )
    
    def get_spawn_location(self):
        x = numpy.random.randint(self.left, self.left + self.width)
        y = numpy.random.randint(self.top, self.top + self.height)
        return x, y
