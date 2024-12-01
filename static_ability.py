class Static_Ability:
    def __init__(self, effect):
        self.effect = effect

    def copy(self):
        return Static_Ability(self.effect)
