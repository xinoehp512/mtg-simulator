from enums import ZoneType


class Static_Ability:
    def __init__(self, effect, functions_in=[ZoneType.BATTLEFIELD]):
        self.effect = effect
        self._object = None
        self.functions_in = functions_in

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, object):
        self._object = object
        self.effect.object = object

    def copy(self):
        return Static_Ability(self.effect, functions_in=self.functions_in)
