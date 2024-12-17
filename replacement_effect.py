from enums import ZoneType


class Replacement_Effect:  # TODO: Make replacement effect a static effect
    def __init__(self, applicability_function, modify_function, functions_in=[ZoneType.BATTLEFIELD]):
        self.applicability_function = applicability_function
        self.modify_function = modify_function
        self.functions_in = functions_in
        self.object = None

    def replaces(self, event):
        return self.applicability_function(event, self.object)

    def replace(self, event):
        return self.modify_function(event, self.object)

    def copy(self):
        return Replacement_Effect(applicability_function=self.applicability_function, modify_function=self.modify_function, functions_in=self.functions_in)
