from enums import ZoneType


class Cost_Modification:
    def __init__(self, conditional, cost, is_reduction, functions_in=[ZoneType.STACK]):
        self.conditional = conditional
        self.cost = cost
        self.is_reduction = is_reduction
        self.functions_in = functions_in

    def copy(self):
        return Cost_Modification(self.conditional, self.cost, self.is_reduction, functions_in=self.functions_in)
