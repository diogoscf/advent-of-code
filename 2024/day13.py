import os
import numpy as np
import re

pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"

filename = "day13.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
# txt = """Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279"""

matches = re.findall(pattern, txt)

total_p1 = 0
total_p2 = 0

for machine in matches:
    dxa, dya, dxb, dyb, xf, yf = map(int, machine)
    A = np.array([[dxa, dxb], [dya, dyb]])
    b = np.array([xf, yf])
    a_presses, b_presses = np.linalg.solve(A, b) # none of the matrices are singular so this works
    if a_presses < 0 or a_presses > 100 or b_presses < 0 or b_presses > 100:
        continue
    # check if integer solution. can't just use is_integer() because of floating point errors
    a_rounded = np.round(a_presses).astype(int)
    b_rounded = np.round(b_presses).astype(int)
    if (dxa * a_rounded + dxb * b_rounded) == xf and (dya * a_rounded + dyb * b_rounded) == yf:
        total_p1 += a_rounded*3 + b_rounded

for machine in matches:
    dxa, dya, dxb, dyb, xf, yf = map(int, machine)
    xf += 10000000000000
    yf += 10000000000000

    A = np.array([[dxa, dxb], [dya, dyb]])
    b = np.array([xf, yf])
    a_presses, b_presses = np.linalg.solve(A, b) # none of the matrices are singular so this works
    if a_presses < 0 or b_presses < 0:
        continue
    # check if integer solution. can't just use is_integer() because of floating point errors
    a_rounded = np.round(a_presses).astype(np.int64)
    b_rounded = np.round(b_presses).astype(np.int64)
    if (dxa * a_rounded + dxb * b_rounded) == xf and (dya * a_rounded + dyb * b_rounded) == yf:
        total_p2 += a_rounded*3 + b_rounded

print("Part 1:", total_p1)
print("Part 2:", total_p2)