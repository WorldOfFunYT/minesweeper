from colored import fore, back, style, fg, bg, attr
import numpy as np
import random
from board import Board
from commands import *

class Game:
    def __init__(self):
        self.running = False
        self.programRunning = True
        self.board = None
        self.commands = {
            "step": Command(
                "step", 
                [Parameter("x position", True),
                 Parameter("y position", True)
                ], 
                "Reveal a spot on the board"
            ),
            "flag": Command(
                "flag", 
                [Parameter("x position", True),
                    Parameter("y position", True)
                ], 
                "Flag a spot on the board"
            ),
            "help": Command(
                "help", 
                [], 
                "Show a list of all commands"
            ),
            "start": Command(
                "start",
                [
                    Parameter("width", True),
                    Parameter("height", True),
                    Parameter("mines", True),
                    Parameter("seed", False)
                ],
                "Start the game"
            ),
            "restart": Command(
                "restart",
                [
                    Parameters([Parameter("width", True),
                    Parameter("height", True),
                    Parameter("mines", True),
                    Parameter("seed", False)], False)
                ],
                "Start a new game. If no arguments are provided, use the same settings as the previous game, including the seed."
            ),
            "quit": Command(
                "quit",
                [],
                "Stop the program"
            )}
        return
    
    def printBoard(self):
        indicies = ''
        boardLines = self.board.getFormattedBoard()
        for i in range(self.board.width):
            indicies += f'{i:^3}' 
        # print(f'x       {' ' + {i} + ' ' for i in range(board.width)}')
        # print(f'{i for i in range(9)}')
        print(f'x       {indicies}\n' + 
              'y\n' + 
              ' '
              )
        for i in range(self.board.height):
            print(f'{i:<8}{boardLines[i]}')
        
    def error(self, text, command):
        print(text)
        print(f'usage: {self.commands[command].usage}')
        print(f'Try {self.commands["help"].name} for more information.')
    
    def runCommand(self, inputCommand):
        inputCommandWithParameters = inputCommand.split(" ")
        commandName = inputCommandWithParameters[0]
        match commandName:
            case "step":
                if not self.board:
                    self.error("Game not started", "start")
                    return
                try:
                    x = int(inputCommandWithParameters[1])
                except IndexError:
                    self.error("2 arguments expected, but none were given", "step")
                    return
                except ValueError:
                    self.error("2 arguments expected, but none were given", "step")
                    return
                try:
                    y = int(inputCommandWithParameters[2])
                    if x < 0 or x > self.board.width-1:
                        self.error("x index out of range", "step")
                        return
                    if y < 0 or y > self.board.height-1:
                        self.error("y index out of range", "step")
                        return
                    if not self.board.initialised:
                        self.board.setup([x, y])
                    self.step(x, y)
                    self.checkIfWon()
                    self.printBoard()
                    if not self.running:
                        self.menuScreen()
                except IndexError:
                    self.error("2 arguments expected, but one was given", "step")
                    return
                except ValueError:
                    self.error("2 arguments expected, but one was given", "step")
                    return
            case "flag":
                if not self.board:
                    self.error("Game not started", "start")
                    return
                try:
                    x = int(inputCommandWithParameters[1])
                except IndexError:
                    self.error("2 arguments expected, but none were given", "flag")
                    return
                except ValueError:
                    self.error("2 arguments expected, but none were given", "flag")
                    return
                try:
                    y = int(inputCommandWithParameters[2])
                    self.flag(x, y)
                    self.printBoard()
                except IndexError:
                    self.error("2 arguments expected, but one was given", "flag")
                    return
                except ValueError:
                    self.error("2 arguments expected, but one was given", "flag")
                    return
            case "help":
                self.help()
            case "start":
                if len(inputCommandWithParameters) < 4:
                    self.error("Not enough arguments", "start")
                    return
                if len(inputCommandWithParameters) > 5:
                    self.error("Too many arguments", "start")
                    return
                for i in range(1, len(inputCommandWithParameters)):
                    if not inputCommandWithParameters[i].isnumeric():
                        self.error("One or more arguments are not integers", "start")
                        return
                if len(inputCommandWithParameters) == 5:
                    self.start(inputCommandWithParameters[1], inputCommandWithParameters[2], inputCommandWithParameters[3], inputCommandWithParameters[4])
                    return
                self.start(inputCommandWithParameters[1], inputCommandWithParameters[2], inputCommandWithParameters[3])
            case "restart":
                if len(inputCommandWithParameters) == 1:
                    self.start(self.board.width, self.board.height, self.board.mines, self.board.seed)
                    return
                elif len(inputCommandWithParameters) < 4:
                    self.error("Not enough arguments", "restart")
                    return
                elif len(inputCommandWithParameters) > 5:
                    self.error("Too many arguments", "restart")
                    return
                for i in range(1, len(inputCommandWithParameters)):
                    if not inputCommandWithParameters[i].isnumeric():
                        self.error("One or more arguments are not integers", "restart")
                        return
                if len(inputCommandWithParameters) == 5:
                    self.start(inputCommandWithParameters[1], inputCommandWithParameters[2], inputCommandWithParameters[3], inputCommandWithParameters[4])
                    return
                self.start(inputCommandWithParameters[1], inputCommandWithParameters[2], inputCommandWithParameters[3])
            case "quit":
                self.programRunning = False
    def step(self, x, y):
        if self.board.board[y, x] == "O":
            self.board.uncovered[self.board.uncovered == False] = True
            print(f"{fg('red')}Game over{attr(0)}")
            self.running = False
        self.board.reveal(x, y)
    
    def start(self, width, height, mines, seed=""):
        width = int(width)
        height = int(height)
        mines = int(mines)
        if seed == "":
            seed = random.randint(0, 1_000_000_000)
            print(seed)
        seed = int(seed)
        
        self.board = Board(width, height, mines, seed)
        self.running = True

    def flag(self, x, y):
        self.board.flags[y, x] = not self.board.flags[y, x]

    def help(self):
        for command in self.commands:
            print(f'{self.commands[command]}\n')
    
    def checkIfWon(self):
        won = True
        for y in range(self.board.height):
            for x in range(self.board.width):
                if not self.board.uncovered[y, x] and not self.board.minePositions[y, x]:
                    won=False
        if won and self.running == True:
            self.board.uncovered[self.board.uncovered == False] = True
            print(f'{fg("green")}You won!{attr(0)}')
        self.running = not won
            
    def menuScreen(self):
        '''
         __  __ ___ _  _ ___ _____      _____ ___ ___ ___ ___ 
        |  \/  |_ _| \| | __/ __\ \    / / __| __| _ \ __| _ \
        | |\/| || || .` | _|\__ \\ \/\/ /| _|| _||  _/ _||   /
        |_|  |_|___|_|\_|___|___/ \_/\_/ |___|___|_| |___|_|_\
                                                       


        '''
        print(
            f'''
             __  __ ___ _  _ ___ _____      _____ ___ ___ ___ ___ 
            |  \/  |_ _| \| | __/ __\ \    / / __| __| _ \ __| _ \\
            | |\/| || || .` | _|\__ \\\\ \/\/ /| _|| _||  _/ _||   /
            |_|  |_|___|_|\_|___|___/ \_/\_/ |___|___|_| |___|_|_\\\n
            {'Type "start <width> <height> <mines> [seed]" to start':^54}
            '''
            )
    