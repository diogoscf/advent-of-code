import os
import numpy as np
from itertools import zip_longest

filename = "day9.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
# txt = "2333133121414131402"
txt_arr = np.array(list(txt), dtype=np.int64)
block_lengths = txt_arr[::2]
fill_lengths = txt_arr[1::2]

filled_length = np.sum(block_lengths)
length_blank = np.sum(fill_lengths)
total_length = filled_length + length_blank

final_values1 = np.full(filled_length, np.nan)

# First pass, filling in values that remain in place
for idx, length in enumerate(block_lengths):
    start_idx_final_fwd = np.sum(block_lengths[:idx]) + np.sum(fill_lengths[:idx])
    final_idx_final_fwd = start_idx_final_fwd + length
    if final_idx_final_fwd < filled_length:
        final_values1[start_idx_final_fwd:final_idx_final_fwd] = idx
    elif start_idx_final_fwd < filled_length:
        final_values1[start_idx_final_fwd:] = idx
        break
    else:
        break

# Second pass, filling in rest of values
orig_order_no_spaces = np.concatenate([[idx]*length for idx, length in enumerate(block_lengths)]).flatten()
for i, emptyidx in enumerate(np.where(np.isnan(final_values1))[0]):
    final_values1[emptyidx] = orig_order_no_spaces[-i-1]

orig_order = np.concatenate([[idx]*l1 + [np.nan]*l2 for idx, (l1, l2) in enumerate(zip_longest(block_lengths, fill_lengths, fillvalue=0))]).flatten()
final_values2 = orig_order.copy()

# Single pass through list for Part 2
for file_id in np.unique(orig_order)[::-1]: # start from end
    if np.isnan(file_id):
        continue
    file_id = int(file_id)
    file_length = block_lengths[file_id]
    start_idx = np.where(orig_order == file_id)[0][0]
    for i in np.where(np.isnan(final_values2))[0]: # check up to its own start index
        if i >= start_idx:
            break
        if np.all(np.isnan(final_values2[i:i+file_length])):
            final_values2[i:i+file_length] = file_id
            final_values2[start_idx:start_idx+file_length] = np.nan
            break

total_p1 = np.sum([v*i for i,v in enumerate(final_values1.astype(np.int64))])
total_p2 = np.sum(np.array([int(v*i) if not np.isnan(v) else 0 for i,v in enumerate(final_values2)]).astype(np.int64))
np.savetxt("day9_outputsum.txt", [int(v*i) if not np.isnan(v) else 0 for i,v in enumerate(final_values2)], fmt="%s")
print(f"Part 1: {total_p1}")
print(f"Part 2: {total_p2}")