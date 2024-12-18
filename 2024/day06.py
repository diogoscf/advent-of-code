import os
import numpy as np

filename = "day06.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
loc_grid = np.array([list(l) for l in txt.split("\n")])



dir_dict = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
change_dir = {"^": ">", ">": "v", "v": "<", "<": "^"}

init_pos = np.where(loc_grid == "^") # starts wth ^

def stuck_in_loop(grid):
    grid_shape = grid.shape
    max_dir = max(grid_shape)
    check_grid = np.full(grid_shape, ".")
    obstacles_x, obstacles_y = np.where(grid == "#")
    obstacles = set(zip(obstacles_x, obstacles_y))

    for e, d in dir_dict.items():
        if e in grid:
            curr_pos = np.where(grid == e)
            grid[curr_pos] = "x"
            direction = d
            dir_marker = e
            break
    
    while True:
        direction = dir_dict[dir_marker]
        
        idxs = [] # indices travelled in this direction
        event = None # what cause the loop to stop
        for n in range(1, max_dir):
            new_idx = tuple([i + (d*n) for i, d in zip(curr_pos, direction)])
            if new_idx[0] < 0 or new_idx[1] < 0 or new_idx[0] >= grid_shape[0] or new_idx[1] >= grid_shape[1]:
                event = "out"
                break # guard has left
            
            if (new_idx[0][0], new_idx[1][0]) in obstacles:
                event = "turn"
                break
            # print(new_idx)
            idxs.append(new_idx)
        
        
        curr_pos = idxs[-1] if len(idxs) > 0 else curr_pos
        
        # print("turn/out", curr_pos, event, change_dir[dir_marker], check_grid[curr_pos])

        if event == "turn":
            dir_marker = change_dir[dir_marker]
            if dir_marker == check_grid[curr_pos]: # already new position in curr_pos
                return True, grid

        for idx in idxs:
            grid[idx] = "x"
            check_grid[idx] = dir_marker # assign here to avoid problematic turns

        if event == "out":
            break
    
    return False, grid



_, path = stuck_in_loop(loc_grid.copy())
instances_X = len(np.where(path == "x")[0])

# np.savetxt("day6_path.txt", path, fmt="%s")


# yes this is brute force but who cares
total_loop = 0
for i in range(loc_grid.shape[0]):
    for j in range(loc_grid.shape[1]):
        if loc_grid[i, j] == "^" or path[i,j] != "x": # initial position, or doesn't pass in original path
            continue

        curr_grid = loc_grid.copy()
        curr_grid[i, j] = "#"
        stuck, _ = stuck_in_loop(curr_grid)
        if stuck:
            total_loop += 1
    print(f"Finished {i}, Current total: {total_loop}", flush=True) 


print("Part 1:", instances_X) 
print("Part 2:", total_loop)