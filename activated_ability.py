class Activated_Ability:
    def __init__(self, name, cost, result_function, mode_choice, activation_restrictions=[], is_mana_ability=False, mana_produced=None) -> None:
        self.name = name
        self.cost = cost
        self.result_function = result_function
        self.mode_choice = mode_choice

        self.activation_restrictions = activation_restrictions
        self.is_mana_ability = is_mana_ability
        self.mana_produced = mana_produced
        self._object = None

    @property
    def is_modal(self):
        return self.mode_choice.mode_number > 1

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, object):
        self._object = object
        self.cost.object = object

    def resolve(self, game, player, targets):
        return self.result_function(game, player, self.object, targets)

    def copy(self):
        return Activated_Ability(self.name, self.cost.copy(), self.result_function, self.mode_choice, activation_restrictions=self.activation_restrictions, is_mana_ability=self.is_mana_ability, mana_produced=self.mana_produced)
