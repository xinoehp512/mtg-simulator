class Replacement_Effect:
    def __init__(self, applicability_function, modify_function):
        self.applicability_function = applicability_function
        self.modify_function = modify_function
        self.object = None

    def replaces(self, event):
        return self.applicability_function(event, self.object)

    def replace(self, event):
        return self.modify_function(event)

    def copy(self):
        return Replacement_Effect(applicability_function=self.applicability_function, modify_function=self.modify_function)
