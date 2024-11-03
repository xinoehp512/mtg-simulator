from enums import EffectType


class Effect:
    def __init__(self, type, duration):
        self.type = type
        self.duration = duration


class PT_Effect(Effect):
    def __init__(self, duration, applicability_function, power_change, toughness_change):
        super().__init__(EffectType.PT, duration)
        self.applicability_function = applicability_function
        self.power_change = power_change
        self.toughness_change = toughness_change

    def applies_to(self, object):
        return self.applicability_function(object)
