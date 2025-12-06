import os

filename = "day02.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

ranges = [[int(y) for y in x.split("-")] for x in txt.split(",")]

part1 = 0
part2 = 0
for a, b in ranges:
    vals = [str(v) for v in range(a, b + 1)]
    for v in vals:
        len_v = len(v)
        len_v2 = len_v // 2
        if v[:len_v2] == v[len_v2:]:
            part1 += int(v)

        for l in range(1, len_v2 + 1):  # not the most efficient solution but oh well
            start = v[:l]
            if all([v[l + i : 2 * l + i] == start for i in range(0, len_v - l, l)]):
                part2 += int(v)
                break

print("Part 1:", part1)
print("Part 2:", part2)
