
from ability_stack_object import Ability_Stack_Object
from action import Action
from cost import Total_Cost
from agent import Agent
from canvas import Text_Canvas
from effects import Prevention_Effect
from enums import AbilityKeyword, ActivationRestrictionType, CounterType, EffectDuration, EffectType, ModeType, Phase, Privacy, StackObjectType, Step
from event import Ability_Activate_Begin_Marker, Ability_Activate_End_Marker, Activation_Event, Attack_Event, Card_Draw_Event, Damage_Event, Mana_Ability_Event, Mana_Produced_Event, Permanent_Died_Event, Permanent_Enter_Event, Permanent_Exiled_Event, Spellcast_Begin_Marker, Spellcast_End_Marker, Spellcast_Event, Step_Begin_Event, Trigger_Stack_Event
from exceptions import IllegalActionException, UnpayableCostException
from exile_object import Exile_Object
from graveyard_object import Graveyard_Object
from hand_object import Hand_Object
from listener import Listener
from permanent import Permanent
from player import Player
from target import Target
from zone import Zone


class Backup_Manager:
    def __init__(self) -> None:
        self.events = []

    @property
    def last_event(self):
        return self.events[-1]

    def add_event(self, event):
        self.events.append(event)

    def reverse_last_event(self):
        last_event = self.events.pop()
        last_event.undo()


