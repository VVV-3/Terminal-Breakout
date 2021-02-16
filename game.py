import os
import time
from colorama import Fore, Back, Style
import numpy as np

import config
# from inp import Get, input_to
from window import Window
from objects import Ball, Paddle

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

        self._level = True
        self._play = False
        self._lives = lives
        self._points = points

        
        self._paddle = Paddle([int(self._height - 5), int(self._width/2) - 16])
        self._balls = [Ball( [self._paddle._pos[0] - 3 , self._paddle._pos[1] + 1] )]
        # self._bricks = []

    def startLevel(self):
    

        while self._level:
            # self.printScreen()
            # print('Press W to start')
            # while not self._play:
            #     ch = input_to(Get())
            #     if ch == 'w':
            #         self._play = True
            self._play = True
            frame = 0
            while self._level and self._play:
                begin = time.monotonic()
                
                if frame == config.FRAME_RATE:
                    frame = 0
                    os.system("clear")
                    self.renderFrame()
                frame += 1
                # while time.monotonic() - begin < config.FRAME_TIME:
                #     pass

    def renderFrame(self):
        #self.handleInput()
        self.moveObjects()
        self.handleCollisions()
        self.printScreen()

    def handleInput(self):
        # self._ch = input_to(Get(),config.FRAME_TIME)
        if (self._paddle._pos[1] - self._paddle._velocity[1] > 1):
            self._paddle._pos -= self._paddle._velocity
        else:
            self._paddle._pos += self._paddle._velocity
        # if (self._paddle._pos[1] + self._paddle._velocity[1] < self._width - 2):
        #     self._paddle._pos += self._paddle._velocity

    def moveObjects(self):
        
        for ball in self._balls:
            ball.move()

    def handleCollisions(self):
        self.handleBorderBallCollisions()
        self.handlePaddleBallCollisions()

    def handleBorderBallCollisions(self):
        for ball in self._balls:
            if(ball._pos[0] + ball._velocity[0] <= 0):
                ball._pos[0] = 1
                ball._velocity *= np.array([-1,1])

            #Life lost
            if(ball._pos[0] + ball._velocity[0] > self._height):
                ball._pos[0] = self._height - 2
                ball._velocity *= np.array([-1,1])

            if(ball._pos[1] + ball._velocity[1] <= 0):
                ball._pos[1] = 1
                ball._velocity *= np.array([1,-1])
            if(ball._pos[1] + ball._velocity[1] > self._width):
                ball._pos[1] = self._width - 2
                ball._velocity *= np.array([1,-1])

    def handlePaddleBallCollisions(self):
        for ball in self._balls:
            if(ball._pos[0] + ball._velocity[0] >= self._paddle._pos[0]):
                size = self._paddle._size[1]/4
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1]) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (size)) ):
                    ball._velocity = np.array([-1,-2])
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1] + (size)) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (2*size)) ):
                    ball._velocity = np.array([-2,-1])
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1] + (2*size)) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (3*size)) ):
                    ball._velocity = np.array([-2,1])
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1] + (3*size)) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (4*size)) ):
                    ball._velocity = np.array([-1,2])


    def printScreen(self):
        self._window.clearBoard()

        for ball in self._balls:
            self._window.addObject(ball.show())

        self._window.addObject(self._paddle.show())
        #print(self._paddle.show()) 

        self._window.printBoard()

lev = Level(1,1,0)
lev.startLevel()