from ability_stack_object import Ability_Stack_Object
from enums import AbilityKeyword, TargetTypeBase, TargetTypeModifier
from graveyard_object import Graveyard_Object
from permanent import Permanent
from player import Player
from target import Target


class TargetType:
    def __init__(self, target_options, is_optional=False):
        self.target_options = target_options
        self.is_optional = is_optional

    @property
    def name(self):
        target_names = []
        for target_option in self.target_options:
            target_name = "target"
            for target_modifier in target_option:
                if target_modifier == TargetTypeBase.DAMAGEABLE:
                    continue
                if target_modifier == TargetTypeBase.CREATURE:
                    target_name += " creature"
                if target_modifier == TargetTypeBase.ARTIFACT:
                    target_name += " artifact"
                if target_modifier == TargetTypeBase.ENCHANTMENT:
                    target_name += " enchantment"
                if target_modifier == TargetTypeBase.PLANESWALKER:
                    target_name += " planeswalker"
                if target_modifier == TargetTypeBase.NL_PERMANENT:
                    target_name += " nonland permanent"
                if target_modifier == TargetTypeBase.GRAVECARD:
                    target_name += " card from a graveyard"
                if target_modifier == TargetTypeModifier.YOU_CONTROL:
                    target_name += " you control"
                if target_modifier == TargetTypeModifier.OPP_CONTROL:
                    target_name += " an opponent controls"
                if target_modifier == TargetTypeModifier.DONT_CONTROL:  # This is different from above only in a team game.
                    target_name += " you don't control"
                if target_modifier == TargetTypeModifier.HAS_FLYING:
                    target_name += " with flying"
            target_names.append(target_name)
        if len(target_names) == 1:
            return target_names[0]
        if len(target_names) == 2:
            return " or ".join(target_names)
        return ", ".join(target_names[:-1])+", or " + target_names[-1]

    def get_targets(self, game, player):
        opponent = game.get_opponents(player)[0]
        objects = []
        base_targets = [target_modifier for target_option in self.target_options for target_modifier in target_option if isinstance(
            target_modifier, TargetTypeBase)]
        if TargetTypeBase.ARTIFACT in base_targets or TargetTypeBase.ENCHANTMENT in base_targets or TargetTypeBase.CREATURE or TargetTypeBase.PLANESWALKER or TargetTypeBase.NL_PERMANENT or TargetTypeBase.DAMAGEABLE in base_targets:
            objects.extend(game.battlefield.objects)
        if TargetTypeBase.DAMAGEABLE in base_targets:
            objects.extend(game.players)
        if TargetTypeBase.GRAVECARD in base_targets:
            for player in game.players:
                objects.extend(player.graveyard.objects)

        def applicability_function(t):
            for target_option in self.target_options:
                fulfilled = True
                for target_modifier in target_option:
                    if target_modifier == TargetTypeBase.DAMAGEABLE:
                        fulfilled = fulfilled and (isinstance(t, Player) or (isinstance(t, Permanent) and t.is_damageable))
                    if target_modifier == TargetTypeBase.CREATURE:
                        fulfilled = fulfilled and (isinstance(t, Permanent) and t.is_creature)
                    if target_modifier == TargetTypeBase.ARTIFACT:
                        fulfilled = fulfilled and (isinstance(t, Permanent) and t.is_artifact)
                    if target_modifier == TargetTypeBase.ENCHANTMENT:
                        fulfilled = fulfilled and (isinstance(t, Permanent) and t.is_enchantment)
                    if target_modifier == TargetTypeBase.PLANESWALKER:
                        fulfilled = fulfilled and (isinstance(t, Permanent) and t.is_planeswalker)
                    if target_modifier == TargetTypeBase.NL_PERMANENT:
                        fulfilled = fulfilled and (isinstance(t, Permanent) and not t.is_land)
                    if target_modifier == TargetTypeBase.GRAVECARD:
                        fulfilled = fulfilled and (isinstance(t, Graveyard_Object))
                    if target_modifier == TargetTypeModifier.YOU_CONTROL:
                        fulfilled = fulfilled and not isinstance(t, Player) and t.controller == player
                    if target_modifier == TargetTypeModifier.OPP_CONTROL:
                        fulfilled = fulfilled and t.controller == opponent
                    if target_modifier == TargetTypeModifier.DONT_CONTROL:  # This is different from above only in a team game.
                        fulfilled = fulfilled and t.controller != player
                    if target_modifier == TargetTypeModifier.HAS_FLYING:
                        fulfilled = fulfilled and AbilityKeyword.FLYING in t.keywords
                if fulfilled:
                    return True
            return False

        targets = [Target(applicability_function, target) for target in objects if applicability_function(target)]
        if self.is_optional:
            targets.append(None)
        return targets
