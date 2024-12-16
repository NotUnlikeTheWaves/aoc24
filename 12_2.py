from typing import Tuple


f = open("12.txt", "r")


grid = f.readlines()

#surround with zeroes
line_length = len(grid[0])
grid = list(map(lambda line: "0" + line.strip('\n') + "0", grid))
grid.insert(0, (line_length+2) * '0')
grid.append((line_length+2) * '0')

grid = list(
        map(lambda line: 
            list(
                zip(
                    list(line), 
                    [False] * len(line),
                    ([[[False, False], [False, False]] for _ in range(len(line))]))), 
            grid)
    )

print(f"{grid=}")

# for i in grid:
#     for j in i:
#         print(j, end=", ")
#     print()

def t(n):
    return int((n + 1) / 2)


def walkY(x, y, nx, plot) -> bool:
    dx = t(nx-x)

    for ny in list(range(0, y))[::-1]:
        if grid[ny][x][0] != plot or grid[ny][nx][0] == plot:
            break
        if grid[ny][x][2][0][dx] == True:
            return True
    
    for ny in list(range(y+1, len(grid))):
        if grid[ny][x][0] != plot or grid[ny][nx][0] == plot:
            break
        if grid[ny][x][2][0][dx] == True:
            return True
    return False

def walkX(x, y, ny, plot) -> bool:
    dy = t(ny-y)

    for nx in list(range(0, x))[::-1]:
        if grid[y][nx][0] != plot or grid[ny][nx][0] == plot:
            break
        if grid[y][nx][2][1][dy] == True:
            return True
    
    for nx in list(range(x+1, len(grid[0]))):
        if grid[y][nx][0] != plot or grid[ny][nx][0] == plot:
            break
        if grid[y][nx][2][1][dy] == True:
            return True
    return False

def get_group_recursive(x: int, y: int, plot: str) -> Tuple[str, int, int]:
    # print(f"suc: {grid[y][x]} -- find {c}")
    if grid[y][x][0] != plot or grid[y][x][1] == True:
        # print("found")
        return (plot, 0, 0)
    neighbours = get_neighbours(x, y)
    land_size = 1
    edge_length = 0
    grid[y][x] = (plot, True, grid[y][x][2])
    # grid[y][x] = (plot, True, [[False, False], [False, False]])
    empty_neighs = []
    true_neighs = []
    for (nx, ny) in neighbours:
        if grid[ny][nx][0] == plot:
            true_neighs.append((nx, ny))
        else:
            empty_neighs.append((nx, ny))

    # if plot == 'M':
    #     print(f"My pos: {x}/{y}")
    #     print(f"{empty_neighs=}")
    #     print(f"{true_neighs=}")
    
    # if plot == 'A':
    #     pass

    # print("((*))")


    # Make recursive
    for (nx, ny) in empty_neighs:
        # This is an edge to the left or right
        if abs(x - nx) > 0:
            dx = t(nx-x)


            # Propagate above/below info on this edge
            # grid[y][x][2][0][dx] = (grid[y-1][x][2][0][dx] and grid[y-1][x][0] == plot) or (grid[y+1][x][2][0][dx] and grid[y+1][x][0] == plot)
            grid[y][x][2][0][dx] = walkY(x, y, nx, plot)
            if grid[y][x][2][0][dx] == False:
                # if (x == 2 and y == 3 and dx == 1):
                #     print(f"setting this from code {plot=}")
                grid[y][x][2][0][dx] = True
                edge_length += 1
            # elif plot == 'M':
            #     print(f"My VERTICAL edge to {nx}/{ny} is already covered due to")
            #     print(f"COND A: {grid[y-1][x][2][0][dx]}  B: {grid[y-1][x][0] == plot}")
            #     print(f"COND C: {grid[y+1][x][2][0][dx]}  D: {grid[y+1][x][0] == plot}")
            #     print(f"{x=} y={y+1} {dx=}")
        # This is an edge to the top or bottom
        elif abs(y - ny) > 0:
            dy = t(ny-y)
            # Propagate left/right info on this edge
            # grid[y][x][2][1][dy] = (grid[y][x-1][2][1][dy] and grid[y][x-1][0] == plot) or (grid[y][x+1][2][1][dy] and grid[y][x+1][0] == plot)
            grid[y][x][2][1][dy] = walkX(x, y, ny, plot)
            if grid[y][x][2][1][dy] == False:
                grid[y][x][2][1][dy] = True
                edge_length += 1
            # elif plot == 'M':
            #     print(f"My HORIZONTAL edge to {nx}/{ny} is already covered due to")
            #     print(f"COND A: {grid[y][x-1][2][1][dy]}  B: {grid[y][x-1][0] == plot}")
            #     print(f"COND C: {grid[y][x+1][2][1][dy]}  D: {grid[y][x+1][0] == plot}")
    
    # print()
    for (nx, ny) in true_neighs:
        (_, nls, nel) = get_group_recursive(nx, ny, plot)
        land_size += nls
        edge_length += nel 
    
    return (plot, land_size, edge_length)


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