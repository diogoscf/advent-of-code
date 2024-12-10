import os
import numpy as np

filename = "day10.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
# txt = """89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732"""
grid = np.array([list(l) for l in txt.split("\n")], dtype=np.int32)

def check_for_path(curr_val, curr_idx, excluded, grid_shape, grid):
    possibilities = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]]) + curr_idx
    actual_possible = []
    # print(excluded)
    for new_idx in possibilities:
        new_idx = tuple(new_idx)
        if new_idx in excluded: # save some time by not checking backwards
            continue
        if new_idx[0] < 0 or new_idx[0] >= grid_shape[0] or new_idx[1] < 0 or new_idx[1] >= grid_shape[1]:
            continue
        if grid[new_idx] == curr_val+1:
            actual_possible.append(new_idx)
    if len(actual_possible) == 0:
        return False, []
    return True, actual_possible

def find_paths(grid, curr_val, curr_idx, idx_list, grid_shape):
    # curr_val = grid[tuple(curr_idx)]
    paths = []
    investigating = []
    next_options = check_for_path(curr_val, curr_idx, idx_list, grid_shape, grid)
    if not next_options[0]:
        return False, []
    
    for next_idx in next_options[1]:
        investigating = idx_list + [next_idx]
        if curr_val + 1 == 9:
            paths.append(investigating)

        path_ends, new_paths = find_paths(grid, curr_val+1, next_idx, investigating, grid_shape)
        if path_ends:
            for p in new_paths:
                paths.append(p)

    if len(paths) == 0:
        return False, []
    return True, paths

trail_head_idxs = np.where(grid == 0)
grid_shape = grid.shape

total_p1 = 0
total_p2 = 0
for trail_head in zip(*trail_head_idxs):
    trails_possible, trails = find_paths(grid, 0, trail_head, [trail_head], grid_shape)
    if trails_possible:
        end_points = set([t[-1] for t in trails]) # remove duplicate ends
        total_p1 += len(end_points)
        total_p2 += len(trails)

print(f"Part 1: {total_p1}")
print(f"Part 2: {total_p2}") # fun fact: I'd accidentally solved this part first while trying to do part 1 :)
