class Spell_Ability:
    def __init__(self, name, result_function, target_types) -> None:
        self.name = name
        self.result_function = result_function
        self.target_types = target_types

    @property
    def is_targeted(self):
        return self.target_types is not None

    def copy(self):
        return Spell_Ability(self.name, self.result_function, self.target_types)
