from .core import CircularThing
from .utils import Color
import math

class Resources(CircularThing):
    def __init__(
        self, x, y, r,
        name, color, life,
        resource_type,
    ):
        super(Resources, self).__init__(
            x, y, r,
            name, color, life,
            dead_decoration=None,
        )

        self.resource_type = resource_type
    
    def decrease_life(self, amount):
        self.life -= amount
    
    def is_used_up(self):
        return self.life <= 0
    
    def transfer_to(self, player):
        pass
        
class MedicalSupplyResource(Resources):
    def __init__(
        self, x, y, r, life,
    ):
        super(MedicalSupplyResource, self).__init__(
            x, y, r,
            "medical supply", Color.RED, life,
            "medical"
        )
    
    def use_by(self, player):
        if self.life > 0 and (player.healing_capacity < 100):
            transfer_amount = min(self.life, 100 - player.healing_capacity)
            self.life -= transfer_amount
            player.healing_capacity += transfer_amount
            print(f"Healing capacity taken: {transfer_amount}")

class AmmoSupplyResource(Resources):
    def __init__(
        self, x, y, r, life,
    ):
        super(AmmoSupplyResource, self).__init__(
            x, y, r,
            "ammo supply", Color.GREEN, life,
            "ammo"
        )
    
    def use_by(self, player):
        weapon = player.weapon
        if (weapon is not None) and weapon.is_firearm:
            consumption_rate = weapon.ammo_resource_consumption_rate()
            if self.life > 0 and (consumption_rate is not None) and (consumption_rate > 0.0):
                # We take the ceiling to guarantee the resource is completely consumed
                max_ammo_taken = math.ceil(self.life / consumption_rate)
                if weapon.ammo < weapon.max_ammo:
                    ammo_taken = min(max_ammo_taken, weapon.max_ammo - weapon.ammo)
                    resource_taken = ammo_taken * consumption_rate
                    weapon.ammo += ammo_taken
                    self.life -= resource_taken
