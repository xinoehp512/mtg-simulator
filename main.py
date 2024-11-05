import random

from agent import Agent
from game import Game
from objects.decks import *

random.seed(1)
with open("user_input.txt", "w") as file:
    file.write("")

game = Game([Agent("Player 1", decktest), Agent("Player 2", decktest)])
game.play_game()
