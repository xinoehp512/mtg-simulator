from targetable_object import Targetable_Object


class Ability_Stack_Object(Targetable_Object):

    def __init__(self, controller, effect_function=None, targets=None, mode=None, card=None):
        super().__init__()
        self.effect_function = effect_function
        self.controller = controller
        self.targets = targets
        self.mode = mode
        self.card = card

    @property
    def is_token(self):
        return False

    @property
    def is_copy(self):
        return False

    @property
    def is_permanent_spell(self):
        return self.card is not None and self.card.is_permanent
