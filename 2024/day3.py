import os
import numpy as np
import re

pattern = r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))"

filename = "day3.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

matches = re.findall(pattern, txt)
total1 = 0
total2 = 0
on = True
print(matches)
for (s, n1, n2) in matches:
    if s == "do()":
        on = True
        continue
    if s == "don't()":
        on = False
        continue

    print(n1, n2)
    total1 += int(n1) * int(n2)
    if on:
        total2 += int(n1) * int(n2)

print("Part 1:", total1)
print("Part 2:", total2)