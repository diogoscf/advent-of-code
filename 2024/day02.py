import os
import pandas as pd
import numpy as np

filename = "day02.txt"

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
    r_not_nan = r[~np.isnan(r)]
    for i in range(len(r_not_nan)):
        if check_safe(np.delete(r_not_nan, i)):
            safe_p2 += 1
            break

print("Part 1:", safe_p1)
print("Part 2:", safe_p2)