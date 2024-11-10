class Activated_Ability:
    def __init__(self, name, cost_predicate, cost_function, result_function, is_mana_ability=False, mana_produced=None) -> None:
        self.name = name
        self.cost_predicate = cost_predicate
        self.cost_function = cost_function
        self.result_function = result_function
        self.is_mana_ability = is_mana_ability
        self.mana_produced = mana_produced
        self.object = None

    def can_be_activated_by(self, game, player):
        return self.cost_predicate(game, player, self.object)

    def pay_cost(self, game, player):
        return self.cost_function(game, player, self.object)

    def resolve(self, game, player, targets):
        return self.result_function(game, player, self.object, targets)

    def copy(self):
        return Activated_Ability(self.name, self.cost_predicate, self.cost_function, self.result_function, is_mana_ability=self.is_mana_ability, mana_produced=self.mana_produced)
