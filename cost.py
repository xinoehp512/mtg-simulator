from enums import CostType, ManaCost, ZoneType


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


class Discard_Cost:
    def __init__(self, acceptance_function, name=""):
        self.acceptance_function = acceptance_function
        self.name = name

    def __str__(self):
        return self.name
    __repr__ = __str__


class Total_Cost:
    def __init__(self, costs, type=None):
        self.costs = costs  # TODO: Combine mana costs into one
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

    @property
    def discard_cost(self):
        return [cost for cost in self.costs if isinstance(cost, Discard_Cost)]

    def reduce_by(self, other):
        mana_reduction = [mana_cost for cost in other.costs if isinstance(cost, Mana_Cost) for mana_cost in cost.mana_cost]
        self_mana_cost = [mana_cost for cost in self.costs if isinstance(cost, Mana_Cost) for mana_cost in cost.mana_cost]
        for mana_cost in mana_reduction:
            if mana_cost in self_mana_cost:
                self_mana_cost.remove(mana_cost)
        self.costs = [cost for cost in self.costs if not isinstance(cost, Mana_Cost)]
        self.costs.append(Mana_Cost(self_mana_cost))

    def copy(self):
        return Total_Cost(self.costs, type=self.type)

    def __str__(self):
        return str(self.costs)

    def __add__(self, other):
        return Total_Cost(self.costs+other.costs)

    __repr__ = __str__


class Additional_Cost:
    def __init__(self, cost_options, functions_in=[ZoneType.STACK]):
        self.cost_options = cost_options
        self.functions_in = functions_in

    def copy(self):
        return Additional_Cost(self.cost_options, functions_in=self.functions_in)


class Alternative_Cost:
    def __init__(self, cost, zones, functions_in=[ZoneType.STACK]):
        self.cost = cost
        self.zones = zones
        self.functions_in = functions_in

    def copy(self):
        return Alternative_Cost(self.cost, self.zones, functions_in=self.functions_in)
