import os
import numpy as np
import itertools

filename = "day8.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
grid = np.array([list(l) for l in txt.split("\n")])
node_grid1 = np.full(grid.shape, ".")
node_grid2 = np.full(grid.shape, ".")

unique_vals = np.unique(grid)

r, c = grid.shape

for antenna_type in unique_vals:
    if antenna_type == ".":
        continue

    idxs = list(zip(*np.where(grid == antenna_type)))
    for ((x1, y1), (x2, y2)) in itertools.combinations(idxs, 2):
        dx = x2 - x1
        dy = y2 - y1

        # Part 1
        new1 = (x1 - dx, y1 - dy)
        new2 = (x2 + dx, y2 + dy)
        if new1[0] >= 0 and new1[1] >= 0 and new1[0] < r and new1[1] < c:
            node_grid1[new1] = "#"
        if new2[0] >= 0 and new2[1] >= 0 and new2[0] < r and new2[1] < c:
            node_grid1[new2] = "#"
        
        # Part 2
        node_grid2[(x1,y1)] = "#"
        node_grid2[(x2,y2)] = "#"
        curr = (x1, y1)
        while True:
            curr = (curr[0] - dx, curr[1] - dy)
            if curr[0] >= 0 and curr[1] >= 0 and curr[0] < r and curr[1] < c:
                node_grid2[curr] = "#"
            else:
                break
        curr = (x2, y2)
        while True:
            curr = (curr[0] + dx, curr[1] + dy)
            if curr[0] >= 0 and curr[1] >= 0 and curr[0] < r and curr[1] < c:
                node_grid2[curr] = "#"
            else:
                break
    # print(idxs)

# print(unique_vals[2])

n_antinodes1 = np.count_nonzero(node_grid1 == "#")
n_antinodes2 = np.count_nonzero(node_grid2 == "#")
print("Part 1:", n_antinodes1)
print("Part 2:", n_antinodes2)