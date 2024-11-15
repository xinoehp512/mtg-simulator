class Triggered_Ability:
    def __init__(self, trigger_function, target_types, result_function):
        self.trigger_function = trigger_function
        self.target_types = target_types
        self.result_function = result_function
        self.object = None

    @property
    def is_targeted(self):
        return self.target_types is not None

    def is_triggered_by(self, event):
        return self.trigger_function(event, self.object)

    def get_trigger(self):
        return Trigger_Instance(self, self.object.controller)

    def copy(self):
        return Triggered_Ability(self.trigger_function, self.target_types, self.result_function)


class Trigger_Instance:
    def __init__(self, ability, controller):
        self.ability = ability
        self.controller = controller

    @property
    def is_targeted(self):
        return self.ability.is_targeted

    @property
    def target_types(self):
        return self.ability.target_types

    @property
    def result_function(self):
        return self.ability.result_function
