import os
import sys
import numpy as np

filename = "day16.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

def pre_process_maze(grid):
    # Remove all dead ends
    while True:
        changes = False
        for i, row in enumerate(grid):
            for j, el in enumerate(row):
                if el == ".":
                    top = grid[i - 1, j] if i > 0 else "#"
                    bottom = grid[i + 1, j] if i < grid.shape[0] - 1 else "#"
                    left = grid[i, j - 1] if j > 0 else "#"
                    right = grid[i, j + 1] if j < grid.shape[1] - 1 else "#"
                    if np.count_nonzero(np.array([top, bottom, left, right]) == "#") >= 3:
                        grid[i, j] = "#"
                        changes = True
        if not changes:
            break
    return grid


grid = pre_process_maze(np.array([list(l) for l in txt.split("\n")]))

moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

possible_locs = set([(a, b) for a, b in np.array(np.where(grid == ".")).T])
end_loc = (np.where(grid == "E")[0][0], np.where(grid == "E")[1][0])
init_loc = (np.where(grid == "S")[0][0], np.where(grid == "S")[1][0])
possible_locs.update([end_loc, init_loc])


# breadth first search
def best_path_finder_BFS(init_loc, init_dir, end_loc, possible_locs, moves):
    queue = {}  # score: [(location, direction, path),...]
    known_locs = {(init_loc, init_dir): 0}  # (location, direction): (best)score
    queue[0] = [(init_loc, init_dir, [init_loc])]

    path_locs = set()
    while True:
        score = min(queue.keys())
        (curr_loc, curr_dir, path) = queue[score].pop()
        if not queue[score]:
            del queue[score]

        if curr_loc == end_loc:  # nothing better!
            final_score = score
            path_locs.update(path)
            break

        for m in moves:
            new_loc = (curr_loc[0] + m[0], curr_loc[1] + m[1])
            if new_loc not in possible_locs or (m[0] * curr_dir[0] + m[1] * curr_dir[1] == -1):
                continue

            extra_score = 1 if m == curr_dir else 1001
            new_score = score + extra_score

            if new_loc == end_loc:
                queue[new_score] = queue.get(new_score, []) + [(new_loc, m, path + [new_loc])]
                continue

            # ignore cases where we got here with a higher score
            if (new_loc, m) in known_locs and known_locs[(new_loc, m)] < new_score:
                continue

            known_locs[(new_loc, m)] = new_score
            queue[new_score] = queue.get(new_score, []) + [(new_loc, m, path + [new_loc])]

    for loc, _, p in queue[final_score]:
        if loc == end_loc:
            path_locs.update(p)

    return final_score, path_locs


score_p1, path_locs = best_path_finder_BFS(init_loc, (0, 1), end_loc, possible_locs, moves)

print("Part 1:", score_p1)
print("Part 2:", len(path_locs))
