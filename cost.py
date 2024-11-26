from enums import AdditionalCostType, CostType, ManaCost


class Cost:
    def __init__(self, costs, type=None):
        self.costs = costs
        self.type = type

    @property
    def mana_cost(self):
        return [cost for cost in self.costs if isinstance(cost, ManaCost)]

    @property
    def sacrifice_cost(self):
        return [cost for cost in self.costs if cost == CostType.SAC_CREATURE]

    @classmethod
    def from_string(cls, str, type=None):
        mana_cost = []
        mana_key = {"W": ManaCost.WHITE, "U": ManaCost.BLUE, "B": ManaCost.BLACK, "R": ManaCost.RED, "G": ManaCost.GREEN}
        for symbol in str:
            if symbol.isnumeric():
                mana_cost += [ManaCost.GENERIC]*int(symbol)
            else:
                mana_cost += [mana_key[symbol]]
        return cls(mana_cost, type=type)

    def __str__(self):
        return str(self.costs)

    def __add__(self, other):
        return Cost(self.costs+other.costs)

    __repr__ = __str__


class Additional_Cost:
    def __init__(self, cost_options):
        self.cost_options = cost_options

    def copy(self):
        return Additional_Cost(self.cost_options)
