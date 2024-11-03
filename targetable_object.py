class Targetable_Object:

    def __init__(self):
        # This becomes false when the object changes zones.
        self.is_alive = True

    def make_dead(self):
        self.is_alive = False
