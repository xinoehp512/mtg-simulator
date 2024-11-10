from enums import ManaCost


class Mana:

    def __init__(self, type, source, restrictions=None):
        self.type = type
        self.source = source
        self.restrictions = restrictions

    def __str__(self):
        return self.type.name

    __repr__ = __str__


class ManaPool:

    def __init__(self) -> None:
        self.mana = []

    def add(self, m):
        self.mana.extend(m)

    def empty(self):
        self.pool = []

    def remove(self, manas):
        for mana in manas:
            self.mana.remove(mana)

    def get_payable_to(self, cost):
        return [m for m in self.mana if cost_paid_by(cost, m)]


def cost_paid_by(mana_cost, mana):
    if mana_cost == ManaCost.GENERIC:
        return True
    return mana_cost.value == mana.type.value
