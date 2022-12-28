import numpy
from zombpyg.core import CircularThing
from zombpyg.resources import MedicalSupplyResource, AmmoSupplyResource


class ResourceSpawnLocation(CircularThing):
    def __init__(
        self, x, y, r, 
        medical_spawn_probability, medical_spawn_life, 
        ammo_spawn_probability, ammo_spawn_life
    ):
        # Note the life for CircularThing is set to 0
        super(ResourceSpawnLocation, self).__init__(
            x, y, r,
            'resource spawn', 'white', 0,
        )
        self.medical_spawn_probability = medical_spawn_probability
        self.medical_spawn_life = medical_spawn_life 
        self.ammo_spawn_probability = ammo_spawn_probability
        self.ammo_spawn_life = ammo_spawn_life
    
    def spawn_resource(self):
        p = numpy.random.random()
        if p <= self.medical_spawn_probability:
            return MedicalSupplyResource(self.x, self.y, self.r, self.medical_spawn_life)
        elif p <= self.medical_spawn_probability + self.ammo_spawn_probability:
            return AmmoSupplyResource(self.x, self.y, self.r, self.ammo_spawn_life)
