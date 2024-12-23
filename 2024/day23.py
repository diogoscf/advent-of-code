import os
import bisect

filename = "day23.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()
connections = [l.split("-") for l in txt.split("\n")]

connected_computers = {}

for a, b in connections:
    connected_computers[a] = connected_computers.get(a, set()).union([b])
    connected_computers[b] = connected_computers.get(b, set()).union([a])


three_groups_p1 = set()
all_three_groups = set()

search_ranges = {} # group -> search range (set)

for computer, connections in connected_computers.items():
    for connected in connections:
        connected_to_both = connected_computers[connected].intersection(connections)
        three_groups_curr = []

        for c in connected_to_both:
            three_group = tuple(sorted((computer, connected, c)))
            three_groups_curr.append(three_group)

            new_search_range = connected_to_both.intersection(connected_computers[c])
            if three_group in search_ranges:
                search_ranges[three_group] = search_ranges[three_group].intersection(new_search_range)
            else:
                search_ranges[three_group] = new_search_range

        all_three_groups.update(three_groups_curr)


        if computer[0] == "t":
            three_groups_p1.update(three_groups_curr)

groups = {3: all_three_groups}
seen = set()
longest = []

while True:
    if len(groups) == 0:
        break

    biggest_group_len = max(groups.keys())
    group = groups[biggest_group_len].pop()
    if not groups[biggest_group_len]: # remove key if empty now
        del groups[biggest_group_len]
    
    if group in seen:
        continue

    seen.add(group)

    common_connections = search_ranges[group]

    for connection in common_connections:
        group_list = list(group)
        bisect.insort(group_list, connection) # keep it sorted
        new_group = tuple(group_list) # needs to be hashable
        groups[len(new_group)] = groups.get(len(new_group), set()).union([new_group])
        
        if len(new_group) > len(longest):
            longest = new_group

        new_search_range = common_connections.intersection(connected_computers[connection])

        if new_group in search_ranges:
            search_ranges[new_group] = search_ranges[new_group].intersection(new_search_range)
        else:
            search_ranges[new_group] = new_search_range

print("Part 1:", len(three_groups_p1))
print("Part 2:", ",".join(longest))
