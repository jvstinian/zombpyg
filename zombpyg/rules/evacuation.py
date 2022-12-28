from zombpyg.rules.rules import Rules
from zombpyg.utils import calculate_distance

class EvacuationRules(Rules):
    """A kind of game where players must get together to be evacuated.

       Team wins when all alive players are at 2 or less distance from another
       alive player, and at least half of the team must survive.
    """
    def get_alive_players(self):
        """Get the alive players."""
        all_players = self.world.agents + self.world.players 
        return [
            player for player in all_players
            if player.life > 0
        ]

    def alive_players_together(self):
        """Are the alive players together (close to each other)?"""
        alive_players = self.get_alive_players()
        together = set()
        pending = [alive_players[0], ]

        while pending:
            player = pending.pop()
            together.add(player)

            neighbors = [
                other for other in alive_players 
                if calculate_distance(player.get_position(), other.get_position()) < 2*(player.r + other.r)
            ]

            for neighbor in neighbors:
                if neighbor not in together:
                    pending.append(neighbor)

        return len(together) == len(alive_players)

    def half_team_alive(self):
        """At least half of the original team alive?"""
        all_players = self.world.agents + self.world.players 
        alive_players = self.get_alive_players()
        return len(alive_players) >= len(all_players) / 2.0

    def game_ended(self):
        """Has the game ended?"""
        if self.half_team_alive():
            return self.alive_players_together()
        else:
            return True

    def game_won(self):
        """Was the game won?"""
        if self.half_team_alive():
            return True, u'players got together and were evacuated :)'
        else:
            return False, u'too few survivors to send a rescue helicopter :('
