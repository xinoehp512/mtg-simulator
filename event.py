class Event:
    def __init__(self):
        self.occurred = False

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

    def execute(self):
        self.game.battlefield.add_objects([self.permanent])
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


class Step_Begin_Event(Event):
    def __init__(self, step, player):
        super().__init__()
        self.step = step
        self.player = player

    def copy(self):
        return Step_Begin_Event(self.step, self.player)
