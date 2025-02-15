# tests/map_builder.py
from contextlib import contextmanager
import pytest
from zombpyg.map.map_builder import MapBuilderFactory, SingleMapBuilder, RandomMapBuilder


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception as ex:
        raise pytest.fail("DID RAISE {0}".format(ex))

def test_simple_map_builder():
    map_config = {
        "tag": "SingleMap",
        "parameters": {
            "map_id": "tiny_space_v1",
            "w": 640, 
            "h": 480
        }
    }
    mb = None
    with not_raises(ValueError):
        mb = MapBuilderFactory.get_map_builder(map_config)
    assert isinstance(mb, (SingleMapBuilder,))

def test_random_map_builder():
    map_config = {
        "tag": "RandomMap",
        "parameters": [
            {
                "weight": 0.25,
                "map_builder": {
                    "tag": "SimpleMap",
                    "parameters": {
                        "map_id": "tiny_space_v1",
                        "w": 640, 
                        "h": 480
                    }
                }
            },
            {
                "weight": 0.75,
                "map_builder": {
                    "tag": "SimpleMap",
                    "parameters": {
                        "map_id": "tiny_space_v0",
                        "w": 640, 
                        "h": 480
                    }
                }
            }
        ]
    }
    mb = None
    with not_raises(ValueError):
        mb = MapBuilderFactory.get_map_builder(map_config)
    assert isinstance(mb, (RandomMapBuilder,))

