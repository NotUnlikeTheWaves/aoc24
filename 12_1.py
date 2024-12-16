from typing import Tuple


f = open("12.txt", "r")


grid = f.readlines()

#surround with zeroes
line_length = len(grid)
grid = list(map(lambda line: "0" + line.strip('\n') + "0", grid))
grid.insert(0, (line_length+2) * '0')
grid.append((line_length+2) * '0')

grid = list(map(lambda line: list(zip(list(line), [False] * len(line))), grid))


for i in grid:
    for j in i:
        print(j, end=", ")
    print()

def get_group_recursive(x: int, y: int, c: str) -> Tuple[str, int, int]:
    # print(f"suc: {grid[y][x]} -- find {c}")
    if grid[y][x][0] != c or grid[y][x][1] == True:
        # print("found")
        return (c, 0, 0)
    neighbours = get_neighbours(x, y)
    land_size = 1
    edge_length = 0
    # print("sos")
    # print(grid[y][x])
    grid[y][x] = (c, True)
    # print(grid[y][x])
    # print("eos")
    for (nx, ny) in neighbours:
        if grid[ny][nx][0] == c:
            (_, nls, nel) = get_group_recursive(nx, ny, c)
            land_size += nls
            edge_length += nel
        else:
            edge_length += 1
    return (c, land_size, edge_length)


def get_neighbours(x,y):
    return [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]

print(type(grid))

groups = []

for y in range(len(grid)):
    for x in range(len(grid[y])):
        pos = grid[y][x]
        char = pos[0]
        visited = pos[1]
        if char == '0' or visited == True:
            continue
        group = get_group_recursive(x, y, char)
        groups.append(group)
        print(group)


print(sum(map(lambda g: g[1] * g[2], groups)))



f.close()