import os
import itertools

filename = "day19.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

towels = set(txt.split("\n")[0].split(", "))
patterns = txt.split("\n")[2:] # 2nd line is empty

total_p1 = 0
for i, pattern in enumerate(patterns):
    curr_possible = set([pattern])
    while len(curr_possible):
        p_curr = min(curr_possible, key=len)
        curr_possible.remove(p_curr)
        for towel in towels:
            if p_curr.startswith(towel):
                new_p = p_curr[len(towel):]
                if len(new_p) == 0:
                    total_p1 += 1
                    curr_possible = set()
                    break
                curr_possible.add(new_p)


def calc_num_possibilities(pattern, towels, pattern_possibilities, max_towel_length):
    curr_possible = set([pattern])
    total_possibilities = 0
    while len(curr_possible):
        p_curr = min(curr_possible, key=len)
        curr_possible.remove(p_curr)
        if p_curr in pattern_possibilities:
            total_possibilities += pattern_possibilities[p_curr]
            continue
        for start_pattern in itertools.accumulate(p_curr[:max_towel_length]):
            if start_pattern in towels:
                new_p = p_curr[len(start_pattern):]
                if len(new_p) == 0:
                    total_possibilities += 1
                else:
                    curr_possible.add(new_p)
    pattern_possibilities.update({pattern: total_possibilities})
    return total_possibilities, pattern_possibilities

total_p2 = 0
max_towel_length = len(max(towels, key=len))
pattern_possibilities = {} # pattern: possibilities
for i, pattern in enumerate(patterns):
    # by doing the following we save all the sub-patterns possibilities
    for end_pattern in itertools.accumulate(pattern[::-1]):
        total_curr, pattern_possibilities = calc_num_possibilities(end_pattern[::-1], towels, pattern_possibilities, max_towel_length)
    total_p2 += total_curr # total_curr will be the final value i.e. full pattern

print("Part 1:", total_p1)
print("Part 2:", total_p2)