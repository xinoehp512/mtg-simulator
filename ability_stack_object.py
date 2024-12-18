from enums import CostType, CastingInformationType, ModeType
from replacement_effect import Replacement_Effect
from targetable_object import Targetable_Object


class Ability_Stack_Object(Targetable_Object):

    def __init__(self, controller, stack_object_type, source=None, event=None, effect_function=None, targets=None, modes=None, card=None):
        super().__init__()
        self.effect_function = effect_function
        self.controller = controller
        self.type = stack_object_type
        self.source = source
        self.event = event
        self.targets = targets
        self.modes = modes
        self.card = card
        if self.card is not None:
            for ability in self.card.abilities:
                ability.object = self

    @property
    def is_token(self):
        return False

    @property
    def is_copy(self):
        return False

    @property
    def is_spell(self):
        return self.card is not None

    @property
    def is_permanent_spell(self):
        return self.card is not None and self.card.is_permanent

    @property
    def is_instant(self):
        return self.card is not None and self.card.is_instant

    @property
    def is_sorcery(self):
        return self.card is not None and self.card.is_sorcery

    @property
    def abilities(self):
        return self.card.abilities if self.card is not None else []

    @property
    def replacement_effects(self):
        return [ability for ability in self.abilities if isinstance(ability, Replacement_Effect)]

    @property
    def keywords(self):
        return []

    @property
    def name(self):
        if self.card is not None:
            return self.card.name
        else:
            return self.type.name+":"+self.source.name

    @property
    def casting_information(self):
        was_kicked = CostType.KICKED in [cost.type for cost in self.modes[ModeType.COSTS_PAID]]
        information = {CastingInformationType.KICKED: was_kicked}
        return information
