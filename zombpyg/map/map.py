from zombpyg.core.wall import Wall
from .objective import ObjectiveLocation
from .spawns import SpawnLocation
from .resourcespawns import ResourceSpawnLocation


class Map(object):
    """A map for a world."""
    def __init__(
        self, size, walls, player_spawns=None, zombie_spawns=None, objectives=None, resource_spawns=None
    ):
        self.size = size
        self.walls = walls
        self.player_spawns = player_spawns
        self.zombie_spawns = zombie_spawns
        self.objectives = objectives
        self.resource_spawns = resource_spawns

class DemoMap(Map):
    @staticmethod
    def build_map(w, h):
        walls = [
            Wall(start=(0, 0), end=(w, 0), width=1),
            Wall(start=(0, h-1), end=(w-1, h-1), width=1),
            Wall(start=(0, 0), end=(0, h-1), width=1),
            Wall(start=(w-1, 0), end=(w-1, h-1), width=1),
            Wall(start=(int(w/2), int(h/3)), end=(int(w/2), int(h*2/3))),
            Wall(start=(int(w/5), int(h/5)), end=(int(w/5), int(h*4/5))),
            Wall(start=(int(w*4/5), int(h/5)), end=(int(w*4/5), int(h*4/5)))
        ]
        player_spawns = [
            SpawnLocation(w - int(w/5), int(h/3), int(w/5), int(h/3))
        ]
        zombie_spawns = [
            SpawnLocation(int(w/5), int(h*2/5), int(w/2) - int(w/5), int(h*1/5)),
            SpawnLocation(int(w/2), int(h*2/5), int(4*w/5) - int(w/2), int(h*1/5), initial_spawn_only=True)
        ]
        objectives = [
            ObjectiveLocation(0, int(h/3), int(w/5), int(h/3))
        ]
        resource_spawns = [
            ResourceSpawnLocation(  int(w/2),    int(h/6), 10, 0.25, 100, 0.75, 2.0),
            ResourceSpawnLocation(  int(w/2),  int(5*h/6), 10, 0.25, 100, 0.75, 2.0),
            ResourceSpawnLocation(  int(w/5), int(1*h/10), 10, 0.25, 100, 0.75, 2.0),
            ResourceSpawnLocation(  int(w/5), int(9*h/10), 10, 0.25, 100, 0.75, 2.0),
            ResourceSpawnLocation(int(4*w/5), int(1*h/10), 10, 0.25, 100, 0.75, 2.0),
            ResourceSpawnLocation(int(4*w/5), int(9*h/10), 10, 0.25, 100, 0.75, 2.0)
        ]
        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
        )

class OpenRoomMap(Map):
    @staticmethod
    def build_map(w, h):
        walls = [
            Wall(start=(0, 0), end=(0, h-1), width=1),
            Wall(start=(0, h-1), end=(w-1, h-1), width=1),
            Wall(start=(w-1, h-1), end=(w-1,0), width=1),
            Wall(start=(w-1, 0), end=(0, 0), width=1),
        ]
        player_spawns = [
            SpawnLocation(int(2*w/5), int(2*h/5), int(w/5), int(h/5))
        ]
        zombie_spawns = [
            SpawnLocation(int(w*2/5), int(h*1/5), int(w/5), int(h/5)),
            SpawnLocation(int(w*2/5), int(h*3/5), int(w/5), int(h/5)),
            SpawnLocation(int(w*1/5), int(h*2/5), int(w/5), int(h/5)),
            SpawnLocation(int(w*3/5), int(h*2/5), int(w/5), int(h/5)),
        ]
        objectives = [
            ObjectiveLocation(int(w*2/5), int(h*0/5), int(w/5), int(h/5)),
            ObjectiveLocation(int(w*2/5), int(h*4/5), int(w/5), int(h/5)),
            ObjectiveLocation(int(w*0/5), int(h*2/5), int(w/5), int(h/5)),
            ObjectiveLocation(int(w*4/5), int(h*2/5), int(w/5), int(h/5)),
        ]
        resource_spawns = [
            ResourceSpawnLocation(int(w*1/10), int(h*1/5), 10, 0.5, 200, 0.5, 2.0),
            ResourceSpawnLocation(int(w*1/10), int(h*4/5), 10, 0.5, 200, 0.5, 2.0),
            ResourceSpawnLocation(int(w*9/10), int(h*1/5), 10, 0.5, 200, 0.5, 2.0),
            ResourceSpawnLocation(int(w*9/10), int(h*4/5), 10, 0.5, 200, 0.5, 2.0),
        ]
        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
        )

