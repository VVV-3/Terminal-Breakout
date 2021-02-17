from random import randint
from sys import stdout
from time import sleep

from colorama import init

offset = 3
height = 30
width = 60


def update_coord(x, y):
    stdout.write(f"\x1b[{offset};0H")
    stdout.write(f"\x1b[{y}B")
    stdout.write(f"\x1b[{x}C")
    stdout.write("-")
    stdout.flush()


init()
for _ in range(height):
    print("x" * width)

while True:
    x = randint(0, width - 1)
    y = randint(0, height - 1)
    update_coord(x, y)
    sleep(0.01)
