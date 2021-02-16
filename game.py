import os
from colorama import Fore, Back, Style

import config
from window import Window

class Game:

    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        if int(rows) < config.BOARD_HEIGHT or int(cols) < config.BOARD_WIDTH:
            print(Fore.RED + 'Fatal Error: Terminal window size too small ! Try playing with a larger terminal window.')
            raise SystemExit
        self._level = 1
        self._lives = config.LIVES
        self._points = 0

    def startGame(self):
        print('hoho')
        # while self._lives > 0:
        #     level = Level(self._level, self._lives, self._points)
        #     self._lives, self._points = level.startLevel()
        #     self._level = self._level + 1
        # endGame()


class Level:

    def __init__(self,level,lives,points):
        self._height = config.BOARD_HEIGHT 
        self._width = config.BOARD_WIDTH

        self._window = Window(self._height, self._width)

        self._level = level
        self._lives = lives
        self._points = points

        # self._balls = [Ball()]
        # self._paddle = Paddle()
        # self._bricks = []

    def startLevel(self):
        while True:
            print('ok')
            