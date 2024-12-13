import os
import numpy as np
import itertools

filename = "day12.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
# txt = """RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE"""
grid = np.array([list(l) for l in txt.split("\n")])

known_ids = set()
score = 0

directions = np.array([(0, 1), (1, 0), (0, -1), (-1, 0)])


def get_score(i, j, val, grid):
    perimeter, locs = find_next(i, j, val, grid, set())
    area = len(locs)
    sides = calc_sides(val, locs, perimeter, grid)
    known_ids.update(locs)
    return area * perimeter, area * sides

def grid_val(i,j, grid):
    if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]):
        return None
    return grid[i, j]

def calc_sides(val, locs, perimeter, grid):
    sides = perimeter
    for loc1, loc2 in itertools.combinations(locs, 2):
        if abs(loc1[0] - loc2[0]) == 1 and abs(loc1[1] - loc2[1]) == 0: # same y, different x (by 1)
            x1, y1 = loc1
            x2, y2 = loc2
            above = (x1, y1+1), (x2, y2+1)
            below = (x1, y1-1), (x2, y2-1)
            if all([a in known_ids for a in above]) or all([grid_val(*a, grid) != val for a in above]):
                sides -= 1
            if all([b in known_ids for b in below]) or all([grid_val(*b, grid) != val for b in below]):
                sides -= 1

        if abs(loc1[0] - loc2[0]) == 0 and abs(loc1[1] - loc2[1]) == 1: # same x, different y (by 1)
            x1, y1 = loc1
            x2, y2 = loc2
            left = (x1-1, y1), (x2-1, y2)
            right = (x1+1, y1), (x2+1, y2)
            if all([l in known_ids for l in left]) or all([grid_val(*l, grid) != val for l in left]):
                sides -= 1
            if all([r in known_ids for r in right]) or all([grid_val(*r, grid) != val for r in right]):
                sides -= 1
    
    return sides


def find_next(i, j, val, grid, locs):
    new_poss = directions + (i, j)
    # locs = curr_ids.copy()
    locs.add((i,j))
    perimeter = 0
    for x, y in new_poss:
        if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
            perimeter += 1
            continue
        if (x, y) in locs:  # already in region, do nothing
            continue
        if (x, y) in known_ids:  # known but not from here i.e. different region
            perimeter += 1
            continue
        if grid[x, y] == val:
            locs.add((x, y))
            p, l = find_next(x, y, val, grid, locs)
            perimeter += p
            locs.update(l)
        else:
            perimeter += 1  # different region
    return perimeter, locs

score_p1 = 0
score_p2 = 0
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        if (i, j) in known_ids:
            continue
        score1, score2 = get_score(i, j, val, grid)
        score_p1 += score1
        score_p2 += score2

print(f"Part 1: {score_p1}")
print(f"Part 2: {score_p2}")
