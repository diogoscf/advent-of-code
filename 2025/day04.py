import os
import numpy as np

filename = "day04.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()


def shift_2d_replace(data, drow, dcol, pad=0):
    shifted_data = np.roll(np.roll(data, dcol, axis=1), drow, axis=0)

    if dcol < 0:
        shifted_data[:, dcol:] = pad
    elif dcol > 0:
        shifted_data[:, :dcol] = pad

    if drow < 0:
        shifted_data[drow:, :] = pad
    elif drow > 0:
        shifted_data[:drow, :] = pad

    return shifted_data


def find_removable_rolls(roll_arr):
    adjacent = np.zeros_like(roll_arr)

    for rowshift in (-1, 0, 1):
        for colshift in (-1, 0, 1):
            if rowshift == 0 and colshift == 0:
                continue
            adjacent += shift_2d_replace(roll_arr, rowshift, colshift)

    return (adjacent < 4) & roll_arr


lines = txt.split("\n")
arr = np.array([[*l] for l in lines])
arr[arr == "."] = 0
arr[arr == "@"] = 1
arr = arr.astype(np.int64)

part1 = np.sum(find_removable_rolls(arr))

curr = arr
part2 = 0

while True:
    removable = find_removable_rolls(curr)
    count_removable = np.sum(removable)
    if count_removable > 0:
        part2 += count_removable
        curr = curr - removable
    else:
        break

print("Part 1:", part1)
print("Part 2:", part2)
