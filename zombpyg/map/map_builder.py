from typing import List, Dict
from abc import ABC, abstractmethod
from enum import StrEnum
import json
from zombpyg.map.map import MapFactory


class GameState(StrEnum):
    UNINITIALIZED = "uninitialized"
    TRUNCATED = "game_truncated"
    GAME_LOST = "game_lost"
    GAME_WON = "game_won"

class MapBuilder(ABC):
    @staticmethod
    def valid_tags():
        return ["SingleMap", "RandomMap"]

    @staticmethod
    def decode_hook(jsonobj):
        if "tag" in jsonobj:
            if (jsonobj["tag"] in ["SingleMap"]) and ("parameters" not in jsonobj):
                raise ValueError(f"A MapBuilder with tag {jsonobj['tag']} must have key \"parameters\"")
            if jsonobj["tag"] == "SingleMap":
                return SingleMapBuilder.from_dict(jsonobj["parameters"])
            elif jsonobj["tag"] == "RandomMap":
                mb = RandomMapBuilder.from_list_of_dicts(jsonobj["parameters"])
                if any([weight <= 0 for weight in mb.weights]):
                    raise ValueError("A negative weight was encountered in a RandomMapBuilder")
                return mb
            else:
                raise ValueError(f"GameRequest \"tag\" must be in {MapBuilder.valid_tags()}")
        else: # Simply pass the object through (used where objects are passed as parameters)
            return jsonobj

    @abstractmethod
    def build_map(self, last_game_state: GameState):
        pass
    
    @abstractmethod
    def get_render_width(self):
        pass
    
    @abstractmethod
    def get_render_height(self):
        pass
    
    # @abstractmethod
    # def get_initial_zombies(self):
    #     pass
    # 
    # @abstractmethod
    # def get_minimum_zombies(self):
    #     pass

class SingleMapBuilder(MapBuilder):
    def __init__(self, map_id: str, w: int, h: int):
    # initial_zombies: int, minimum_zombies: int
        self.map_id = map_id
        self.w = w
        self.h = h
        # self.initial_zombies = initial_zombies
        # self.minimum_zombies = minimum_zombies

    @classmethod
    def from_dict(cls, parameters: Dict):
        return cls(
            parameters.get("map_id"),
            parameters.get("w"),
            parameters.get("h"),
        )
    
    def build_map(self, last_game_state: GameState):
        if last_game_state == GameState.UNINITIALIZED:
            return True, MapFactory.build_map(self.map_id, self.w, self.h)
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

class RandomMapBuilder(MapBuilder):
    def __init__(self, weights: List[float], map_builders: List[MapBuilder]):
        self.weights = weights
        self.map_builders = map_builders
        self.last_map_builder_index = None

    @classmethod
    def from_list_of_dicts(cls, parameters: List[Dict]):
        return cls(
            [p.get("weight") for p in parameters],
            [p.get("map_builder") for p in parameters],
        )
    
    def build_map(self, last_game_state: GameState):
        next_index = random.choices(range(0, len(self.weights)), weights=self.weights)
        if self.last_map_builder_index is None or (self.last_map_builder_index != next_index):
            self.last_map_builder_index = next_index
            map_builder = self.map_builders[self.last_map_builder_index]
        else:
            # No change in map
            return False, None

    def get_render_width(self):
        return max([mb.w for mb in self.map_builders])
    
    def get_render_height(self):
        return max([mb.h for mb in self.map_builders])

class MapBuilderFactory(object):
    @staticmethod
    def get_map_builder(map_configuration: Dict):
        if "tag" in map_configuration:
            if (map_configuration["tag"] in ["SingleMap", "RandomMap"]) and ("parameters" not in map_configuration):
                raise ValueError(f"A MapBuilder with tag {map_configuration['tag']} must have key \"parameters\"")
            if map_configuration["tag"] == "SingleMap":
                return SingleMapBuilder.from_dict(map_configuration["parameters"])
            if map_configuration["tag"] == "RandomMap":
                mb = RandomMapBuilder.from_list_of_dicts(map_configuration["parameters"])
                if any([weight <= 0 for weight in mb.weights]):
                    raise ValueError("A negative weight was encountered in a RandomMapBuilder")
                return mb
            else:
                raise ValueError(f"GameRequest \"tag\" must be in {MapBuilder.valid_tags()}")
        else:
            raise ValueError("The map builder configuration must have a key \"tag\"")

