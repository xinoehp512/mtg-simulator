from action import Action
from activated_ability import Activated_Ability
from additional_cost import Kicker
from card import Artifact_Token, Creature_Token
from effects import Ability_Grant_Effect, PT_Effect
from enums import AbilityKeyword, AdditionalCostType, ArtifactType, CardType, Color, CounterType, EffectDuration, ManaCost, ManaType, ModeType, Step, TargetTypeBase, TargetTypeModifier
from event import Attack_Event, Permanent_Enter_Event, Permanent_Tapped_Event, Step_Begin_Event, Targeting_Event
from exceptions import IllegalActionException, UnpayableCostException
from keyword_ability import Keyword_Ability
from mana import Mana
from modes import Mode, ModeChoice, SingleMode
from replacement_effect import Replacement_Effect
from spell_ability import Spell_Ability
from target_type import TargetType
from triggered_ability import Triggered_Ability

flash = Keyword_Ability(AbilityKeyword.FLASH)
vigilance = Keyword_Ability(AbilityKeyword.VIGILANCE)
haste = Keyword_Ability(AbilityKeyword.HASTE)
trample = Keyword_Ability(AbilityKeyword.TRAMPLE)
none = Keyword_Ability(None)


def can_tap_self(game, _, object):
    return not (object.tapped or (object.is_creature and object.summoning_sick))


def can_sac(game, _, object):
    return object.is_alive


def tap_self(game, _, object):  # TODO: Check if creature and summoning sick.
    if object.tapped or (object.is_creature and object.summoning_sick):
        raise UnpayableCostException
    game.tap(object)
    return Permanent_Tapped_Event(object)


def tap_sac_pay_2(game, player, object):
    if object.tapped:
        raise UnpayableCostException
    game.player_activate_mana(player, [ManaCost.GENERIC]*2)
    game.player_pay_cost(player, [ManaCost.GENERIC]*2)
    game.tap(object)
    game.sacrifice(player, object)


def sac_pay_1(game, player, object):
    game.player_activate_mana(player, [ManaCost.GENERIC]*2)
    game.player_pay_cost(player, [ManaCost.GENERIC]*2)
    game.sacrifice(player, object)


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


def add_x_or_y_mana(color1, color2):
    def _(game, player, object, targets):
        color = player.agent.choose_one([color1, color2])
        return game.add_mana(player, [Mana(color, object)])
    return _


def gain_x(amount):
    def _(game, controller, source, event, modes, targets):
        game.player_gain_life(controller, amount)
    return _


food_ability = Activated_Ability("{T}, Sacrifice this artifact: You gain 3 life.",
                                 can_tap_self, tap_sac_pay_2, gain_x(3), SingleMode(None))
food = Artifact_Token("Food Token", None, [CardType.ARTIFACT, ArtifactType.FOOD], [food_ability], "")


def deal_3(game, controller, source, event, modes, targets):
    game.deal_damage(targets[0].object, 3)


def grow_3(game, controller, source, event, modes, targets):
    target = targets[0].object
    effect = PT_Effect(EffectDuration.EOT, lambda p: p == target, 3, 3)
    game.create_continuous_effect(effect)


def make_2_tokens(game, controller, source, event, modes, targets):
    token = Creature_Token("Elemental Token", None, [CardType.CREATURE], [], "", 1, 1, color_indicator=[Color.RED, Color.BLUE])
    game.create_token(controller, token.copy())
    game.create_token(controller, token.copy())


def exile_gravecard(game, controller, source, event, modes, targets):
    if targets == None:
        return
    target = targets[0].object
    game.exile_from_graveyard(target)


def put_2_counters_or_gain_4(game, controller, source, event, modes, targets):
    mode = modes[ModeType.MODES_CHOSEN][0]
    if mode == 0:
        target = targets[0].object
        game.put_counters_on(CounterType.P1P1, 2, target)
    if mode == 1:
        game.player_gain_life(controller, 4)


