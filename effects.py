from enums import EffectType


class Effect:
    def __init__(self, type, duration, applicability_function):
        self.type = type
        self.duration = duration
        self.applicability_function = applicability_function

    def applies_to(self, object):
        return self.applicability_function(object)


class PT_Effect(Effect):
    def __init__(self, duration, applicability_function, power_change, toughness_change):
        super().__init__(EffectType.PT, duration, applicability_function)
        self.power_change = power_change
        self.toughness_change = toughness_change


class Ability_Grant_Effect(Effect):
    def __init__(self, duration, applicability_function, abilities):
        super().__init__(EffectType.ABILITY, duration, applicability_function)
        self.abilities = abilities
