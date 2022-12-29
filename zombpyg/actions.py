from abc import ABC, abstractmethod

class MoveableThing(ABC):
    @abstractmethod
    def move_forward(self):
        pass
    
    @abstractmethod
    def move_right(self):
        pass
    
    @abstractmethod
    def move_backward(self):
        pass
    
    @abstractmethod
    def move_left(self):
        pass

class RotatableThing(ABC):
    @abstractmethod
    def rotate(self, angle: float):
        pass

class AttackingThing(ABC):
    @abstractmethod
    def attack(self):
        pass

class HealingThing(ABC):
    @abstractmethod
    def heal_self(self):
        pass
    
    @abstractmethod
    def heal_player(self):
        pass

class ExecutableAction(ABC):
    @abstractmethod
    def execute_action(self) -> None:
        pass

class ForwardMoveAction(ExecutableAction):
    def __init__(self, thing: MoveableThing):
        super().__init__()
        self.thing = thing

    def execute_action(self):
        self.thing.move_forward()
        
class RightMoveAction(ExecutableAction):
    def __init__(self, thing: MoveableThing):
        super().__init__()
        self.thing = thing

    def execute_action(self):
        self.thing.move_right()
        
class BackwardMoveAction(ExecutableAction):
    def __init__(self, thing: MoveableThing):
        super().__init__()
        self.thing = thing

    def execute_action(self):
        self.thing.move_backward()
        
class LeftMoveAction(ExecutableAction):
    def __init__(self, thing: MoveableThing):
        super().__init__()
        self.thing = thing

    def execute_action(self):
        self.thing.move_left()
 
class RotateAction(ExecutableAction):
    def __init__(self, thing: RotatableThing, angle: float):
        super().__init__()
        self.thing = thing
        self.angle = angle

    def execute_action(self):
        self.thing.rotate(self.angle)
 
class AttackAction(ExecutableAction):
    def __init__(self, thing: AttackingThing):
        super().__init__()
        self.thing = thing

    def execute_action(self):
        self.thing.attack()
 
class HealSelfAction(ExecutableAction):
    def __init__(self, thing: HealingThing):
        super().__init__()
        self.thing = thing

    def execute_action(self):
        self.thing.heal_self()

class HealPlayerAction(ExecutableAction):
    def __init__(self, thing: HealingThing):
        super().__init__()
        self.thing = thing

    def execute_action(self):
        self.thing.heal_player()
