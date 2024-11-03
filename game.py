
from ability_stack_object import Ability_Stack_Object
from action import Action
from agent import Agent
from canvas import Text_Canvas
from enums import EffectDuration, EffectType, Phase, Privacy, Step, TargetType
from exceptions import IllegalActionException
from graveyard_object import Graveyard_Object
from hand_object import Hand_Object
from permanent import Permanent
from player import Player
from target import Target
from zone import Zone


class Backup_Manager:
    def __init__(self) -> None:
        self.currently_reversible_actions = []
        self.reversible_actions_stack = []

    def begin_dangerous_operation(self):
        self.reversible_actions_stack.append(self.currently_reversible_actions)
        self.currently_reversible_actions = []

    def end_dangerous_operation(self):
        self.currently_reversible_actions = self.reversible_actions_stack.pop()

    def add_reverse(self, reverse):
        self.currently_reversible_actions.append(reverse)


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

        self.permanent_id = 0

        self.effects = []
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

    def get_alive_players(self):
        return [player for player in self.players if player.is_alive]

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
            for card in player.hand.get_by_criteria(lambda x: x.is_spell and not x.is_instant):
                actions.append(
                    Action(descriptor=f"Cast: {card.name}", action=create_spellcast_action(card)))
        for card in player.hand.get_by_criteria(lambda x: x.is_spell and x.is_instant):
            actions.append(
                Action(descriptor=f"Cast: {card.name}", action=create_spellcast_action(card)))
        return actions

    def get_permanents(self):
        return self.battlefield.get_by_criteria(lambda obj: True)

    def get_permanents_of(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.controller == player)

    def get_creatures(self):
        return self.battlefield.get_by_criteria(lambda p: p.is_creature)

    def get_activated_abilities_of(self, player):
        permanents_with_ability = self.battlefield.get_by_criteria(
            lambda p: p.controller == player and p.has_activated_ability)
        return [ability for permanent in permanents_with_ability for ability in permanent.activated_abilities if ability.can_be_activated_by(self, player)]

    def get_mana_abilities_of(self, player):
        return [
            ability for ability in self.get_activated_abilities_of(player)
            if ability.is_mana_ability
        ]
    # Targeting

    def get_damageable(self):
        damageable = []
        damageable.extend(self.players)
        damageable.extend(self.battlefield.get_by_criteria(lambda p: p.is_damageable))
        return damageable

    def get_targets(self, target_type):
        if target_type == TargetType.DAMAGEABLE:
            return [Target(lambda t: isinstance(t, Player) or (isinstance(t, Permanent) and t.is_damageable), target) for target in self.get_damageable()]
        if target_type == TargetType.CREATURE:
            return [Target(lambda t: isinstance(t, Permanent) and t.is_creature, target) for target in self.get_creatures()]
    # Combat Query functions

    def get_legal_attackers(self, player):
        return self.battlefield.get_by_criteria(lambda p: p.controller == player and p.is_creature and not p.summoning_sick and not p.tapped)

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

    def is_combat_damage_legally_assigned(self, creature):
        for defending_creature in creature.combat_damage_assigned[:-1]:
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
            player.lands_played_this_turn = 0
        self.add_turn()

    def advance_step(self):
        if len(self.step_queue) == 0:
            raise Exception("Step queue is empty.")
        step = self.step_queue.pop(0)
        self.current_phase = step[0]
        self.current_step = step[1]

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
            self.check_state_based_actions()
            if self.is_ended:
                return
            priority_player_index = self.active_player_index
            num_players_passing = 0
            while num_players_passing < self.num_players:
                priority_player = self.players[priority_player_index]
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
            self.resolve_stack_object(self.stack.pop())

    def resolve_stack_object(self, stack_object):
        stack_object.is_alive = False
        if stack_object.targets is not None:
            for target in stack_object.targets:
                if target.is_legal():
                    break
                else:
                    if stack_object.card is not None:
                        self.put_in_graveyard(
                            stack_object.card.owner, stack_object.card)
                    return
        # Note: a copy of a permanent spell becomes a token as it resolves.
        if stack_object.is_permanent_spell:
            self.create_battlefield_object(
                stack_object.controller, stack_object.card)
        else:
            stack_object.effect_function(
                self, stack_object.controller, stack_object.targets)

    def check_state_based_actions(self):
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
                    self.put_in_graveyard(permanent.owner, permanent)
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

    def apply_effects(self):
        for creature in self.get_creatures():
            creature.power_modification = 0
            creature.toughness_modification = 0
        for effect in self.effects:
            if effect.type == EffectType.PT:
                for creature in self.get_creatures():
                    if effect.applies_to(creature):
                        creature.power_modification += effect.power_change
                        creature.toughness_modification += effect.toughness_change
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
            self.tap(attacker)
        if len(attacks) > 0:
            self.add_step([Phase.COMBAT, Step.COMBAT_DAMAGE])
            self.add_step([Phase.COMBAT, Step.DECLARE_BLOCKERS])

    def turn_declare_blockers(self):
        for defending_player in self.inactive_players:
            legal_blockers = self.get_legal_blockers(defending_player)
            attackers = self.get_legal_block_targets(defending_player)
            blocks = defending_player.agent.choose_blocks(
                self, legal_blockers, attackers)
            for block in blocks:
                blocker, attacker = block
                self.creature_block(blocker, attacker)

        for attacker in self.get_all_attackers():
            if not attacker.is_blocked:
                self.creature_become_unblocked(attacker)

        for player in self.apnap_order:
            damage_orders = player.agent.choose_damage_order(
                self, self.get_requiring_damage_order(player))
            for damage_order in damage_orders:
                creature, order = damage_order
                creature.combat_damage_order = order

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
    def make_land_drop(self, player, land):
        if land not in player.hand.objects:
            raise Exception("Player does not have land in hand.")
        player.hand.remove(land)
        self.create_battlefield_object(player, land.card)
        player.lands_played_this_turn += 1
        return True

    def create_battlefield_object(self, controller, card):
        permanent = Permanent(card, controller, self.permanent_id)
        self.permanent_id += 1
        self.battlefield.add_objects([permanent])

    def create_token(self, controller, token):
        token.owner = controller
        self.create_battlefield_object(controller, token)

    def put_in_graveyard(self, player, card):
        grave_card = Graveyard_Object(card)
        player.graveyard.add_objects([grave_card])

    def remove_player(self, player):
        player.is_alive = False
        if len(self.get_alive_players()) == 1:
            self.is_ended = True
            self.winner = self.get_alive_players()[0]
        if len(self.get_alive_players()) == 0:
            self.is_ended = True

    def destroy(self, permanent):
        self.battlefield.remove(permanent)
        permanent.is_alive = False
        self.put_in_graveyard(permanent.owner, permanent.card)

    def untap(self, permanent):
        permanent.tapped = False

    def tap(self, permanent):
        permanent.tapped = True

    def deal_damage(self, target, damage):
        target.take_damage(damage)

    def put_on_stack(self, spell_object):
        self.stack.add_objects([spell_object])

    def add_mana(self, player, mana):
        player.mana_pool.add(mana)

    def player_draw(self, player):
        player.hand.add_objects([Hand_Object(player.library.pop())])

    def player_discard(self, player, card):
        if card not in player.hand.objects:
            raise Exception("Can't discard a card that isn't there!")
        player.hand.remove(card)
        self.put_in_graveyard(player, card.card)

    def player_discard_to_hand_size(self, player):
        if player.max_hand_size is not None and player.hand.size > player.max_hand_size:
            cards_to_discard = player.agent.choose_cards_to_discard(
                self, player.hand.objects, player.hand.size-player.max_hand_size)
            for card in cards_to_discard:
                self.player_discard(player, card)

    def player_activate_ability(self, player, ability):
        # Send some sort of signal to the mana manager to provide a backup point.

        # If the ability is a mana ability, simply test the costs, then carry it out.
        if ability.is_mana_ability:
            if ability.pay_cost(self, player):
                ability.resolve(self, player, None)
                if ability.reversible:
                    self.backup_manager.add_reverse(Action(f"Reverse {ability}", lambda: ability.reverse(self, player)))
            else:
                # This exception indicates a rollback needs to take place.
                raise Exception("Illegal Action")
        return True

    def player_cast_spell(self, player, spell):
        self.backup_manager.begin_dangerous_operation()
        if spell not in player.hand.objects:
            raise Exception("Player does not have that spell in hand.")
        player.hand.remove(spell)
        targets = None
        if spell.is_volatile and spell.spell_ability.is_targeted:
            targets_required = spell.spell_ability.target_types
            targets = self.player_choose_targets(player, targets_required)

        spell_object = Ability_Stack_Object(
            player, spell.card.spell_effect, targets=targets, card=spell.card)
        cost = spell.cost
        self.player_activate_mana(player, cost)
        try:
            self.player_pay_cost(player, cost)
        except IllegalActionException:
            while True:
                action = player.agent.reverse_action(self, player, self.backup_manager.currently_reversible_actions)
                if action:
                    try:
                        action.invoke()
                        self.backup_manager.currently_reversible_actions.remove(action)
                    except IllegalActionException:
                        print("Can't reverse that!")
                else:
                    break
            player.hand.add_objects([spell])
            self.backup_manager.end_dangerous_operation()
            return False
        self.put_on_stack(spell_object)
        self.backup_manager.end_dangerous_operation()
        return True

    def player_activate_mana(self, player, cost):
        while True:
            ability = player.agent.mana_act(self, player, cost)
            if not ability:
                break
            self.player_activate_ability(player, ability)

    def player_pay_cost(self, player, cost):
        mana_to_pay = player.agent.choose_mana_to_pay(
            self, player.mana_pool, cost)
        if mana_to_pay is None:
            raise IllegalActionException("Illegal Action")
        player.mana_pool.remove(mana_to_pay)

    def player_choose_targets(self, player, targets_required):
        targets = player.agent.choose_targets(self, targets_required)
        if targets is None:
            raise Exception("Illegal Action")
        return targets

    def creature_attack(self, creature, target):
        creature.is_attacking = True
        creature.attack_target = target

    def creature_block(self, blocker, attacker):
        blocker.is_blocking = True
        blocker.blocking.append(attacker)
        attacker.is_blocked = True
        attacker.blockers.append(blocker)

    def creature_become_unblocked(self, creature):
        creature.is_unblocked = True

    def creature_deal_combat_damage(self, creature):
        for damage_amount, target in creature.combat_damage_assignment:
            self.deal_damage(target, damage_amount)

    def remove_marked_damage_and_end_turn(self):
        for permanent in self.get_permanents():
            permanent.remove_marked_damage()
        self.effects = [effect for effect in self.effects if effect.duration != EffectDuration.EOT]

    def create_continuous_effect(self, effect):
        self.effects.append(effect)
        self.apply_effects()

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

        player_card_width = 20
        player_card_height = 5
        player_card_x = 0
        player1_card_y = p1_hand_y
        player2_card_y = p2_hand_y

        turn_card_width = 20
        turn_card_height = 5
        turn_card_x = canvas_width-turn_card_width
        turn_card_y = canvas_height-turn_card_height

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

        # Battlefield
        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[0] and p.is_land)):
            draw_card(1+i*(card_width+1), p1_lands_y, permanent)
        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[1] and p.is_land)):
            draw_card(1+i*(card_width+1), p2_lands_y, permanent)

        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[0] and not p.is_land)):
            draw_card(1+i*(card_width+1), p1_battlefield_y, permanent)
        for i, permanent in enumerate(self.battlefield.get_by_criteria(lambda p: p.controller == self.players[1] and not p.is_land)):
            draw_card(1+i*(card_width+1), p2_battlefield_y, permanent)

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
