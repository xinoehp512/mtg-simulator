from ability_stack_object import Ability_Stack_Object
from action import Action
from activated_ability import Activated_Ability
from cost import Additional_Cost, Alternative_Cost, Discard_Cost, Mana_Cost, Sacrifice_Cost, Tap_Cost, Total_Cost
from card import Artifact_Token, Creature_Token
from cost_modification import Cost_Modification
from effects import Ability_Grant_Effect, Block_Restriction_Effect, Control_Effect, Cost_Modification_Effect, PT_Effect, Prevention_Effect
from enums import AbilityKeyword, ActivationRestrictionType, CostType, ArtifactType, CardType, CastingInformationType, Color, CounterType, CreatureType, EffectDuration, ManaCost, ManaType, ModeType, ObjectType, Step, ZoneType
from event import Attack_Event, Card_Draw_Event, Damage_Event, Gravecard_Exiled_Event, Lifegain_Event, Permanent_Died_Event, Permanent_Enter_Event, Permanent_Tapped_Event, Spellcast_Event, Stack_Died_Event, Stack_Exiled_Event, Step_Begin_Event, Targeting_Event
from exceptions import IllegalActionException, UnpayableCostException
from keyword_ability import Keyword_Ability
from mana import Mana
from modes import Mode, ModeChoice, SingleMode
from permanent import Permanent
from player import Player
from replacement_effect import Replacement_Effect
from spell_ability import Spell_Ability
from static_ability import Static_Ability
from target_word import TargetWord
from triggered_ability import Triggered_Ability

flash = Keyword_Ability(AbilityKeyword.FLASH)
vigilance = Keyword_Ability(AbilityKeyword.VIGILANCE)
haste = Keyword_Ability(AbilityKeyword.HASTE)
trample = Keyword_Ability(AbilityKeyword.TRAMPLE)
menace = Keyword_Ability(AbilityKeyword.MENACE)
flying = Keyword_Ability(AbilityKeyword.FLYING)
reach = Keyword_Ability(AbilityKeyword.REACH)
lifelink = Keyword_Ability(AbilityKeyword.LIFELINK)
defender = Keyword_Ability(AbilityKeyword.DEFENDER)
deathtouch = Keyword_Ability(AbilityKeyword.DEATHTOUCH)
first_strike = Keyword_Ability(AbilityKeyword.FIRST_STRIKE)
double_strike = Keyword_Ability(AbilityKeyword.DOUBLE_STRIKE)

none = Keyword_Ability(None)


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


def add_any_color_mana(game, player, object, targets):
    color = player.agent.choose_one([ManaType.WHITE, ManaType.BLUE, ManaType.BLACK, ManaType.RED, ManaType.GREEN])
    return game.add_mana(player, [Mana(color, object)])


def gain_x(amount):
    def _(game, controller, source, event, modes, targets):
        game.player_gain_life(controller, amount)
    return _


tap_self = Tap_Cost(lambda p, o: p == o)
sac_self = Sacrifice_Cost(lambda p, o: p == o)
sac_other_creature = Sacrifice_Cost(lambda p, o: p != o and p.is_creature)

food_ability = Activated_Ability("{T}, Sacrifice this artifact: You gain 3 life.",
                                 Total_Cost([Mana_Cost.from_string("2"), tap_self, sac_self]), gain_x(3), SingleMode(None))
food = Artifact_Token("Food Token", None, [CardType.ARTIFACT, ArtifactType.FOOD], [food_ability])
treasure_ability = Activated_Ability("{T}, Sacrifice this artifact: Add one mana of any color.", Total_Cost([tap_self, sac_self]), add_any_color_mana, SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.WHITE, ManaType.BLUE, ManaType.BLACK, ManaType.RED, ManaType.GREEN])
treasure = Artifact_Token("Treasure Token", None, [CardType.ARTIFACT, ArtifactType.TREASURE], [treasure_ability])


def deal_x(amount):
    def _(game, controller, source, event, modes, targets):
        game.deal_damage(targets[0].object, source, amount)
    return _


def deal_1_to_opponents(game, controller, source, event, modes, targets):
    opponents = game.get_opponents(controller)
    for opponent in opponents:
        game.deal_damage(opponent, source, 1)


def grow_3(game, controller, source, event, modes, targets):
    target = targets[0].object
    effect = PT_Effect(EffectDuration.EOT, lambda p, o: p == target, 3, 3)
    game.create_continuous_effect(effect)


def shrink_x(x):
    def shrink(game, controller, source, event, modes, targets):
        target = targets[0].object
        effect = PT_Effect(EffectDuration.EOT, lambda p, o: p == target, -x, -x)
        game.create_continuous_effect(effect)
    return shrink


def make_2_tokens(game, controller, source, event, modes, targets):
    token = Creature_Token("Elemental Token", None, [CardType.CREATURE], [], 1, 1, color_indicator=[Color.RED, Color.BLUE])
    game.create_token(controller, token.copy())
    game.create_token(controller, token.copy())


