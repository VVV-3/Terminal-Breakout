import os
import sys
import time
import random
from colorama import Fore, Back, Style
import numpy as np
from time import monotonic as clock, sleep

import config
from keyboard_input import KBHit
from window import Window
from objects import Ball, Paddle, Brick, Power_Up



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
  
        self._paddle = Paddle([int(self._height - 8), int(self._width/2 - 8)])
        self._balls = [Ball([30,30 + 12])]
        self._bricks = [Brick([5,5],0), Brick([10,10],1) , Brick([15,15],3) , Brick([20,20],2)]
        self._brick_count = 3
        self._power_ups = [] #Power_Up([5,5],1),Power_Up([10,10],2)
        self._power_up_count = 3

    
    def startLevel(self):

        while self._level:
            self._window.clearBoard()
            self._window.printText([self._height - 5, 35], 'Level: ' + str(self._lvl))
            self._window.printText([self._height - 2, 30], 'TERMINAL - BREAKOUT')
            self._window.printText([self._height - 3, 15], 'Press W to start and A and D keys to control Paddle ')
            self.printScreen()

            while not self._play:
                if self._keyboard.kbhit():
                    inp = self._keyboard.getch()
                    inp = inp.lower()
                    if inp == 'w':
                        self._play = True 
                        self._window.clearObject(([self._height - 3, 0],[1,self._width]))
                    self._keyboard.flush()

            while self._level and self._play:  
                start_time = clock()

                self.expirePowerUps()
                self.handleInput()
                self.moveObjects()
                self.handleCollisions()
                self.printScreen()
                
                while clock() - start_time < config.FRAME_TIME:
                    pass

        return self._lives,self._points


    def expirePowerUps(self):
        i = 0
        while i < len(self._power_ups):
            power = self._power_ups[i]
            self._window.clearObject(power.show())
            
            if power._on == True:
                if power.expiry():

                    if power._id == 1:
                        self._paddle._size[1] -= (config.EXPAND_PADDLE_POWER_UP_LENGTH)
                    elif power._id == 2:
                        self._paddle._size[1] += (config.SHRINK_PADDLE_POWER_UP_LENGTH)
                    elif power._id == 4:
                        for ball in self._balls:
                            ball._velocity[1] -= 1
                    elif power._id == 5:
                        for ball in self._balls:
                            ball._strength = config.BALL_STRENGTH
                    elif power._id == 6:
                        self._paddle._grab = False


                    t = self._power_ups[i]
                    self._power_ups.pop(i)
                    del t
                    i-=1
            i+=1
        
      
    def handleInput(self):
        if self._keyboard.kbhit():
            inp = self._keyboard.getch().lower()
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

        i = 0
        while i < len(self._power_ups):
            power = self._power_ups[i]
            self._window.clearObject(power.show())
            if power._on == False:
                power.move()
                if power._pos[0] > self._height - 5 : 
                    t = self._power_ups[i]
                    self._power_ups.pop(i)
                    del t
                    i-=1
            i+=1


    def handleCollisions(self):
        self.handleBrickBallCollisions()
        self.handleBorderBallCollisions()
        self.handlePaddleBallCollisions()
        self.handlePaddlePowerUpCollisons()


    def handleBrickBallCollisions(self):
        for ball in self._balls:
            i = 0
            while i < len(self._bricks):
                brick = self._bricks[i]
                collide = False
                hit = False

                if (ball._pos[0] + ball._velocity[0] >= brick._pos[0]) and (ball._pos[0] + ball._velocity[0] < brick._pos[0] + brick._size[0]):
                    if (ball._pos[1] + ball._velocity[1] >= brick._pos[1]) and (ball._pos[1] + ball._velocity[1] < brick._pos[1] + brick._size[1]):
                        collide = True

                if collide:
                    if ball._strength != -1:
                        ball._velocity *= np.array([-1,1])
                    hit = brick.hit(ball._strength)
                    self._points += config.POINTS_PER_HIT

                    if hit :
                        if self._power_up_count > 0:
                            if (random.random() < float(self._power_up_count/self._brick_count)):
                                temp = random.randint(1,len(config.POWER_UP_COLOR_MAP) - 1)
                                self._power_ups.append(Power_Up(brick._pos, temp))
                                self._power_up_count -= 1


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
                    self._paddle = Paddle([int(self._height - 8), int(self._width/2 - 8)])
                    self._balls = [Ball([30,30 + 12])]
                    self._power_ups = []
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
                    if self._paddle._grab:
                        self._play = False
                    ball._velocity = np.array(config.PADDLE_DEFLECT_LIST[0])
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1] + (size)) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (2*size)) ):
                    if self._paddle._grab:
                        self._play = False
                    ball._velocity = np.array(config.PADDLE_DEFLECT_LIST[1])
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1] + (2*size)) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (3*size)) ):
                    if self._paddle._grab:
                        self._play = False
                    ball._velocity = np.array(config.PADDLE_DEFLECT_LIST[2])
                if( (ball._pos[1] + ball._velocity[1] >= self._paddle._pos[1] + (3*size)) and (ball._pos[1] + ball._velocity[1] < self._paddle._pos[1] + (4*size)) ):
                    if self._paddle._grab:
                        self._play = False
                    ball._velocity = np.array(config.PADDLE_DEFLECT_LIST[3])


    def handlePaddlePowerUpCollisons(self):
        for power in self._power_ups:
            if (power._pos[0] >= self._paddle._pos[0]) and (power._pos[0] < self._paddle._pos[0] + self._paddle._size[0]):
                if (power._pos[1] >= self._paddle._pos[1]) and (power._pos[1] < self._paddle._pos[1] + self._paddle._size[1]):

                    power.activate()
                    
                    if power._id == 1:
                        self._paddle._size[1] += (config.EXPAND_PADDLE_POWER_UP_LENGTH)
                    elif power._id == 2:
                        self._paddle._size[1] -= (config.SHRINK_PADDLE_POWER_UP_LENGTH)
                    elif power._id == 3:
                        new_balls = []
                        for ball in self._balls:
                            pos = np.array(ball._pos)
                            vel = np.array(ball._velocity)*np.array([1,-1])
                            ba = Ball(pos= pos)
                            ba._velocity = vel
                            new_balls.append(ba)
                        self._balls += new_balls
                    elif power._id == 4:
                        for ball in self._balls:
                            ball._velocity[1] += 1
                    elif power._id == 5:
                        for ball in self._balls:
                            ball._strength = -1
                    elif power._id == 6:
                        self._paddle._grab = True


    def printScreen(self):
        for power in self._power_ups:
            self._window.addObject(power.show())

        for brick in self._bricks:
            self._window.addObject(brick.show())

        for ball in self._balls:
            self._window.addObject(ball.show())

        self._window.addObject(self._paddle.show())

        self._window.printText([self._height - 5, 5], 'Lives: ' + str(self._lives))
        self._window.printText([self._height - 5, self._width - 15], 'Points: ' + str(self._points))