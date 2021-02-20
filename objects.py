import numpy as np
from time import monotonic as clock, sleep
import config

class BaseObject:
    def __init__( self, pos, size, sprite, color):
        self._pos = pos
        self._size = size
        self._sprite = sprite
        self._color = color
    
    def show(self):
        return self._pos, self._size, self._sprite, self._color
    

class Ball(BaseObject):
    def __init__( self, pos, size = None, velocity = None, color = None, strength = None):

        if size == None:
            size = [1,1]
        if velocity == None:
            velocity = config.BALL_VELOCITY
        if color == None:
            color = config.BALL_COLOR
        if strength == None:
            strength = config.BALL_STRENGTH

        super().__init__( np.array(pos), np.array(size), config.BALL_SPRITE, color)
        self._velocity = velocity
        self._strength = strength

    def move(self):
        self._pos += self._velocity


class Paddle(BaseObject):
    def __init__( self, pos, size = None, velocity = None, color = None):

        if size == None:
            size = config.PADDLE_SIZE
        if velocity == None:
            velocity = config.PADDLE_VELOCITY
        if color == None:
            color = config.PADDLE_COLOR

        super().__init__( np.array(pos), np.array(size), config.PADDLE_SPRITE, color)
        self._grab = False
        self._velocity = velocity


class Brick(BaseObject):
    def __init__(self, pos, health = None, size = None):
        if size == None:
            size = config.BRICK_SIZE
        if health == None:
            health = config.BRICK_HEALTH
        self._color_map = config.BRICK_COLOR_MAP
        self._sprite_map = config.BRICK_SPRITE_MAP
        super().__init__( np.array(pos), np.array(size), self._sprite_map[health], self._color_map[health] )
        self._health = health

    def hit(self, strength ):
        if(strength == -1):
            return True
        elif (self._health != 0):
            if strength >= self._health:
                return True
            else:
                self._health -= strength
                self._color = self._color_map[self._health]
                self._sprite = self._sprite_map[self._health]
        return False


class Power_Up(BaseObject):
    def __init__(self, pos, i):
        self._id = i
        super().__init__(np.array(pos), np.array(config.POWER_UP_SIZE), config.POWER_UP_SPRITE_MAP[self._id], config.POWER_UP_COLOR_MAP[self._id])
        self._velocity = np.array(config.POWER_UP_VELOCITY)
        self._on = False
        self._start_time = None

    def move(self):
        if self._on == False:
            self._pos += self._velocity

    def activate(self):
        self._on = True
        self._pos = np.array([config.BOARD_HEIGHT - 4, config.BOARD_WIDTH -15 + self._id])
        self._start_time = clock()

    def expiry(self):
        if clock() - self._start_time > config.POWER_UP_TIME:
            return True
        return False