def make_elf_warrior(game, controller, source, event, modes, targets):
    token = Creature_Token("Elf Warrior Token", None, [CardType.CREATURE, CreatureType.ELF,
                           CreatureType.WARRIOR], [], 1, 1, color_indicator=[Color.GREEN])
    game.create_token(controller, token.copy())


def make_treasure(game, controller, source, event, modes, targets):
    game.create_token(controller, treasure.copy())


def make_insect(game, controller, source, event, modes, targets):
    token = Creature_Token("Insect Token", None, [CardType.CREATURE, CreatureType.INSECT], [
                           flying], 1, 1, color_indicator=[Color.GREEN, Color.BLACK])
    game.create_token(controller, token.copy())


def make_cat(game, controller, source, event, modes, targets):
    token = Creature_Token("Cat Token", None, [CardType.CREATURE, CreatureType.CAT], [], 1, 1, color_indicator=[Color.WHITE])
    game.create_token(controller, token.copy())


def exile_gravecard(game, controller, source, event, modes, targets):
    if targets == None:
        return
    target = targets[0].object
    game.exile_from_graveyard(target)


def attach(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.attach_permanents(target, source)


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


def put_counter_targets(game, controller, source, event, modes, targets):
    if targets == None:
        return
    creatures = [target.object for target in targets]
    for creature in creatures:
        game.put_counters_on(CounterType.P1P1, 1, creature)


def give_haste(game, controller, source, event, modes, targets):
    target = targets[0].object
    effect = Ability_Grant_Effect(EffectDuration.EOT, lambda p, o: p == target, [haste])
    game.create_continuous_effect(effect)


def give_fake_death_ability(game, controller, source, event, modes, targets):
    target = targets[0].object
    ability = Triggered_Ability(trigger_on_death, SingleMode(None), return_tapped_with_treasure)
    effect = Ability_Grant_Effect(EffectDuration.EOT, lambda p, o: p == target, [ability])
    game.create_continuous_effect(effect)
    effect = PT_Effect(EffectDuration.EOT, lambda p, o: p == target, 2, 0)
    game.create_continuous_effect(effect)


def stun_blocks(game, controller, source, event, modes, targets):
    target = targets[0].object
    effect = Block_Restriction_Effect(EffectDuration.EOT, lambda p, o: p == target)
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


def exile_permanent(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.exile_from_battlefield(target)


def bounce_permanent(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.return_permanent_to_hand(target)


def pump_self_pxpy(x, y):
    def pump(game, controller, source, event, modes, targets):
        effect = PT_Effect(EffectDuration.EOT, lambda p, o: p == source, x, y)
        game.create_continuous_effect(effect)
    return pump


def pump_self_p1p0_and_menace(game, controller, source, event, modes, targets):
    effect = PT_Effect(EffectDuration.EOT, lambda p, o: p == source, 1, 0)
    menace_effect = Ability_Grant_Effect(EffectDuration.EOT, lambda p, o: p == source, [menace])
    game.create_continuous_effect(effect)
    game.create_continuous_effect(menace_effect)


def creature_bite(game, controller, source, event, modes, targets):
    biter = targets[0].object
    bitee = targets[1].object
    game.deal_damage(bitee, biter, biter.power)


def opponents_discard(game, controller, source, event, modes, targets):
    opponents = game.get_opponents(controller)
    for opponent in opponents:
        game.player_discard_x(opponent, 1)


def deal_2_kicked_4(game, controller, source, event, modes, targets):
    target = targets[0].object
    was_kicked = CostType.KICKED in [cost.type for cost in modes[ModeType.COSTS_PAID]]
    if was_kicked:
        game.deal_damage(target, source, 4)
    else:
        game.deal_damage(target, source, 2)


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


def tutor_tapped_basic(game, controller, source, event, modes, targets):
    def tap(permanent):
        permanent.tapped = True
    game.player_tutor_to_battlefield(controller, lambda c: c.is_land and c.is_basic, modify_function=tap)


def draw_card(game, controller, source, event, modes, targets):
    game.player_draw(controller)


def draw_x(x):
    def draw(game, controller, source, event, modes, targets):
        for i in range(x):
            game.player_draw(controller)
    return draw


def loot(game, controller, source, event, modes, targets):
    game.player_draw(controller)
    game.player_discard_x(controller, 1)


def surveil(x):
    def surveil_x(game, controller, source, event, modes, targets):
        game.player_surveil(controller, x)
    return surveil_x


def drain_opponents_1(game, controller, source, event, modes, targets):
    opponents = game.get_opponents(controller)
    for opponent in opponents:
        game.player_lose_life(opponent, 1)
    game.player_gain_life(controller, 1)


#


def weaken_draw(game, controller, source, event, modes, targets):
    target = targets[0].object
    effect = PT_Effect(EffectDuration.EOT, lambda p, o: p == target, -1, 0)
    game.create_continuous_effect(effect)
    game.player_draw(controller)


def return_tapped_with_treasure(game, controller, source, event, modes, targets):
    def tap(permanent):
        permanent.tapped = True
    game.return_gravecard_to_battlefield(event.grave_card.owner, event.grave_card, modify_function=tap)
    game.create_token(controller, treasure.copy())


def fleeting_flight_effect(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.put_counters_on(CounterType.P1P1, 1, target)
    effect = Ability_Grant_Effect(EffectDuration.EOT, lambda p, o: p == target, [flying])
    game.create_continuous_effect(effect)
    effect = Prevention_Effect(EffectDuration.EOT, lambda e, o: e.is_combat_damage and e.target == target, prevent_damage)
    game.create_continuous_effect(effect)


def goblin_surprise_effect(game, controller, source, event, modes, targets):
    mode = modes[ModeType.MODES_CHOSEN][0]
    if mode == 0:
        # Pump
        creatures = game.get_creatures_of(controller)
        effect = PT_Effect(EffectDuration.EOT, lambda p, o: p in creatures, 2, 0)
        game.create_continuous_effect(effect)
    if mode == 1:
        # Tokens
        token = Creature_Token("Goblin Token", None, [CardType.CREATURE, CreatureType.GOBLIN], [], 1, 1, color_indicator=[Color.RED])
        game.create_token(controller, token.copy())
        game.create_token(controller, token.copy())


def grow_from_the_ashes_effect(game, controller, source, event, modes, targets):
    was_kicked = CostType.KICKED in [cost.type for cost in modes[ModeType.COSTS_PAID]]
    if was_kicked:
        game.player_tutor_to_battlefield(controller, lambda c: c.is_land and c.is_basic, amount=2)
    else:
        game.player_tutor_to_battlefield(controller, lambda c: c.is_land and c.is_basic)


def gutless_plunderer_effect(game, controller, source, event, modes, targets):
    seen_cards = game.player_look_at_top_x(controller, 3)
    chosen_card = controller.agent.choose_one(seen_cards+[None])
    if chosen_card is not None:
        seen_cards.remove(chosen_card)
    for card in seen_cards:
        game.library_to_graveyard(controller, card)


def hare_apparent_effect(game, controller, source, event, modes, targets):
    other_hares = game.get_permanents_of_that(controller, lambda p: p != source and p.is_creature and p.name == "Hare Apparent")
    token = Creature_Token("Rabit Token", None, [CardType.CREATURE, CreatureType.RABBIT], [], 1, 1, color_indicator=[Color.WHITE])
    for hare in other_hares:
        game.create_token(controller, token.copy())


def incinerating_blast_effect(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.deal_damage(target, source, 6)
    if controller.hand.size > 0:
        if controller.agent.choose_yes_or_no("Discard a card to draw a card?"):
            game.player_discard_x(controller, 1)
            game.player_draw(controller)


def involuntary_employment_effect(game, controller, source, event, modes, targets):
    target = targets[0].object
    effect = Control_Effect(EffectDuration.EOT, lambda p, o: p == target, controller)
    game.create_continuous_effect(effect)
    game.untap(target)
    effect = Ability_Grant_Effect(EffectDuration.EOT, lambda p, o: p == target, [haste])
    game.create_continuous_effect(effect)
    game.create_token(controller, treasure.copy())


def macabre_waltz_effect(game, controller, source, event, modes, targets):
    cards = []
    if targets != None:
        cards = [target.object for target in targets]
    for card in cards:
        game.return_gravecard_to_hand(card)
    game.player_discard_x(controller, 1)


def blight_priest_effect(game, controller, source, event, modes, targets):
    opponents = game.get_opponents(controller)
    for opponent in opponents:
        game.player_lose_life(opponent, 1)


def pilfer_effect(game, controller, source, event, modes, targets):
    target = targets[0].object
    seen_cards = game.player_look_at_hand(controller, target)
    chosen_card = controller.agent.choose_one(seen_cards)
    game.player_discard_card(target, chosen_card)


def refute_effect(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.counter_stack_object(target)
    game.player_draw(controller)
    game.player_discard_x(controller, 1)


def run_away_effect(game, controller, source, event, modes, targets):
    creatures = [target.object for target in targets]
    for creature in creatures:
        game.return_permanent_to_hand(creature)


def soul_shackled_effect(game, controller, source, event, modes, targets):
    if targets == None:
        return
    cards = [target.object for target in targets]
    creature_card_exiled = False
    for card in cards:
        event = game.exile_from_graveyard(card)
        if isinstance(event, Gravecard_Exiled_Event) and event.grave_card.is_creature:
            creature_card_exiled = True
    if creature_card_exiled:
        for opponent in game.get_opponents(controller):
            game.player_lose_life(opponent, 2)
        game.player_gain_life(controller, 2)


def squad_rallier_effect(game, controller, source, event, modes, targets):
    game.player_seek_to_hand(controller, 4, lambda c: c.is_creature and c.power <= 2)


def sure_strike_effect(game, controller, source, event, modes, targets):
    target = targets[0].object
    effect = PT_Effect(EffectDuration.EOT, lambda p, o: p == target, 3, 0)
    ability_effect = Ability_Grant_Effect(EffectDuration.EOT, lambda p, o: p == target, [first_strike])
    game.create_continuous_effect(effect)
    game.create_continuous_effect(ability_effect)


def uncharted_voyage_effect(game, controller, source, event, modes, targets):
    target = targets[0].object
    position = target.owner.agent.choose_one(["Top", "Bottom"], message="Choose Top or Bottom: ")
    if position == "Top":
        position = 0
    else:
        position = -1
    game.return_permanent_to_library(target, position)
    game.player_surveil(controller, 1)


def soulcaller_effect(game, controller, source, event, modes, targets):
    target = targets[0].object
    game.return_gravecard_to_hand(target)
# Triggers


def trigger_on_etb(game, event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent == object


def trigger_on_landfall(game, event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent.is_land and event.permanent.controller == object.controller


def trigger_on_controlled_creature_enter(game, event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent != object and event.permanent.is_creature and event.permanent.controller == object.controller


def trigger_on_death(game, event, object):
    return isinstance(event, Permanent_Died_Event) and event.permanent == object


def trigger_on_opponent_target(game, event, object):
    return event.contains(Targeting_Event) and object in event.targets and event.stack_object.controller in game.get_opponents(object.controller)


def trigger_on_noncreature_cast(game, event, object):
    return isinstance(event, Spellcast_Event) and event.spell_object.controller == object.controller and not event.spell_object.card.is_creature


def morbid_end_step(game, event, object):
    return isinstance(event, Step_Begin_Event) and event.step == Step.END and event.player == object.controller and game.creature_died_this_turn


def trigger_on_3_creatures_attack(game, event, object):
    return isinstance(event, Attack_Event) and event.num_attacking >= 3


def trigger_on_attack(game, event, object):
    return isinstance(event, Attack_Event) and object in event.attackers


def trigger_on_attack_with_ferocious(game, event, object):
    return isinstance(event, Attack_Event) and object in event.attackers and game.player_has_ferocious(object.controller)


def trigger_on_attack_with_threshold(game, event, object):
    return isinstance(event, Attack_Event) and object in event.attackers and game.player_has_threshold(object.controller)


def trigger_on_equipped_combat_damage(game, event, object):
    return isinstance(event, Damage_Event) and object.attached_permanent == event.source


def trigger_on_second_card(game, event, object):
    return isinstance(event, Card_Draw_Event) and event.number_this_turn == 2


def trigger_on_lifegain(game, event, object):
    return isinstance(event, Lifegain_Event) and event.player == object.controller


def trigger_on_first_lifegain(game, event, object):
    return isinstance(event, Lifegain_Event) and event.player == object.controller and event.player.life_gained_this_turn == event.amount


def trigger_on_etb_or_death(game, event, object):
    if isinstance(event, Permanent_Enter_Event):
        pass
    if isinstance(event, Permanent_Died_Event):
        if event.permanent == object:
            pass
    return (isinstance(event, Permanent_Enter_Event) or isinstance(event, Permanent_Died_Event)) and event.permanent == object

# Replacement Effects


def replace_enters(event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent == object


def replace_enters_if_kicked(event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent == object and event.permanent.casting_information.get(CastingInformationType.KICKED, False)


def replace_enters_if_raid(event, object):
    return isinstance(event, Permanent_Enter_Event) and event.permanent == object and event.permanent.controller.attacked_this_turn


def replace_leave_stack(event, object):
    # TODO: fix to catch all zone transitions. consider moving flashbacking logic here
    return isinstance(event, Stack_Died_Event) and event.stack_object == object


def enters_tapped(event, object):
    new_event = event.copy()
    new_event.permanent.tapped = True
    return new_event


def enters_counters(x):
    def _(event, object):
        new_event = event.copy()
        new_event.permanent.add_counters(CounterType.P1P1, x)  # TODO: This modifies the event to include putting counters.
        return new_event
    return _


def prevent_damage(event, object):
    new_event = event.copy()
    new_event.prevented = True
    return new_event


def flashback_to_exile(event, object):
    was_flashedback = CostType.FLASHBACK in [cost.type for cost in object.modes[ModeType.COSTS_PAID]]
    if was_flashedback:
        new_event = Stack_Exiled_Event(event.stack_object)
        return new_event
    return event

# Conditionals


def control_other_elf(game, event, object):
    return game.player_controls_permanent_that(object.controller, lambda p: p.is_creature and p != object and CreatureType.ELF in p.types)


def attacked_this_turn(game, event, object):
    return object.controller.attacked_this_turn

# Spell conditionals


def luminous_cost_calculation(game, spell):
    for target in spell.targets:
        if isinstance(target.object, Permanent) and target.object.is_creature and target.object.tapped == True:
            return Total_Cost([Mana_Cost.from_string("3")])
    return Total_Cost([])


def tolarian_cost_calculation(game, spell):
    instants_sorceries_in_grave = 0
    for card in spell.controller.graveyard.objects:
        if card.is_instant or card.is_sorcery:
            instants_sorceries_in_grave += 1
    return Total_Cost([Mana_Cost.from_string(str(instants_sorceries_in_grave))])


damageable_target = TargetWord([ObjectType.PERMANENT, ObjectType.PLAYER],
                               lambda g, t, p, s: isinstance(t, Player) or (isinstance(t, Permanent) and t.is_damageable), "any target")
creature_target = TargetWord([ObjectType.PERMANENT],
                             lambda g, t, p, s: t.is_creature, "target creature")
opt_gravecard_target = TargetWord([ObjectType.GRAVE_CARD],
                                  lambda g, t, p, s: True, "up to one target card in a graveyard", is_optional=True)
creature_you_control_target = TargetWord([ObjectType.PERMANENT],
                                         lambda g, t, p, s: t.is_creature and t.controller == p, "target creature you control")
creature_dont_control_target = TargetWord([ObjectType.PERMANENT],
                                          lambda g, t, p, s: t.is_creature and t.controller != p, "target creature you don't control")
creature_opp_control_target = TargetWord([ObjectType.PERMANENT],
                                         lambda g, t, p, s: t.is_creature and t.controller in g.get_opponents(p), "target creature an opponent controls")
nl_permanent_opp_control_target = TargetWord([ObjectType.PERMANENT],
                                             lambda g, t, p, s: t.controller in g.get_opponents(p), "target nonland permanent an opponent controls")
creature_planeswalker_dont_control_target = TargetWord([ObjectType.PERMANENT],
                                                       lambda g, t, p, s: (t.is_creature or t.is_planeswalker) and t.controller != p, "target creature or planeswalker you don't control")
broken_wings_target = TargetWord([ObjectType.PERMANENT],
                                 lambda g, t, p, s: (t.is_artifact or t.is_enchantment or (t.is_creature and AbilityKeyword.FLYING in t.keywords)), "target artifact, enchantment, or creature with flying")
artifact_enchanment_target = TargetWord([ObjectType.PERMANENT],
                                        lambda g, t, p, s: t.is_artifact or t.is_enchantment, "target artifact or enchantment")
creature_planeswalker_target = TargetWord([ObjectType.PERMANENT],
                                          lambda g, t, p, s: t.is_creature or t.is_planeswalker, "target creature or planeswalker")
opt_two_other_creatures_you_control_target = TargetWord([ObjectType.PERMANENT],
                                                        lambda g, t, p, s: t.is_creature and t.controller == p and t != s, "up to two target creatures", number=2, is_optional=True)
opt_two_creature_your_gravecards = TargetWord([ObjectType.GRAVE_CARD],
                                              lambda g, t, p, s: t.owner == p and t.is_creature, "up to two creature cards from your graveyard", number=2, is_optional=True)
make_your_move_target = TargetWord([ObjectType.PERMANENT],
                                   lambda g, t, p, s: (t.is_artifact or t.is_enchantment or (t.is_creature and t.power >= 4)), "target artifact, enchantment, or creature with power 4 or greater")
opponent_target = TargetWord([ObjectType.PLAYER],
                             lambda g, t, p, s: t in g.get_opponents(p), "target opponent")
spell_target = TargetWord([ObjectType.STACK_OBJECT],
                          lambda g, t, p, s: t.is_spell, "target spell")
run_away_target = TargetWord([ObjectType.PERMANENT],
                             lambda g, t, p, s: t.is_creature, "two target creatures controlled by different players", number=2, total_req_function=lambda w: w[0].object.controller != w[1].object.controller)
soul_shackled_target = TargetWord([ObjectType.GRAVE_CARD],
                                  lambda g, t, p, s: True, "up to two target cards from a single graveyard", number=2, total_req_function=lambda w: len(w) < 2 or w[0].object.owner == w[1].object.owner, is_optional=True)
soulcaller_target = TargetWord([ObjectType.GRAVE_CARD],
                               lambda g, t, p, s: t.owner == p and t.is_creature, "target creature card from your graveard")

plains_ability = Activated_Ability("{T}: Add {W}", Total_Cost([tap_self]),
                                   add_one_white_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.WHITE])
island_ability = Activated_Ability("{T}: Add {U}", Total_Cost([tap_self]),
                                   add_one_blue_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.BLUE])
swamp_ability = Activated_Ability("{T}: Add {B}", Total_Cost([tap_self]),
                                  add_one_black_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.BLACK])
mountain_ability = Activated_Ability("{T}: Add {R}", Total_Cost([tap_self]),
                                     add_one_red_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.RED])
forest_ability = Activated_Ability("{T}: Add {G}", Total_Cost([tap_self]),
                                   add_one_green_mana, SingleMode(None), is_mana_ability=True, mana_produced=[ManaType.GREEN])


# lightning_ability = Spell_Ability("Deal 3 damage to any target.", deal_3, [damageable_target])
# reinforcements_ability = Spell_Ability("Create 2 1/1 red and blue Elementals.", make_2_tokens, None)


def kicker(x):
    return Additional_Cost([Total_Cost([Mana_Cost.from_string(x)], type=CostType.KICKED), None])


def ward(x):
    cost = Total_Cost([Mana_Cost.from_string(x)])

    def rhystic_counter(game, controller, source, event, modes, targets):
        ability_stack_object = event.stack_object
        if game.player_pay_cost(ability_stack_object.controller, cost):
            return
        game.counter_stack_object(ability_stack_object)
    return Triggered_Ability(trigger_on_opponent_target, SingleMode(None), rhystic_counter)


def equip(x):
    return Activated_Ability(f"Equip {x}", Total_Cost([Mana_Cost.from_string(x)]), attach, SingleMode([creature_you_control_target]), activation_restrictions=[ActivationRestrictionType.SORCERY])


def flashback(x):
    # TODO: Flashback only works for instants and sorceries.
    flashback_cost = Alternative_Cost(Total_Cost([Mana_Cost.from_string(x)], type=CostType.FLASHBACK), [ZoneType.GRAVEYARD])
    flashback_exile = Replacement_Effect(replace_leave_stack, flashback_to_exile, functions_in=[ZoneType.STACK])
    return [flashback_cost, flashback_exile]


prowess = Triggered_Ability(trigger_on_noncreature_cast, SingleMode(None), pump_self_pxpy(1, 1))

ambush_wolf_etb = Triggered_Ability(trigger_on_etb, SingleMode([opt_gravecard_target]), exile_gravecard)
apothecary_stomper_etb = Triggered_Ability(trigger_on_etb, ModeChoice(
    1, [Mode([creature_you_control_target], "Put two +1/+1 counters on target creature you control", 0), Mode(None, "You gain 4 life", 1)]), put_2_counters_or_gain_4)
armasaur_guide_attack = Triggered_Ability(trigger_on_3_creatures_attack, SingleMode([creature_you_control_target]), put_counter)
banishing_light_ability = Triggered_Ability(trigger_on_etb, SingleMode([nl_permanent_opp_control_target]), exile_until_leaves)
beastkin_ranger_pump = Triggered_Ability(trigger_on_controlled_creature_enter, SingleMode(None), pump_self_pxpy(1, 0))
bigfin_bouncer_etb = Triggered_Ability(trigger_on_etb, SingleMode([creature_opp_control_target]), bounce_permanent)
gain_1_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), gain_x(1))
burglar_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), opponents_discard)
cackling_prowler_morbid = Triggered_Ability(morbid_end_step, SingleMode(None), put_counter_self)
campus_guide_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), tutor_land_top_opt)
courageous_goblin_attack = Triggered_Ability(trigger_on_attack_with_ferocious, SingleMode(None), pump_self_p1p0_and_menace)
crackling_cyclops_pump = Triggered_Ability(trigger_on_noncreature_cast, SingleMode(None), pump_self_pxpy(3, 0))
crypt_feaster_threshold = Triggered_Ability(trigger_on_attack_with_threshold, SingleMode(None), pump_self_pxpy(2, 0))
dazzling_angel_gain = Triggered_Ability(trigger_on_controlled_creature_enter, SingleMode(None), gain_x(1))
dwynens_elite_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), make_elf_warrior, intervening_if_conditional=control_other_elf)
elfsworn_giant_landfall = Triggered_Ability(trigger_on_landfall, SingleMode(None), make_elf_warrior)
erudite_wizard_2card = Triggered_Ability(trigger_on_second_card, SingleMode(None), put_counter_self)
felidar_savior_etb = Triggered_Ability(trigger_on_etb, SingleMode([opt_two_other_creatures_you_control_target]), put_counter_targets)
firebrand_archer_ping = Triggered_Ability(trigger_on_noncreature_cast, SingleMode(None), deal_1_to_opponents)
gleaming_barrier_death = Triggered_Ability(trigger_on_death, SingleMode(None), make_treasure)
goldvein_damage_trigger = Triggered_Ability(trigger_on_equipped_combat_damage, SingleMode(None), make_treasure)
gorehorn_raider_etb = Triggered_Ability(trigger_on_etb, SingleMode(
    [damageable_target]), deal_x(2), intervening_if_conditional=attacked_this_turn)
