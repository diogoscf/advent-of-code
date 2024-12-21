import os
import numpy as np
import itertools

filename = "day21.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
# txt = "029A"
codes = txt.split("\n")

numkey_locs = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
dirkey_locs = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}


def find_numkey_opts(code, key_locs=numkey_locs):
    options = []
    prev = key_locs["A"]
    for k in code:
        newloc = key_locs[k]
        distance_x = newloc[0] - prev[0]
        distance_y = newloc[1] - prev[1]

        k_x = "v" * distance_x if distance_x > 0 else "^" * (-distance_x)
        k_y = ">" * distance_y if distance_y > 0 else "<" * (-distance_y)

        total_key_presses = k_x + k_y
        alloptions = set(itertools.permutations(total_key_presses))

        if (prev[0] == 3 or newloc[0] == 3) and (prev[1] == 0 or newloc[1] == 0):  # gap at (3,0)
            toremove = tuple(k_x + k_y) if distance_x > 0 else tuple(k_y + k_x)
            alloptions.discard(toremove)

        options.append(["".join(option) + "A" for option in alloptions])
        prev = newloc

    return options


known = {}  # sequence: {1: len_1pad, 2: len_2pads, 3: len_3pads, ...}


def determine_shortest_dirkeypath(sequence, numdirpads, key_locs=dirkey_locs):
    prev = key_locs["A"]
    lenkeys = 0  # there will be one A press at the end
    if sequence in known:
        if numdirpads in known[sequence]:
            return known[sequence][numdirpads]

    for k in sequence:
        newloc = key_locs[k]
        distance_x = newloc[0] - prev[0]
        distance_y = newloc[1] - prev[1]

        k_x = "v" * distance_x if distance_x > 0 else "^" * (-distance_x)
        k_y = ">" * distance_y if distance_y > 0 else "<" * (-distance_y)

        total_key_presses = k_x + k_y
        alloptions = set(itertools.permutations(total_key_presses))

        if (prev[0] == 0 or newloc[0] == 0) and (prev[1] == 0 or newloc[1] == 0):  # gap at (0,0)
            toremove = tuple(k_y + k_x) if distance_x > 0 else tuple(k_x + k_y)
            alloptions.discard(toremove)

        newseq_opts = ["".join(option) + "A" for option in alloptions]
        if numdirpads > 1:
            lenkeys += min([determine_shortest_dirkeypath(seq, numdirpads - 1, key_locs) for seq in newseq_opts])
        else:
            lenkeys += len(newseq_opts[0])
        prev = newloc

    if sequence not in known:
        known[sequence] = {}
    known[sequence][numdirpads] = lenkeys

    return lenkeys


total_p1 = 0
total_p2 = 0
n_keypads_p1 = 2  # number of robot keypads
n_keypads_p2 = 25  # number of robot keypads
for code in codes:
    numvalue = int(code.replace("A", ""))

    keypad1_options = find_numkey_opts(code)
    for dirkeyseq in keypad1_options:
        best_p1 = np.inf
        best_p2 = np.inf
        for dirkeyopt in dirkeyseq:
            final_p1 = determine_shortest_dirkeypath(dirkeyopt, n_keypads_p1)
            if final_p1 < best_p1:
                best_p1 = final_p1
            final_p2 = determine_shortest_dirkeypath(dirkeyopt, n_keypads_p2)
            if final_p2 < best_p2:
                best_p2 = final_p2
        total_p1 += best_p1 * numvalue
        total_p2 += best_p2 * numvalue

print("Part 1:", total_p1)
print("Part 2:", total_p2)
