import os
import numpy as np

filename = "day20.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
grid = np.array([list(l) for l in txt.split("\n")])

moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

possible_locs = set([(a, b) for a, b in np.array(np.where(grid == ".")).T])
end_loc = (np.where(grid == "E")[0][0], np.where(grid == "E")[1][0])
init_loc = (np.where(grid == "S")[0][0], np.where(grid == "S")[1][0])
possible_locs.update([end_loc, init_loc])

def best_path_finder_BFS(init_loc, end_loc, possible_locs, moves):
    queue = {}  # score: [(location, path),...]
    known_locs = {init_loc: 0}  # (location): (best)score
    queue[0] = [(init_loc, [init_loc])]

    while True:
        if not queue:
            return False, None
        score = min(queue.keys())
        (curr_loc, path) = queue[score].pop()
        if not queue[score]:
            del queue[score]
        for m in moves:
            new_loc = (curr_loc[0] + m[0], curr_loc[1] + m[1])

            if new_loc not in possible_locs or new_loc in path:
                continue

            new_score = score + 1

            if new_loc == end_loc:
                return True, path + [new_loc]

            # ignore cases where we got here with a higher score
            if new_loc in known_locs and known_locs[new_loc] <= new_score:
                continue

            known_locs[new_loc] = new_score
            queue[new_score] = queue.get(new_score, []) + [(new_loc, path + [new_loc])]


# not necessary to do a BFS but I cba to write new code and this doesn't take *that* long
# (particularly compared to the rest of the code :)))
_, path = best_path_finder_BFS(init_loc, end_loc, possible_locs, moves)


total_p1 = 0
total_p2 = 0

min_skip = 100
max_cheat_len_p1 = 2
max_cheat_len_p2 = 20
for i, loc1 in enumerate(path[:-(min_skip)]):
    for j, loc2 in enumerate(path[i + (min_skip):]):
        distance = abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

        if 2 <= distance <= max_cheat_len_p1 and j - distance >= 0:
            total_p1 += 1
        
        if 2 <= distance <= max_cheat_len_p2 and j - distance >= 0:
            total_p2 += 1

print("Part 1:", total_p1)
print("Part 2:", total_p2)