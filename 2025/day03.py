import os

filename = "day03.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

banks = txt.split("\n")

part1 = 0
part2 = 0

nums = [str(i) for i in range(9, 0, -1)]


def find_largest_voltage(bank, length):
    usable_bank = bank[: -(length - 1)] if length > 1 else bank
    for n in nums:
        loc = usable_bank.find(n)
        if loc >= 0:
            volts = n
            break

    if length > 1:
        return volts + find_largest_voltage(bank[loc + 1 :], length - 1)

    return volts


for b in banks:
    part1 += int(find_largest_voltage(b, 2))
    part2 += int(find_largest_voltage(b, 12))

print("Part 1:", part1)
print("Part 2:", part2)
