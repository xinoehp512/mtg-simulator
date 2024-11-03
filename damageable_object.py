from targetable_object import Targetable_Object


class Damageable_Object(Targetable_Object):

    def __init__(self):
        super().__init__()

    def take_damage(self, _damage) -> None:
        raise Exception("take_damage() not implemented.")