gutless_plunderer_etb = Triggered_Ability(trigger_on_etb, SingleMode(
    None), gutless_plunderer_effect, intervening_if_conditional=attacked_this_turn)
hare_apparent_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), hare_apparent_effect)
helpful_hunter_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), draw_card)
icewind_elemental_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), loot)
infestation_sage_death = Triggered_Ability(trigger_on_death, SingleMode(None), make_insect)
lightshell_duo_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), surveil(2))
blight_priest_ability = Triggered_Ability(trigger_on_lifegain, SingleMode(None), blight_priest_effect)
prideful_parent_etb = Triggered_Ability(trigger_on_etb, SingleMode(None), make_cat)
syphoner_attack = Triggered_Ability(trigger_on_attack, SingleMode(None), drain_opponents_1)
soul_shackled_etb = Triggered_Ability(trigger_on_etb, SingleMode([soul_shackled_target]), soul_shackled_effect)
spitfire_landfall = Triggered_Ability(trigger_on_landfall, SingleMode(None), deal_1_to_opponents)
soulcaller_etb = Triggered_Ability(trigger_on_etb, SingleMode([soulcaller_target]), soulcaller_effect)
vanguard_seraph_trigger = Triggered_Ability(trigger_on_first_lifegain, SingleMode(None), surveil(1))
thespian_etb_die = Triggered_Ability(trigger_on_etb_or_death, SingleMode(None), surveil(1))

