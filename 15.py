from functools import reduce
import itertools
from typing import Tuple

class Spaces:
    BOX = 'O'
    WALL = '#'
    EMPTY = '.'

def findPos(g) -> Tuple[int, int]:
    for y in range(len(g)):
        for x  in range(len(g[y])):
            if g[y][x] == '@':
                return (x, y)
    return (-1, -1)

def getMoveXY(move: str) -> Tuple[int, int]:
    match move:
        case '>':
            return (1, 0)
        case '<':
            return (-1, 0)
        case '^':
            return (0, -1)
        case 'v':
            return (0, 1)
        case _:
            print(f"ERROR: Unknown move {move}")
            exit()

fm = open("15_map.txt", "r")
fw = open("15_walk.txt", "r")

grid = fm.readlines()
grid = list (map(lambda l: list(l.strip('\n')), grid ))
print(grid)

walk = fw.readlines()
fm.close()
fw.close()

# bullshit ass language
walk = reduce(lambda l1, l2: l1.strip() + l2.strip(), walk)
print(walk)



(pX, pY) = findPos(grid)
grid[pY][pX] = Spaces.EMPTY
print(f"Starting search with character at post {pX=},{pY=}")

def printGrid():
    for y in grid:
        print(y)

def propagateBox(bX: int, bY: int, dX: int, dY: int) -> bool:
    print(f"PropagateBox {bX=} {bY=} {dX=} {dY=}")
    printGrid()
    # print(f"Grid {grid[bY+dY][bX+dX]=}")
    match grid[bY+dY][bX+dX]:
        case Spaces.WALL:
            return False
        case Spaces.EMPTY:
            grid[bY][bX] = Spaces.EMPTY
            grid[bY+dY][bX+dX] = Spaces.BOX
            return True
        case Spaces.BOX:
            if propagateBox(bX + dX, bY + dY, dX, dY):
                grid[bY][bX] = Spaces.EMPTY
                grid[bY+dY][bX+dX] = Spaces.BOX
                return True
            else:
                return False
        case e:
            print(f"Unknown character in propagate boxes: {e}")
            exit()

idx = 0
for move in walk:
    print(idx)
    idx += 1
    (dX, dY) = getMoveXY(move)
    (nX, nY) = (pX + dX, pY + dY)
    match grid[nY][nX]: ##.O
        case Spaces.WALL: # Wall hit
            print(f"Hit the wall at {pX=},{pY=}")
            continue
        case Spaces.EMPTY: # Valid move
            pX = nX
            pY = nY
            continue
        case Spaces.BOX: # Box hit
            if propagateBox(nX, nY, dX, dY): # If we can move the box, we can go there next
                pX = nX
                pY = nY
        case e:
            print(f"ERROR: Unknown what to do with grid item {e}")
            exit()

score = 0

for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] == Spaces.BOX:
            score += 100 * y + x

print(score)
