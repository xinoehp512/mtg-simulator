from ability_stack_object import Ability_Stack_Object
from enums import AbilityKeyword, ObjectType
from graveyard_object import Graveyard_Object
from permanent import Permanent
from player import Player
from target import Target


class TargetWord:
    def __init__(self, object_types, req_function, name, number=1, total_req_function=None, is_optional=False):
        self.number = number
        self.object_types = object_types
        self.req_function = req_function
        self.name = name
        self.total_req_function = total_req_function
        self.is_optional = is_optional

    def get_targets(self, game, player, source):
        opponent = game.get_opponents(player)[0]
        objects = []
        if ObjectType.PERMANENT in self.object_types:
            objects.extend(game.battlefield.objects)
        if ObjectType.PLAYER in self.object_types:
            objects.extend(game.players)
        if ObjectType.GRAVE_CARD in self.object_types:
            for player_ in game.players:
                objects.extend(player_.graveyard.objects)
        if ObjectType.STACK_OBJECT in self.object_types:
            objects.extend(game.stack.objects)

        targets = [Target(self.req_function, target) for target in objects if self.req_function(game, target, player, source)]
        if self.is_optional:
            targets.append(None)
        return targets
