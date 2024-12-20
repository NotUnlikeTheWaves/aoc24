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

##grid = list (map(lambda l: list(l.strip('\n')), lines))
grid = []
grid_length = 71
for y in range(grid_length):
    grid.append(list('.' * grid_length))

def printBasicGrid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(grid[y][x], end="")
        print()

#pt 1:
lines = lines[0:1024]
for line in lines:
    s = line.split(',')
    x = int(s[0])
    y = int(s[1])
    grid[y][x] = Spaces.WALL

grid[0][0] = Spaces.START
grid[grid_length-1][grid_length-1] = Spaces.END


printBasicGrid()
print(lines)

position_grid = []

def addUndirectedEdge(a: Node, b: Node, weight: int):
    a.connects.append((b, weight))
    b.connects.append((a, weight))


start = None
end = None

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

dist = {}
prev = {}
Q: List[Node]= []

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
# prev[id(start)] = None # likely not necessary

print("Start solving")

while len(Q) > 0:
    # print(f"Remaining length: {len(Q)}")
    Q.sort(key=lambda q: dist[id(q)])
    u = Q[0]
    Q = Q[1:]
    
    for (v, w) in u.connects:
        alt = dist[id(u)] + w
        if alt < dist[id(v)]:
            dist[id(v)] = alt
            prev[id(v)] = u

print("Done with bulding the map")

print(dist[id(end)])


# rev_set: Set[Position] = set()
# check_list: List[Position] = list()
# def walk_back(me: Node, idx: int):
#     rev_set.add(id(me.position))
#     if dist[id(me)] == 0: # If we are at the start
#         return
#     previous: Node = prev[id(me)]
#     previous_distance: int = dist[id(previous)]
#     my_distance: int = dist[id(me)]
#     for (c, edge_length) in me.connects: # All with optimal path should end on this node with the same distance
#         # print(f"A: {idx}")
#         if (dist[id(c)] + edge_length == my_distance):
#             # print(f"{previous_distance=} {edge_length=} {my_distance=}")
#             walk_back(c, idx+1)
#         # elif edge_length == 0:



# def printWithWalkback():
#     for row in position_grid:
#         position: Position | None
#         for position in row:
#             if isinstance(position, Position):
#                 if id(position) in rev_set:
#                     print("O", end="")
#                 else:
#                     print('.', end="")
#             else:
#                 print('#', end="")
#         print()

# def printWithDist():
#     for row in position_grid:
#         position: Position | None
#         for position in row:
#             if isinstance(position, Position):
#                 print(str(min(dist[id(position.updown)], dist[id(position.leftright)])).zfill(5), end="")
#             else:
#                 print('#####', end="")
#             print("  ", end="")
#         print()

    

# walk_back(final_node, 0)

# printWithWalkback()
# printWithDist()
# print(rev_set)
# print(len(rev_set))
# print(max(dist.values()))

# PT 2
# Find all seats that are part of the optimum map