import numpy as np

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
            strength == config.BALL_STRENGTH

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
        self._velocity = velocity


    
        

# ball = Ball([0,0])
# pos,size,rep = ball.show()
# ball.move()
# print(ball._velocity)