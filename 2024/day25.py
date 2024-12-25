import os
import numpy as np
import itertools

filename = "day25.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

subgrids = txt.split("\n\n")

keys = []
locks = []

for s in subgrids:
    grid = np.array([list(l) for l in s.split("\n")])
    if grid[0,0] == "#": # lock
        locks.append(np.count_nonzero(grid[1:,:] == "#", axis=0))
    else: # key
        keys.append(np.count_nonzero(grid[:-1,:] == "#", axis=0))

total_p1 = 0
for key, lock in itertools.product(keys, locks):
    if np.all(key+lock <= 5):
        total_p1 += 1

print("Part 1:", total_p1)