axgard_cavalry_tap = Activated_Ability("{T}: Target creature gains haste until end of turn.",
                                       Total_Cost([tap_self]), give_haste, SingleMode([creature_target]))
cathar_sac = Activated_Ability("{1}, Sacrifice this creature: Destroy target artifact or enchantment.",
                               Total_Cost([Mana_Cost.from_string("1"), sac_self]), destroy_permanent, SingleMode([artifact_enchanment_target]))
evolving_wilds_sac = Activated_Ability(
    "{T}, Sacrifice this land: Tutor a basic land card to the battlefield tapped.", Total_Cost([tap_self, sac_self]), tutor_tapped_basic, SingleMode(None))
fanatical_firebrand_sac = Activated_Ability(
    "{T}, Sacrifice this creature: It deals 1 damage to any target.", Total_Cost([tap_self, sac_self]), deal_x(1), SingleMode([damageable_target]))
hungry_ghoul_sac = Activated_Ability("{1}, Sacrifice another creature: Put a +1/+1 counter on this creature.",
                                     Total_Cost([Mana_Cost.from_string("1"), sac_other_creature]), put_counter_self, SingleMode(None))
sower_of_chaos_activated = Activated_Ability("{2R}: Target creature can't block this turn.", Total_Cost(
    [Mana_Cost.from_string("2R")]), stun_blocks, SingleMode([creature_target]))
