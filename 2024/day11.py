import os
import numpy as np
from collections import Counter

filename = "day11.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
# txt = "125 17"
stones = np.array([int(s) for s in txt.split(" ")], dtype=np.int64)

known_vals = set([0])
known_ass = {0: [{1: 1}]}
# val: {[newvals_1step, newvals_2step,...]} with newvals_xstep a counter {val1: count1, val2: count2, ...}


def blink_steps(val, steps):
    if val in known_vals:
        curr_known_ass = known_ass[val]
        if (max_steps := len(curr_known_ass)) >= steps:
            return curr_known_ass[steps - 1], curr_known_ass  # return end value, whole tree
        best = curr_known_ass[max_steps - 1]

        end = {}
        end_get = end.get
        tree = [{} for _ in range(steps - max_steps)]

        if isinstance(best, list):
            print("list", best, val, max_steps, curr_known_ass)
        for b, count in best.items():
            e, t = blink_steps(b, steps - max_steps)  # end, tree

            # beyond steps-max is more information than we can hold for now
            for level, curr_end in enumerate(t[: (steps - max_steps)]):
                tree_level_get = tree[level].get
                for k, v in curr_end.items():
                    tree[level][k] = tree_level_get(k, 0) + (v * count)
            for k, v in e.items():
                end[k] = end_get(k, 0) + v * count

        known_ass[val] = curr_known_ass[:max_steps] + tree  # have to be careful with re-assignments in sub loops

        return end, known_ass[val]  # known_ass[val] will have the up to date value now

    digits = len(str(val))  # faster than mathematical determination
    if digits % 2 == 0:
        exponent = 10 ** (digits // 2)
        newvals = [val // exponent, val % exponent]
        newvals = {newvals[0]: 2} if newvals[0] == newvals[1] else {newvals[0]: 1, newvals[1]: 1}
        if steps == 1:
            known_vals.add(val)
            known_ass[val] = [newvals]
            return newvals, [newvals]  # whole tree is just one step

        end = {}
        end_get = end.get
        tree = [{} for _ in range(steps - 1)]
        for b, count in newvals.items():
            e, t = blink_steps(b, steps - 1)  # end, tree

            # beyond steps-1 is more information than we can hold for now
            for level, curr_end in enumerate(t[: (steps - 1)]):
                tree_level_get = tree[level].get
                for k, v in curr_end.items():
                    tree[level][k] = tree_level_get(k, 0) + (v * count)
            for k, v in e.items():
                end[k] = end_get(k, 0) + v * count

        return_tree = [newvals] + tree
        known_vals.add(val)
        known_ass[val] = return_tree
        return end, return_tree

    newv = val * 2024
    newval = {newv: 1} if val != 0 else {1: 1}

    if steps == 1:
        known_vals.add(val)
        known_ass[val] = [newval]
        return newval, [newval]  # whole tree is just one step

    end, tree = blink_steps(newv, steps - 1)  # end, tree
    return_tree = [newval] + tree

    known_vals.add(val)
    known_ass[val] = return_tree
    return end, return_tree


total_p1 = 0
p1steps = 25
for s in stones:
    total_p1 += sum(blink_steps(s, p1steps)[0].values())

print(f"Part 1: {total_p1}")

p2steps = 75
total_p2 = 0
# we restart from 0 which is maybe not the most efficient, but we still have all the known stuff from the 25 loops before
for s in stones:
    total_p2 += sum(blink_steps(s, p2steps)[0].values())

print(f"Part 2: {total_p2}")

# NOTE: Might take up to ~15s to run
