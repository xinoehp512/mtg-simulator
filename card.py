from activated_ability import Activated_Ability
from cost import Additional_Cost
from enums import CardType, ColorVis, SuperType, color_to_vis, cost_to_colors, AbilityKeyword
from keyword_ability import Keyword_Ability


class Card:

    def __init__(self, name, cost, colors, types, abilities, text) -> None:
        self.name = name
        self.cost = cost
        self.color_indicator = colors
        self.types = types
        self.abilities = abilities
        self.text = text
        self.owner = None
        self.is_alive = True

        self.is_token = False
        self.is_copy = False

    # Deck Setup Functions

    def set_owner(self, player):
        self.owner = player
        return self

    def copy(self):
        return Card(self.name, self.cost, self.color_indicator, self.types,
                    [ability.copy() for ability in self.abilities], self.text)

    # Properties
    @property
    def colors(self):
        if self.cost is None:
            return self.color_indicator
        colors = set(self.color_indicator)
        for cost_sym in self.cost.mana_cost:
            for color in cost_to_colors(cost_sym):
                colors.add(color)
        return list(colors)

    @property
    def color_vis(self):
        colors = []
        for color in self.colors:
            colors.append(color_to_vis(color))
        for ability in self.abilities:
            if isinstance(ability, Activated_Ability) and ability.mana_produced is not None:
                colors.extend(color_to_vis(color) for color in ability.mana_produced)

        if len(colors) == 1:
            return colors[0]
        elif len(colors) == 0:
            return ColorVis.COLORLESS
        else:
            return ColorVis.MULTICOLOR

    @property
    def is_basic(self):
        return SuperType.BASIC in self.types

    @property
    def is_creature(self):
        return CardType.CREATURE in self.types

    @property
    def is_land(self):
        return CardType.LAND in self.types

    @property
    def is_artifact(self):
        return CardType.ARTIFACT in self.types

    @property
    def is_enchantment(self):
        return CardType.ENCHANTMENT in self.types

    @property
    def is_planeswalker(self):
        return CardType.PLANESWALKER in self.types

    @property
    def is_spell(self):
        return not self.is_land

    @property
    def is_instant(self):
        return CardType.INSTANT in self.types

    @property
    def is_volatile(self):
        return CardType.INSTANT in self.types or CardType.SORCERY in self.types

    @property
    def is_instant_speed(self):
        if self.is_instant:
            return True
        for ability in self.abilities:
            if isinstance(ability, Keyword_Ability) and ability.keyword_ability == AbilityKeyword.FLASH:
                return True
        return False

    @property
    def additional_costs(self):
        return [ability for ability in self.abilities if isinstance(ability, Additional_Cost)]

    @property
    def spell_ability(self):
        if not self.is_volatile:
            raise Exception("Permanents do not have spell abilities")
        return self.abilities[0]

    @property
    def spell_effect(self):
        return self.spell_ability.result_function if self.is_volatile else lambda g, c, t: False

    @property
    def is_permanent(self):
        return not self.is_volatile

    def __str__(self):
        return self.name

    __repr__ = __str__


class Creature_Card(Card):

    def __init__(self, name, cost, types, abilities,  power, toughness, text="", color_indicator=[]):
        super().__init__(name, cost, color_indicator, types, abilities, text)
        self.power = power
        self.toughness = toughness

    def copy(self):
        return Creature_Card(self.name, self.cost, self.types,
                             [ability.copy() for ability in self.abilities],
                             self.power, self.toughness, text=self.text, color_indicator=self.color_indicator)


class Enchantment_Card(Card):
    def __init__(self, name, cost, types, abilities, text="", color_indicator=[]):
        super().__init__(name, cost, color_indicator, types, abilities, text)

    def copy(self):
        return Enchantment_Card(self.name, self.cost, self.types, [ability.copy() for ability in self.abilities], text=self.text, color_indicator=self.color_indicator)


class Land_Card(Card):

    def __init__(self, name, types, abilities, text=""):
        super().__init__(name, None, [], types, abilities, text)

    def copy(self):
        return Land_Card(self.name, self.types,
                         [ability.copy() for ability in self.abilities], text=self.text)


class Instant_Card(Card):

    def __init__(self, name, cost, types, abilities, text=""):
        super().__init__(name, cost, [], types, abilities, text)

    def copy(self):
        return Instant_Card(self.name, self.cost, self.types,
                            [ability.copy() for ability in self.abilities], text=self.text)


class Sorcery_Card(Card):
    def __init__(self, name, cost, types, abilities, text=""):
        super().__init__(name, cost, [], types, abilities, text)

    def copy(self):
        return Sorcery_Card(self.name, self.cost, self.types,
                            [ability.copy() for ability in self.abilities], text=self.text)


class Creature_Token(Card):
    def __init__(self, name, cost, types, abilities, power, toughness, text="", color_indicator=[]):
        super().__init__(name, cost, color_indicator, types, abilities, text)
        self.power = power
        self.toughness = toughness
        self.is_token = True

    def copy(self):
        return Creature_Token(self.name, self.cost, self.types,
                              [ability.copy() for ability in self.abilities],
                              self.power, self.toughness, text=self.text, color_indicator=self.color_indicator)


class Artifact_Token(Card):
    def __init__(self, name, cost, types, abilities, text="", color_indicator=[]):
        super().__init__(name, cost, color_indicator, types, abilities, text)
        self.is_token = True

    def copy(self):
        return Artifact_Token(self.name, self.cost, self.types,
                              [ability.copy() for ability in self.abilities], text=self.text)
