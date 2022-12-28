from abc import ABC, abstractmethod
from .survival import SurvivalRules
from .evacuation import EvacuationRules
from .extermination import ExterminationRules
from .safehouse import SafeHouseRules


class RulesFactory(object):
    @staticmethod
    def get_default(world):
        return SurvivalRules(world)
    
    @staticmethod
    def get_rules(rules_id, world, objectives):
        if rules_id == "survival":
            return SurvivalRules(world)
        elif rules_id == "safehouse":
            return SafeHouseRules(world, objectives)
        elif rules_id == "extermination":
            return ExterminationRules(world)
        elif rules_id == "evacuation":
            return EvacuationRules(world)
        else:
            return RulesFactory.get_default(world)

