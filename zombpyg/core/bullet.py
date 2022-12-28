import numpy
import pygame
from operator import itemgetter

from zombpyg.utils.geometry import calculate_parameter_of_point_on_segment, get_nearest_point_and_distance_to_path

# TODO: Add to utils
BulletRed = (255, 0, 0, 128)


class Bullet(object):
    color = BulletRed
    width = 6

    def __init__(self, start, direction, damage_range, max_total_damage, speed, agent, world):
        self.current_location = start
        self.direction = direction
        self.damage_range = damage_range
        self.max_total_damage = max_total_damage
        self.speed = speed
        self.time_remaining = 0.5
        self.active = True
        self.agent = agent
        self.world = world
        self.first_hit_occurred = False

    def collide_with_walls(self, start, end):
        closest_wall_point = None
        min_l = 1.01 # Set to > 1 in case end is on a wall
        for wall in self.world.walls:
            point = wall.collide(start, end)
            if point is not None:
                l = calculate_parameter_of_point_on_segment(start, end, point)
                if l < min_l:
                    closest_wall_point = point
                    min_l = min(min_l, l)
        return closest_wall_point

    def next_step(self):
        dt = self.world.step_time_delta
        end = (
            self.current_location[0] + dt * self.speed * self.direction[0],
            self.current_location[1] + dt * self.speed * self.direction[1]
        )
        hits_wall = False
        wall_point = self.collide_with_walls(self.current_location, end)
        if wall_point is not None:
            end = wall_point
            hits_wall = True

        potential_targets = [
            (agent, 'agent') for agent in self.world.agents if agent.life > 0
        ] + [
            (player, 'player') for player in self.world.players if player.life > 0
        ] + [
            (zombie, 'zombie') for zombie in self.world.zombies if zombie.life > 0
        ]
        potential_hits = []
        for fighter, fighter_type in potential_targets:
            near_pt, fighter_dist, _ = get_nearest_point_and_distance_to_path(self.current_location, end, fighter.get_position())
            if fighter_dist < fighter.r:
                ell = calculate_parameter_of_point_on_segment(self.current_location, end, near_pt)
                potential_hits.append(
                    (fighter, fighter_type, fighter_dist, ell)
                )
        potential_hits = sorted(potential_hits, key=itemgetter(3), reverse=False)
        for fighter, fighter_type, fighter_dist, ell in potential_hits:
            if fighter == self.agent:
                # Shouldn't happen, but just in case
                continue
            damage = 0
            if fighter_dist < fighter.r/2:
                damage = 100.0
            elif fighter_dist < fighter.r:
                damage = numpy.random.randint(*self.damage_range)
            fighter.life -= damage
            self.max_total_damage -= damage
            if (fighter_type == "zombie") and not self.first_hit_occurred:
                self.first_hit_occurred = True
                self.agent.attack_hits += 1

            if fighter.life <= 0:
                if fighter_type == "zombie":
                    self.agent.zombies_killed += 1
                elif (fighter_type == "player") or (fighter_type == "agent"):
                    print(f"Fratricide: {self.agent.name} killed {fighter.name}")
                    self.agent.fratricide += 1
            elif (fighter_type == "player") or (fighter_type == "agent"):
                print(f"Friendly fire incident: {self.agent.name} hit {fighter.name}")
                self.agent.friendly_fire += 1

            if self.max_total_damage <= 0:
                break

        # Update state
        self.current_location = end
        self.time_remaining -= dt
        if (
            hits_wall or (self.time_remaining <= 0) or
            (self.max_total_damage <= 0) or
            (self.current_location[0] < 0) or (self.current_location[0] >= self.world.w) or
            (self.current_location[1] < 0) or (self.current_location[1] >= self.world.h)
        ):
            self.active = False

    def get_path_decoration(self):
        dt = self.world.step_time_delta
        display_start = (int(self.current_location[0]), int(self.current_location[1]))
        display_end = (
            int(self.current_location[0] + dt * self.speed * self.direction[0]),
            int(self.current_location[1] + dt * self.speed * self.direction[1])
        )
        return BulletDecoration(display_start, display_end, 1.5*dt)

    def draw(self, game):
        dt = self.world.step_time_delta # 1.0 / game.fps
        display_start = (int(self.current_location[0]), int(self.current_location[1]))
        display_end = (
            int(self.current_location[0] + dt * self.speed * self.direction[0]),
            int(self.current_location[1] + dt * self.speed * self.direction[1])
        )
        pygame.draw.line(game.DISPLAYSURF, Bullet.color, display_start, display_end, Bullet.width)

class BulletDecoration(object):
    color = BulletRed
    width = 6

    def __init__(self, start, end, display_duration):
        self.start = start
        self.end = end
        self.life = display_duration

    def decrement_life(self, amount):
        self.life -= amount

    def draw(self, game):
        pygame.draw.line(game.DISPLAYSURF, Bullet.color, self.start, self.end, BulletDecoration.width)