class Game:

    def __init__(self, agents) -> None:
        self.exile = Zone(name="Exile", privacy=Privacy.PUBLIC)
        self.battlefield = Zone(name="Battlefield", privacy=Privacy.PUBLIC)
        self.stack = Zone(name="Stack", privacy=Privacy.PUBLIC)
        self.players = [Player(agent=agent, game=self) for agent in agents]
        self.active_player_index = 0
        self.backup_manager = Backup_Manager()

        self.current_step = Step.NONE
        self.current_phase = Phase.NONE
        self.step_queue = []
        self.turn_number = 0
        self.is_ended = False
        self.winner = None

        self.creature_died_this_turn = False

        self.permanent_id = 0

        self.effects = []
        self.triggers_waiting = []
        self.listeners = []
    # Properties

    @property
    def num_players(self):
        return len(self.players)

    @property
    def active_player(self):
        return self.players[self.active_player_index]

    @property
    def inactive_players(self):
        return self.players[self.active_player_index + 1:] + self.players[:self.active_player_index]

    @property
    def apnap_order(self):
        return self.players[self.active_player_index:] + self.players[:self.active_player_index]

    # Query Functions

    def player_id_after(self, player_id):
        return (player_id + 1) % self.num_players

    def player_can_make_land_drop(self, player):
        return player.land_drops_per_turn > player.lands_played_this_turn and self.player_can_sorcery(player)

    def player_can_sorcery(self, player):
        return player == self.active_player and self.current_phase == Phase.MAIN and self.stack.is_empty()

    def player_has_ferocious(self, player):
        for creature in self.get_creatures_of(player):
            if creature.power >= 4:
                return True
        return False

    def player_has_threshold(self, player):
        return player.graveyard.size >= 7

    def get_alive_players(self):
        return [player for player in self.players if player.is_alive]

    def get_opponents(self, player):
        return [p for p in self.players if p != player]

    def get_priority_actions(self, player):
        actions = []

        def create_land_drop_action(land):

            def _():
                return self.make_land_drop(player, land)

            return _

        def create_ability_action(activated_ability):
            def _():
                return self.player_activate_ability(player, activated_ability)

            return _

        def create_spellcast_action(spell_card):
            def _():
                return self.player_cast_spell(player, spell_card)

            return _

        if self.player_can_make_land_drop(player):
            for card in player.hand.get_by_criteria(lambda x: x.is_land):
                actions.append(Action(
                    descriptor=f"Land Drop: {card.name}", action=create_land_drop_action(card)))
        for ability in self.get_activated_abilities_of(player):
            actions.append(Action(
                descriptor=f"Activated Ability: {ability.name}", action=create_ability_action(ability), is_priority_holding=not ability.is_mana_ability))
        if self.player_can_sorcery(player):
            for card in player.hand.get_by_criteria(lambda x: x.is_spell and not (x.is_instant_speed)):
                actions.append(
                    Action(descriptor=f"Cast: {card.name}", action=create_spellcast_action(card)))
        for card in player.hand.get_by_criteria(lambda x: x.is_spell and x.is_instant_speed):
            actions.append(
                Action(descriptor=f"Cast: {card.name}", action=create_spellcast_action(card)))
        return actions

    def get_permanents(self):
        return self.battlefield.get_by_criteria(lambda obj: True)

    def get_permanents_of(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.controller == player)

    def get_tappable_permanents_of(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.controller == player and p.tapped == False and not (p.is_creature and p.summoning_sick and not AbilityKeyword.HASTE in p.keywords))

    def get_nonland_permanents_of(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.controller == player and not p.is_land)

    def has_permanent(self, permanent):
        return permanent in self.battlefield.objects

    def player_controls_permanent_that(self, player, conditional):
        for permanent in self.get_permanents_of(player):
            if conditional(permanent):
                return True
        return False

    def get_creatures(self):
        return self.battlefield.get_by_criteria(lambda p: p.is_creature)

    def get_creatures_of(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.is_creature and p.controller == player)

    def get_planeswalkers_of(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.is_planeswalker and p.controller == player)

    def player_can_pay_cost(self, player, cost):
        tap_cost = cost.tap_cost
        tappable_permanents = self.get_tappable_permanents_of(player)
        for use_cost in tap_cost:
            options = [permanent for permanent in tappable_permanents if use_cost.acceptance_function(permanent, cost.object)]
            if len(options) == 0:
                return False
        sacrifice_cost = cost.sacrifice_cost
        saccable_permanents = self.get_permanents_of(player)
        for use_cost in sacrifice_cost:
            options = [permanent for permanent in saccable_permanents if use_cost.acceptance_function(permanent, cost.object)]
            if len(options) == 0:
                return False
        return True

    def player_can_activate_ability(self, player, ability):
        if ActivationRestrictionType.SORCERY in ability.activation_restrictions and not self.player_can_sorcery(player):
            return False
        return self.player_can_pay_cost(player, ability.cost)

    def get_activated_abilities_of(self, player):
        permanents_with_ability = self.battlefield.get_by_criteria(
            lambda p: p.controller == player and p.has_activated_ability)
        return [ability for permanent in permanents_with_ability for ability in permanent.activated_abilities if self.player_can_activate_ability(player, ability)]

    def get_mana_abilities_of(self, player):
        return [
            ability for ability in self.get_activated_abilities_of(player)
            if ability.is_mana_ability
        ]

    def get_triggered_abilities(self):
        permanents_with_ability = self.battlefield.get_by_criteria(lambda p: p.has_triggered_ability)
        return [ability for permanent in permanents_with_ability for ability in permanent.triggered_abilities]

    def get_prevention_effects(self):
        return [effect for effect in self.effects if isinstance(effect, Prevention_Effect)]

    def get_static_effects(self):
        permanents_with_ability = self.battlefield.get_by_criteria(lambda p: p.has_static_ability)
        return [ability for permanent in permanents_with_ability for ability in permanent.static_abilities]

    # Targeting

    def get_damageable(self):
        damageable = []
        damageable.extend(self.players)
        damageable.extend(self.battlefield.get_by_criteria(lambda p: p.is_damageable))
        return damageable

    def get_gravecards(self):
        gravecards = []
        for player in self.players:
            gravecards.extend(player.graveyard.objects)
        return gravecards

    def get_targets(self, player, target_type, source):  # TODO: De-function this function.
        return target_type.get_targets(self, player, source)
    # Combat Query functions

    def get_legal_attackers(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.controller == player and p.is_creature and (not p.summoning_sick or AbilityKeyword.HASTE in p.keywords) and not p.tapped and not AbilityKeyword.DEFENDER in p.keywords)

    def get_legal_attack_targets(self, player):
        return [opponent for opponent in self.players if opponent != player]

    def get_legal_blockers(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.controller == player and p.is_creature and not p.tapped)

    def get_legal_block_targets(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.attack_target == player)

    def get_all_attackers(self):
        return self.battlefield.get_by_criteria(lambda p: p.is_attacking)

    def get_requiring_damage_order(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.controller == player and p.is_creature and (p.is_blocked or p.is_blocking))

    def get_all_in_combat(self):
        return self.battlefield.get_by_criteria(lambda p: p.in_combat)

    def get_all_in_combat_of(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.in_combat and p.controller == player)

    def get_combat_damage_assignments(self):
        combat_damage_assignments = []
        for creature in self.get_all_in_combat():
            combat_damage_assignments.extend(creature.combat_damage_assignment)
        return combat_damage_assignments

    def is_blocked_legally(self, creature):
        if creature.is_blocked:
            if AbilityKeyword.MENACE in creature.keywords and len(creature.blockers) < 2:
                return False
            if AbilityKeyword.FLYING in creature.keywords:
                for blocker in creature.blockers:
                    if AbilityKeyword.FLYING not in blocker.keywords and AbilityKeyword.REACH not in blocker.keywords:
                        return False

        return True

    def is_combat_damage_legally_assigned(self, creature):
        if creature.attack_target in creature.combat_damage_assigned:
            for defending_creature in creature.blockers:
                if not self.is_creature_lethaled(defending_creature):
                    return False
        return True

    def is_creature_lethaled(self, creature):
        assigned_damage = sum([damage_amount for damage_amount,
                              damaged_creature in self.get_combat_damage_assignments() if damaged_creature == creature])
        return assigned_damage+creature.marked_damage >= creature.toughness

    # Note to self: Fix this!! No need to check for gamestate actions, ask forgiveness not permission.
    def gamestate_action_required(self):
        for player in self.players:
            if player.life <= 0:
                return True

        for player in self.players:
            if player.decked:
                return True

        zones = [self.exile, self.battlefield, self.stack]
        for player in self.players:
            zones.extend([player.hand, player.graveyard, player.library])
        for zone in zones:
            if zone.name != "Battlefield":
                to_remove = zone.get_by_criteria(lambda p: p.is_token)
                if len(to_remove) > 0:
                    return True
            if zone.name != "Stack":
                to_remove = zone.get_by_criteria(lambda p: p.is_copy)
                if len(to_remove) > 0:
                    return True

        for permanent in self.get_permanents():
            if permanent.is_creature and permanent.toughness <= 0:
                return True

        for permanent in self.get_permanents():
            if permanent.is_creature and permanent.lethal_damage_dealt:
                return True

    # Turn Structure Functions

    def play_game(self):
        for player in self.players:
            player.start_game()
        self.add_turn()
        self.turn_number = 1
        while not self.is_ended:
            self.advance_step()
        self.game_end()

    def add_turn(self):
        self.step_queue.extend([
            [Phase.BEGINNING, Step.UNTAP],
            [Phase.BEGINNING, Step.UPKEEP],
            [Phase.BEGINNING, Step.DRAW],
            [Phase.MAIN, Step.NONE],
            [Phase.COMBAT, Step.COMBAT_BEGIN],
            [Phase.COMBAT, Step.DECLARE_ATTACKERS],
            [Phase.COMBAT, Step.COMBAT_END],
            [Phase.MAIN, Step.NONE],
            [Phase.ENDING, Step.END],
            [Phase.ENDING, Step.CLEANUP],
        ])

    def add_step(self, step):
        self.step_queue.insert(0, step)

    def next_turn(self):
        self.turn_number += 1
        self.active_player_index = self.player_id_after(
            self.active_player_index)
        for player in self.players:
            player.reset_turn_counters()
        self.creature_died_this_turn = False
        self.add_turn()

    def advance_step(self):
        if len(self.step_queue) == 0:
            raise Exception("Step queue is empty.")
        step = self.step_queue.pop(0)
        self.current_phase = step[0]
        self.current_step = step[1]

        advance_event = Step_Begin_Event(self.current_step, self.active_player)
        self.check_event_for_triggers(advance_event)

        if self.current_step == Step.UNTAP:
            self.turn_untap()
        if self.current_step == Step.DRAW:
            self.turn_draw()
        if self.current_step == Step.DECLARE_ATTACKERS:
            self.turn_declare_attackers()
        if self.current_step == Step.DECLARE_BLOCKERS:
            self.turn_declare_blockers()
        if self.current_step == Step.COMBAT_DAMAGE:
            self.turn_resolve_combat_damage()
        if self.current_step == Step.CLEANUP:
            self.turn_cleanup()
            if self.gamestate_action_required():
                self.add_step([Phase.ENDING, Step.CLEANUP])
                self.resolve_priority()
            else:
                self.next_turn()

        if self.current_step != Step.UNTAP and self.current_step != Step.CLEANUP:
            self.resolve_priority()
        if self.is_ended:
            return

        if self.current_step == Step.COMBAT_END:
            self.turn_end_combat()
        self.turn_empty_mana()

    def game_end(self):
        self.display()

    # Gameplay Functions
    def resolve_priority(self):
        while True:

            priority_player_index = self.active_player_index
            num_players_passing = 0
            while num_players_passing < self.num_players:
                priority_player = self.players[priority_player_index]
                self.check_state_based_actions_and_triggered_abilities()
                if self.is_ended:
                    return
                action = priority_player.agent.act(
                    game=self, player=priority_player)
                if action:
                    action_result = action.invoke()
                    if not action_result:
                        continue
                    num_players_passing = 0
                else:
                    priority_player_index = self.player_id_after(
                        priority_player_index)
                    num_players_passing += 1
            if self.stack.is_empty():
                return
            self.resolve_stack_object(self.stack.pop())  # TODO: Objects don't leave the stack until they've resolved.

    def resolve_stack_object(self, stack_object):
        stack_object.is_alive = False
        if stack_object.targets is not None:  # TODO: Update targeting to work properly (note to turn illegal targets to 'None')
            for target in stack_object.targets:
                if target.is_legal():
                    break
                else:
                    if stack_object.card is not None:
                        self.put_in_graveyard(stack_object.card.owner, stack_object.card)
                    return
        # Note: a copy of a permanent spell becomes a token as it resolves.
        if stack_object.is_permanent_spell:
            self.create_battlefield_object(stack_object.controller, stack_object.card, casting_information=stack_object.casting_information)
        else:
            stack_object.effect_function(
                self, stack_object.controller, stack_object.source, stack_object.event, stack_object.modes, stack_object.targets)
            if stack_object.card is not None:
                self.put_in_graveyard(stack_object.card.owner, stack_object.card)
        self.apply_effects()

    def check_state_based_actions_and_triggered_abilities(self):
        while True:
            if self.is_ended:
                return
            state_based_action_performed = False
            # If a player has 0 or less life, that player loses the game.
            for player in self.players:
                if player.life <= 0:
                    self.remove_player(player)
                    state_based_action_performed = True
            # If a player attempted to draw a card from a library with no cards in it since
            # the last time state-based actions were checked, that player loses the game.
            for player in self.players:
                if player.decked:
                    self.remove_player(player)
                    player.decked = False
                    state_based_action_performed = True
            # If a token is in a zone other than the battlefield or a copy of a spell is in a
            # zone other than the stack, it ceases to exist.
            zones = [self.exile, self.battlefield, self.stack]
            for player in self.players:
                zones.extend([player.hand, player.graveyard, player.library])
            for zone in zones:
                if zone.name != "Battlefield":
                    removed = zone.remove_by_criteria(lambda p: p.is_token)
                    if removed:
                        state_based_action_performed = True
                if zone.name != "Stack":
                    removed = zone.remove_by_criteria(lambda p: p.is_copy)
                    if removed:
                        state_based_action_performed = True
            # If a creature has toughness 0 or less, it's put into its owner's graveyard.
            for permanent in self.get_permanents():
                if permanent.is_creature and permanent.toughness <= 0:
                    self.permanent_to_graveyard(permanent)
                    state_based_action_performed = True
            # If a creature has toughness greater than 0, it has damage marked on it, and the
            # total damage marked on it is greater than or equal to its toughness, that
            # creature has been dealt lethal damage and is destroyed.
            for permanent in self.get_permanents():
                if permanent.is_creature and permanent.lethal_damage_dealt:
                    self.destroy(permanent)
                    state_based_action_performed = True
            if not state_based_action_performed:
                break
        if len(self.triggers_waiting) > 0:
            for trigger in self.triggers_waiting:  # TODO: Order by APNAP, allow player choice
                self.trigger_ability(trigger)
            self.triggers_waiting = []

    def check_event_for_triggers(self, event):
        self.apply_effects()
        triggered_abilities = self.get_triggered_abilities()
        if isinstance(event, Permanent_Died_Event):
            triggered_abilities.extend(event.permanent.triggered_abilities)
        for ability in triggered_abilities:
            if ability.is_triggered_by(self, event):
                self.triggers_waiting.append(ability.get_trigger(event))
        for listener in self.listeners:
            if listener.dead:
                continue
            if listener.condition_met(self):
                listener.invoke()
        self.listeners = [listener for listener in self.listeners if not listener.dead]

    def apply_effects(self):
        for creature in self.get_creatures():
            creature.power_modification = 0
            creature.toughness_modification = 0
            creature.added_abilities = []  # TODO: All permanents
        effects = []
        effects.extend(self.effects)
        for permanent in self.get_permanents():
            for static in permanent.static_abilities:
                effects.append(static.effect)
        for effect in effects:  # TODO: Layers, layers layers!
            if effect.type == EffectType.PT:
                for creature in self.get_creatures():
                    if effect.applies_to(creature):
                        creature.power_modification += effect.power_change
                        creature.toughness_modification += effect.toughness_change
            if effect.type == EffectType.ABILITY:
                for creature in self.get_creatures():
                    if effect.applies_to(creature):
                        for ability in effect.abilities:
                            creature_ability = ability.copy()  # TODO: This won't work with effects that give abilities with state
                            creature.added_abilities.append(creature_ability)
                            creature_ability.object = creature
        for creature in self.get_creatures():
            if CounterType.P1P1 in creature.counters:
                creature.power_modification += creature.counters[CounterType.P1P1]
                creature.toughness_modification += creature.counters[CounterType.P1P1]

    # Turn actions

    def turn_untap(self):
        active_permanents = self.get_permanents_of(self.active_player)
        for permanent in active_permanents:
            self.untap(permanent)
            permanent.summoning_sick = False

    def turn_draw(self):
        self.player_draw(self.active_player)

    def turn_declare_attackers(self):
        legal_attackers = self.get_legal_attackers(self.active_player)
        targets = self.get_legal_attack_targets(self.active_player)
        attacks = self.active_player.agent.choose_attacks(
            self, legal_attackers, targets)
        for attack in attacks:
            attacker, target = attack
            self.creature_attack(attacker, target)
            if not AbilityKeyword.VIGILANCE in attacker.keywords:
                self.tap(attacker)
        if len(attacks) > 0:
            self.add_step([Phase.COMBAT, Step.COMBAT_DAMAGE])
            self.add_step([Phase.COMBAT, Step.DECLARE_BLOCKERS])
            self.active_player.attacked_this_turn = True
            event = Attack_Event(attacks)
            self.check_event_for_triggers(event)

    def turn_declare_blockers(self):
        for defending_player in self.inactive_players:
            legal_blockers = self.get_legal_blockers(defending_player)
            attackers = self.get_legal_block_targets(defending_player)
            blocks_legally_declared = False
            while not blocks_legally_declared:
                blocks = defending_player.agent.choose_blocks(
                    self, legal_blockers, attackers)
                for block in blocks:
                    blocker, attacker = block
                    self.creature_block(blocker, attacker)
                blocks_legally_declared = True
                for attacker in attackers:
                    if not self.is_blocked_legally(attacker):
                        blocks_legally_declared = False
                        break
                if not blocks_legally_declared:
                    for block in blocks:
                        blocker, attacker = block
                        self.reverse_block(blocker, attacker)

        for attacker in self.get_all_attackers():
            if not attacker.is_blocked:
                self.creature_become_unblocked(attacker)

    def turn_resolve_combat_damage(self):
        for player in self.apnap_order:
            creatures = self.get_all_in_combat_of(player)
            damage_assignment_legally_assigned = False
            while not damage_assignment_legally_assigned:
                damage_assignments = player.agent.choose_damage_assignments(
                    self, creatures)
                for damage_assignment in damage_assignments:
                    damaging_creature, damages = damage_assignment
                    damaging_creature.combat_damage_assignment = damages
                damage_assignment_legally_assigned = True
                for creature in creatures:
                    if not creature.is_unblocked and not self.is_combat_damage_legally_assigned(creature):
                        damage_assignment_legally_assigned = False
                        break
                if not damage_assignment_legally_assigned:
                    for creature in creatures:
                        creature.combat_damage_assignment = []
        for creature in self.get_all_in_combat():
            self.creature_deal_combat_damage(creature)

    def turn_end_combat(self):
        for permanent in self.get_permanents():
            permanent.remove_from_combat()

    def turn_cleanup(self):
        self.player_discard_to_hand_size(self.active_player)
        self.remove_marked_damage_and_end_turn()

    def turn_empty_mana(self):
        for player in self.players:
            player.mana_pool.empty()

    # Events
    def remove_player(self, player):
        player.is_alive = False
        if len(self.get_alive_players()) == 1:
            self.is_ended = True
            self.winner = self.get_alive_players()[0]
        if len(self.get_alive_players()) == 0:
            self.is_ended = True

    def make_land_drop(self, player, land):
        if land not in player.hand.objects:
            raise Exception("Player does not have land in hand.")
        player.hand.remove(land)
        self.create_battlefield_object(player, land.card)
        player.lands_played_this_turn += 1
        return True

    def create_battlefield_object(self, controller, card, casting_information={}, modify_function=None):
        permanent = Permanent(card, controller, self.permanent_id, casting_information=casting_information)
        if modify_function is not None:
            modify_function(permanent)
        self.permanent_id += 1
        # TODO: Update continuous effects here
        event = Permanent_Enter_Event(self, permanent)
        for effect in permanent.replacement_effects:  # TODO: Make replacement effects work right.
            if effect.replaces(event):
                event = effect.replace(event)
        event.execute()
        self.check_event_for_triggers(event)

    def create_token(self, controller, token):
        token.owner = controller
        self.create_battlefield_object(controller, token)

    def put_in_graveyard(self, player, card):  # TODO: Refactor to standardize zone changes!
        grave_card = Graveyard_Object(card)
        player.graveyard.add_objects([grave_card])
        return grave_card

    def permanent_to_graveyard(self, permanent):
        self.battlefield.remove(permanent)
        permanent.is_alive = False
        grave_card = self.put_in_graveyard(permanent.owner, permanent.card)
        event = Permanent_Died_Event(permanent, grave_card)
        if permanent.is_creature:
            self.creature_died_this_turn = True
        self.check_event_for_triggers(event)

    def destroy(self, permanent):
        self.permanent_to_graveyard(permanent)

    def sacrifice(self, player, permanent):
        if (permanent.controller != player):
            return False
        self.permanent_to_graveyard(permanent)

    def exile_from_battlefield(self, permanent):
        self.battlefield.remove(permanent)
        permanent.is_alive = False
        exile_card = Exile_Object(permanent.card)
        self.exile.add_objects([exile_card])
        event = Permanent_Exiled_Event(permanent, exile_card)
        self.check_event_for_triggers(event)
        return event

    def exile_from_graveyard(self, card):
        card.owner.graveyard.remove(card)
        card.is_alive = False
        exile_card = Exile_Object(card)
        self.exile.add_objects([exile_card])

    def exile_until_leaves(self, permanent_exiled, permanent_key):
        if not permanent_key.is_alive:
            return
        exile_event = self.exile_from_battlefield(permanent_exiled)
        exile_card = exile_event.exile_card

        return_listener = Listener(lambda game: not game.has_permanent(permanent_key),
                                   lambda: self.create_battlefield_object(exile_card.owner, exile_card.card))
        self.listeners.append(return_listener)

    def return_permanent_to_hand(self, permanent):
        self.battlefield.remove(permanent)
        permanent.is_alive = False
        owner = permanent.owner
        owner.hand.add_objects([Hand_Object(permanent.card)])

    def return_gravecard_to_battlefield(self, controller, grave_card, modify_function=None):
        grave_card.owner.graveyard.remove(grave_card)
        self.create_battlefield_object(controller, grave_card.card, modify_function=modify_function)

    def counter_stack_object(self, stack_object):
        self.stack.remove(stack_object)
        stack_object.is_alive = False
        if stack_object.card is not None:
            self.put_in_graveyard(stack_object.card.owner, stack_object.card)

    def untap(self, permanent):
        permanent.tapped = False

    def tap(self, permanent):
        permanent.tapped = True

    def put_counters_on(self, counter_type, number, permanent):
        permanent.add_counters(counter_type, number)
        self.apply_effects()

    def attach_permanents(self, base, attachment):
        attachment.attached_permanent = base

    def deal_damage(self, target, source, damage, is_combat_damage=False):
        if damage <= 0:
            return
        event = Damage_Event(target, source, damage, is_combat_damage)
        for effect in self.get_prevention_effects():  # TODO: Function this out with replacement effects
            if effect.applies_to(event):
                event = effect.prevent(event)
        event.execute()
        self.check_event_for_triggers(event)

    def fight(self, creature1, creature2):
        if creature1 == creature2:
            self.deal_damage(creature1, creature1, creature1.power*2)
        self.deal_damage(creature1, creature2, creature2.power)
        self.deal_damage(creature2, creature1, creature1.power)

    def put_on_stack(self, spell_object):
        self.stack.add_objects([spell_object])

    def add_mana(self, player, mana):
        player.mana_pool.add(mana)
        return Mana_Produced_Event(player, mana)

    def player_gain_life(self, player, amount):
        player.life += amount

    def player_draw(self, player):
        if player.library.is_empty():
            return False
        card = Hand_Object(player.library.pop())
        player.hand.add_objects([card])
        player.cards_drawn_this_turn += 1
        event = Card_Draw_Event(card, player.cards_drawn_this_turn)
        self.check_event_for_triggers(event)

    def player_tutor_to_hand(self, player, search_function, amount=1):
        # TODO: Move tutoring to agent.
        tutor_targets = player.library.get_by_criteria(search_function)
        cards = player.agent.choose_x(tutor_targets, amount, message=f'Choose {amount}:')
        for card in cards:
            player.library.remove(card)
            player.hand.add_objects([Hand_Object(card)])
        player.library.shuffle()

    def player_tutor_to_top(self, player, search_function, amount=1):
        tutor_targets = player.library.get_by_criteria(search_function)
        cards = player.agent.choose_x(tutor_targets, amount, message=f'Choose {amount}:')
        for card in cards:
            player.library.remove(card)
        player.library.shuffle()
        player.library.add_objects(cards)

    def player_tutor_to_battlefield(self, player, search_function, amount=1, modify_function=None):
        tutor_targets = player.library.get_by_criteria(search_function)
        cards = player.agent.choose_x(tutor_targets, amount, message=f'Choose {amount}:')
        for card in cards:
            player.library.remove(card)
            self.create_battlefield_object(player, card, modify_function=modify_function)
        player.library.shuffle()

    def player_discard_card(self, player, card):
        if card not in player.hand.objects:
            raise Exception("Can't discard a card that isn't there!")
        player.hand.remove(card)
        self.put_in_graveyard(player, card.card)

    def player_discard_x(self, player, num):
        num = min(num, player.hand.size)
        cards_to_discard = player.agent.choose_cards_to_discard(
            self, player.hand.objects, num)
        for card in cards_to_discard:
            self.player_discard_card(player, card)

    def player_discard_to_hand_size(self, player):
        if player.max_hand_size is not None and player.hand.size > player.max_hand_size:
            self.player_discard_x(player, player.hand.size-player.max_hand_size)

    def player_activate_ability(self, player, ability):
        # Send some sort of signal to the mana manager to provide a backup point.
        self.backup_manager.add_event(Ability_Activate_Begin_Marker(player, ability))
        # If the ability is a mana ability, simply test the costs, then carry it out.
        if ability.is_mana_ability:
            if self.player_pay_cost(player, ability.cost):
                ability.resolve(self, player, None)
        else:
            modes = None  # TODO: Refactor out mode choice and target choice.
            if ability.is_modal:
                modes = self.player_choose_modes(player, ability.mode_choice)
            else:
                modes = ability.mode_choice.modes
            targets = []
            for mode in modes:
                if mode.is_targeted:
                    targets_required = mode.target_types
                    mode_targets = self.player_choose_targets(player, targets_required, source=ability.object)
                    if mode_targets == None:
                        raise Exception("Illegal Action")
                    targets.extend(mode_targets)
            if targets == []:
                targets = None
            activation_object = Ability_Stack_Object(player, StackObjectType.ACTIVATED, effect_function=ability.result_function, source=ability.object,
                                                     targets=targets, modes={ModeType.MODES_CHOSEN: [mode.id for mode in modes]})

            if not self.player_pay_cost(player, ability.cost):
                raise Exception("Illegal Action")
            self.put_on_stack(activation_object)
            event = Activation_Event(activation_object)
            self.check_event_for_triggers(event)
        self.backup_manager.add_event(Ability_Activate_End_Marker(player, ability))

        return True

    def player_cast_spell(self, player, spell):
        self.backup_manager.add_event(Spellcast_Begin_Marker(player, spell))
        if spell not in player.hand.objects:
            raise Exception("Player does not have that spell in hand.")
        player.hand.remove(spell)
        additional_costs = spell.additional_costs
        cost_increase = Total_Cost([])
        costs_paid = []
        modes = []  # TODO: Refactor out mode choice and target choice.
        targets = None
        if len(additional_costs) > 0:
            for additional_cost in additional_costs:
                cost = player.agent.choose_one(additional_cost.cost_options, message="Choose additional cost:")
                if cost is None:
                    continue
                cost_increase += cost
                costs_paid.append(cost)
        if spell.is_volatile:
            if spell.spell_ability.is_modal:
                modes = self.player_choose_modes(player, spell.spell_ability.mode_choice)
            else:
                modes = spell.spell_ability.mode_choice.modes

            targets = []
            for mode in modes:
                if mode.is_targeted:
                    targets_required = mode.target_types
                    mode_targets = self.player_choose_targets(player, targets_required)
                    if mode_targets == None:
                        raise Exception("Illegal Action")
                    targets.extend(mode_targets)
            if targets == []:
                targets = None

        spell_object = Ability_Stack_Object(
            player, StackObjectType.SPELL, effect_function=spell.card.spell_effect, source=None, modes={ModeType.MODES_CHOSEN: [mode.id for mode in modes], ModeType.COSTS_PAID: costs_paid}, targets=targets, card=spell.card)
        spell_object.source = spell_object

        cost = Total_Cost([spell.cost])+cost_increase
        try:
            if not self.player_pay_cost(player, cost):
                raise IllegalActionException("Illegal Action")  # TODO: Tidy up
        except IllegalActionException:
            while not isinstance(self.backup_manager.last_event, Spellcast_Begin_Marker):
                self.backup_manager.reverse_last_event()
            self.backup_manager.reverse_last_event()
            player.hand.add_objects([spell])
            return False
        self.put_on_stack(spell_object)  # TODO: Spells are actually on the stack at the very start of the process.
        self.backup_manager.add_event(Spellcast_End_Marker(player, spell))
        event = Spellcast_Event(spell_object)
        self.check_event_for_triggers(event)
        return True

    def trigger_ability(self, ability):
        controller = ability.controller
        modes = None
        if ability.is_modal:
            modes = self.player_choose_modes(controller, ability.mode_choice)
        else:
            modes = ability.mode_choice.modes

        targets = []
        for mode in modes:
            if mode.is_targeted:
                targets_required = mode.target_types
                mode_targets = self.player_choose_targets(controller, targets_required, source=ability.object)
                if mode_targets == None:  # TODO: Make modes without valid targets un-choosable.
                    return
                targets.extend(mode_targets)
        if targets == []:
            targets = None
        result_function = ability.result_function
        if ability.intervening_if_conditional is not None:
            def new_result_function(game, controller, source, event, modes, targets):
                if ability.intervening_if_conditional(game, event, source):
                    return ability.result_function(game, controller, source, event, modes, targets)
            result_function = new_result_function

        trigger_object = Ability_Stack_Object(controller, StackObjectType.TRIGGERED, effect_function=result_function, source=ability.object,
                                              targets=targets, modes={ModeType.MODES_CHOSEN: [mode.id for mode in modes]}, event=ability.event)
        self.put_on_stack(trigger_object)
        event = Trigger_Stack_Event(trigger_object)
        self.check_event_for_triggers(event)

    def player_activate_mana(self, player, cost):
        while True:
            ability = player.agent.mana_act(self, player, cost)
            if not ability:
                break
            self.player_activate_ability(player, ability)

    def player_pay_cost(self, player, cost):
        mana_cost = [mana_sym for mana_cost in cost.mana_cost for mana_sym in mana_cost.mana_cost]
        if len(mana_cost) > 0:
            self.player_activate_mana(player, cost)
        mana_to_pay = player.agent.choose_mana_to_pay(
            self, player.mana_pool, mana_cost)
        if mana_to_pay is None:
            return False
        tap_cost = cost.tap_cost
        permanents_to_tap = player.agent.choose_permanents_to_pay_cost(self, self.get_tappable_permanents_of(player), tap_cost, cost.object)
        if permanents_to_tap is None:
            return False

        sacrifice_cost = cost.sacrifice_cost
        permanents_to_sacrifice = player.agent.choose_permanents_to_pay_cost(
            self, self.get_permanents_of(player), sacrifice_cost, cost.object)
        if permanents_to_sacrifice is None:
            return False

        player.mana_pool.remove(mana_to_pay)
        for permanent in permanents_to_tap:
            self.tap(permanent)
        for permanent in permanents_to_sacrifice:
            self.sacrifice(player, permanent)
        return True

    def player_choose_targets(self, player, targets_required, source=None):
        targets = player.agent.choose_targets(self, player, targets_required, source)
        if targets is None:
            raise Exception("Illegal Action")
        return targets

    def player_choose_modes(self, player, mode_choice):
        mode = player.agent.choose_modes(self, mode_choice)
        return mode

    def creature_attack(self, creature, target):
        creature.is_attacking = True
        creature.attack_target = target

    def creature_block(self, blocker, attacker):
        blocker.is_blocking = True
        blocker.blocking.append(attacker)
        attacker.is_blocked = True
        attacker.blockers.append(blocker)

    def reverse_block(self, blocker, attacker):
        blocker.is_blocking = False
        blocker.blocking.remove(attacker)
        attacker.is_blocked = False
        attacker.blockers.remove(blocker)

    def creature_become_unblocked(self, creature):
        creature.is_unblocked = True

    def creature_deal_combat_damage(self, creature):
        for damage_amount, target in creature.combat_damage_assignment:
            self.deal_damage(target, creature, damage_amount, is_combat_damage=True)

    def remove_marked_damage_and_end_turn(self):
        for permanent in self.get_permanents():
            permanent.remove_marked_damage()
        self.effects = [effect for effect in self.effects if effect.duration != EffectDuration.EOT]
        self.apply_effects()

    def create_continuous_effect(self, effect):
        self.effects.append(effect)
        self.apply_effects()

    # Direct Gamestate Editing functions
    def add_permanents(self, controller, cards):
        for card in cards:
            card.set_owner(controller)
            permanent = Permanent(card, controller, self.permanent_id)
            self.permanent_id += 1
            self.battlefield.add_objects([permanent])

    def add_cards(self, player, cards):
        for card in cards:
            card.set_owner(player)
        player.hand.add_objects([Hand_Object(card) for card in cards])

    def add_gravecards(self, player, cards):
        for card in cards:
            card.set_owner(player)
        player.graveyard.add_objects([Graveyard_Object(card) for card in cards])

    def add_to_library(self, player, cards):
        for card in cards:
            card.set_owner(player)
        player.library.add_objects(cards)

    # Display functions
    def display(self):
        # White 255
        # Red 196
        # Blue 21
        # Green 76
        # Black 234
        # Gold 220
        # Gray 110
        colors = [255, 21, 234, 196, 76, 110, 220]
        canvas_width = 180
        canvas_height = 60
        card_width = 8
        card_height = 8

        p1_hand_y = 0
        p2_hand_y = (canvas_height-(card_height+2))
        p1_lands_y = p1_hand_y+card_height+4
        p2_lands_y = p2_hand_y-(card_height+3)
        p1_battlefield_y = p1_lands_y+(card_height+1)
        p2_battlefield_y = p2_lands_y-(card_height+1)

        p1_noncreatures_x = 1+card_width*8
        p2_noncreatures_x = 1+card_width*8
        p1_noncreatures_y = p1_lands_y
        p2_noncreatures_y = p2_lands_y

        p1_graveyard_y = p1_hand_y
        p2_graveyard_y = p2_hand_y
        graveyard_card_width = 20
        graveyard_card_height = card_height+2
        player_graveyard_x = canvas_width-graveyard_card_width

        player_card_width = 20
        player_card_height = 5
        player_card_x = 0
        player1_card_y = p1_hand_y
        player2_card_y = p2_hand_y

        turn_card_width = 20
        turn_card_height = 5
        turn_card_x = canvas_width-turn_card_width
        turn_card_y = p2_hand_y-turn_card_height

        stack_card_width = 20
        stack_card_height = 10
        stack_card_x = canvas_width-stack_card_width
        stack_card_y = p1_lands_y

        end_card_width = 20
        end_card_height = 5
        end_card_x = canvas_width//2-end_card_width//2
        end_card_y = canvas_height//2-end_card_height//2

        canvas = Text_Canvas(canvas_width, canvas_height)

        def draw_card(x, y, card_object):
            color = colors[card_object.card.color_vis.value]
            if isinstance(card_object, Permanent) and card_object.tapped:
                canvas.draw_rect(x, y, card_width, card_height, 176)
            else:
                canvas.draw_rect(x, y, card_width, card_height, 0)
            canvas.draw_rect(x+1, y+1, card_width-2, card_height-2, color)

            text = card_object.name
            text_width = card_width-2
            for i in range((len(text)-1)//text_width+1):
                canvas.draw_text(x+1, y+1+i, card_object.name[i*text_width:min((i+1)*text_width, len(text))], 0, color)
            if card_object.is_creature:
                pow_tough = f"{card_object.power}/{card_object.toughness}"
                if isinstance(card_object, Permanent):
                    pow_tough = f"{card_object.power}/{card_object.toughness-card_object.marked_damage}"
                canvas.draw_text(x+(card_width-1)-len(pow_tough), y+card_height-2, pow_tough, 0, color)

        canvas.draw_rect(0, p1_hand_y+card_height+2, canvas_width, 1, 0)
        canvas.draw_rect(0, p2_hand_y-1, canvas_width, 1, 0)

        # Player Hands
        for i, card in enumerate(self.players[0].hand.objects):
            draw_card(player_card_width+1+i*(card_width+1), p1_hand_y+1, card)
        for i, card in enumerate(self.players[1].hand.objects):
            draw_card(player_card_width+1+i*(card_width+1), p2_hand_y+1, card)

        # Player Graveyards
        canvas.draw_rect(player_graveyard_x, p1_graveyard_y, graveyard_card_width, graveyard_card_height, 0)
        canvas.draw_rect(player_graveyard_x+1, p1_graveyard_y+1, graveyard_card_width-2, graveyard_card_height-2, 255)
        canvas.draw_text(player_graveyard_x+1, p1_graveyard_y+1, "Graveyard", 0, 255)
        for i, card in enumerate(self.players[0].graveyard.objects):
            canvas.draw_text(player_graveyard_x+1, p1_graveyard_y+1+(i+1), card.name, 0, 255)

        canvas.draw_rect(player_graveyard_x, p2_graveyard_y, graveyard_card_width, graveyard_card_height, 0)
        canvas.draw_rect(player_graveyard_x+1, p2_graveyard_y+1, graveyard_card_width-2, graveyard_card_height-2, 255)
        canvas.draw_text(player_graveyard_x+1, p2_graveyard_y+1, "Graveyard", 0, 255)
        for i, card in enumerate(self.players[1].graveyard.objects):
            canvas.draw_text(player_graveyard_x+1, p2_graveyard_y+1+(i+1), card.name, 0, 255)

        # Battlefield
        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[0] and p.is_land)):
            draw_card(1+i*(card_width+1), p1_lands_y, permanent)
        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[1] and p.is_land)):
            draw_card(1+i*(card_width+1), p2_lands_y, permanent)

        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[0] and not (p.is_creature or p.is_land))):
            draw_card(p1_noncreatures_x+i*(card_width+1), p1_noncreatures_y, permanent)
            if permanent.attached_permanent is not None:
                canvas.draw_text(p1_noncreatures_x+i*(card_width+1), p1_noncreatures_y +
                                 card_height, f"Atchd {permanent.attached_permanent.name}", 0, 255)
        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[1] and not (p.is_creature or p.is_land))):
            draw_card(p2_noncreatures_x+i*(card_width+1), p2_noncreatures_y, permanent)
            if permanent.attached_permanent is not None:
                canvas.draw_text(p1_noncreatures_x+i*(card_width+1), p1_noncreatures_y +
                                 card_height, f"Atchd {permanent.attached_permanent.name}", 0, 255)

        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[0] and p.is_creature)):
            draw_card(1+i*(card_width+1), p1_battlefield_y, permanent)
        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[1] and p.is_creature)):
            draw_card(1+i*(card_width+1), p2_battlefield_y, permanent)

        # Stack
        canvas.draw_rect(stack_card_x, stack_card_y, stack_card_width, stack_card_height, 0)
        canvas.draw_rect(stack_card_x+1, stack_card_y+1, stack_card_width-2, stack_card_height-2, 255)
        canvas.draw_text(stack_card_x+1, stack_card_y+1, "Stack", 0, 255)
        for i, stack_object in enumerate(self.stack.objects):
            canvas.draw_text(stack_card_x+1, stack_card_y+1+(i+1), stack_object.name, 0, 255)

        # Turn Box
        canvas.draw_rect(turn_card_x, turn_card_y, turn_card_width, turn_card_height, 0)
        canvas.draw_rect(turn_card_x+1, turn_card_y+1, turn_card_width-2, turn_card_height-2, 255)
        canvas.draw_text(turn_card_x+1, turn_card_y+1, f"Turn {self.turn_number}", 0, 255)
        canvas.draw_text(turn_card_x+1, turn_card_y+2, f"Phase: {self.current_phase.name}", 0, 255)
        canvas.draw_text(turn_card_x+1, turn_card_y+3, f"Step: {self.current_step.name}", 0, 255)

        # Player Cards
        canvas.draw_rect(player_card_x, player1_card_y, player_card_width, player_card_height, 0)
        canvas.draw_rect(player_card_x+1, player1_card_y+1, player_card_width-2, player_card_height-2, 255)
        canvas.draw_text(player_card_x+1, player1_card_y+1, self.players[0].name, 0, 255)
        canvas.draw_text(player_card_x+1, player1_card_y+2, f"Life: {self.players[0].life}", 0, 255)

        canvas.draw_rect(player_card_x, player2_card_y, player_card_width, player_card_height, 0)
        canvas.draw_rect(player_card_x+1, player2_card_y+1, player_card_width-2, player_card_height-2, 255)
        canvas.draw_text(player_card_x+1, player2_card_y+1, self.players[1].name, 0, 255)
        canvas.draw_text(player_card_x+1, player2_card_y+2, f"Life: {self.players[1].life}", 0, 255)

        # Game End Box
        if self.is_ended:
            canvas.draw_rect(end_card_x, end_card_y, end_card_width, end_card_height, 0)
            canvas.draw_rect(end_card_x+1, end_card_y+1, end_card_width-2, end_card_height-2, 255)
            canvas.draw_text(end_card_x+1, end_card_y+end_card_height//2, f"{self.winner} Wins!", 0, 255)

        canvas.display()
