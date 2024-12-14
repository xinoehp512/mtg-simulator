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
game.add_cards(player1, [])
game.add_cards(player2, [cards.forest.copy()])
game.add_permanents(player1, [cards.treasure.copy() for i in range(6)]+[cards.sower_of_chaos.copy()])
game.add_permanents(player2, [cards.island.copy() for i in range(3)]+[cards.apothecary_stomper.copy(), cards.beast_kin_ranger.copy()])
game.add_to_library(player1, [cards.mountain.copy(), cards.forest.copy(),
                    cards.bloodfell_caves.copy(), cards.island.copy(), cards.blossoming_sands.copy()])
game.add_to_library(player2, [cards.mountain.copy(), cards.forest.copy(),
                    cards.bloodfell_caves.copy(), cards.island.copy(), cards.blossoming_sands.copy()])
game.add_gravecards(player1, [cards.campus_guide.copy(), cards.forest.copy(), cards.sanguine_syphoner.copy()])
game.add_gravecards(player2, [cards.axgard_cavalry.copy(), cards.mountain.copy(), cards.island.copy()])
game.play_game()
