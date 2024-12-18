import os
import numpy as np
from operator import mul, add
from itertools import product

filename = "day07.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
eqs = [[int(n.strip(":")) for n in l.split(" ")] for l in txt.split("\n")]

def concat_nums(a, b):
    return int(str(a) + str(b))


operations_1 = [mul, add]
operations_2 = [mul, add, concat_nums]
max_opts = np.max([len(e) for e in eqs]) - 2
options = [order[::-1] for order in list(product(operations_1, repeat=max_opts))] # reverse order so all options are covered even if cut off

total_p1 = 0
for res, *nums in eqs:
    len_opts_curr = 2**(len(nums)-1)
    options_curr = options[:len_opts_curr]
    for opt in options_curr:
        curr_res = nums[0]
        for i, n in enumerate(nums[1:]):
            curr_res = opt[i](curr_res, n)
        if curr_res == res:
            total_p1 += res
            # print(res, nums, opt)
            break

print("Part 1:", total_p1, flush=True)

# a bit slow but eh
options_p2 = [order[::-1] for order in list(product(operations_2, repeat=max_opts))] # reverse order so all options are covered even if cut off
total_p2 = 0
for res, *nums in eqs:
    len_opts_curr = 3**(len(nums)-1)
    options_curr = options_p2[:len_opts_curr]
    for opt in options_curr:
        curr_res = nums[0]
        for i, n in enumerate(nums[1:]):
            curr_res = opt[i](curr_res, n)
        if curr_res == res:
            total_p2 += res
            # print(res, nums, opt)
            break

print("Part 2:", total_p2)