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
# game.add_cards(player1, [cards.apothecary_stomper.copy()])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.forest.copy() for i in range(6)]+[cards.axgard_cavalry.copy()])
# game.add_permanents(player2, [cards.aegis_turtle.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.bake_into_a_pie.copy()])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.swamp.copy() for i in range(6)])
# game.add_permanents(player2, [cards.aegis_turtle.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.banishing_light.copy()])
# game.add_cards(player2, [cards.forest.copy(), cards.destroy.copy()])
# game.add_permanents(player1, [cards.plains.copy() for i in range(3)])
# game.add_permanents(player2, [cards.aegis_turtle.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.beast_kin_ranger.copy()]+[cards.aegis_turtle.copy() for i in range(3)])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.forest.copy() for i in range(3)]+[cards.island.copy() for i in range(3)])
# game.add_permanents(player2, [cards.ambush_wolf.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.bigfin_bouncer.copy()])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.island.copy() for i in range(4)])
# game.add_permanents(player2, [cards.ambush_wolf.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.bite_down.copy()])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.forest.copy() for i in range(2)]+[cards.beast_kin_ranger.copy()])
# game.add_permanents(player2, [cards.ambush_wolf.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.blossoming_sands.copy()]+[cards.axgard_cavalry])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.bloodfell_caves.copy() for i in range(2)])
# game.add_permanents(player2, [cards.ambush_wolf.copy()])

# player1 = game.players[0]
# player2 = game.players[1]
# game.add_cards(player1, [cards.broken_wings.copy()])
# game.add_cards(player2, [cards.forest.copy()])
# game.add_permanents(player1, [cards.forest.copy() for i in range(3)])
# game.add_permanents(player2, [cards.ambush_wolf.copy(), cards.banishing_light.copy()])

player1 = game.players[0]
player2 = game.players[1]
game.add_cards(player1, [cards.burglar_rat.copy()])
game.add_cards(player2, [cards.forest.copy()])
game.add_permanents(player1, [cards.swamp.copy() for i in range(2)])
game.add_permanents(player2, [cards.ambush_wolf.copy(), cards.banishing_light.copy()])

game.play_game()
