from enums import AdditionalCostType, ManaCost


class Mana_Cost:
    def __init__(self, mana):
        self.mana_cost = mana

    @classmethod
    def from_string(cls, str):
        mana_cost = []
        mana_key = {"W": ManaCost.WHITE, "U": ManaCost.BLUE, "B": ManaCost.BLACK, "R": ManaCost.RED, "G": ManaCost.GREEN}
        for symbol in str:
            if symbol.isnumeric():
                mana_cost += [ManaCost.GENERIC]*int(symbol)
            else:
                mana_cost += [mana_key[symbol]]
        return cls(mana_cost)

    def __str__(self):
        return "Pay "+str(self.mana_cost.count(ManaCost.GENERIC))+"W"*self.mana_cost.count(ManaCost.WHITE)+"U"*self.mana_cost.count(ManaCost.BLUE)+"B"*self.mana_cost.count(ManaCost.BLACK)+"R"*self.mana_cost.count(ManaCost.RED)+"G"*self.mana_cost.count(ManaCost.GREEN)

    __repr__ = __str__


class Sacrifice_Cost:
    def __init__(self, acceptance_function, name=""):
        self.acceptance_function = acceptance_function
        self.name = name

    def __str__(self):
        return self.name
    __repr__ = __str__


class Tap_Cost:
    def __init__(self, acceptance_function, name=""):
        self.acceptance_function = acceptance_function
        self.name = name

    def __str__(self):
        return self.name
    __repr__ = __str__


class Total_Cost:
    def __init__(self, costs, type=None):
        self.costs = costs
        self.type = type
        self.object = None

    @property
    def mana_cost(self):
        return [cost for cost in self.costs if isinstance(cost, Mana_Cost)]

    @property
    def sacrifice_cost(self):
        return [cost for cost in self.costs if isinstance(cost, Sacrifice_Cost)]

    @property
    def tap_cost(self):
        return [cost for cost in self.costs if isinstance(cost, Tap_Cost)]

    def copy(self):
        return Total_Cost(self.costs, type=self.type)

    def __str__(self):
        return str(self.costs)

    def __add__(self, other):
        return Total_Cost(self.costs+other.costs)

    __repr__ = __str__


class Additional_Cost:
    def __init__(self, cost_options):
        self.cost_options = cost_options

    def copy(self):
        return Additional_Cost(self.cost_options)
