from .rules import Rules

class SurvivalRules(Rules):
    """Rules to decide when a game ends, and when it's won."""
    def game_ended(self):
        """Has the game ended?"""
        return not self.players_alive()

    def game_won(self):
        """Was the game won?"""
        if self.players_alive():
            # never should happen, but illustrative
            return True, u'you won a game that never ends (?!)'
        else:
            return False, u'everybody is dead :('