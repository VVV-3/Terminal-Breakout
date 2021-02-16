import numpy as np
from colorama import Fore, Back, Style

import config

class Window:
    CURSOR_0 = "\033[0;0H"
    CLEAR = "\033[2J"

    def __init__(self, height, width):
        self._height = height
        self._width = width

        self._back_board = np.array([[" " for j in range(self._width)] for i in range(self._height)], dtype='object')

        for j in range(1,self._width-1):
            self._back_board[0][j] = config.BORDER_COLOR + "━"
            self._back_board[self._height - 1][j] = config.BORDER_COLOR + "━"
        
        for i in range(1,self._height-1):
            self._back_board[i][0] = config.BORDER_COLOR + "┃"
            self._back_board[i][self._width - 1] = config.BORDER_COLOR + "┃"

        self._back_board[0][0] = config.BORDER_COLOR + "┏"
        self._back_board[0][self._width - 1] = config.BORDER_COLOR + "┓"
        self._back_board[self._height - 1][0] = config.BORDER_COLOR + "┗"
        self._back_board[self._height - 1][ self._width - 1] = config.BORDER_COLOR + "┛" + Back.RESET

        self._board = np.array(self._back_board)

    def clearBoard(self):
        for i in range(self._height):
            for j in range(self._width):
                self._board[i][j] = self._back_board[i][j] 

    def addObject(self, obj):
        pos,size,sprite,color = obj
        for i in range(size[0]):
            for j in range(size[1]):
                self._board[ pos[0] + i ][ pos[1] + j ] = color + sprite + Fore.RESET
    
    def printBoard(self):
        print(self.CURSOR_0)
        for i in range(self._height):
            for j in range(self._width):
                print(self._board[i][j], end='')
            print('')
                

