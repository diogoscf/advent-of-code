import os
import numpy as np
import re

pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"

filename = "day14.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
# txt = """"""

matches = re.findall(pattern, txt)
robots = [(int(x), int(y), int(vx), int(vy)) for x, y, vx, vy in matches]

w, h = 101, 103 # width, height

def get_score(robots, t, w, h):
    q1, q2, q3, q4 = 0, 0, 0, 0

    for xi, yi, vxi, vyi in robots:
        xf = (xi + vxi * t) % w
        yf = (yi + vyi * t) % h
        if xf < w//2 and yf < h//2:
            q1 += 1
        elif xf > w//2 and yf < h//2:
            q2 += 1
        elif xf < w//2 and yf > h//2:
            q3 += 1
        elif xf > w//2 and yf > h//2:
            q4 += 1
    
    return q1*q2*q3*q4

def define_figure(robots, t, w, h):
    figure = np.full((w, h), " ")
    for xi, yi, vxi, vyi in robots:
        xf = (xi + vxi * t) % w
        yf = (yi + vyi * t) % h
        figure[xf, yf] = "#"
    return figure

print("Part 1:", get_score(robots, 100, w, h))


filename = "day14_part2.txt"
try:
    os.remove(filename) # make sure file iss clear
except OSError:
    pass
# after 10403 it will loop (101x103). initially starting with 0 to 200, an interesting vertical pattern appears at t=20 and t=121
# the pattern is similar but not identical, given the 101 step keeping x-wise values the same (but not y => 103)
# so we loop from 20 in steps of 101 until 10403
# christmas tree appears at t=6888
with open(filename, "ab") as f:
    # for t in range(200): 
    for t in range(20,10403,101): 
        f.write(b"============================================================  t=" + str(t).encode() + b"  ============================================================\n")
        np.savetxt(f, define_figure(robots, t, w, h).T, fmt="%s", delimiter="")   
        f.write(b"\n\n\n\n\n\n")