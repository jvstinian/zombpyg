import numpy
from zombpyg.core.things import RectangularThing


class SpawnLocation(RectangularThing):
    def __init__(self, left, top, width, height, initial_spawn_only=False):
        super(SpawnLocation, self).__init__(
            left, top, width, height,
            'objective', 'green', 0, 
        )
        self.initial_spawn_only = initial_spawn_only
    
    def get_spawn_location(self):
        x = numpy.random.randint(self.left, self.left + self.width)
        y = numpy.random.randint(self.top, self.top + self.height)
        return x, y
