class Triggered_Ability:
    def __init__(self, trigger_function, mode_choice, result_function):
        self.trigger_function = trigger_function
        self.mode_choice = mode_choice
        self.result_function = result_function
        self.object = None

    def is_triggered_by(self, game, event):
        return self.trigger_function(game, event, self.object)

    def get_trigger(self, event):
        return Trigger_Instance(self, self.object.controller, event)

    def copy(self):
        return Triggered_Ability(self.trigger_function, self.mode_choice, self.result_function)


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
