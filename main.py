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
game.add_cards(player1, [cards.erudite_wizard.copy(), cards.draw.copy()])
game.add_cards(player2, [cards.forest.copy() for i in range(1)])
game.add_permanents(player1, [cards.island.copy() for i in range(6)])
game.add_permanents(player2, [cards.beast_kin_ranger.copy(), cards.campus_guide.copy(), cards.dazzling_angel.copy()])
game.add_to_library(player1, [cards.draw.copy() for i in range(5)])

game.play_game()
