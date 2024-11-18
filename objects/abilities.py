from action import Action
from activated_ability import Activated_Ability
from card import Creature_Token
from effects import Ability_Grant_Effect, PT_Effect
from enums import AbilityKeyword, CardType, Color, CounterType, EffectDuration, ManaType, TargetType
from event import Attack_Event, Permanent_Enter_Event, Permanent_Tapped_Event
from exceptions import IllegalActionException, UnpayableCostException
from keyword_ability import Keyword_Ability
from mana import Mana
from modes import Mode, ModeChoice, SingleMode
from spell_ability import Spell_Ability
from triggered_ability import Triggered_Ability

flash = Keyword_Ability(AbilityKeyword.FLASH)
vigilance = Keyword_Ability(AbilityKeyword.VIGILANCE)
haste = Keyword_Ability(AbilityKeyword.HASTE)


def can_be_tapped(game, _, object):
    return not object.tapped


def tap_self(game, _, object):
    if object.tapped:
        raise UnpayableCostException
    game.tap(object)
    return Permanent_Tapped_Event(object)


def add_one_white_mana(game, player, object, _):
    return game.add_mana(player, [Mana(ManaType.WHITE, object)])


def add_one_blue_mana(game, player, object, _):
    return game.add_mana(player, [Mana(ManaType.BLUE, object)])


def add_one_black_mana(game, player, object, _):
    return game.add_mana(player, [Mana(ManaType.BLACK, object)])


def add_one_red_mana(game, player, object, _):
    return game.add_mana(player, [Mana(ManaType.RED, object)])


def add_one_green_mana(game, player, object, _):
    return game.add_mana(player, [Mana(ManaType.GREEN, object)])


def deal_3(game, controller, modes, targets):
    game.deal_damage(targets[0].object, 3)


def grow_3(game, controller, modes, targets):
    target = targets[0].object
    effect = PT_Effect(EffectDuration.EOT, lambda p: p == target, 3, 3)
    game.create_continuous_effect(effect)


def make_2_tokens(game, controller, modes, targets):
    token = Creature_Token("Elemental Token", None, [CardType.CREATURE], [], "", 1, 1, color_indicator=[Color.RED, Color.BLUE])
    game.create_token(controller, token.copy())
    game.create_token(controller, token.copy())


def exile_gravecard(game, controller, modes, targets):
    if targets == None:
        return
    target = targets[0].object
    game.exile_from_graveyard(target)


def put_2_counters_or_gain_4(game, controller, modes, targets):
    mode = modes[0]
    if mode == 0:
        target = targets[0].object
        game.put_counters_on(CounterType.P1P1, 2, target)
    if mode == 1:
        game.player_gain_life(controller, 4)


def put_counter(game, controller, modes, targets):
    target = targets[0].object
    game.put_counters_on(CounterType.P1P1, 1, target)


def give_haste(game, controller, modes, targets):
    target = targets[0].object
    effect = Ability_Grant_Effect(EffectDuration.EOT, lambda p: p == target, [haste])
    game.create_continuous_effect(effect)


def trigger_on_etb(event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent == object


def trigger_on_3_creatures_attack(event, object):
    return isinstance(event, Attack_Event) and event.num_attacking >= 3


plains_ability = Activated_Ability("{T}: Add {W}", can_be_tapped, tap_self,
                                   add_one_white_mana, SingleMode(None), is_mana_ability=True, mana_produced=ManaType.WHITE)
island_ability = Activated_Ability("{T}: Add {U}", can_be_tapped, tap_self,
                                   add_one_blue_mana, SingleMode(None), is_mana_ability=True, mana_produced=ManaType.BLUE)
swamp_ability = Activated_Ability("{T}: Add {B}", can_be_tapped, tap_self,
                                  add_one_black_mana, SingleMode(None), is_mana_ability=True, mana_produced=ManaType.BLACK)
mountain_ability = Activated_Ability("{T}: Add {R}", can_be_tapped, tap_self,
                                     add_one_red_mana, SingleMode(None), is_mana_ability=True, mana_produced=ManaType.RED)
forest_ability = Activated_Ability("{T}: Add {G}", can_be_tapped, tap_self,
                                   add_one_green_mana, SingleMode(None), is_mana_ability=True, mana_produced=ManaType.GREEN)


lightning_ability = Spell_Ability("Deal 3 damage to any target.", deal_3, [TargetType.DAMAGEABLE])
giant_growth_ability = Spell_Ability("Target creature gets +3/+3 until end of turn.", grow_3, [TargetType.CREATURE])
reinforcements_ability = Spell_Ability("Create 2 1/1 red and blue Elementals.", make_2_tokens, None)


ambush_wolf_etb = Triggered_Ability(trigger_on_etb, SingleMode([TargetType.OPT_GRAVECARD]), exile_gravecard)
apothecary_stomper_etb = Triggered_Ability(trigger_on_etb, ModeChoice(
    1, [Mode([TargetType.CREATURE_YOU_CONTROL], "Put two +1/+1 counters on target creature you control", 0), Mode([], "You gain 4 life", 1)]), put_2_counters_or_gain_4)
armasaur_guide_attack = Triggered_Ability(trigger_on_3_creatures_attack, SingleMode([TargetType.CREATURE_YOU_CONTROL]), put_counter)
axgard_cavalry_tap = Activated_Ability("{T}: Target creature gains haste until end of turn.",
                                       can_be_tapped, tap_self, give_haste, SingleMode([TargetType.CREATURE]))
