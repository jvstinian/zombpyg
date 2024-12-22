# tests/weapons/agent.py
import pytest
from zombpyg.core.weapons import WeaponFactory


weapon_names = [
    "rifle", "shotgun", "gun", "axe", "knife"
]

@pytest.mark.parametrize("weapon_name", weapon_names)
def test_weapon_factory(weapon_name):
    weapon = WeaponFactory.create_weapon(weapon_name)
    assert weapon is not None
    assert weapon.name.lower() == weapon_name

def test_weapon_factory_for_random():
    weapon = WeaponFactory.create_weapon("random")
    assert weapon is not None
    assert weapon.name.lower() in weapon_names

