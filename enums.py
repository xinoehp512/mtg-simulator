from enum import Enum


class Privacy(Enum):
    PUBLIC = 0
    PRIVATE = 1
    HIDDEN = 2


class Phase(Enum):
    NONE = -1
    BEGINNING = 0
    MAIN = 1
    COMBAT = 2
    ENDING = 3


class Step(Enum):
    NONE = -1
    UNTAP = 0
    UPKEEP = 1
    DRAW = 2
    COMBAT_BEGIN = 3
    DECLARE_ATTACKERS = 4
    DECLARE_BLOCKERS = 5
    COMBAT_DAMAGE = 7
    COMBAT_END = 8
    END = 9
    CLEANUP = 10


class CardType(Enum):
    LAND = 0
    CREATURE = 1
    ARTIFACT = 2
    ENCHANTMENT = 3
    INSTANT = 4
    SORCERY = 5


class BasicLandType(Enum):
    PLAINS = 0
    ISLAND = 1
    SWAMP = 2
    MOUNTAIN = 3
    FOREST = 4


class TargetType(Enum):
    DAMAGEABLE = 0
    CREATURE = 1


class EffectDuration(Enum):
    EOT = 0


class EffectType(Enum):
    PT = 0


class Color(Enum):
    WHITE = 0
    BLUE = 1
    BLACK = 2
    RED = 3
    GREEN = 4


class ManaType(Enum):
    WHITE = 0
    BLUE = 1
    BLACK = 2
    RED = 3
    GREEN = 4
    COLORLESS = 5


class ManaCost(Enum):
    WHITE = 0
    BLUE = 1
    BLACK = 2
    RED = 3
    GREEN = 4
    COLORLESS = 5
    GENERIC = 6


class ColorVis(Enum):
    WHITE = 0
    BLUE = 1
    BLACK = 2
    RED = 3
    GREEN = 4
    COLORLESS = 5
    MULTICOLOR = 6


def cost_to_colors(symbol):
    if symbol.value == 5 or symbol.value == 6:
        return []
    else:
        return [Color(symbol.value)]


def color_to_vis(color):
    return ColorVis(color.value)
