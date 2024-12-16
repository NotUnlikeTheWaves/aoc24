from dataclasses import dataclass
import re
from typing import List
import numpy as np
# width = 11
# width_half = 5
# height = 7
# height_half = 3
width = 101
width_half = 50
height = 103
height_half = 51

import time

@dataclass
class Robot():
    pos_x: int
    pos_y: int
    vel_x: int
    vel_y: int

    def step(self, n: int):
        self.pos_x = (self.pos_x + self.vel_x * n) % width
        self.pos_y = (self.pos_y + self.vel_y * n) % height
    
    def get_quadrant(self):
        print(f"RX: {self.pos_x} \t-- RY: {self.pos_y}")
        if self.pos_x == width_half or self.pos_y == height_half:
            return np.array([[0,0],[0,0]])
        if self.pos_x > width_half:
            if self.pos_y > height_half:
                print("TR")
                return np.array([[0,1],[0,0]])
            else:
                print("BR")
                return np.array([[0,0],[0,1]])
        elif self.pos_x < width_half:
            if self.pos_y > height_half:
                print("TL")
                return np.array([[0,0],[1,0]])
            else:
                return np.array([[1,0], [0,0]])
    
    def get_on_map(self):
        arr = np.zeros((height, width))
        arr[self.pos_y][self.pos_x] = 1
        return arr

robots : List[Robot] = []
f = open("14.txt", "r")
lines = f.readlines()
for line in lines:
    re_line = re.search("p=(.*),(.*) v=(.*),(.*)", line)
    pos_x = int(re_line.group(1))
    pos_y = int(re_line.group(2))
    vel_x = int(re_line.group(3))
    vel_y = int(re_line.group(4))
    robot = Robot(pos_x, pos_y, vel_x, vel_y)
    # robot.step(100) # P1
    robots.append(robot)

# print(sum(map(lambda r: r.get_quadrant(), robots))) # P1

def get_map():
    arr = np.zeros((height, width))
    for r in robots:
        arr[r.pos_y][r.pos_x] = 1
    return arr

def print_map(map):
    for y in range(height):
        for x in range(width):
            pt = "*" if map[y][x] > 0 else " "
            print(pt, end="")
        print()

robots[0].pos_x -= robots[0].vel_x
robots[0].pos_y -= robots[0].vel_y
f.close()
idx = 0
first = get_map()

for r in robots:
    r.step(idx)
while True:
    idx += 1
    for robot in robots:
        robot.step(1)
    rmap = get_map()
    # print_map(rmap)
    # if idx % 1000 == 0:
    #     print(f"Step no: {idx}")
    print(f"Step no: {idx}")

    if np.array_equal(rmap, first):
        print("repeat found!")
        break
    # time.sleep(0.1)
