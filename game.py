import os
import sys
import time
from colorama import Fore, Back, Style
import numpy as np
from time import monotonic as clock, sleep

import config
from keyboard_input import KBHit
from window import Window
from objects import Ball, Paddle, Brick

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
        while self._lives > 0:
            level = Level(self._level, self._lives, self._points)
            self._lives, self._points = level.startLevel()
            self._level = self._level + 1
        os.system("clear")
        print('GAME OVER..... POINTS: ' + str(self._points))


class Level:

    def __init__(self,level,lives,points):


        self._height = config.BOARD_HEIGHT 
        self._width = config.BOARD_WIDTH

        self._keyboard = KBHit()
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
        os.system("clear")
        self._window = Window(self._height, self._width)

        self._lvl = level
        self._level = True
        self._play = False
        self._lives = lives
        self._points = points

        
        self._paddle = None
        self._balls = []
        self._bricks = [Brick([5,5],0), Brick([10,10],1) , Brick([15,15],3) , Brick([20,20],2)]
        self._brick_count = 3

        

    def startLevel(self):

        while self._level:

            self._window.printBoard()
            self._window.printText([self._height - 5, 35], 'Level: ' + str(self._lvl))
            self._window.printText([self._height - 2, 30], 'TERMINAL - BREAKOUT')
            self._window.printText([self._height - 5, 5], 'Lives: ' + str(self._lives))
            self._window.printText([self._height - 5, 65], 'Points: ' + str(self._points))
            self._window.printText([self._height - 4, 15], 'Press W to start and A and D keys to control Paddle ')
            self._paddle = Paddle([int(self._height - 8), int(self._width/2 - 8)])
            self._balls = [Ball([30,30 + 12])]
            self.printScreen()

            while not self._play:
                if self._keyboard.kbhit():
                    inp = self._keyboard.getch()
                    if inp == 'w':
                        self._play = True 
                        self._window.clearObject(([self._height - 4, 0],[1,self._width]))   

            while self._level and self._play:
                start_time = clock()

                self.handleInput()
                self.moveObjects()
                self.handleCollisions()


                self.printScreen()
                self._window.printText([self._height - 5, 5], 'Lives: ' + str(self._lives))
                self._window.printText([self._height - 5, 65], 'Points: ' + str(self._points))
                
                while clock() - start_time < config.FRAME_TIME:
                    pass

        return self._lives,self._points
      

    def handleInput(self):
        if self._keyboard.kbhit():
            inp = self._keyboard.getch()
            if (inp == 'a') and (self._paddle._pos[1] - self._paddle._velocity[1] >= 0):
                self._window.clearObject(([self._paddle._pos[0],0],[self._paddle._size[0],self._width]))
                self._paddle._pos -= self._paddle._velocity
            if (inp == 'd') and (self._paddle._pos[1] + self._paddle._size[1] + self._paddle._velocity[1] <= self._width ):
                self._window.clearObject(([self._paddle._pos[0],0],[self._paddle._size[0],self._width]))
                self._paddle._pos += self._paddle._velocity
            self._keyboard.flush()

    def moveObjects(self):       
        for ball in self._balls:
            self._window.clearObject(ball.show())
            ball.move()

    def handleCollisions(self):
        self.handleBrickBallCollisions()
        self.handleBorderBallCollisions()
        self.handlePaddleBallCollisions()
        
    def handleBrickBallCollisions(self):
        for ball in self._balls:
            i = 0
            while i < len(self._bricks):

                brick = self._bricks[i]
                collide = False
                hit = False
                ball_y = ball._pos[0]
                ball_x = ball._pos[1]
                ball_vy = ball._velocity[0]
                ball_vx = ball._velocity[1]
                brick_y = brick._pos[0]
                brick_x = brick._pos[1]
                brick_hi = brick._size[0]
                brick_wi = brick._size[1]

                if (ball_y >= brick_y - 1) and (ball_y + ball_vy <= brick_y - 1):
                    if (ball_x >= brick_x) and (ball_x <= brick_x + brick_wi):
                       collide = True
                    elif (ball_x  + ball_vx >= brick_x ) and (ball_x + ball_vx <= brick_x + brick_wi):
                        collide = True
                elif (ball_y <= brick_y + brick_hi ) and (ball_y + ball_vy >= brick_y + brick_hi):
                    if (ball_x >= brick_x) and (ball_x <= brick_x + brick_wi):
                        collide = True
                    elif (ball_x  + ball_vx >= brick_x ) and (ball_x + ball_vx <= brick_x + brick_wi):
                        collide = True


                if collide:
                    ball._velocity *= np.array([-1,1])
                    hit = brick.hit(ball._strength)
                    self._points += config.POINTS_PER_HIT
                    if hit :
                        t = self._bricks[i]
                        self._window.clearObject(self._bricks[i].show())
                        if self._bricks[i]._health != 0:
                            self._brick_count -=1
                        self._bricks.pop(i)
                        if self._brick_count == 0:
                            self._level = False
                        del t
                        i-=1
                i+=1

    def handleBorderBallCollisions(self):
        i = 0
        while i < len(self._balls):

            ball = self._balls[i]

            if(ball._pos[1] + ball._velocity[1] <= 0):  #Left Border
                ball._pos[1] = 1
                ball._velocity *= np.array([1,-1])

            if(ball._pos[1] + ball._velocity[1] > self._width): #Right Border
                ball._pos[1] = self._width - 2
                ball._velocity *= np.array([1,-1])

            if(ball._pos[0] + ball._velocity[0] <= 0): #Top Border
                ball._pos[0] = 1
                ball._velocity *= np.array([-1,1])

            if(ball._pos[0]  >= self._height - 5): #Bottom - Ball lost when hit & life lost when 0 blals left
                t = self._balls[i]
                self._window.clearObject(self._balls[i].show())
                self._balls.pop(i)
                del t

                if len(self._balls) == 0:
                    self._lives -= 1
                    if self._lives <= 0:
                        self._level = False
                    self._play = False
                    break

                i-=1

            i+=1
            
    def handlePaddleBallCollisions(self):
        for ball in self._balls:
            if(ball._pos[0] + ball._velocity[0] >= self._paddle._pos[0]):
                size = self._paddle._size[1]/4
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1]) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (size)) ):
                    ball._velocity = np.array([-1,-2])
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1] + (size)) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (2*size)) ):
                    ball._velocity = np.array([-1,-1])
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1] + (2*size)) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (3*size)) ):
                    ball._velocity = np.array([-1,1])
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1] + (3*size)) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (4*size)) ):
                    ball._velocity = np.array([-1,2])


    def printScreen(self):
        #self._window.clearBoard()
        for brick in self._bricks:
            self._window.addObject(brick.show())

        for ball in self._balls:
            self._window.addObject(ball.show())

        self._window.addObject(self._paddle.show())
        #print(self._paddle.show()) 

        #self._window.printBoard()
