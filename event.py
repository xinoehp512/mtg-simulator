from enums import AbilityKeyword
from permanent import Permanent


class Event:
    def __init__(self):
        self.occurred = False
        self.child_events = []

    def contains(self, event):
        return event in self.child_events

    def undo(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError


class Ability_Activate_Begin_Marker(Event):
    def __init__(self, player, ability):
        super().__init__()
        self.player = player
        self.ability = ability

    def undo(self):
        pass


class Ability_Activate_End_Marker(Event):
    def __init__(self, player, ability):
        super().__init__()
        self.player = player
        self.ability = ability

    def undo(self):
        pass


class Spellcast_Begin_Marker(Event):
    def __init__(self, player, spell):
        super().__init__()
        self.player = player
        self.spell = spell

    def undo(self):
        pass


class Spellcast_End_Marker(Event):
    def __init__(self, player, spell):
        super().__init__()
        self.player = player
        self.spell = spell

    def undo(self):
        pass


class Mana_Produced_Event(Event):
    def __init__(self, player, mana_produced):
        super().__init__()
        self.player = player
        self.mana_produced = mana_produced

    def undo(self):
        self.player.mana_pool.remove(self.mana_produced)


class Permanent_Tapped_Event(Event):
    def __init__(self, permanent):
        super().__init__()
        self.permanent = permanent

    def undo(self):
        self.permanent.tapped = False


class Mana_Ability_Event(Event):
    def __init__(self, cost_event, mana_produced_event):
        super().__init__()
        self.cost_event = cost_event
        self.mana_produced_event = mana_produced_event

    def undo(self):
        self.mana_produced_event.undo()
        self.cost_event.undo()


class Permanent_Enter_Event(Event):
    def __init__(self, game, permanent):
        super().__init__()
        self.game = game
        self.permanent = permanent

    def execute(self, game):
        game.battlefield.add_objects([self.permanent])
        self.occurred = True

    def copy(self):
        return Permanent_Enter_Event(self.game, self.permanent)


class Permanent_Exiled_Event(Event):
    def __init__(self, permanent, exile_card):
        super().__init__()
        self.permanent = permanent
        self.exile_card = exile_card


class Permanent_Died_Event(Event):
    def __init__(self, permanent, grave_card):
        super().__init__()
        self.permanent = permanent
        self.grave_card = grave_card


class Attack_Event(Event):
    def __init__(self, attacks):
        super().__init__()
        self.attacks = attacks

    @property
    def num_attacking(self):
        return len(self.attacks)

    @property
    def attackers(self):
        return [attacker for attacker, target in self.attacks]


class Step_Begin_Event(Event):
    def __init__(self, step, player):
        super().__init__()
        self.step = step
        self.player = player

    def copy(self):
        return Step_Begin_Event(self.step, self.player)


class Targeting_Event(Event):
    def __init__(self):
        super().__init__()


class Spellcast_Event(Event):
    def __init__(self, spell_object):
        super().__init__()
        self.spell_object = spell_object
        self.child_events = []
        if spell_object.targets is not None:
            self.child_events.append(Targeting_Event)

    @property
    def targets(self):
        return [target.object for target in self.stack_object.targets]

    @property
    def stack_object(self):
        return self.spell_object


class Activation_Event(Event):
    def __init__(self, activation_object):
        super().__init__()
        self.activation_object = activation_object
        self.child_events = []
        if activation_object.targets is not None:
            self.child_events.append(Targeting_Event)

    @property
    def targets(self):
        return [target.object for target in self.stack_object.targets]

    @property
    def stack_object(self):
        return self.activation_object


class Trigger_Stack_Event(Event):
    def __init__(self, trigger_object):
        super().__init__()
        self.trigger_object = trigger_object
        self.child_events = []
        if trigger_object.targets is not None:
            self.child_events.append(Targeting_Event)

    @property
    def targets(self):
        return [target.object for target in self.stack_object.targets]

    @property
    def stack_object(self):
        return self.trigger_object


class Card_Draw_Event(Event):
    def __init__(self, card, number_this_turn):
        super().__init__()
        self.card = card
        self.number_this_turn = number_this_turn


class Damage_Event(Event):
    def __init__(self, target, source, damage_amount, is_combat_damage, prevented=False):
        super().__init__()
        self.target = target
        self.source = source
        self.damage_amount = damage_amount
        self.is_combat_damage = is_combat_damage
        self.prevented = prevented

    def execute(self, game):
        if self.prevented:
            return
        self.target.take_damage(self.damage_amount)
        if AbilityKeyword.LIFELINK in self.source.keywords:
            game.player_gain_life(self.source.controller, self.damage_amount)
        if AbilityKeyword.DEATHTOUCH in self.source.keywords and isinstance(self.target, Permanent):
            self.target.is_deathtouched = True
        self.occurred = True

    def copy(self):
        return Damage_Event(self.target, self.source, self.damage_amount, self.is_combat_damage, prevented=self.prevented)


class Lifegain_Event(Event):
    def __init__(self, player, amount):
        super().__init__()
        self.player = player
        self.amount = amount

    def copy(self):
        return Lifegain_Event(self.player, self.amount)
