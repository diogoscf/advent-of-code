import os
import numpy as np
import re

filename = "day06.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

txtt = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

lines = txt.split("\n")
col_starts = [m.start() for m in re.finditer(r"(\+|\*)", lines[-1])]
problems = np.array([[l[i : j - 1] for i, j in zip(col_starts, col_starts[1:] + [len(l) + 1])] for l in lines]).T

part1 = 0
part2 = 0

for p in problems:
    op = np.sum if p[-1].strip() == "+" else np.prod

    part1 += op(p[:-1].astype(int))
    part2 += op(np.array(["".join(k) for k in np.array([[*n] for n in p[:-1]]).T]).astype(int))

print("Part 1:", part1)
print("Part 2:", part2)
