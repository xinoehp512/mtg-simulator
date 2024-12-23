from activated_ability import Activated_Ability
from damageable_object import Damageable_Object
from keyword_ability import Keyword_Ability
from replacement_effect import Replacement_Effect
from static_ability import Static_Ability
from triggered_ability import Triggered_Ability


class Permanent(Damageable_Object):

    def __init__(self, card, controller, id, casting_information={}):
        super().__init__()
        self.card = card
        self.base_controller = controller
        self.id = id
        self.casting_information = casting_information

        self.summoning_sick = True
        self.tapped = False

        # Combat
        self.is_attacking = False
        self.is_blocking = False
        self.attack_target = None
        self.blocking = []
        self.is_unblocked = False
        self.is_blocked = False
        self.blockers = []
        self.combat_damage_assignment = []

        # Effects
        self.power_modification = 0
        self.toughness_modification = 0
        self.added_abilities = []
        self.modified_controller = None
        self.additional_effects = []

        self.counters = {}

        self.attached_permanent = None

        self.marked_damage = 0
        self.is_deathtouched = False
        for ability in self.card.abilities:
            ability.object = self
    # Static Properties

    @property
    def name(self):
        return self.card.name

    @property
    def types(self):
        return self.card.types

    @property
    def is_creature(self):
        return self.card.is_creature

    @property
    def is_land(self):
        return self.card.is_land

    @property
    def is_artifact(self):
        return self.card.is_artifact

    @property
    def is_enchantment(self):
        return self.card.is_enchantment

    @property
    def is_planeswalker(self):
        return self.card.is_planeswalker

    @property
    def is_token(self):
        return self.card.is_token

    @property
    def is_copy(self):
        return self.card.is_copy

    @property
    def is_damageable(self):
        return self.is_creature

    @property
    def owner(self):
        return self.card.owner

    @property
    def controller(self):
        return self.base_controller if self.modified_controller is None else self.modified_controller

    @property
    def power(self):
        return self.card.power+self.power_modification if self.card.power is not None else 0

    @property
    def toughness(self):
        return self.card.toughness+self.toughness_modification if self.card.toughness is not None else 0

    @property
    def abilities(self):
        return self.card.abilities+self.added_abilities

    @property
    def has_activated_ability(self):
        for ability in self.abilities:
            if isinstance(ability, Activated_Ability):
                return True

    @property
    def has_triggered_ability(self):
        for ability in self.abilities:
            if isinstance(ability, Triggered_Ability):
                return True

    @property
    def has_static_ability(self):
        for ability in self.abilities:
            if isinstance(ability, Static_Ability):
                return True

    @property
    def activated_abilities(self):
        abilities = []
        for ability in self.abilities:
            if isinstance(ability, Activated_Ability):
                abilities.append(ability)
        return abilities

    @property
    def triggered_abilities(self):  # TODO: make these functions work like the bottom two
        abilities = []
        for ability in self.abilities:
            if isinstance(ability, Triggered_Ability):
                abilities.append(ability)
        return abilities

    @property
    def static_abilities(self):
        return [ability for ability in self.abilities if isinstance(ability, Static_Ability)]

    @property
    def replacement_effects(self):
        return [ability for ability in self.abilities if isinstance(ability, Replacement_Effect)]

    @property
    def keywords(self):
        keywords = []
        for ability in self.abilities:
            if isinstance(ability, Keyword_Ability):
                keywords.append(ability.keyword_ability)
        return keywords

    # Dynamic Properties

    @property
    def lethal_damage_dealt(self):
        return self.toughness - self.marked_damage <= 0

    @property
    def in_combat(self):
        return self.is_attacking or self.is_blocking

    @property
    def combat_foes(self):
        if self.is_blocked:
            return [blocker for blocker in self.blockers if blocker.is_alive]
        elif self.is_blocking:
            return [attacker for attacker in self.blocking if attacker.is_alive]
        else:
            raise Exception("Not blocked or blocking")

    @property
    def combat_damage_assigned(self):
        return [creature for damage, creature in self.combat_damage_assignment]

    #
    def remove_from_combat(self):
        self.is_attacking = False
        self.is_blocking = False
        self.attack_target = None
        self.blocking = []
        self.is_unblocked = False
        self.is_blocked = False
        self.blockers = []

    def take_damage(self, damage):
        self.marked_damage += damage

    def remove_marked_damage(self):
        self.marked_damage = 0

    def add_counters(self, counter_type, number):
        if number == 0:
            return
        if counter_type in self.counters:
            self.counters[counter_type] += number
        else:
            self.counters[counter_type] = number

    def __str__(self):
        return str(self.card)

    __repr__ = __str__