def put_counter(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.put_counters_on(CounterType.P1P1, 1, target)


def put_counter_self(game, controller, source, event, modes, targets):
    game.put_counters_on(CounterType.P1P1, 1, source)


def give_haste(game, controller, source, event, modes, targets):
    target = targets[0].object
    effect = Ability_Grant_Effect(EffectDuration.EOT, lambda p: p == target, [haste])
    game.create_continuous_effect(effect)


def destroy_creature_and_make_food(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.destroy(target)
    game.create_token(controller, food.copy())


def exile_until_leaves(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.exile_until_leaves(target, source)


def destroy_permanent(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.destroy(target)


def bounce_permanent(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.return_permanent_to_hand(target)


def pump_self_p1p0(game, controller, source, event, modes, targets):
    effect = PT_Effect(EffectDuration.EOT, lambda p: p == source, 1, 0)
    game.create_continuous_effect(effect)


def creature_bite(game, controller, source, event, modes, targets):
    biter = targets[0].object
    bitee = targets[1].object
    game.deal_damage(bitee, biter.power)


def opponents_discard(game, controller, source, event, modes, targets):
    opponents = game.get_opponents(controller)
    for opponent in opponents:
        game.player_discard_x(opponent, 1)


def deal_2_kicked_4(game, controller, source, event, modes, targets):
    target = targets[0].object
    was_kicked = AdditionalCostType.KICKED in modes[ModeType.COSTS_PAID]
    if was_kicked:
        game.deal_damage(target, 4)
    else:
        game.deal_damage(target, 2)


def tutor_land_or_fight(game, controller, source, event, modes, targets):
    mode = modes[ModeType.MODES_CHOSEN][0]
    if mode == 0:
        # Tutor
        game.player_tutor_to_hand(controller, lambda c: c.is_land and c.is_basic)
    if mode == 1:
        target1 = targets[0].object
        target2 = targets[1].object
        game.fight(target1, target2)


def tutor_land_top_opt(game, controller, source, event, modes, targets):
    if controller.agent.choose_yes_or_no("Search for a basic land?"):
        game.player_tutor_to_top(controller, lambda c: c.is_land and c.is_basic)


def trigger_on_etb(game, event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent == object


def trigger_on_3_creatures_attack(game, event, object):
    return isinstance(event, Attack_Event) and event.num_attacking >= 3


def trigger_on_controlled_creature_enter(game, event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent != object and event.permanent.is_creature and event.permanent.controller == object.controller


def trigger_on_opponent_target(game, event, object):
    return event.contains(Targeting_Event) and object in event.targets and event.stack_object.controller in game.get_opponents(object.controller)


def morbid_end_step(game, event, object):
    return isinstance(event, Step_Begin_Event) and event.step == Step.END and event.player == object.controller and game.creature_died_this_turn


def replace_enters(game, event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent == object


def enters_tapped(event):
    new_event = event.copy()
    new_event.permanent.tapped = True
    return new_event


damageable_target = TargetType([(TargetTypeBase.DAMAGEABLE,)])
creature_target = TargetType([(TargetTypeBase.CREATURE,)])
opt_gravecard_target = TargetType([(TargetTypeBase.GRAVECARD,)], True)
creature_you_control_target = TargetType([(TargetTypeBase.CREATURE, TargetTypeModifier.YOU_CONTROL)])
creature_dont_control_target = TargetType([(TargetTypeBase.CREATURE, TargetTypeModifier.DONT_CONTROL)])
creature_opp_control_target = TargetType([(TargetTypeBase.CREATURE, TargetTypeModifier.OPP_CONTROL)])
nl_permanent_opp_control_target = TargetType([(TargetTypeBase.NL_PERMANENT, TargetTypeModifier.OPP_CONTROL)])
creature_planeswalker_dont_control_target = TargetType(
    [(TargetTypeBase.CREATURE, TargetTypeModifier.DONT_CONTROL), (TargetTypeBase.PLANESWALKER, TargetTypeModifier.DONT_CONTROL)])
broken_wings_target = TargetType([(TargetTypeBase.ARTIFACT,), (TargetTypeBase.ENCHANTMENT,),
                                 (TargetTypeBase.CREATURE, TargetTypeModifier.HAS_FLYING)])
artifact_enchanment_target = TargetType([(TargetTypeBase.ARTIFACT,), (TargetTypeBase.ENCHANTMENT,)])

plains_ability = Activated_Ability("{T}: Add {W}", can_tap_self, tap_self,
                                   add_one_white_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.WHITE])
island_ability = Activated_Ability("{T}: Add {U}", can_tap_self, tap_self,
                                   add_one_blue_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.BLUE])
swamp_ability = Activated_Ability("{T}: Add {B}", can_tap_self, tap_self,
                                  add_one_black_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.BLACK])
mountain_ability = Activated_Ability("{T}: Add {R}", can_tap_self, tap_self,
                                     add_one_red_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.RED])
forest_ability = Activated_Ability("{T}: Add {G}", can_tap_self, tap_self,
                                   add_one_green_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.GREEN])


# lightning_ability = Spell_Ability("Deal 3 damage to any target.", deal_3, [damageable_target])
# giant_growth_ability = Spell_Ability("Target creature gets +3/+3 until end of turn.", grow_3, [creature_target])
# reinforcements_ability = Spell_Ability("Create 2 1/1 red and blue Elementals.", make_2_tokens, None)


def kicker(x):
    return Kicker(x)


def ward(x):
    def rhystic_counter(game, controller, source, event, modes, targets):
        ability_stack_object = event.stack_object
        game.player_activate_mana(ability_stack_object.controller, x)
        if game.player_pay_cost(ability_stack_object.controller, x):
            return
        game.counter_stack_object(ability_stack_object)
    return Triggered_Ability(trigger_on_opponent_target, SingleMode(None), rhystic_counter)


ambush_wolf_etb = Triggered_Ability(trigger_on_etb, SingleMode([opt_gravecard_target]), exile_gravecard)
apothecary_stomper_etb = Triggered_Ability(trigger_on_etb, ModeChoice(
    1, [Mode([creature_you_control_target], "Put two +1/+1 counters on target creature you control", 0), Mode(None, "You gain 4 life", 1)]), put_2_counters_or_gain_4)
armasaur_guide_attack = Triggered_Ability(trigger_on_3_creatures_attack, SingleMode([creature_you_control_target]), put_counter)
banishing_light_ability = Triggered_Ability(trigger_on_etb, SingleMode([nl_permanent_opp_control_target]), exile_until_leaves)
beastkin_ranger_pump = Triggered_Ability(trigger_on_controlled_creature_enter, SingleMode(None), pump_self_p1p0)
bigfin_bouncer_etb = Triggered_Ability(trigger_on_etb, SingleMode([creature_opp_control_target]), bounce_permanent)
gain_1_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), gain_x(1))
burglar_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), opponents_discard)
cackling_prowler_morbid = Triggered_Ability(morbid_end_step, SingleMode(None), put_counter_self)
campus_guide_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), tutor_land_top_opt)

