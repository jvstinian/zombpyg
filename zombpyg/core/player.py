from zombpyg.core.things import FightingThing, DeadBody


class Player(FightingThing):
    MAX_LIFE = 100

    def __init__(
        self, x, y, radius,
        name, color, weapon=None
    ):
        if weapon is None:
            weapon = random.choice([Gun, Shotgun, Rifle, Knife, Axe])()

        dead_decoration = DeadBody(radius, f"dead player {name}", Color.BRONZE)

        super(Player, self).__init__(
            x, y, radius,
            name, color, Player.MAX_LIFE, weapon, 
            dead_decoration
        )
