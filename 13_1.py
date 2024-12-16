from typing import List
import cpmpy as cp
import re

def solve(a_x, a_y, b_x, b_y, res_x, res_y):
    a = cp.intvar(0, 10000000000000, name="a")
    b = cp.intvar(0, 10000000000000, name="b")
    model = cp.Model()
    model += [res_x == ((a * a_x) + (b * b_x))]
    model += [res_y == ((a * a_y) + (b * b_y))]
    model.minimize(3 * a + b)

    if model.solve():
        # print("Solution found")
        # print(f"A: {a.value()} \tB: {b.value()}")
        solves.append(3 * a.value() + b.value())
    # else:
    #     print("No solution found :(")

f = open("13.txt", "r")
lines = f.readlines()
lines = list(map(lambda l: l.strip('\n'), lines))
solves : List[int]= []
while lines != []:
    A_line = re.search("Button A: X\\+([0-9]+), Y\\+([0-9]+)", lines[0])
    A_x = int(A_line.group(1))
    A_y = int(A_line.group(2))
    B_line = re.search("Button B: X\\+([0-9]+), Y\\+([0-9]+)", lines[1])
    B_x = int(B_line.group(1))
    B_y = int(B_line.group(2))
    result_line = re.search("Prize: X=([0-9]+), Y=([0-9]+)", lines[2])
    res_x = int(result_line.group(1)) + 10000000000000
    res_y = int(result_line.group(2)) + 10000000000000
    solve(A_x, A_y, B_x, B_y, res_x, res_y)
    lines = lines[4:]
f.close()

print(sum(solves))