class EasyExitMap(Map):
    @staticmethod
    def build_map(w, h):
        walls = [
            Wall(start=(0, 0), end=(0, h-1), width=1),
            Wall(start=(0, h-1), end=(w-1, h-1), width=1),
            Wall(start=(w-1, h-1), end=(w-1,0), width=1),
            Wall(start=(w-1, 0), end=(0, 0), width=1),
        ]
        player_spawns = [
            SpawnLocation(int(2*w/5), int(2*h/5), int(w/5), int(h/5))
        ]
        zombie_spawns = [
            SpawnLocation(int(w*2/5), int(h*0/5), int(w/5), int(h/5)),
            SpawnLocation(int(w*2/5), int(h*4/5), int(w/5), int(h/5)),
            SpawnLocation(int(w*0/5), int(h*2/5), int(w/5), int(h/5)),
            SpawnLocation(int(w*4/5), int(h*2/5), int(w/5), int(h/5)),
        ]
        objectives = [
            ObjectiveLocation(int(w*0/5), int(h*0/5), int(w/5), int(h/5)),
            ObjectiveLocation(int(w*0/5), int(h*4/5), int(w/5), int(h/5)),
            ObjectiveLocation(int(w*4/5), int(h*0/5), int(w/5), int(h/5)),
            ObjectiveLocation(int(w*4/5), int(h*4/5), int(w/5), int(h/5)),
        ]
        resource_spawns = [
            ResourceSpawnLocation(int(w*(1+2*i)/10), int(h*j/5), 10, 0.5, 200, 0.5, 2.0)
            for i in range(0, 5)
            for j in range(1, 5)
        ]
        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
        )

class SimpleHallwayMap(Map):
    @staticmethod
    def build_map(w, h):
        walls = [
            Wall(start=(0, 0), end=(0, h-1), width=1),
            Wall(start=(0, h-1), end=(w-1, h-1), width=1),
            Wall(start=(w-1, h-1), end=(w-1,0), width=1),
            Wall(start=(w-1, 0), end=(0, 0), width=1),
            Wall(start=(0, int(h*2/5)), end=(w-1, int(h*2/5)), width=1),
            Wall(start=(0, int(h*3/5)), end=(w-1, int(h*3/5)), width=1),
        ]
        player_spawns = [
            SpawnLocation(int(1*w/5), int(h*2/5), int(w/5), int(h/5))
        ]
        zombie_spawns = [
            SpawnLocation(int(w*0/5), int(h*2/5), int(w/5), int(h/5)),
            SpawnLocation(int(w*3/5), int(h*2/5), int(w/5), int(h/5), initial_spawn_only=True),
        ]
        objectives = [
            ObjectiveLocation(int(w*4/5), int(h*2/5), int(w/5), int(h/5)),
        ]
        resource_spawns = [
            ResourceSpawnLocation(int(w*(1+2*i)/10), int(h*5/10), 10, 0.5, 200, 0.5, 2.0)
            for i in range(2, 4)
        ]
        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
        )

class MapFactory(object):
    @staticmethod
    def get_default(w, h):
        return DemoMap.build_map(w, h)
    
    @staticmethod
    def build_map(map_id, w, h):
        if map_id == "demo":
            return DemoMap.build_map(w, h)
        elif map_id == "open_room":
            return OpenRoomMap.build_map(w, h)
        elif map_id == "easy_exit":
            return EasyExitMap.build_map(w, h)
        elif map_id == "simple_hallway":
            return SimpleHallwayMap.build_map(w, h)
        else:
            return MapFactory.get_default(w, h)
