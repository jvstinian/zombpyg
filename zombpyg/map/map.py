import random
from zombpyg.core.wall import Wall
from .objective import ObjectiveLocation
from .spawns import SpawnLocation
from .resourcespawns import ResourceSpawnLocation
from .checkpoint import Checkpoint


class Map(object):
    """A map for a world."""
    def __init__(
        self, size, walls, player_spawns=None, zombie_spawns=None, objectives=None, resource_spawns=None, checkpoints=None
    ):
        self.size = size
        self.walls = walls
        self.player_spawns = player_spawns
        self.zombie_spawns = zombie_spawns
        self.objectives = objectives
        self.resource_spawns = resource_spawns
        self.checkpoints = checkpoints

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
        resource_spawn_start = int(3*w/10)
        resource_spawn_end = int(9*w/10)
        resource_spawn_steps = (resource_spawn_end - resource_spawn_start)//20
        resource_spawns = [
            ResourceSpawnLocation(resource_spawn_start + i*20, int(h/2), 10, 0.01, 20, 0.99, 0.1)
            for i in range(resource_spawn_steps+1)
        ] + [
            ResourceSpawnLocation(int(w/2), int(h/2)-20, 10, 0.5, 50, 0.5, 0.5),
            ResourceSpawnLocation(int(w/2), int(h/2)+20, 10, 0.5, 50, 0.5, 0.5),
        ]
        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
        )

class NarrowHallwayMap(Map):
    @staticmethod
    def build_map(w, h):
        main_hallway_lower_h = int(h/2) - int(h/20)
        main_hallway_upper_h = int(h/2) + int(h/20)
        second_hallway_lower_h = main_hallway_lower_h - int(h*1/5)
        second_hallway_upper_h = main_hallway_upper_h + int(h*1/5)
        second_hallway_lower_w = int(w*3/10)
        second_hallway_upper_w = int(w*4/10)
        exit_lower_h = main_hallway_lower_h - int(h*1/10)
        exit_upper_h = main_hallway_upper_h + int(h*1/10)
        exit_lower_w = int(w*9/10)
        exit_upper_w = int(w-1)
            
        lower_wall_points = [
            (0, main_hallway_lower_h),
            (second_hallway_lower_w, main_hallway_lower_h),
            (second_hallway_lower_w, second_hallway_lower_h),
            (second_hallway_upper_w, second_hallway_lower_h),
            (second_hallway_upper_w, main_hallway_lower_h),
            (exit_lower_w, main_hallway_lower_h),
            (exit_lower_w, exit_lower_h),
            (exit_upper_w, exit_lower_h),
        ]

        upper_wall_points = [
            (0, main_hallway_upper_h),
            (second_hallway_lower_w, main_hallway_upper_h),
            (second_hallway_lower_w, second_hallway_upper_h),
            (second_hallway_upper_w, second_hallway_upper_h),
            (second_hallway_upper_w, main_hallway_upper_h),
            (exit_lower_w, main_hallway_upper_h),
            (exit_lower_w, exit_upper_h),
            (exit_upper_w, exit_upper_h),
        ]

        walls = [
            Wall(start=(0, 0), end=(0, h-1), width=1),
            Wall(start=(0, h-1), end=(w-1, h-1), width=1),
            Wall(start=(w-1, h-1), end=(w-1,0), width=1),
            Wall(start=(w-1, 0), end=(0, 0), width=1),
            ] + list(
                map(lambda pts: Wall(start=pts[0], end=pts[1], width=1), zip(lower_wall_points[0:-1], lower_wall_points[1:]))
            ) + list(
                map(lambda pts: Wall(start=pts[0], end=pts[1], width=1), zip(upper_wall_points[0:-1], upper_wall_points[1:]))
            )

        player_spawns = [
            SpawnLocation(
                second_hallway_lower_w, 
                second_hallway_lower_h, 
                second_hallway_upper_w - second_hallway_lower_w,
                second_hallway_upper_h - second_hallway_lower_h,
            )
        ]
        zombie_spawns = [
            SpawnLocation(int(w*0/5), main_hallway_lower_h, second_hallway_lower_w, main_hallway_upper_h - main_hallway_lower_h),
            SpawnLocation(
                second_hallway_upper_w, main_hallway_lower_h, exit_lower_w - second_hallway_upper_w, main_hallway_upper_h - main_hallway_lower_h,
                initial_spawn_only=True
            ),
        ]
        objectives = [
            ObjectiveLocation(
                exit_lower_w, exit_lower_h, exit_upper_w - exit_lower_w, exit_upper_h - exit_lower_h
            ),
        ]
        resource_spawn_start = (second_hallway_lower_w + second_hallway_upper_w)//2
        resource_spawn_end = (exit_lower_w + exit_upper_w)//2
        resource_spawn_steps = (resource_spawn_end - resource_spawn_start)//20
        resource_spawns = [
            ResourceSpawnLocation(resource_spawn_start + i*20, (main_hallway_lower_h + main_hallway_upper_h)//2, 10, 0.01, 20, 0.99, 0.1)
            for i in range(resource_spawn_steps+1)
        ]
        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
        )

