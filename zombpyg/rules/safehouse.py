from .rules import Rules


class SafeHouseRules(Rules):
    """A kind of game where players must get into a safe house.

       Team wins when all alive players are inside the safe house.
    """
    def __init__(self, world, objectives):
        super(SafeHouseRules, self).__init__(world)
        self.objectives = objectives

    def __player_at_objective__(self, player):
        return any([
            objective.contains(player.get_position()) for objective in self.objectives
        ])

    def alive_players_in_house(self):
        """Are the alive players in the safe house (objective locations)?"""
        all_players = self.world.agents + self.world.players
        in_house = [
            self.__player_at_objective__(player) for player in all_players
            if player.life > 0
        ]
        return all(in_house)

    def game_ended(self):
        """Has the game ended?"""
        if self.objectives is None:
            raise Exception('Safe house game requires objectives defined.')

        if self.players_alive():
            return self.alive_players_in_house()
        else:
            return True

    def game_won(self):
        """Was the game won?"""
        if self.players_alive():
            return True, u'everybody made it into the safehouse :)'
        else:
            return False, u'nobody made it into the safehouse :('
