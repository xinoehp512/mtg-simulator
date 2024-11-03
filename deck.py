class Deck:

    def __init__(self, cards):
        self.cards = cards

    def copy(self):
        return Deck([card.copy() for card in self.cards])

    def get_cards(self):
        return self.cards

    def set_owner(self, player):
        for card in self.cards:
            card.set_owner(player)
        return self
