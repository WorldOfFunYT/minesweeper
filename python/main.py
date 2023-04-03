from colored import fore, back, style, fg, bg, attr
import numpy as np
import random
from board import Board
from game import Game
from commands import *

gameHandler = Game()
gameHandler.menuScreen()

while gameHandler.running:
    # gameHandler.checkIfWon()
    # if not gameHandler.running:
    #     break
    command = input()
    gameHandler.runCommand(command)


