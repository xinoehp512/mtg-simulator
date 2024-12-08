class Cost_Modification:
    def __init__(self, conditional, cost, is_reduction):
        self.conditional = conditional
        self.cost = cost
        self.is_reduction = is_reduction

    def copy(self):
        return Cost_Modification(self.conditional, self.cost, self.is_reduction)
