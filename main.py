from colorama import init
from game import Game

init()
print('\033[2J') # clear screen
game = Game()
game.startGame()