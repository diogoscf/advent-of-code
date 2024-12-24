import os
import re

filename = "day24.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()


initial_values, operations = txt.split("\n\n")

curr_values = {wire: int(val) for wire, val in [l.split(": ") for l in initial_values.split("\n")]}
operations = re.findall(r"([a-z0-9]{3}) (XOR|AND|OR) ([a-z0-9]{3}) -> ([a-z0-9]{3})", operations)


def do_operation(val1, val2, op):
    if op == "AND":
        return val1 & val2
    elif op == "OR":
        return val1 | val2
    elif op == "XOR":
        return val1 ^ val2
    else:
        raise ValueError(f"Invalid operation: {op}")

# not the most efficient way but it works:tm:

def calc_final_values(ops, curr_values):
    operations = ops.copy() # don't change what we're iterating over
    sorted_ops = []

    while len(operations) > 0:
        curr_ops = operations.copy()
        to_delete = []
        sorted_curr_iter = []
        for i, (val1, op, val2, res) in enumerate(curr_ops): # start from biggest so we can delete without issues
            if val1 in curr_values and val2 in curr_values:
                curr_values[res] = do_operation(curr_values[val1], curr_values[val2], op)
                to_delete.append(i)
                sorted_curr_iter.append((res, val1, op, val2))
        sorted_ops.append(sorted(sorted_curr_iter, key=lambda x: x[0]))
        for i in to_delete[::-1]:
            operations.pop(i)
    
    return curr_values, sorted_ops

curr_values, sorted_ops = calc_final_values(operations, curr_values)

def determine_number(letterleft, curr_values):
    max_letter_key = max([int(k[1:]) for k in curr_values if k[0] == letterleft])
    total = 0
    for n in range(max_letter_key + 1):
        key = f"{letterleft}{n:02}"
        total += curr_values[key] << n
    
    return total


total_p1 = determine_number("z", curr_values)
print("Part 1:", total_p1)

x_value = determine_number("x", curr_values)
y_value = determine_number("y", curr_values)
z_value_wanted = x_value + y_value

binary_z_obtained = bin(total_p1)[2:]
binary_z_wanted = bin(z_value_wanted)[2:]

total_z_keys = max([int(k[1:]) for k in curr_values if k[0] == "z"])
wrong_z_vals = [n for n in range(total_z_keys + 1) if binary_z_obtained[-(n + 1)] != binary_z_wanted[-(n + 1)]]

print("Wrong z values:", wrong_z_vals, len(wrong_z_vals))
# zkk = (ykk XOR xkk) XOR carry(kk-1), where carry(kk-1) = (ykk-1 AND xkk-1) OR (carry(kk-2) AND (ykk-1 XOR xkk-1))
# knowing the above, look through wrong values manually and find where to switch

print("Part 2:", ",".join(sorted(["z06", "fhc", "z11", "qhj", "ggt", "mwh", "hqk", "z35"]))) # note this won't be correct for other inputs