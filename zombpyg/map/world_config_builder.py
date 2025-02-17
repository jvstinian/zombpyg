from typing import List, Dict
from abc import ABC, abstractmethod
from enum import StrEnum
import json
import random
from zombpyg.map.map import MapFactory


class GameState(StrEnum):
    UNINITIALIZED = "uninitialized"
    INITIALIZED = "initialized"
    TRUNCATED = "game_truncated" # TODO: Is this needed?
    GAME_LOST = "game_lost"
    GAME_WON = "game_won"

class WorldConfiguration(object):
    def __init__(self, game_map: str, initial_zombies: int, minimum_zombies: int):
        self.game_map = game_map
        # self.w = w
        # self.h = h
        self.initial_zombies = initial_zombies 
        self.minimum_zombies = minimum_zombies

class WorldConfigurationBuilder(ABC):
    @staticmethod
    def valid_tags():
        return ["SingleMap", "RandomMap"]

    @staticmethod
    def decode_hook(jsonobj):
        if "tag" in jsonobj:
            if (jsonobj["tag"] in ["SingleMap", "RandomMap"]) and ("parameters" not in jsonobj):
                raise ValueError(f"A WorldConfigurationBuilder with tag {jsonobj['tag']} must have key \"parameters\"")
            if jsonobj["tag"] == "SingleMap":
                return SingleMapBuilder.from_dict(jsonobj["parameters"])
            elif jsonobj["tag"] == "RandomMap":
                mb = RandomMapBuilder.from_list_of_dicts(jsonobj["parameters"])
                if any([weight <= 0 for weight in mb.weights]):
                    raise ValueError("A negative weight was encountered in a RandomMapBuilder")
                return mb
            else:
                raise ValueError(f"GameRequest \"tag\" must be in {WorldConfigurationBuilder.valid_tags()}")
        else: # Simply pass the object through (used where objects are passed as parameters)
            return jsonobj

    @abstractmethod
    def build_world_configuration(self, last_game_state: GameState) -> WorldConfiguration:
        pass
    
    @abstractmethod
    def get_render_width(self) -> int:
        pass
    
    @abstractmethod
    def get_render_height(self) -> int:
        pass
    
class SingleMapBuilder(WorldConfigurationBuilder):
    def __init__(self, map_id: str, w: int, h: int, initial_zombies: int, minimum_zombies: int):
        self.map_id = map_id
        self.w = w
        self.h = h
        self.initial_zombies = initial_zombies
        self.minimum_zombies = minimum_zombies

    @classmethod
    def from_dict(cls, parameters: Dict):
        return cls(
            parameters.get("map_id"),
            parameters.get("w"),
            parameters.get("h"),
            parameters.get("initial_zombies"),
            parameters.get("minimum_zombies"),
        )
    
    def build_world_configuration(self, last_game_state: GameState):
        if last_game_state == GameState.UNINITIALIZED:
            game_map = MapFactory.build_map(self.map_id, self.w, self.h)
            return True, WorldConfiguration(game_map, self.initial_zombies, self.minimum_zombies)
        else:
            return False, None
    
    def get_render_width(self):
        return self.w
    
    def get_render_height(self):
        return self.h
    
    # def get_initial_zombies(self):
    #     return self.initial_zombies

    # def get_minimum_zombies(self):
    #     return self.minimum_zombies
    
class RandomMapBuilder(WorldConfigurationBuilder):
    def __init__(self, weights: List[float], map_builders: List[WorldConfigurationBuilder]):
        self.weights = weights
        self.map_builders = map_builders
        self.last_map_builder_index = None

    @classmethod
    def from_list_of_dicts(cls, parameters: List[Dict]):
        return cls(
            [p.get("weight") for p in parameters],
            [WorldConfigurationBuilderFactory.get_world_configuration_builder(p.get("map_builder")) for p in parameters],
        )
    
    def build_world_configuration(self, last_game_state: GameState):
        next_index = random.choices(range(0, len(self.weights)), weights=self.weights, k=1)[0]
        if self.last_map_builder_index is None or (self.last_map_builder_index != next_index):
            self.last_map_builder_index = next_index
            map_builder = self.map_builders[self.last_map_builder_index]
            return map_builder.build_world_configuration(last_game_state)
        else:
            # No change in map
            return False, None

    def get_render_width(self):
        return max([mb.get_render_width() for mb in self.map_builders])
    
    def get_render_height(self):
        return max([mb.get_render_height() for mb in self.map_builders])

class WorldConfigurationBuilderFactory(object):
    # @staticmethod
    # def get_map_builder_from_json(jsonobj: str):
    #     try:
    #         obj = json.loads(jsonobj, object_hook=MapBuilder.decode_hook)
    #         if not isinstance(obj, (MapBuilder,)):
    #             raise ValueError(f"Expected parsed JSON to be of type MapBuilder, but has type {type(obj)} instead")
    #     except Exception as ex:
    #         raise ex
    #     else:
    #         return obj

    @staticmethod
    def get_world_configuration_builder(map_configuration: Dict):
        if "tag" in map_configuration:
            if (map_configuration["tag"] in ["SingleMap", "RandomMap"]) and ("parameters" not in map_configuration):
                raise ValueError(f"A WorldConfigurationBuilder with tag {map_configuration['tag']} must have key \"parameters\"")
            if map_configuration["tag"] == "SingleMap":
                return SingleMapBuilder.from_dict(map_configuration["parameters"])
            if map_configuration["tag"] == "RandomMap":
                mb = RandomMapBuilder.from_list_of_dicts(map_configuration["parameters"])
                if any([weight <= 0 for weight in mb.weights]):
                    raise ValueError("A negative weight was encountered in a RandomMapBuilder")
                return mb
            else:
                raise ValueError(f"GameRequest \"tag\" must be in {WorldConfigurationBuilder.valid_tags()}")
        else:
            raise ValueError("The map builder configuration must have a key \"tag\"")

