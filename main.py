import random

from agent import Agent
from game import Game
from objects.decks import *

random.seed(1)
with open("user_input.txt", "w") as file:
    file.write("")

# game = Game([Agent("Player 1", deck1), Agent("Player 2", deck2)])
game = Game([Agent("Player 1", deck_empty), Agent("Player 2", deck_empty)])

# TODO: Add test suites

player1 = game.players[0]
player2 = game.players[1]
player1.starting_hand_size = 0
game.add_cards(player1, [cards.bushwhack.copy()])
game.add_cards(player2, [cards.forest.copy()])
game.add_permanents(player1, [cards.forest.copy() for i in range(1)]+[cards.apothecary_stomper.copy()])
game.add_permanents(player2, [cards.beast_kin_ranger.copy()])
game.add_to_library(player1, [cards.forest.copy() for i in range(3)]+[cards.mountain.copy() for i in range(3)])


game.play_game()
