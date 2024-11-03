from activated_ability import Activated_Ability
from damageable_object import Damageable_Object


class Permanent(Damageable_Object):

    def __init__(self, card, controller, id):
        super().__init__()
        self.card = card
        self.controller = controller
        self.id = id

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
        self._combat_damage_order = []
        self.combat_damage_assignment = []

        # Effects
        self.power_modification = 0
        self.toughness_modification = 0

        self.marked_damage = 0
        for ability in self.card.abilities:
            ability.object = self
    # Static Properties

    @property
    def name(self):
        return self.card.name

    @property
    def is_creature(self):
        return self.card.is_creature

    @property
    def is_land(self):
        return self.card.is_land

    @property
    def is_token(self):
        return self.card.is_token

    @property
    def is_copy(self):
        return self.card.is_copy

    @property
    def owner(self):
        return self.card.owner

    @property
    def power(self):
        return self.card.power+self.power_modification if self.card.power is not None else 0

    @property
    def toughness(self):
        return self.card.toughness+self.toughness_modification if self.card.toughness is not None else 0

    @property
    def is_damageable(self):
        return self.is_creature

    @property
    def has_activated_ability(self):
        for ability in self.card.abilities:
            if isinstance(ability, Activated_Ability):
                return True

    @property
    def activated_abilities(self):
        abilities = []
        for ability in self.card.abilities:
            if isinstance(ability, Activated_Ability):
                abilities.append(ability)
        return abilities

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
            return list(self.blockers)
        elif self.is_blocking:
            return list(self.blocking)
        else:
            raise Exception("Not blocked or blocking")

    @property
    def combat_damage_order(self):
        self._combat_damage_order = [
            creature for creature in self._combat_damage_order
            if creature.is_alive and creature.in_combat
        ]
        return self._combat_damage_order

    @combat_damage_order.setter
    def combat_damage_order(self, value):
        self._combat_damage_order = value

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
        self._combat_damage_order = []

    def take_damage(self, damage):
        self.marked_damage += damage

    def remove_marked_damage(self):
        self.marked_damage = 0

    def __str__(self):
        return str(self.card)

    __repr__ = __str__
