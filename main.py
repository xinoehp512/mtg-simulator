import random

from agent import Agent
from enums import CounterType
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
player2.starting_hand_size = 0
game.add_cards(player1, [cards.run_away_together.copy()])
game.add_cards(player2, [cards.forest.copy()])
game.add_permanents(player1, [cards.treasure.copy() for i in range(6)]+[cards.campus_guide.copy()])
game.add_permanents(player2, [cards.island.copy() for i in range(3)]+[cards.apothecary_stomper.copy() for i in range(2)])
game.add_to_library(player1, [cards.mountain.copy(), cards.forest.copy(),
                    cards.bloodfell_caves.copy(), cards.island.copy(), cards.blossoming_sands.copy()])
game.add_to_library(player2, [cards.mountain.copy(), cards.forest.copy(),
                    cards.bloodfell_caves.copy(), cards.island.copy(), cards.blossoming_sands.copy()])
game.play_game()
