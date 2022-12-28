from abc import ABC, abstractmethod

class Rules(object):
    def __init__(self, world):
        self.world = world

    def players_alive(self):
        """Are there any alive players?"""
        all_players = self.world.players + self.world.agents
        for player in all_players:
            if player.life > 0:
                return True
        return False

    @abstractmethod
    def game_ended(self) -> bool:
        pass

    def game_won(self) -> (bool, str):
        pass
