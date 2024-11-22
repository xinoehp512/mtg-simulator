class Spell_Ability:
    def __init__(self, result_function, mode_choice) -> None:
        self.result_function = result_function
        self.mode_choice = mode_choice

    @property
    def is_modal(self):
        return self.mode_choice.mode_number > 1

    def copy(self):
        return Spell_Ability(self.result_function, self.mode_choice)
