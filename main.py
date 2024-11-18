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

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.ambush_wolf.copy()])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.forest.copy(), cards.forest.copy(), cards.forest.copy()])
# game.add_permanents(player2, [cards.forest.copy(), cards.forest.copy(), cards.forest.copy()])
# game.add_gravecards(player1, [cards.forest.copy()])
# game.add_gravecards(player2, [cards.ambush_wolf.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.apothecary_stomper.copy()])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.forest.copy() for i in range(6)])
# game.add_permanents(player2, [cards.aegis_turtle.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.armasaur_guide.copy()])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.plains.copy() for i in range(6)] +
#                     [cards.aegis_turtle.copy(), cards.ambush_wolf.copy(), cards.apothecary_stomper.copy()])
# game.add_permanents(player2, [cards.aegis_turtle.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.axgard_cavalry.copy()])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.mountain.copy() for i in range(2)]+[cards.axgard_cavalry.copy()])
# game.add_permanents(player2, [cards.aegis_turtle.copy()])

player1 = game.players[0]
player2 = game.players[1]
game.add_cards(player1, [cards.apothecary_stomper.copy(), cards.haste_test_card.copy()])
game.add_cards(player2, [cards.forest.copy()])
game.add_permanents(player1, [cards.forest.copy() for i in range(6)]+[cards.mountain.copy()])
game.add_permanents(player2, [cards.aegis_turtle.copy()])

game.play_game()
