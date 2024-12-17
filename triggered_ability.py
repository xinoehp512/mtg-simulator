from enums import ZoneType


class Triggered_Ability:
    def __init__(self, trigger_function, mode_choice, result_function, intervening_if_conditional=None, functions_in=[ZoneType.BATTLEFIELD]):
        self.trigger_function = trigger_function
        self.mode_choice = mode_choice
        self.result_function = result_function
        self.intervening_if_conditional = intervening_if_conditional
        self.functions_in = functions_in
        self.object = None

    def is_triggered_by(self, game, event):
        if self.intervening_if_conditional is None or self.intervening_if_conditional(game, event, self.object):
            return self.trigger_function(game, event, self.object)
        return False

    def get_trigger(self, event):
        return Trigger_Instance(self, self.object.controller, event)

    def copy(self):
        return Triggered_Ability(self.trigger_function, self.mode_choice, self.result_function, intervening_if_conditional=self.intervening_if_conditional, functions_in=self.functions_in)


class Trigger_Instance:
    def __init__(self, ability, controller, event):
        self.ability = ability
        self.controller = controller
        self.event = event

    @property
    def mode_choice(self):
        return self.ability.mode_choice

    @property
    def is_modal(self):
        return self.ability.mode_choice.mode_number > 1

    @property
    def result_function(self):
        return self.ability.result_function

    @property
    def object(self):
        return self.ability.object

    @property
    def intervening_if_conditional(self):
        return self.ability.intervening_if_conditional
