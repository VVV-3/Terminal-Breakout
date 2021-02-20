import numpy as np
from colorama import Fore, Back, Style
from sys import stdout

import config

class Window:
    CURSOR_0 = "\033[0;0H"
    CLEAR = "\033[2J"

    def __init__(self, height, width):
        self._height = height
        self._width = width

        self._back_board = np.array([[" " for j in range(self._width)] for i in range(self._height)], dtype='object')

        for j in range(1,self._width-1):
            self._back_board[0][j] = config.BORDER_COLOR + '-'#"━"
            self._back_board[self._height - 6][j] = Fore.RED + '-'#"━"
            self._back_board[self._height - 1][j] = Fore.WHITE + '-'#"━"
        
        for i in range(1,self._height-1):
            self._back_board[i][0] = config.BORDER_COLOR + '|'#"┃"
            self._back_board[i][self._width - 1] = config.BORDER_COLOR + '|'#"┃"

        self._back_board[0][0] = config.BORDER_COLOR + '+'#"┏"
        self._back_board[0][self._width - 1] = config.BORDER_COLOR + '+'#"┓"
        self._back_board[self._height - 1][0] = Fore.WHITE + '+'#config.BORDER_COLOR + "┗"
        self._back_board[self._height - 1][ self._width - 1] = Fore.WHITE + '+'#config.BORDER_COLOR + "┛" + Back.RESET


    def clearBoard(self):
        for i in range(self._height):
            for j in range(self._width):
                stdout.write(f"\x1b[{0};0H")
                stdout.write(f"\x1b[{i+1}B")
                stdout.write(f"\x1b[{j+1}C")
                stdout.write(self._back_board[i][j])
                stdout.flush()


    def printText(self,pos,text):
        le = len(text)
        for i in range(le):
            stdout.write(f"\x1b[{0};0H")
            stdout.write(f"\x1b[{pos[0] + 1}B")
            stdout.write(f"\x1b[{pos[1] + i + 1}C")
            stdout.write(config.TEXT_COLOR + text[i])
            stdout.flush()


    def clearObject(self, obj):
        pos,size = obj[0],obj[1]
        for i in range(size[0]):
            for j in range(size[1]):
                stdout.write(f"\x1b[{0};0H")
                stdout.write(f"\x1b[{pos[0] + i + 1}B")
                stdout.write(f"\x1b[{pos[1] + j + 1}C")
                stdout.write(self._back_board[pos[0] + i][pos[1] + j])
                stdout.flush()


    def addObject(self, obj):
        pos,size,sprite,color = obj
        for i in range(size[0]):
            for j in range(size[1]):
                stdout.write(f"\x1b[{0};0H")
                stdout.write(f"\x1b[{pos[0] + i+1}B")
                stdout.write(f"\x1b[{pos[1] + j+1}C")
                stdout.write(color + sprite)
                stdout.flush()