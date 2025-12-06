import os

filename = "day01.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

rots = [int(x) for x in txt.replace("L", "-").replace("R", "").split("\n")]

start = 50

curr = start
dialsize = 100
counter1 = 0
counter2 = 0

for r in rots:
    curr += r
    passes0 = curr // dialsize
    new = curr % dialsize
    prev = counter2
    if curr - r != 0 or new == 0 or passes0 >= 0:
        counter2 += abs(passes0)
    else:  # left move from 0. if not ending at 0, we need to ignore the "extra" pass at 0
        counter2 += abs(passes0) - 1

    if passes0 <= 0 and new == 0:  # correction for left moves that end at 0
        counter2 += 1

    if new == 0:
        counter1 += 1

    curr = new

print("Part 1:", counter1)
print("Part 2:", counter2)
