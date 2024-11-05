from action import Action
from activated_ability import Activated_Ability
from card import Creature_Token
from effects import PT_Effect
from enums import AbilityKeyword, CardType, Color, EffectDuration, ManaType, TargetType
from exceptions import IllegalActionException
from keyword_ability import Keyword_Ability
from mana import Mana
from spell_ability import Spell_Ability


def can_be_tapped(game, _, object):
    return not object.tapped


def tap_self(game, _, object):
    if object.tapped:
        return False
    game.tap(object)
    return True


def add_one_white_mana(game, player, object, _):
    game.add_mana(player, Mana(ManaType.WHITE, object))


def add_one_blue_mana(game, player, object, _):
    game.add_mana(player, Mana(ManaType.BLUE, object))


def add_one_black_mana(game, player, object, _):
    game.add_mana(player, Mana(ManaType.BLACK, object))


def add_one_red_mana(game, player, object, _):
    game.add_mana(player, Mana(ManaType.RED, object))


def add_one_green_mana(game, player, object, _):
    game.add_mana(player, Mana(ManaType.GREEN, object))


def basic_land_reverse(game, player, object):
    legal_mana = [mana for mana in player.mana_pool.mana if mana.source == object]
    if len(legal_mana) == 0:
        raise IllegalActionException("Illegal Action")
    player.mana_pool.remove([legal_mana[0]])
    object.tapped = False


def deal_3(game, controller, targets):
    game.deal_damage(targets[0].object, 3)


def grow_3(game, controller, targets):
    target = targets[0].object
    effect = PT_Effect(EffectDuration.EOT, lambda p: p == target, 3, 3)
    game.create_continuous_effect(effect)


def make_2_tokens(game, controller, targets):
    token = Creature_Token("Elemental Token", None, [Color.RED, Color.BLUE], [CardType.CREATURE], [], "", 1, 1)
    game.create_token(controller, token.copy())
    game.create_token(controller, token.copy())


plains_ability = Activated_Ability("{T}: Add {W}", can_be_tapped, tap_self,
                                   add_one_white_mana, is_mana_ability=True, mana_produced=ManaType.WHITE, reverse_function=basic_land_reverse)
island_ability = Activated_Ability("{T}: Add {U}", can_be_tapped, tap_self,
                                   add_one_blue_mana, is_mana_ability=True, mana_produced=ManaType.BLUE, reverse_function=basic_land_reverse)
swamp_ability = Activated_Ability("{T}: Add {B}", can_be_tapped, tap_self,
                                  add_one_black_mana, is_mana_ability=True, mana_produced=ManaType.BLACK, reverse_function=basic_land_reverse)
mountain_ability = Activated_Ability("{T}: Add {R}", can_be_tapped, tap_self,
                                     add_one_red_mana, is_mana_ability=True, mana_produced=ManaType.RED, reverse_function=basic_land_reverse)
forest_ability = Activated_Ability("{T}: Add {G}", can_be_tapped, tap_self,
                                   add_one_green_mana, is_mana_ability=True, mana_produced=ManaType.GREEN, reverse_function=basic_land_reverse)


lightning_ability = Spell_Ability("Deal 3 damage to any target.", deal_3, [TargetType.DAMAGEABLE])
giant_growth_ability = Spell_Ability("Target creature gets +3/+3 until end of turn.", grow_3, [TargetType.CREATURE])
reinforcements_ability = Spell_Ability("Create 2 1/1 red and blue Elementals.", make_2_tokens, None)

flash = Keyword_Ability(AbilityKeyword.FLASH)