class CatacombsMap(Map):
    @staticmethod
    def get_rectangle_walls(w0, h0, w1, h1):
        return [
            Wall(start=(w0, h0), end=(w0, h1), width=1),
            Wall(start=(w0, h1), end=(w1, h1), width=1),
            Wall(start=(w1, h1), end=(w1, h0), width=1),
            Wall(start=(w1, h0), end=(w0, h0), width=1),
        ]
            
    @staticmethod
    def build_map(w, h):
        walls = [
            Wall(start=(0, 0), end=(0, h-1), width=1),
            Wall(start=(0, h-1), end=(w-1, h-1), width=1),
            Wall(start=(w-1, h-1), end=(w-1,0), width=1),
            Wall(start=(w-1, 0), end=(0, 0), width=1),
        ]
        
        cell_width = int(w*1/10)
        cell_height = int(h*1/10)

        for i in range(0, 3):
            for j in range(0, 3):
                lower_w = (1 + 3*i)*cell_width
                lower_h = (1 + 3*j)*cell_height
                upper_w = (1 + 3*i + 2)*cell_width
                upper_h = (1 + 3*j + 2)*cell_height
                if (i == 0) and (j ==2):
                    upper_h = (1 + 3*j + 1)*cell_height
                if (i == 2) and (j ==0):
                    upper_w = (1 + 3*i + 1)*cell_width

                walls.extend(
                    CatacombsMap.get_rectangle_walls(
                        lower_w, lower_h, upper_w, upper_h
                    )
                )

        player_spawns = [
            SpawnLocation(0*cell_width, 8*cell_height, 4*cell_width, 2*cell_height)
        ]
        zombie_spawns = [
            SpawnLocation(0*cell_width, 3*cell_height, w, cell_height),
            SpawnLocation(0*cell_width, 6*cell_height, w, cell_height),
        ]
        objectives = [
            ObjectiveLocation(8*cell_width, 0*cell_height, 2*cell_width, 3*cell_height),
        ]
        
        path_width_nodes = [(6*i + 1)*cell_width // 2 for i in range(0, 4)]
        path_height_nodes = [(6*i + 1)*cell_height // 2 for i in range(0, 4)]
        path_height_nodes.reverse()
        up_nodes = random.sample(range(0, 6), 3)
        
        # We consider resource spawns just off the crossroads.
        # We enumerate a shift in each direction at the crossroads.
        # For each crossroad on the path (excluding beginning and ending)
        # we identify the incoming and outgoing directions, and 
        # put resource spawns in the other directions.
        resource_spawns = []
        four_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        prev_node = (0, 0)
        for i in range(0,5): # We consider only the internal crossroads, so no need to consider the last index
            exclude_locations = []
            # Determine the indices for the current node and the directions to exclude
            if i in up_nodes:
                current_node = (prev_node[0], prev_node[1]+1)
                exclude_locations = [(0,-1)]
            else:
                current_node = (prev_node[0]+1, prev_node[1])
                exclude_locations = [(-1,0)]
            if (i+1) in up_nodes:
                exclude_locations.append((0,1))
            else:
                exclude_locations.append((1,0))
            # The directions to consider
            resource_locations = [direction for direction in four_directions if (direction not in exclude_locations)]
            for loc in resource_locations: # Iterate over the possible directions
                # We set up the node coordinates, but only to test if the direction is viable
                test_coords = (current_node[0]+loc[0], current_node[1]+loc[1])
                if (test_coords[0] >= 0) and (test_coords[0] < 4) and (test_coords[1] >=0) and (test_coords[1] < 4):
                    # The direction represented by loc is viable
                    cw = path_width_nodes[current_node[0]]
                    ch = path_height_nodes[current_node[1]]
                    # In the following, since the path_height_nodes are reverse ordered, we multiply 
                    # the delta by -1 (i.e., "up" represents a smaller y-coordinate value).
                    resource_spawns.append(
                        ResourceSpawnLocation(cw + loc[0]*20, ch + (-1)*loc[1]*20, 10, 0.5, 200, 0.5, 2.0)
                    )
            prev_node = current_node
        
        last_node = (0, 0)
        checkpoints = []
        for i in range(0, 6):
            if i in up_nodes:
                cw = path_width_nodes[last_node[0]]
                # Note that heights are reverse ordered
                ch0 = path_height_nodes[last_node[1]]
                ch1 = path_height_nodes[last_node[1]+1]
                steps = (ch0 - ch1) // 20
                checkpoints.extend(
                    [Checkpoint(cw, ch0 - i*20, 10) for i in range(steps)]
                )
                last_node = (last_node[0], last_node[1]+1)
            else:
                ch = path_height_nodes[last_node[1]]
                cw0 = path_width_nodes[last_node[0]]
                cw1 = path_width_nodes[last_node[0]+1]
                steps = (cw1 - cw0) // 20
                checkpoints.extend(
                    [Checkpoint(cw0 + i*20, ch, 10) for i in range(steps)]
                )
                last_node = (last_node[0]+1, last_node[1])

        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
            checkpoints=checkpoints,
        )

class HallwayElevatorMap(Map):
    @staticmethod
    def build_map(w, h):
        lower_wall_points = [
            (         0, int(h*2/5)),
            (int(w*3/5), int(h*2/5)),
            (int(w*3/5), int(h*1/5)),
            (       w-1, int(h*1/5)),
        ]
        
        upper_wall_points = [
            (         0, int(h*3/5)),
            (int(w*3/5), int(h*3/5)),
            (int(w*3/5), int(h*4/5)),
            (       w-1, int(h*4/5)),
        ]

        walls = [
            Wall(start=(0, 0), end=(0, h-1), width=1),
            Wall(start=(0, h-1), end=(w-1, h-1), width=1),
            Wall(start=(w-1, h-1), end=(w-1,0), width=1),
            Wall(start=(w-1, 0), end=(0, 0), width=1),
            Wall(start=(int(w*4/5), int(h*2/5)), end=(int(w*4/5), int(h*3/5)), width=1),
        ] + list(
            map(lambda pts: Wall(start=pts[0], end=pts[1], width=1), zip(lower_wall_points[0:-1], lower_wall_points[1:]))
        ) + list(
            map(lambda pts: Wall(start=pts[0], end=pts[1], width=1), zip(upper_wall_points[0:-1], upper_wall_points[1:]))
        )
        
        player_spawns = [
            SpawnLocation(int(1*w/5), int(h*2/5), int(w/5), int(h/5))
        ]
        zombie_spawns = [
            SpawnLocation(int(w*0/5), int(h*2/5), int(w/5), int(h/5)),
            SpawnLocation(int(w*3/5), int(h*2/5), int(w/5), int(h*2/5), initial_spawn_only=True),
        ]
        objectives = [
            ObjectiveLocation(int(w*4/5), int(h*2/5), int(w/5), int(h/5)),
        ]
        rsw1 = (int(w*1/5)+ int(w*2/5))//2
        rsw2 = (int(w*3/5)+ int(w*4/5))//2
        rsw3 = (int(w*4/5)+ (w-1))//2
        rsh1 = (int(h*1/5)+ int(h*2/5))//2
        rsh2 = (int(h*3/5)+ int(h*4/5))//2
        steps1 = (rsw2 - rsw1)//20
        steps2 = (rsh2 - rsh1)//20
        steps3 = (rsw3 - rsw2)//20
        resource_spawns = [
            ResourceSpawnLocation(rsw1 + i*20, int(h*5/10)-20, 10, 0.01, 20, 0.99, 0.1)
            for i in range(steps1)
        ] + [
            ResourceSpawnLocation(rsw2-20, rsh1 + i*20, 10, 0.01, 20, 0.99, 0.1)
            for i in range(steps2+1)
        ] + [
            ResourceSpawnLocation(rsw2 + i*20, rsh1-20, 10, 0.01, 20, 0.99, 0.1)
            for i in range(1,steps3+1)
        ] + [
            ResourceSpawnLocation(rsw2 + i*20, rsh2+20, 10, 0.01, 20, 0.99, 0.1)
            for i in range(1,steps3+1)
        ]
        # resource_spawns = [
        #     ResourceSpawnLocation(int(w*7/10), int(h*5/10), 10, 0.5, 200, 0.5, 2.0),
        #     ResourceSpawnLocation(int(w*7/10), int(h*3/10), 10, 0.5, 200, 0.5, 2.0),
        #     ResourceSpawnLocation(int(w*7/10), int(h*7/10), 10, 0.5, 200, 0.5, 2.0),
        #     ResourceSpawnLocation(int(w*9/10), int(h*3/10), 10, 0.5, 200, 0.5, 2.0),
        #     ResourceSpawnLocation(int(w*9/10), int(h*7/10), 10, 0.5, 200, 0.5, 2.0),
        # ]
        checkpoints = [
            Checkpoint(rsw1 + i*20, int(h*5/10), 10)
            for i in range(steps1)
        ] + [
            Checkpoint(rsw2, rsh1 + i*20, 10)
            for i in range(steps2+1)
        ] + [
            Checkpoint(rsw2 + i*20, rsh1, 10)
            for i in range(1,steps3+1)
        ] + [
            Checkpoint(rsw2 + i*20, rsh2, 10)
            for i in range(1,steps3+1)
        ] + [
            Checkpoint(rsw3, rsh1 + i*20, 10)
            for i in range(1, steps2)
        ]
        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
            checkpoints=checkpoints,
        )

