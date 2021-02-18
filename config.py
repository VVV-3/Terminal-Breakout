from colorama import Fore, Back, Style
import numpy as np



#GAME PROPERTIES
FRAME_TIME = 0.1
FRAME_RATE = 200000
LIVES = 3
POINTS_PER_HIT = 1


#WINDOW PROPERTIES
BOARD_HEIGHT = 40
BOARD_WIDTH = 80
BG_COLOR = Back.BLACK
TEXT_COLOR = Fore.WHITE
BORDER_COLOR = Fore.WHITE


#BALL PROPERTIES
BALL_VELOCITY =  np.array([1,1])
BALL_COLOR = Fore.GREEN
BALL_SPRITE = 'o'#'⬤'
BALL_STRENGTH = 1

#PADDLE PROPERTIES
PADDLE_SIZE = [1,20]
PADDLE_COLOR = Fore.WHITE
PADDLE_VELOCITY =  np.array([0,4])
PADDLE_SPRITE = 'x'#'▒'

#BRICK PROPERTIES
BRICK_SIZE = [1,16]
BRICK_HEALTH = 0
BRICK_COLOR_MAP = [Fore.WHITE, Fore.BLUE, Fore.YELLOW, Fore.RED ]
BRICK_SPRITE_MAP = ['I','1','2','3']