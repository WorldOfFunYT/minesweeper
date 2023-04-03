from colored import fg, bg, attr
import numpy as np
import random
from commands import *

class Board:
    def __init__(self, width, height, mines, seed):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = np.array([["0" for i in range(self.width)] for i in range(self.height)])
        self.uncovered = np.array([[False for i in range(self.width)] for i in range(self.height)])
        self.flags = np.array([[False for i in range(self.width)] for i in range(self.height)])
        self.minePositions = np.array([[False for i in range(self.width)] for i in range(self.height)])
        if self.mines >= self.width * self.height:
            self.mines = self.width * self.height-1
        if self.mines <= 0:
            self.mines = 1
        self.seed = seed

    def pad(self):
        self.board = np.pad(self.board, 1, mode='constant', constant_values="1")
        self.uncovered = np.pad(self.uncovered, 1, mode='constant')
        self.width += 2
        self.height += 2

    def unpad(self):
        self.board = self.board[1:-1, 1:-1]
        self.uncovered = self.uncovered[1:-1, 1:-1]
        self.width -= 2
        self.height -= 2

    def setup(self, banned_coord):
        for i in range(self.mines):
            random.seed(self.seed+i)
            x, y = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            while self.board[y, x] == "O" or [x, y] == banned_coord:
                x, y = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            self.board[y, x] = "O"
            self.minePositions[y, x] = True
    
    
    def reveal(self, x, y):
        surroundIndexes = [[y-1, x-1], [y-1, x], [y-1, x+1],[y, x-1], [y, x+1],[y+1, x-1], [y+1, x], [y+1, x+1]]
        if self.uncovered[y, x] == True:
            return
        self.uncovered[y, x] = True
        if self.board[y, x] == "0":
            self.pad()
            for i in surroundIndexes:
                self.reveal(i[1]+1, i[0]+1)
            self.unpad()
        
    def addNumbers(self):
        self.pad()

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i, j] == "O":
                    surroundIndexes = [[i-1, j-1], [i-1, j], [i-1, j+1],[i, j-1], [i, j+1],[i+1, j-1], [i+1, j], [i+1, j+1]]
                    for index in surroundIndexes:
                        if self.board[index[0], index[1]] != "O":
                            self.board[index[0], index[1]] = str(int(self.board[index[0], index[1]]) + 1)
        self.unpad()
    
    def __str__(self):
        
        formattedBoard = ""
        for y in range(self.height):
            lineString = ""
            for x in range(self.width):
                char = self.board[y, x]
                colour = ""
                match char:
                    case "1":
                        colour = fg(4)
                    case "2":
                        colour = fg(10)
                    case "3":
                        colour = fg(196)
                    case "4":
                        colour = fg(25)
                    case "5":
                        colour = fg(88)
                    case "6":
                        colour = fg(6)
                    case "7":
                        colour = fg(255)
                    case "8":
                        colour = fg(243)
                    case "O":
                        colour = bg(1)
                    case "0":
                        # colour = bg(242)
                        char = "-"
                    case "F":
                        colour = bg(214) + fg(0)
                    case _:
                        colour = bg(238)
                lineString += f'{colour} {char} {attr(0)}'
            formattedBoard += lineString + "\n"
        return formattedBoard
    def getFormattedBoard(self):
        formattedBoard = []
        for y in range(self.height):
            lineString = ""
            for x in range(self.width):
                if self.uncovered[y, x]:
                    char = self.board[y, x]
                elif self.flags[y, x]:
                    char = "F"
                else:
                    char = ' '
                colour = ""
                match char:
                    case "1":
                        colour = fg(4)
                    case "2":
                        colour = fg(10)
                    case "3":
                        colour = fg(196)
                    case "4":
                        colour = fg(25)
                    case "5":
                        colour = fg(88)
                    case "6":
                        colour = fg(6)
                    case "7":
                        colour = fg(256)
                    case "8":
                        colour = fg(243)
                    case "O":
                        colour = bg(1)
                    case "0":
                        # colour = bg(242)
                        char = "-"
                    case "F":
                        colour = bg(214)
                    case _:
                        colour = bg(238)
                lineString += f'{colour} {char} {attr(0)}'
            formattedBoard.append(lineString)
        return formattedBoard
