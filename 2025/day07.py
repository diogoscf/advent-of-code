import os
import numpy as np

filename = "day07.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

lines = txt.split("\n")
arr = np.array([[*l] for l in lines])
beams = np.zeros(arr.shape, dtype=np.int64)
beams[0, lines[0].index("S")] = 1

arr[arr == "."] = 0
arr[arr == "^"] = 1
arr = arr[1:, :].astype(np.int64)

part1 = 0

for i, row in enumerate(arr):
    for beam_idx in np.where(beams[i, :] >= 1)[0]:
        beam = beams[i, beam_idx]
        if row[beam_idx] == 1:
            part1 += 1
            beams[i + 1, beam_idx - 1] += beam
            beams[i + 1, beam_idx + 1] += beam
        else:
            beams[i + 1, beam_idx] += beam

print("Part 1:", part1)
print("Part 2:", np.sum(beams[-1, :]))
