import os
import numpy as np

filename = "day5.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

rules, orders = [p.split("\n") for p in txt.split("\n\n")]
orders = [[int(n) for n in order.split(",")] for order in orders]

rule_dict = {} # each number will map to those that need to be after it
for r in rules:
    k, v = r.split("|")
    k, v  = int(k), int(v)
    if k in rule_dict:
        rule_dict[k].append(v)
    else:
        rule_dict[k] = [v]

total_p1 = 0
bad_orders = []

def check_order(order):
    for i, o in enumerate(order):
        if i == 0:
            continue
        if any([prev in rule_dict[o] for prev in order[:i]]):
            return False
    return True

for order in orders:
    if check_order(order):
        total_p1 += order[len(order)//2]
    else:
        bad_orders.append(order)

total_p2 = 0

for order in bad_orders:
    curr_order = order
    curr_i = 0
    while not check_order(curr_order):
        order_minus_curr_i = curr_order[:curr_i] + curr_order[curr_i+1:]
        curr_el = curr_order[curr_i]
        for i, el in enumerate(order_minus_curr_i[::-1]):
            if curr_el in rule_dict[el]:
                i_orig = len(order_minus_curr_i) - i # index of el in original order
                curr_order = order_minus_curr_i[:i_orig+1] + [curr_el] + order_minus_curr_i[i_orig+1:]
                break
            elif i == len(order_minus_curr_i) - (curr_i+1): # it can be placed at the start, move on
                curr_i += 1
                break
    total_p2 += curr_order[len(curr_order)//2]

print("Part 1:", total_p1)
print("Part 2:", total_p2)