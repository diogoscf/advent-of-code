import os

filename = "day05.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

ranges, ingredients = [x.split("\n") for x in txt.split("\n\n")]

ranges = [tuple([int(x) for x in r.split("-")]) for r in ranges]
ingredients = [int(x) for x in ingredients]


part1 = 0
for ing in ingredients:
    for start, end in ranges:
        if ing >= start and ing <= end:
            part1 += 1
            break


def remove_range_overlap(range_list):  # honestly one of the jankiest pieces of code I've written but it works!
    flag = False
    mod_range = set()
    nooverlap = set(range(len(range_list)))

    for i, (s1, e1) in enumerate(range_list[:-1]):
        for j, (s2, e2) in enumerate(range_list[(i + 1) :]):
            s2_in_1 = s1 <= s2 <= e1
            e2_in_1 = s1 <= e2 <= e1
            whole1_in_2 = s2 <= s1 <= e2 and s2 <= e1 <= e2

            if whole1_in_2:
                new_s, new_e = s2, e2
            elif s2_in_1 and e2_in_1:  # whole 2 in 1
                new_s, new_e = s1, e1
            elif s2_in_1:
                new_s, new_e = s1, e2
            elif e2_in_1:
                new_s, new_e = s2, e1

            if s2_in_1 or e2_in_1 or whole1_in_2:
                flag = True
                mod_range.add((new_s, new_e))
                nooverlap.discard(i)
                nooverlap.discard(j + i + 1)
                break

    for i in nooverlap:
        mod_range.add(range_list[i])

    if not flag:
        return list(mod_range)

    return remove_range_overlap(list(mod_range))


non_overlapped_ranges = remove_range_overlap(ranges)

part2 = 0
for start, end in non_overlapped_ranges:
    part2 += (end - start) + 1

print("Part 1:", part1)
print("Part 2:", part2)
