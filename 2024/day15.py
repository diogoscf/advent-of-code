import os
import numpy as np
import itertools

filename = "day15.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

grid_height = 50  # grid part is 50 lines
grid = np.array([list(l) for l in txt.split("\n")[:grid_height]])
moves = list(itertools.chain.from_iterable([list(l) for l in txt.split("\n")[grid_height:]]))
chr_to_move = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
moves = [chr_to_move[m] for m in moves]

grid_p1 = grid.copy()
grid_p2 = np.full((grid.shape[0], grid.shape[1] * 2), ".")
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        grid_1 = grid[i, j]
        if grid_1 == "@":
            grid_p2[i, 2 * j] = "@"
        elif grid_1 == "O":
            grid_p2[i, 2 * j] = "["
            grid_p2[i, 2 * j + 1] = "]"
        elif grid_1 == "#":
            grid_p2[i, 2 * j] = "#"
            grid_p2[i, 2 * j + 1] = "#"


def make_move_p1(curr_pos, direction, grid):
    new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
    if grid[new_pos] == "#":
        return False, curr_pos, grid
    if grid[new_pos] == "O":
        can_move, _, grid = make_move_p1(new_pos, direction, grid)

        if not can_move:
            return False, curr_pos, grid

        grid[new_pos] = grid[curr_pos].copy()
        grid[curr_pos] = "."
        return True, new_pos, grid

    grid[new_pos] = grid[curr_pos].copy()
    grid[curr_pos] = "."
    return True, new_pos, grid


# Unlike part 1, this only checks if the move is possible, it doesn't make the move
# returns whether it can make the move + ids of blocks to be moved
def can_move_p2(curr_pos, direction, grid):
    new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
    if grid[new_pos] == "#":
        return False, []

    if grid[new_pos] in "[]":
        if direction[1] != 0:  # horizontal moves are basically the same as part 1
            can_move, other_changes = can_move_p2(new_pos, direction, grid)
            if not can_move:
                return False, []
            return True, [curr_pos] + other_changes

        if grid[new_pos] == "[":  # vertical direction is a bit different
            can_move_left, other_changes_left = can_move_p2(new_pos, direction, grid)
            can_move_right, other_changes_right = can_move_p2((new_pos[0], new_pos[1] + 1), direction, grid)
        else:  # ] case
            can_move_left, other_changes_left = can_move_p2((new_pos[0], new_pos[1] - 1), direction, grid)
            can_move_right, other_changes_right = can_move_p2(new_pos, direction, grid)

        if not (can_move_left and can_move_right):
            return False, []

        # use list(set()) to remove duplicates
        return True, [curr_pos] + list(set(other_changes_left + other_changes_right))

    return True, [curr_pos]  # get here if position is "."


def get_score(grid):
    locs_block = np.where((grid == "O") | (grid == "["))  # part 1: O, part 2: [
    score = 0
    for i, j in zip(*locs_block):
        score += 100 * i + j
    return score


robot_pos_p1 = np.where(grid_p1 == "@")[0][0], np.where(grid_p1 == "@")[1][0]
robot_pos_p2 = np.where(grid_p2 == "@")[0][0], np.where(grid_p2 == "@")[1][0]

for move in moves:
    _, robot_pos_p1, grid_p1 = make_move_p1(robot_pos_p1, move, grid_p1)

    can_move2, changes = can_move_p2(robot_pos_p2, move, grid_p2)
    if can_move2:
        tmp_grid = grid_p2.copy()
        lst_new_pos = []
        for pos_to_change in changes:
            new_pos = (pos_to_change[0] + move[0], pos_to_change[1] + move[1])
            lst_new_pos.append(new_pos)
            tmp_grid[new_pos] = grid_p2[pos_to_change].copy()
            if pos_to_change not in lst_new_pos:
                tmp_grid[pos_to_change] = "."
        robot_pos_p2 = (robot_pos_p2[0] + move[0], robot_pos_p2[1] + move[1])
        grid_p2 = tmp_grid.copy()

score_p1 = get_score(grid_p1)
score_p2 = get_score(grid_p2)

print(f"Part 1: {score_p1}")
print(f"Part 2: {score_p2}")
