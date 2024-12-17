from card_object import Card_Object
from enums import ZoneType


class Graveyard_Object(Card_Object):
    def __init__(self, card) -> None:
        super().__init__(card)

    @property
    def can_cast(self):  # TODO: Move can_cast into Card Object
        for alternative_cost in self.alternative_costs:
            if ZoneType.GRAVEYARD in alternative_cost.zones:
                return True
        return False
