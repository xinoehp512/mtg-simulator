from enums import ZoneType


class Cost_Modification:
    def __init__(self, calc_function, is_reduction, functions_in=[ZoneType.STACK]):
        self.calc_function = calc_function
        self.is_reduction = is_reduction
        self.functions_in = functions_in

    def copy(self):
        return Cost_Modification(self.calc_function, self.is_reduction, functions_in=self.functions_in)
