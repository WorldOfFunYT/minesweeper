from colored import fore, back, style, fg, bg, attr
import numpy as np
import random
from board import Board
from commands import *

class Game:
    def __init__(self):
        self.running = True
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
                    self.step(x, y)
                    self.printBoard()
                except IndexError:
                    self.error("2 arguments expected, but one was given", "step")
                    return
                except ValueError:
                    self.error("2 arguments expected, but one was given", "step")
                    return
            case "flag":
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
            
    def step(self, x, y):
        if self.board.board[y, x] == "O":
            self.board.uncovered[self.board.uncovered == False] = True
            print("Game over")
            self.running = False
        self.board.reveal(x, y)
    
    def start(self, width, height, mines, seed):
        if seed == "":
            seed = random.randint(0, 1_000_000_000)
            print(seed)
        if type(seed) == str:
            # Turn string into number somehow
            pass
        
        self.board = Board(width, height, mines, seed)

    def flag(self, x, y):
        self.board.flags[y, x] = not self.board.flags[y, x]

    def help(self):
        for command in self.commands:
            print(command + '\n')
    
    def checkIfWon(self):
        won = True
        for y in range(self.board.height):
            for x in range(self.board.width):
                if not self.board.uncovered[y, x] and not self.board.minePositions[y, x]:
                    won=False
        if won:
            self.board.uncovered[self.board.uncovered == False] = True
            print("You won!")
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
    