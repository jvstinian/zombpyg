# tests/test_gym_env_imports.py
from tests.helpers import not_raises


def test_imports():
    with not_raises(ImportError):
        import zombpyg.gym_env
        import zombpyg.game

