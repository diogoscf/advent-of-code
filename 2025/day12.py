import os

filename = "day12.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

txt_parts = txt.split("\n\n")

shapes = [[list(map(int,l)) for l in s.replace("#", "1").replace(".","0").split("\n")[1:]] for s in txt_parts[:-1]]
shape_areas = [sum([x for xs in s for x in xs]) for s in shapes]

regions = [l.split(": ") for l in txt_parts[-1].split("\n")]
regions = [(list(map(int, a.split("x"))), list(map(int, b.split(" ")))) for a,b in regions]

part1 = 0
for region_shape, presents in regions:
    if sum([shape_areas[i]*p for i,p in enumerate(presents)]) > region_shape[0]*region_shape[1]:
        continue # not enough squares to be covered!
    
    if sum(presents) <= (region_shape[0] // 3)*(region_shape[1] // 3):
        part1 += 1 # we can definitely fit them!
        continue
    
    raise NotImplementedError # In theory this is a possibility but apparently we don't need to consider it :))))
    
print("Part 1:", part1)