axgard_cavalry_tap = Activated_Ability("{T}: Target creature gains haste until end of turn.",
                                       can_tap_self, tap_self, give_haste, SingleMode([creature_target]))
cathar_sac = Activated_Ability("{1}, Sacrifice this creature: Destroy target artifact or enchantment.",
                               can_sac, sac_pay_1, destroy_permanent, SingleMode([artifact_enchanment_target]))

enters_tapped_replacement = Replacement_Effect(replace_enters, enters_tapped)
rakdos_land_ability = Activated_Ability("{T}: Add {B} or {R}", can_tap_self, tap_self, add_x_or_y_mana(ManaType.BLACK, ManaType.RED), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.BLACK, ManaType.RED])
selesnya_land_ability = Activated_Ability("{T}: Add {G} or {W}", can_tap_self, tap_self, add_x_or_y_mana(ManaType.GREEN, ManaType.WHITE), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.GREEN, ManaType.WHITE])

bake_into_a_pie_ability = Spell_Ability(destroy_creature_and_make_food, SingleMode([creature_target]))
destroy_ability = Spell_Ability(destroy_permanent, SingleMode([nl_permanent_opp_control_target]))
bite_down_ability = Spell_Ability(creature_bite, SingleMode([creature_you_control_target, creature_planeswalker_dont_control_target]))
broken_wings_ability = Spell_Ability(destroy_permanent, SingleMode([broken_wings_target]))
burst_lightning_ability = Spell_Ability(deal_2_kicked_4, SingleMode([damageable_target]))
bushwhack_ability = Spell_Ability(tutor_land_or_fight, ModeChoice(
    1, [Mode(None, "Search for a basic land", 0), Mode([creature_you_control_target, creature_dont_control_target], "Target creature you control fights target creature you don't control.", 1)]))
