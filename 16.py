from dataclasses import dataclass
import math
from typing import List, Set, Tuple

TURN_PENALTY    = 1000
STEP_PENALTY    = 1

class Spaces:
    WALL = '#'
    EMPTY = '.'
    START = 'S'
    END = 'E'

@dataclass
class Node:
    connects: List[Tuple['Node', int]]

@dataclass
class Position:
    up: Node
    down: Node
    left: Node
    right: Node

f = open("16.txt", "r")
lines = f.readlines()
f.close()
grid = list (map(lambda l: list(l.strip('\n')), lines))

position_grid = []

def addUndirectedEdge(a: Node, b: Node, weight: int):
    a.connects.append((b, weight))
    b.connects.append((a, weight))

def genDirectionalNode() -> Position:
    up = Node([])
    down = Node([])
    left = Node([])
    right = Node([])
    addUndirectedEdge(up, left, TURN_PENALTY)
    addUndirectedEdge(up, right, TURN_PENALTY)
    addUndirectedEdge(down, left, TURN_PENALTY)
    addUndirectedEdge(down, right, TURN_PENALTY)
    addUndirectedEdge(up, down, 0)
    addUndirectedEdge(left, right, 0)
    position = Position(up, down, left, right)
    up.position = position
    down.position = position
    left.position = position
    right.position = position
    return position

def connectToGrid(a: Position, x: int, y: int):
    # Look left and up
    if x > 0:
        b = position_grid[y][x-1]
        if isinstance(b, Position):
            addUndirectedEdge(a.left, b.right, STEP_PENALTY)
    if y > 0:
        b = position_grid[y-1][x]
        if isinstance(b, Position):
            addUndirectedEdge(a.up, b.down, STEP_PENALTY)

start = None
end = None

# Create nodes
for y in range(len(grid)):
    node_row: List[Position | None] = []
    for x in range(len(grid[y])):
        match grid[y][x]:
            case Spaces.WALL:
                node_row.append(None)
            case Spaces.EMPTY:
                position = genDirectionalNode()
                node_row.append(position)
            case Spaces.START:
                position = genDirectionalNode()
                node_row.append(position)
                start = position.right
            case Spaces.END:
                end = genDirectionalNode()
                node_row.append(end)
            case e:
                print(f"Unknown item in map {e=}")
                exit()
    position_grid.append(node_row)

dist = {}
prev = {}
Q: List[Node]= []

# Connect edges in the grid
for y in range(len(position_grid)):
    for x in range(len(position_grid[y])):
        position = position_grid[y][x]
        # print(f"{x=} {y=}")
        if isinstance(position, Position):
            connectToGrid(position, x, y)
            dist[id(position.up)] = math.inf
            prev[id(position.up)] = None
            dist[id(position.down)] = math.inf
            prev[id(position.down)] = None
            dist[id(position.left)] = math.inf
            prev[id(position.left)] = None
            dist[id(position.right)] = math.inf
            prev[id(position.right)] = None
            Q.append(position.up)
            Q.append(position.down)
            Q.append(position.left)
            Q.append(position.right)

dist[id(start)] = 0
# prev[id(start)] = None # likely not necessary

print("Start solving")

while len(Q) > 0:
    print(f"Remaining length: {len(Q)}")
    Q.sort(key=lambda q: dist[id(q)])
    u = Q[0]
    Q = Q[1:]
    
    for (v, w) in u.connects:
        alt = dist[id(u)] + w
        if alt < dist[id(v)]:
            dist[id(v)] = alt
            prev[id(v)] = u

print("Done with bulding the map")

print(dist[id(end.down)])
print(dist[id(end.up)])
print(dist[id(end.left)])
print(dist[id(end.right)])

final_node = end.down if dist[id(end.down)] < dist[id(end.left)] else end.left

rev_set: Set[Position] = set()
def walk_back(me: Node):
    rev_set.add(id(me.position))
    if dist[id(me)] == 0: # If we are at the start
        return
    previous: Node = prev[id(me)]
    previous_distance: int = dist[id(previous)]
    my_distance: int = dist[id(me)]
    for (c, edge_length) in me.connects: # All with optimal path should end on this node with the same distance
        if (previous_distance + edge_length == my_distance):
            walk_back(c)
        # elif edge_length == 0:



def printWithWalkback():
    for row in position_grid:
        position: Position | None
        for position in row:
            if isinstance(position, Position):
                if id(position) in rev_set:
                    print("O", end="")
                else:
                    print('.', end="")
            else:
                print('#', end="")
        print()

def printWithDist():
    for row in position_grid:
        position: Position | None
        for position in row:
            if isinstance(position, Position):
                print(str(min(dist[id(position.down)], dist[id(position.left)])).zfill(5), end="")
            else:
                print('#####', end="")
            print("  ", end="")
        print()

    

walk_back(final_node)

printWithWalkback()
printWithDist()
print(rev_set)
print(len(rev_set))
print(max(dist.values()))

# PT 2
# Find all seats that are part of the optimum map