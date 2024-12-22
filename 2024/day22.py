import os
import itertools

filename = "day22.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
nums = [int(n) for n in txt.split("\n")]


def evolve_num(n):
    n = ((n << 6) ^ n) & (2**24 - 1) # n*64 XOR n mod 2^24
    n = ((n >> 5) ^ n) & (2**24 - 1) # n/32 XOR n mod 2^24
    n = ((n << 11) ^ n) & (2**24 - 1) # n*2048 XOR n mod 2^24
    return n

total_p1 = 0
monkey_prices = []
for n in nums:
    curr = n
    changes = []
    prices = {}
    for i in range(2000):
        nextnum = evolve_num(curr)
        price = nextnum % 10
        changes.append(price - (curr % 10))
        curr = nextnum
        if i >= 3:
            seq = tuple(changes[i-3:i+1])
            if (seq not in prices): # only the first occurence of a sequence matters
                prices[seq] = price
    total_p1 += curr
    monkey_prices.append(prices)

print("Part 1:", total_p1)

# NOTE: this takes about 40 seconds, could be faster but who cares
total_p2 = 0
for i, sequence in enumerate(itertools.permutations(range(-9,10),4)): # -9 to 9
    total = sum([pdict.get(sequence, 0) for pdict in monkey_prices])
    if total > total_p2:
        total_p2 = total

print("Part 2:", total_p2)