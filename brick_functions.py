import numpy as np
from objects import Brick


def brickPattern(level):
    if level == 3:
        bricks = []
        for i in range(6):
            for j in range(6):
                bricks.append(Brick([10+j,10+10*i],(i+j -1)%5))
        return bricks,29

    elif level == 2:
        return [
            Brick([15,20], 4),
            Brick([14,30], 4),
            Brick([14,20], 2),
            Brick([14,40], 3),
            Brick([13,40], 4),
            Brick([12,50], 4),
            Brick([11,60], 4),
            Brick([16,10], 4),
            Brick([5,5],1),
        ], 9

    return [
        Brick([5, 20], 0),
        Brick([10, 30], 1),
        Brick([10, 40], 3),
        Brick([15, 50], 2),
    ], 3


def explodeBrick(pos, size, bricks , brick_count):
    new_bricks = bricks
    i = 0
    while i < len(new_bricks):
        brick = new_bricks[i]
        pts = [
            [brick._pos[0], brick._pos[1]],
            [brick._pos[0], brick._pos[1] + brick._size[1]],
            [brick._pos[0] + brick._size[0], brick._pos[1]],
            [brick._pos[0] + brick._size[0], brick._pos[1] + brick._size[1]],
        ]
        explode = False
        for pt in pts:
            if (pt[0] == pos[0]) and (pt[1] >= pos[1] and pt[1] <= pos[1] + size[1]): #top side
                explode = True
            elif (pt[0] == pos[0] + size[0]) and (pt[1] >= pos[1] and pt[1] <= pos[1] + size[1]): #bottom side
                explode = True
            elif (pt[1] == pos[1] ) and (pt[0] >= pos[0] and pt[0] <= pos[0] + size[0]): #left side
                explode = True
            elif (pt[1] == pos[1] + size[1]) and (pt[0] >= pos[0] and pt[0] <= pos[0] + size[0]): #right side
                explode = True
        if explode:

            t = new_bricks[i]
            new_bricks.pop(i)
            if t._health != 0:
                brick_count -= 1
            i -=1
            if t._health == 4:
                new_bricks, brick_count = explodeBrick(t._pos,t._size,new_bricks, brick_count)
                i = -1
        i+=1
    return new_bricks, brick_count