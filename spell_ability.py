from enums import ZoneType


class Spell_Ability:
    def __init__(self, result_function, mode_choice, functions_in=[ZoneType.STACK]) -> None:
        self.result_function = result_function
        self.mode_choice = mode_choice
        self.functions_in = functions_in

    @property
    def is_modal(self):
        return self.mode_choice.mode_number > 1

    def copy(self):
        return Spell_Ability(self.result_function, self.mode_choice, functions_in=self.functions_in)
