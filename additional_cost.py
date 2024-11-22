from enums import AdditionalCostType


class Additional_Cost:
    def __init__(self, cost, optional, paid_marker):
        self.cost = cost
        self.optional = optional
        self.paid_marker = paid_marker

    def copy(self):
        raise NotImplementedError

    def __str__(self):
        return f"Cost: {self.cost}"
    __repr__ = __str__


class Kicker(Additional_Cost):
    def __init__(self, cost):
        super().__init__(cost, True, AdditionalCostType.KICKED)

    def copy(self):
        return Kicker(self.cost)
