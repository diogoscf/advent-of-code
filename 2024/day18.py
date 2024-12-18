import os
import sys
import numpy as np

filename = "day18.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

fallen_bytes = [(int(a), int(b)) for a, b in [l.split(",") for l in txt.split("\n")]]

moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
h, w = 70 + 1, 70 + 1
possible_locs = set([(a, b) for a in range(h) for b in range(w)])

end_loc = (h - 1, w - 1)
init_loc = (0, 0)

possible_locs = possible_locs - set(fallen_bytes[:1024])


# from day 16
def best_path_finder_BFS(init_loc, end_loc, possible_locs, moves):
    queue = {}  # score: [(location, path),...]
    known_locs = {init_loc: 0}  # (location): (best)score
    queue[0] = [(init_loc, set([init_loc]))]

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
                return True, new_score

            # ignore cases where we got here with a higher score
            if new_loc in known_locs and known_locs[new_loc] <= new_score:
                continue

            known_locs[new_loc] = new_score
            queue[new_score] = queue.get(new_score, []) + [(new_loc, path.union([new_loc]))]


_, score_p1 = best_path_finder_BFS(init_loc, end_loc, possible_locs, moves)

part2 = None
for a, b in fallen_bytes[1024:]:
    possible_locs.discard((a, b))
    if not best_path_finder_BFS(init_loc, end_loc, possible_locs, moves)[0]:
        part2 = (a, b)
        break


print("Part 1:", score_p1)
print("Part 2:", part2)
# NOTE: takes about 20 seconds