import numpy
import random

from zombpyg.core.things import Weapon
from zombpyg.utils.geometry import rotate_vector, get_angle_and_distance_to_point
from zombpyg.core.bullet import Bullet


class MeleeWeapon(Weapon):
    def __init__(self, name, damage_range, max_range, max_angle):
        super(MeleeWeapon, self).__init__(name, damage_range, max_range)
        self.max_angle = max_angle
        self.is_firearm = False
    
    def find_target(self, attacker):
        potential_targets = [
            agent for agent in attacker.world.agents if agent.life > 0
        ] + [
            player for player in attacker.world.players if player.life > 0
        ] + [
            zombie for zombie in attacker.world.zombies if zombie.life > 0
        ]
        min_distance = 1.01 * self.max_range # Set larger than max distance
        target_fighter = None
        
        for fighter in potential_targets:
            if fighter == attacker:
                continue

            angle, distance, _ = get_angle_and_distance_to_point(attacker.get_position(), attacker.orientation, fighter.get_position())
            if distance >= self.max_range:
                continue
            
            rectified_angle = numpy.rad2deg(numpy.arctan2(fighter.r, distance))
            if angle >= -self.max_angle-rectified_angle and angle <= self.max_angle+rectified_angle:
                if distance < min_distance:
                    min_distance = min(min_distance, distance)
                    target_fighter = fighter
        
        return target_fighter
    
    def use(self, attacker):
        target = self.find_target(attacker)
        attacker.attack_count += 1
        if target is not None:
            damage = random.randint(*self.damage_range)
            target.life -= damage
    
    def ammo_resource_consumption_rate(self):
        return None

class ZombieClaws(MeleeWeapon):
    def __init__(self):
        super(ZombieClaws, self).__init__(
            'ZombieClaws', (1, 2), 3*10, 45
        )
    
    def get_weapon_id(self) -> int:
        return 1

class Knife(MeleeWeapon):
    def __init__(self):
        super(Knife, self).__init__(
            'Knife', (40, 70), 3*10, 30
        )
    
    def get_weapon_id(self) -> int:
        return 16

class Axe(MeleeWeapon):
    def __init__(self):
        super(Axe, self).__init__(
            'Axe', (75, 100), 4*10, 45
        )
    
    def get_weapon_id(self) -> int:
        return 17

class Firearm(Weapon):
    TIME_IN_AIR = 0.5

    def __init__(self, name, damage_range, max_total_damage, bullet_velocity, max_ammo, ammo):
        super(Firearm, self).__init__(name, damage_range, Firearm.TIME_IN_AIR*bullet_velocity)
        self.is_firearm = True
        self.max_total_damage = max_total_damage
        self.bullet_velocity = bullet_velocity
        self.max_ammo = max_ammo
        self.ammo = ammo
    
    def generate_bullets(self, attacker):
        # Implement in derived classes
        pass
    
    def generate_bullet_straight_ahead(self, attacker):
        x, y = attacker.get_position()
        radius = attacker.r
        orientation = attacker.orientation
        orientation_vector = (
            numpy.sin(numpy.deg2rad(orientation)),
            -numpy.cos(numpy.deg2rad(orientation))
        )
        bullet_start = (
            x + 1.01*radius*orientation_vector[0],
            y + 1.01*radius*orientation_vector[1]
        )
        return [
            Bullet(bullet_start, orientation_vector, self.damage_range, self.max_total_damage, self.bullet_velocity, attacker, attacker.world)
        ]
    
    def generate_bullets_at_angles(self, attacker, angles):
        bullets = []
        anglesrad = numpy.deg2rad(angles)

        x, y = attacker.get_position()
        radius = attacker.r
        orientation = attacker.orientation
        orientation_vector = (
            numpy.sin(numpy.deg2rad(orientation)),
            -numpy.cos(numpy.deg2rad(orientation))
        )
        bullet_start = (
            x + 1.01*radius*orientation_vector[0],
            y + 1.01*radius*orientation_vector[1]
        )
        for angle in anglesrad:
            direction_vector = rotate_vector(orientation_vector, angle)
            bullets.append(
                Bullet(bullet_start, direction_vector, self.damage_range, self.max_total_damage, self.bullet_velocity, attacker, attacker.world)
            )
        return bullets
    
    def use(self, attacker):
        if self.ammo > 0:
            bullets = self.generate_bullets(attacker)
            self.ammo -= 1
            attacker.attack_count += 1
            # Take first step with bullet
            for bullet in bullets:
                attacker.world.decorations.append(bullet.get_path_decoration())
                bullet.next_step()
                attacker.world.add_bullet(bullet)

    def ammo_resource_consumption_rate(self):
        return 1.0/self.max_ammo
    
    def reset(self):
        self.ammo = self.max_ammo

class Gun(Firearm):
    def __init__(self):
        super(Gun, self).__init__(
            'Gun', (30, 70), 100, 250*50,
            150, 150
        )
    
    def generate_bullets(self, attacker):
        return self.generate_bullet_straight_ahead(attacker)
    
    def get_weapon_id(self) -> int:
        return 32

class Rifle(Firearm):
    def __init__(self):
        super(Rifle, self).__init__(
            'Rifle', (80, 200), 300, 700*50,
            270, 270
        )
    
    def generate_bullets(self, attacker):
        return self.generate_bullet_straight_ahead(attacker)

    def get_weapon_id(self) -> int:
        return 33

class Shotgun(Firearm):
    def __init__(self):
        super(Shotgun, self).__init__(
            'Shotgun', (60, 120), 150, 365*50,
            90, 90
        )
    
    def generate_bullets(self, attacker):
        return self.generate_bullets_at_angles(attacker, [-1.0, 0.0, 1.0])

    def get_weapon_id(self) -> int:
        return 34

class WeaponFactory(object):
    @staticmethod
    def create_weapon(weapon_id):
        if weapon_id == "rifle":
            return Rifle()
        elif weapon_id == "shotgun":
            return Shotgun()
        elif weapon_id == "gun":
            return Gun()
        elif weapon_id == "axe":
            return Axe()
        elif weapon_id == "knife":
            return Knife()
        elif weapon_id == "random":
            return random.choice([Knife(), Axe(), Gun(), Rifle(), Shotgun()])
        else:
            return None
