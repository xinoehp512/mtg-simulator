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


class ArtifactType(Enum):
    FOOD = 1


class CreatureType(Enum):
    ANGEL = 0
    ARCHER = 1
    BEAST = 2
    BERSERKER = 3
    BIRD = 4
    CAT = 5
    CLERIC = 6
    CYCLOPS = 7
    DEVIL = 8
    DINOSAUR = 9
    DRUID = 10
    DWARF = 11
    ELEMENTAL = 12
    ELEPHANT = 13
    ELF = 14
    GIANT = 15
    GOBLIN = 16
    GOLEM = 17
    HUMAN = 18
    HYENA = 19
    KNIGHT = 20
    LIZARD = 21
    MINOTAUR = 22
    NOBLE = 23
    OTTER = 24
    PIRATE = 25
    RABBIT = 26
    RANGER = 27
    RAT = 28
    ROGUE = 29
    SCOUT = 30
    SERPENT = 31
    SHARK = 32
    SKELETON = 33
    SOLDIER = 34
    SPIDER = 35
    TURTLE = 36
    VAMPIRE = 37
    WALL = 38
    WARLOCK = 39
    WARRIOR = 40
    WIZARD = 41
    WOLF = 42
    ZOMBIE = 43


class AbilityKeyword(Enum):
    FLASH = 0
    VIGILANCE = 1
    HASTE = 2
    TRAMPLE = 3


class TargetType(Enum):
    DAMAGEABLE = 0
    CREATURE = 1
    CREATURE_YOU_CONTROL = 2
    NL_PERMANENT_OPP_CONTROL = 3
    OPT_GRAVECARD = 4
    CREATURE_OPP_CONTROL = 5
    CREATURE_DONT_CONTROL = 6  # Are these two the same? Not in team games!


class EffectDuration(Enum):
    EOT = 0


class EffectType(Enum):
    PT = 0
    ABILITY = 1


class CounterType(Enum):
    P1P1 = 0


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
