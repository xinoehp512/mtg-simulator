class Static_Ability:
    def __init__(self, effect):
        self.effect = effect
        self._object = None

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, object):
        self._object = object
        self.effect.object = object

    def copy(self):
        return Static_Ability(self.effect)