squad_rallier_activated = Activated_Ability("{2W}: Seek 4 for a creature card with power 2 or less.", Total_Cost([
                                            Mana_Cost.from_string("2W")]), squad_rallier_effect, SingleMode(None))
strix_loot = Activated_Ability("{1U}{T}: Loot.", Total_Cost([Mana_Cost.from_string("1U"), tap_self]), loot, SingleMode(None))
treetop_snarespinner_activated = Activated_Ability("{2G}: Put a +1/+1 counter on target creature you control. Activate as a sorcery.", Total_Cost([
                                                   Mana_Cost.from_string("2G")]), put_counter, SingleMode([creature_you_control_target]), activation_restrictions=[ActivationRestrictionType.SORCERY])

enters_tapped_replacement = Replacement_Effect(replace_enters, enters_tapped)
rakdos_land_ability = Activated_Ability("{T}: Add {B} or {R}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.BLACK, ManaType.RED), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.BLACK, ManaType.RED])
selesnya_land_ability = Activated_Ability("{T}: Add {G} or {W}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.GREEN, ManaType.WHITE), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.GREEN, ManaType.WHITE])
dimir_land_ability = Activated_Ability("{T}: Add {U} or {B}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.BLUE, ManaType.BLACK), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.BLUE, ManaType.BLACK])
golgari_land_ability = Activated_Ability("{T}: Add {B} or {G}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.BLACK, ManaType.GREEN), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.BLACK, ManaType.GREEN])
gruul_land_ability = Activated_Ability("{T}: Add {R} or {G}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.RED, ManaType.GREEN), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.RED, ManaType.GREEN])
orzhov_land_ability = Activated_Ability("{T}: Add {W} or {B}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.WHITE, ManaType.BLACK), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.WHITE, ManaType.BLACK])
izzet_land_ability = Activated_Ability("{T}: Add {U} or {R}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.BLUE, ManaType.RED), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.BLUE, ManaType.RED])
simic_land_ability = Activated_Ability("{T}: Add {G} or {U}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.GREEN, ManaType.BLUE), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.GREEN, ManaType.BLUE])
azorius_land_ability = Activated_Ability("{T}: Add {W} or {U}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.WHITE, ManaType.BLUE), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.WHITE, ManaType.BLUE])
boros_land_ability = Activated_Ability("{T}: Add {R} or {W}", Total_Cost([tap_self]), add_x_or_y_mana(ManaType.RED, ManaType.WHITE), SingleMode(
    None), is_mana_ability=True, mana_produced=[ManaType.RED, ManaType.WHITE])

destroy_ability = Spell_Ability(destroy_permanent, SingleMode([nl_permanent_opp_control_target]))
draw_card_ability = Spell_Ability(draw_card, SingleMode(None))

bake_into_a_pie_ability = Spell_Ability(destroy_creature_and_make_food, SingleMode([creature_target]))
bite_down_ability = Spell_Ability(creature_bite, SingleMode([creature_you_control_target, creature_planeswalker_dont_control_target]))
broken_wings_ability = Spell_Ability(destroy_permanent, SingleMode([broken_wings_target]))
burst_lightning_ability = Spell_Ability(deal_2_kicked_4, SingleMode([damageable_target]))
bushwhack_ability = Spell_Ability(tutor_land_or_fight, ModeChoice(
    1, [Mode(None, "Search for a basic land", 0), Mode([creature_you_control_target, creature_dont_control_target], "Target creature you control fights target creature you don't control.", 1)]))
eaten_alive_ability = Spell_Ability(exile_permanent, SingleMode([creature_planeswalker_target]))
fake_your_own_death_ability = Spell_Ability(give_fake_death_ability, SingleMode([creature_target]))
fleeting_distraction_ability = Spell_Ability(weaken_draw, SingleMode([creature_target]))
fleeting_flight_ability = Spell_Ability(fleeting_flight_effect, SingleMode([creature_target]))
giant_growth_ability = Spell_Ability(grow_3, SingleMode([creature_target]))
goblin_surprise_ability = Spell_Ability(goblin_surprise_effect, ModeChoice(
    1, [Mode(None, "Creatures you control get +2/+0 until end of turn", 0), Mode(None, "Create two 1/1 red Goblin creature tokens.", 1)]))
grow_from_the_ashes_ability = Spell_Ability(grow_from_the_ashes_effect, SingleMode(None))
incinerating_blast_ability = Spell_Ability(incinerating_blast_effect, SingleMode([creature_target]))
involuntary_employment_ability = Spell_Ability(involuntary_employment_effect, SingleMode([creature_target]))
luminous_rebuke_ability = Spell_Ability(destroy_permanent, SingleMode([creature_target]))
macabre_waltz_ability = Spell_Ability(macabre_waltz_effect, SingleMode([opt_two_creature_your_gravecards]))
make_your_move_ability = Spell_Ability(destroy_permanent, SingleMode([make_your_move_target]))
pilfer_ability = Spell_Ability(pilfer_effect, SingleMode([opponent_target]))
refute_ability = Spell_Ability(refute_effect, SingleMode([spell_target]))
run_away_together_ability = Spell_Ability(run_away_effect, SingleMode([run_away_target]))
stab_ability = Spell_Ability(shrink_x(2), SingleMode([creature_target]))
sure_strike_ability = Spell_Ability(sure_strike_effect, SingleMode([creature_target]))
think_twice_ability = Spell_Ability(draw_card, SingleMode(None))
thrill_ability = Spell_Ability(draw_x(2), SingleMode(None))
uncharted_voyage_ability = Spell_Ability(uncharted_voyage_effect, SingleMode([creature_target]))

eaten_alive_extra_cost = Additional_Cost([Total_Cost([Mana_Cost.from_string("3B")]),
                                         Total_Cost([Sacrifice_Cost(lambda p, o: p.is_creature, name="Sacrifice a creature")])])
thrill_extra_cost = Additional_Cost([Total_Cost([Discard_Cost(lambda c: True, name="Discard a Card")])])

gnarlid_kicked_enters = Replacement_Effect(replace_enters_if_kicked, enters_counters(2))
goblin_boarders_enters = Replacement_Effect(replace_enters_if_raid, enters_counters(1))


def is_equipped_creature(p, o): return o.attached_permanent == p


gnarlid_counter_lord = Static_Ability(Ability_Grant_Effect(
    EffectDuration.STATIC, lambda p, o: p.counters.get(CounterType.P1P1, 0) > 0, [trample]))
goldvein_equip_buff = Static_Ability(PT_Effect(EffectDuration.STATIC, is_equipped_creature, 1, 1))
paladin_self_anthem = Static_Ability(Ability_Grant_Effect(EffectDuration.YOUR_TURN, lambda p, o: p == o, [first_strike]))
paladin_counter_lord = Static_Ability(Ability_Grant_Effect(
    EffectDuration.YOUR_TURN, lambda p, o: p.counters.get(CounterType.P1P1, 0) > 0, [first_strike]))
mocking_sprite_discount = Static_Ability(Cost_Modification_Effect(
    EffectDuration.STATIC, lambda s: s.is_instant or s.is_sorcery, Total_Cost([Mana_Cost.from_string("1")]), True))
katana_equip_buff_1 = Static_Ability(PT_Effect(EffectDuration.YOUR_TURN, is_equipped_creature, 2, 0)
                                     )  # TODO: Combine these effects into one
katana_equip_buff_2 = Static_Ability(Ability_Grant_Effect(EffectDuration.YOUR_TURN, is_equipped_creature, [first_strike]))
cant_block = Static_Ability(Block_Restriction_Effect(EffectDuration.STATIC, lambda p, o: p == o))

# luminous_cost_reduction = Cost_Modification(targets_tapped_creature, Total_Cost([Mana_Cost.from_string("3")]), True)
luminous_cost_reduction = Cost_Modification(luminous_cost_calculation, True)
tolarian_cost_reduction = Cost_Modification(tolarian_cost_calculation, True)
