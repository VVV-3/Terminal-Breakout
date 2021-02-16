import numpy as np 

import config

class Window:
    CURSOR_0 = "\033[0;0H"
    CLEAR = "\033[2J"

    def __init__(self, height, width):
        self._height = height
        self._width = width

        self._back_board = np.array([[config.BG_COLOR + " " for j in range(self._width)] for i in range(self._height)], dtype='object')

        for j in range(1,self._width-1):
            self._back_board[0][j] = config.BG_COLOR + "━"
            self._back_board[self._height - 1][j] = config.BG_COLOR + "━"
        
        for i in range(1,self._height-1):
            self._back_board[i][0] = config.BG_COLOR + "┃"
            self._back_board[i][self._width - 1] = config.BG_COLOR + "┃"

        self._back_board[0][0] = config.BG_COLOR + "┏"
        self._back_board[0][self._width - 1] = config.BG_COLOR + "┓"
        self._back_board[self._height - 1][0] = config.BG_COLOR + "┗"
        self._back_board[self._height - 1][ self._width - 1] = config.BG_COLOR + "┛"

        self._board = self._back_board

    def print_board(self):
        print(self.CURSOR_0)
        for i in range(self._height):
            for j in range(self._width):
                print(self._board[i][j], end='')
            print('')
                

