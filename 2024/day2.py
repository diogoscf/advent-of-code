import os
import pandas as pd
import numpy as np

filename = "day2.txt"

data = pd.read_csv(os.path.join(os.path.dirname(__file__), filename), sep=" ", header=None).to_numpy()
rows = data.tolist()

def check_safe(r):
    seq_diffs = [r[i+1] - r[i] for i in range(len(r)-1) if not np.isnan(r[i+1])]
    if not any([abs(s) > 3 for s in seq_diffs]):    
        if all([s > 0 for s in seq_diffs]) or all([s < 0 for s in seq_diffs]):
            return True
    
    return False

safe_p1 = 0
unsafe_rows = []
for i, r in enumerate(rows):
    if check_safe(r):
        safe_p1 += 1
    else:
        unsafe_rows.append(i)

safe_p2 = safe_p1
for r in data[unsafe_rows]:
    # seq_diffs = np.array([r[i+1] - r[i] for i in range(len(r)-1) if not np.isnan(r[i+1])])
    # larger_3 = np.abs(seq_diffs) > 3
    # if np.sum(larger_3) >= 3: # There can't be more than 2 diff>3 as removing one level will never correct 2+ "bad" differences
    #     continue
    # elif np.sum(larger_3) == 2: # can only be safe with a level removed if the two diff>3 are next to each other (required, not sufficient)
    #     id1, id2 = np.where(larger_3)[0]
    #     if not np.abs(id1 - id2) == 1:
    #         continue
    #     if check_safe(np.delete(r, id2)): # the element at id2 is removed as it is the same id as the "middle" element between the unsafes
    #         safe_p2 += 1
    #         continue
    # elif np.sum(larger_3) == 1 and (check_safe(np.delete(r, np.where(larger_3)[0]+1)) or check_safe(np.delete(r, np.where(larger_3)[0]))):
    #     safe_p2 += 1
    #     id1 = np.where(larger_3)[0][0]
    #     print(r, id1, np.delete(r, id1+1), np.delete(r, id1))

    # signs = np.sign(seq_diffs)
    r_not_nan = r[~np.isnan(r)]
    for i in range(len(r_not_nan)):
        if check_safe(np.delete(r_not_nan, i)):
            safe_p2 += 1
            break

print("Part 1:", safe_p1)
print("Part 2:", safe_p2)