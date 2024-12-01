from damageable_object import Damageable_Object
from enums import Privacy
from hand_object import Hand_Object
from mana import ManaPool
from zone import Zone


class Player(Damageable_Object):
    def __init__(self, agent, game) -> None:
        super().__init__()
        self.hand = Zone(name="Hand", privacy=Privacy.PRIVATE,
                         assigned_player=self)
        self.graveyard = Zone(
            name="Graveyard", privacy=Privacy.PUBLIC, assigned_player=self)
        self.library = Zone(
            name="Library", privacy=Privacy.HIDDEN, assigned_player=self)
        self.mana_pool = ManaPool()

        self.life = 0
        self.starting_life = 20
        self.starting_hand_size = 7
        self.max_hand_size = 7
        self.land_drops_per_turn = 1

        self.lands_played_this_turn = 0
        self.cards_drawn_this_turn = 0
        self.attacked_this_turn = False

        self.decked = False

        self.agent = agent
        self.game = game

        self.name = agent.get_name()

    def start_game(self):
        self.life = self.starting_life
        self.library.add_objects(
            self.agent.get_deck().set_owner(self).get_cards())
        self.library.shuffle()

        starting_hand = []
        for _ in range(self.starting_hand_size):
            if self.library.is_empty():
                break
            starting_hand.append(Hand_Object(self.library.pop()))
        self.hand.add_objects(starting_hand)

    def take_damage(self, damage):
        self.life -= damage

    def reset_turn_counters(self):
        self.lands_played_this_turn = 0
        self.cards_drawn_this_turn = 0
        self.attacked_this_turn = False

    def __str__(self):
        return self.name

    __repr__ = __str__
