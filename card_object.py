from cost import Alternative_Cost
from cost_modification import Cost_Modification
from targetable_object import Targetable_Object


class Card_Object(Targetable_Object):
    def __init__(self, card) -> None:
        super().__init__()
        self.card = card
        for ability in self.card.abilities:
            ability.object = self
    # Properties

    @property
    def name(self):
        return self.card.name

    @property
    def cost(self):
        return self.card.cost

    @property
    def owner(self):
        return self.card.owner

    @property
    def controller(self):
        return self.owner

    @property
    def is_creature(self):
        return self.card.is_creature

    @property
    def is_land(self):
        return self.card.is_land

    @property
    def is_spell(self):
        return self.card.is_spell

    @property
    def is_instant(self):
        return self.card.is_instant

    @property
    def is_instant_speed(self):
        return self.card.is_instant_speed

    @property
    def is_volatile(self):
        return self.card.is_volatile

    @property
    def is_permanent(self):
        return self.card.is_permanent

    @property
    def additional_costs(self):
        return self.card.additional_costs

    @property
    def spell_ability(self):
        return self.card.spell_ability

    @property
    def cost_modifications(self):
        abilities = []
        for ability in self.card.abilities:
            if isinstance(ability, Cost_Modification):
                abilities.append(ability)
        return abilities

    @property
    def alternative_costs(self):
        return [ability for ability in self.card.abilities if isinstance(ability, Alternative_Cost)]

    @property
    def is_token(self):
        return self.card.is_token

    @property
    def is_copy(self):
        return self.card.is_copy

    @property
    def power(self):
        return self.card.power if self.card.power is not None else 0

    @property
    def toughness(self):
        return self.card.toughness if self.card.toughness is not None else 0

    def __str__(self):
        return self.card.name

    __repr__ = __str__
