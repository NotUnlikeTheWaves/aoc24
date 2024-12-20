from dataclasses import dataclass
import math
from typing import List, Set, Tuple

STEP_PENALTY    = 1

class Spaces:
    WALL = '#'
    EMPTY = '.'
    START = 'S'
    END = 'E'

@dataclass
class Node:
    connects: List[Tuple['Node', int]]

f = open("18.txt", "r")
lines = list(map(lambda l: l.strip('\n'), f.readlines()))
f.close()

# grid = []
# position_grid = []
# start = None
# end = None
# dist = {}
# prev = {}
# Q: List[Node]= []

def printBasicGrid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(grid[y][x], end="")
        print()

def addUndirectedEdge(a: Node, b: Node, weight: int):
    a.connects.append((b, weight))
    b.connects.append((a, weight))

def connectToGrid(a: Node, x: int, y: int):
    # Look left and up
    if x > 0:
        b = position_grid[y][x-1]
        if isinstance(b, Node):
            addUndirectedEdge(a, b, STEP_PENALTY)
    if y > 0:
        b = position_grid[y-1][x]
        if isinstance(b, Node):
            addUndirectedEdge(a, b, STEP_PENALTY)

def solve(i):
    # Setup basic grid
    global grid
    grid = []
    global position_grid
    position_grid = []
    global start
    start = None
    global end
    end = None
    global dist
    dist = {}
    global prev
    prev = {}
    global Q
    Q = []

    grid_length = 71
    for y in range(grid_length):
        grid.append(list('.' * grid_length))

    for line in lines[0:i]:
        s = line.split(',')
        x = int(s[0])
        y = int(s[1])
        grid[y][x] = Spaces.WALL

    grid[0][0] = Spaces.START
    grid[grid_length-1][grid_length-1] = Spaces.END

    # Setup node grid
    # Create nodes
    for y in range(len(grid)):
        node_row: List[Node | None] = []
        for x in range(len(grid[y])):
            match grid[y][x]:
                case Spaces.WALL:
                    node_row.append(None)
                case Spaces.EMPTY:
                    node_row.append(Node([]))
                case Spaces.START:
                    start = Node([])
                    node_row.append(start)
                case Spaces.END:
                    end = Node([])
                    node_row.append(end)
                case e:
                    print(f"Unknown item in map {e=}")
                    exit()
        position_grid.append(node_row)

    # Connect edges in the grid
    for y in range(len(position_grid)):
        for x in range(len(position_grid[y])):
            node = position_grid[y][x]
            # print(f"{x=} {y=}")
            if isinstance(node, Node):
                connectToGrid(node, x, y)
                dist[id(node)] = math.inf
                prev[id(node)] = None
                Q.append(node)

    dist[id(start)] = 0
    print("Start solving")

    while len(Q) > 0:
        Q.sort(key=lambda q: dist[id(q)])
        u = Q[0]
        Q = Q[1:]
        
        for (v, w) in u.connects:
            alt = dist[id(u)] + w
            if alt < dist[id(v)]:
                dist[id(v)] = alt
                prev[id(v)] = u

    return dist[id(end)]

def binary_search_until_break(start, end):
    mid = (start + end) // 2
    val = solve(mid)
    print(f"Binary searching: {start=}  {mid=}  {end=}  {val=}")
    if val == math.inf:
        if solve(mid - 1) != math.inf:
            return mid
        else:
            return binary_search_until_break(start, mid)
    else:
        return binary_search_until_break(mid, end)

breakpoint = binary_search_until_break(0, len(lines))
print(f"{breakpoint=} == {lines[breakpoint]}")

print(solve(3026)) # apparently this is the correct one
print(solve(3027))
print(solve(3028))