class TinySpace0Map(Map):
    @staticmethod
    def build_map(w, h):
        w1 = int(w*1/5)
        w2 = int(w*4/5)
        h1 = int(h*2/5)
        h2 = int(h*3/5)
        subbox_width = (w2 - w1) // 3
        walls = [
            # Wall(start=(0, 0), end=(0, h-1), width=1), # We don't even need the outer edges
            # Wall(start=(0, h-1), end=(w-1, h-1), width=1),
            # Wall(start=(w-1, h-1), end=(w-1,0), width=1),
            # Wall(start=(w-1, 0), end=(0, 0), width=1),
            Wall(start=(w1, h1), end=(w1, h2), width=1),
            Wall(start=(w1, h2), end=(w2, h2), width=1),
            Wall(start=(w2, h2), end=(w2, h1), width=1),
            Wall(start=(w2, h1), end=(w1, h1), width=1),
        ]
        player_spawns = [
            SpawnLocation(w1, h1, subbox_width, h2-h1)
        ]
        zombie_spawns = [
            SpawnLocation(w1+subbox_width, h1, subbox_width, h2-h1),
        ]
        objectives = [
            ObjectiveLocation(w1+2*subbox_width, h1, subbox_width, h2-h1),
        ]

        resource_spawn_start = w1 + (w2-w1)//6
        resource_spawn_end = w2 - (w2-w1)//6
        resource_spawn_steps = (resource_spawn_end - resource_spawn_start)//20
        resource_spawns = [
            ResourceSpawnLocation(resource_spawn_start + i*20, (h1 + h2)//2, 10, 0.01, 20, 0.99, 0.1)
            for i in range(resource_spawn_steps+1)
        ]
        
        checkpoints = [
            Checkpoint(resource_spawn_start + i*20, (h1 + h2)//2 - 20, 10)
            for i in range(resource_spawn_steps+1)
        ]

        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
            checkpoints=checkpoints,
        )

class TinySpace1Map(Map):
    @staticmethod
    def build_map(w, h):
        w1 = int(w*1/5)
        w2 = int(w*2/5)
        w3 = int(w*3/5)
        w4 = int(w*4/5)
        h1 = int(h*1/5)
        h2 = int(h*2/5)
        h3 = int(h*3/5)
        h4 = int(h*4/5)

        # Unlike in the hallway maps, we go all the way around the perimeter
        wall_points = [
            (w1, h2), # start on the far left
            (w2, h2), # right
            (w2, h1), # up
            (w3, h1), # right
            (w3, h2), # down
            (w4, h2), # right
            (w4, h3), # down
            (w3, h3), # left
            (w3, h4), # down
            (w2, h4), # left
            (w2, h3), # up
            (w1, h3), # left
            (w1, h2), # up
        ]
        walls = list(
            map(lambda pts: Wall(start=pts[0], end=pts[1], width=1), zip(wall_points[0:-1], wall_points[1:]))
        )

        player_spawns = [
            SpawnLocation(w1, h2, w2-w1, h3-h2)
        ]
        zombie_spawns = [
            SpawnLocation(w2, h2, w3-w2, h3-h2, initial_spawn_only=True),
            SpawnLocation(w2, h1, w3-w2, h2-h1),
            SpawnLocation(w2, h3, w3-w2, h4-h3),
        ]
        objectives = [
            ObjectiveLocation(w3, h2, w4-w3, h3-h2),
        ]

        resource_spawn_start = (w1 + w2)//2 
        resource_spawn_end = (w3 + w4)//2 
        resource_spawn_steps = (resource_spawn_end - resource_spawn_start)//20
        resource_spawns = [
            ResourceSpawnLocation(resource_spawn_start + i*20, (h2 + h3)//2, 10, 0.01, 20, 0.99, 0.1)
            for i in range(resource_spawn_steps+1)
        ] + [
            ResourceSpawnLocation((w2 + w3)//2, (h2 + h3)//2 - 20, 10, 0.5, 200, 0.5, 2.0),
            ResourceSpawnLocation((w2 + w3)//2, (h2 + h3)//2 + 20, 10, 0.5, 200, 0.5, 2.0),
        ]
        checkpoints = [
            Checkpoint(resource_spawn_start + i*20, (h2 + h3)//2 + 20, 10)
            for i in range(resource_spawn_steps+1)
        ]
        return Map(
            (w, h),
            walls,
            player_spawns=player_spawns,
            zombie_spawns=zombie_spawns,
            objectives=objectives,
            resource_spawns=resource_spawns,
            checkpoints=checkpoints,
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
        elif map_id == "narrow_hallway":
            return NarrowHallwayMap.build_map(w, h)
        elif map_id == "catacombs":
            return CatacombsMap.build_map(w, h)
        elif map_id == "elevator":
            return HallwayElevatorMap.build_map(w, h)
        elif map_id == "tiny_space_v0":
            return TinySpace0Map.build_map(w, h)
        elif map_id == "tiny_space_v1":
            return TinySpace1Map.build_map(w, h)
        else:
            return MapFactory.get_default(w, h)
