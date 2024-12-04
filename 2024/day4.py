import os
import numpy as np
import re

filename = "day4.txt"
# pattern = r"(XMAS|SMAX)"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
as_array = np.array([list(l) for l in txt.split("\n")])
h, w = as_array.shape

# horizontal_instances = len(re.findall(pattern, txt))
# txt_transposed = "\n".join(["".join(l) for l in as_array.T])
# vertical_instances = len(re.findall(pattern, txt_transposed))

count_p1 = 0
count_p2 = 0


""" LOCATIONS

NW N  NE
W  X  E
SW S  SE
"""

# This checks for a "XMAS" diagonally, horizontally or vertically
def check_from_X(r, c, arr):
    loc_count = 0
    h, w = arr.shape
    # To E
    if r + 3 < h:
        if arr[r+1, c] == "M" and arr[r+2, c] == "A" and arr[r+3, c] == "S":
            loc_count += 1
    # To W
    if r - 3 >= 0:
        if arr[r-1, c] == "M" and arr[r-2, c] == "A" and arr[r-3, c] == "S":
            loc_count += 1
    # To S
    if c + 3 < w:
        if arr[r, c+1] == "M" and arr[r, c+2] == "A" and arr[r, c+3] == "S":
            loc_count += 1
    # To N
    if c - 3 >= 0:
        if arr[r, c-1] == "M" and arr[r, c-2] == "A" and arr[r, c-3] == "S":
            loc_count += 1
    # To NE
    if r - 3 >= 0 and c + 3 < w:
        if arr[r-1, c+1] == "M" and arr[r-2, c+2] == "A" and arr[r-3, c+3] == "S":
            loc_count += 1
    # To NW
    if r - 3 >= 0 and c - 3 >= 0:
        if arr[r-1, c-1] == "M" and arr[r-2, c-2] == "A" and arr[r-3, c-3] == "S":
            loc_count += 1
    
    # To SE
    if r + 3 < h and c + 3 < w:
        if arr[r+1, c+1] == "M" and arr[r+2, c+2] == "A" and arr[r+3, c+3] == "S":
            loc_count += 1
    
    # To SW
    if r + 3 < h and c - 3 >= 0:
        if arr[r+1, c-1] == "M" and arr[r+2, c-2] == "A" and arr[r+3, c-3] == "S":
            loc_count += 1
    
    return loc_count


# This checks for an X-"MAS" i.e. two MAS in a cross -> always an A in the centre
def check_from_A(r, c, arr):
    h, w = arr.shape
    if r == 0 or r == h - 1 or c == 0 or c == w - 1:
        return 0

    check_MAS_NWSE = (arr[r-1,c-1] == "M" and arr[r+1,c+1] == "S")
    check_MAS_SENW = (arr[r-1,c-1] == "S" and arr[r+1,c+1] == "M")

    check_MAS_NESW = (arr[r-1,c+1] == "M" and arr[r+1,c-1] == "S")
    check_MAS_SWNE = (arr[r-1,c+1] == "S" and arr[r+1,c-1] == "M")

    if (check_MAS_NWSE or check_MAS_SENW) and (check_MAS_NESW or check_MAS_SWNE):
        return 1

    return 0
        

for r in range(h):
    for c in range(w):
        if as_array[r, c] == "X":
            count_p1 += check_from_X(r, c, as_array)
        if as_array[r, c] == "A":
            count_p2 += check_from_A(r, c, as_array)

print("Part 1:", count_p1)
print("Part 2:", count_p2)