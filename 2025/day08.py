import os
import numpy as np

from collections import defaultdict

filename = "day08.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

len_conn = 1000
largest_to_consider_p1 = 3

coords = [tuple([int(x) for x in l.split(",")]) for l in txt.split("\n")]
circuits = []

incircuit = defaultdict(lambda: None)

def point_dist(p1, p2):
    return np.sqrt(np.sum([(x1-x2)**2 for x1, x2 in zip(p1,p2)]))

distances = np.zeros((len(coords), len(coords)))

# This is a bit slow, and this will be a symmetrical matrix so you could halve the iterations by being clever but idc
for i, c1 in enumerate(coords):
    for j, c2 in enumerate(coords):
        if i == j:
            continue
        distances[i,j] = point_dist(c1, c2)

distances = np.tril(distances)
distances[distances == 0] = np.inf
   
i = 0
part1 = 0
part2 = 0

len_coords = len(coords)
while True:
    connection = np.unravel_index(distances.argmin(), distances.shape)
    distances[connection] = np.inf # whatever we do we will not consider this pair again
   
    # both in same circuit already (need first bit as otherwise None = None is True)
    if incircuit[connection[0]] and incircuit[connection[0]] == incircuit[connection[1]]:
        pass # do nothing
   
    elif incircuit[connection[0]] and incircuit[connection[1]]: # both in circuits but different ones!
        idx1, idx2 = (incircuit[connection[0]], incircuit[connection[1]])
        newcircuit = circuits[idx1] + circuits[idx2]
        newidx = len(circuits) # new idx is equal to old length!
       
        for idx in newcircuit:
            incircuit[idx] = newidx
       
        # do not just delete as otherwise every index reference breaks!
        circuits[idx1] = []
        circuits[idx2] = []
        circuits.append(newcircuit)
           
   
    elif incircuit[connection[0]]: # second one not yet connected
        idx = incircuit[connection[0]]
        circuits[idx].append(connection[1])
        incircuit[connection[1]] = idx
    elif incircuit[connection[1]]: # first one not yet connected
        idx = incircuit[connection[1]]
        circuits[idx].append(connection[0])
        incircuit[connection[0]] = idx
    else: # neither is connected yet
        newidx = len(circuits) # new idx is equal to old length!
        circuits.append(list(connection))
        incircuit[connection[0]] = newidx
        incircuit[connection[1]] = newidx
   
    if i == len_conn:
        circuit_lengths = np.array([len(c) for c in circuits])
        top_lengths = circuit_lengths[np.argpartition(circuit_lengths, -largest_to_consider_p1)[-largest_to_consider_p1:]]
        part1 = np.prod(top_lengths)
       
    i += 1
   
    if np.max([len(c) for c in circuits]) == len_coords: # all circuits connected!
        part2 = coords[connection[0]][0] * coords[connection[1]][0]
        break
   
print("Part 1:", part1)
print("Part 2:", part2)
