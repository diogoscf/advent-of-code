import numpy as np
import os

from itertools import combinations_with_replacement, product

filename = "day10.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

INF_CORR_MAX = 10  # value to use as 'ends' for the iteration when a limit cannot be found
# somehow 10 seems to be enough. your mileage may vary...


# modified from https://github.com/lan496/hsnf/
def smith_normal_form(matrix, UV=None, s=0):
    # determine SNF up to the s-th row and column elements
    matrix = matrix.copy()
    if UV is None:
        U, V = np.eye(matrix.shape[0]), np.eye(matrix.shape[1])
    else:
        U = UV[0].copy()
        V = UV[1].copy()

    if s == min(matrix.shape):
        return matrix, U, V

    # choose a pivot
    row, col = (None, None)
    valmin = None
    for i in range(s, matrix.shape[0]):
        for j in range(s, matrix.shape[1]):
            if matrix[i, j] == 0:
                continue
            if valmin is None or np.abs(matrix[i, j]) < valmin:
                row, col = (i, j)
                valmin = np.abs(matrix[i, j])

    if col is None:
        # if no remaining non-zero elements, this procedure ends.
        return matrix, U, V

    U[[s, row]] = U[[row, s]]
    matrix[[s, row]] = matrix[[row, s]]

    V[:, [[s, col]]] = V[:, [[col, s]]]
    matrix[:, [[s, col]]] = matrix[:, [[col, s]]]

    # eliminate the s-th column entries
    for i in range(s + 1, matrix.shape[0]):
        if matrix[i, s] != 0:
            k = matrix[i, s] // matrix[s, s]
            U[i] += U[s] * (-k)
            matrix[i, :] += matrix[s, :] * (-k)

    # eliminate the s-th row entries
    for j in range(s + 1, matrix.shape[1]):
        if matrix[s, j] != 0:
            k = matrix[s, j] // matrix[s, s]
            V[:, j] += V[:, s] * (-k)
            matrix[:, j] += matrix[:, s] * (-k)

    # if no remaining non-zero element in s-th row and column, find next entry
    remaining = np.nonzero(matrix[s, (s + 1) :])[0].size + np.nonzero(matrix[(s + 1) :, s])[0].size
    if remaining == 0:
        res = None
        for i in range(s + 1, matrix.shape[0]):
            for j in range(s + 1, matrix.shape[1]):
                if matrix[i, j] % matrix[s, s] != 0:
                    res = i, j
        if res:
            i, j = res
            U[s] += U[i]
            matrix[s, :] += matrix[i, :]
            return smith_normal_form(matrix, (U, V), s)
        
        elif matrix[s, s] < 0:
            U[s] *= -1
            matrix[s, :] *= -1
        return smith_normal_form(matrix, (U, V), s + 1)

    else:
        return smith_normal_form(matrix, (U, V), s)


light_meaning = {".": 0, "#": 1}
machines = []

for line in txt.split("\n"):
    lights_txt, rest = line.split("] ")
    buttons_txt, joltage_txt = rest.split("{")
    lights_vector = np.array([light_meaning[c] for c in lights_txt[1:]]).T

    buttons = [ntxt[1:] for ntxt in buttons_txt.split(") ")[:-1]]
    button_matrix = np.zeros((lights_vector.shape[0], len(buttons)))

    for i, b in enumerate(buttons):
        locs = [int(bt) for bt in b.split(",")]
        button_matrix[locs, i] = 1

    joltage_vector = np.array([int(n) for n in joltage_txt[:-1].split(",")]).T
    machines.append([lights_vector, button_matrix, joltage_vector])

# This is a bit cursed but it mostly works
# Do not ask me for the working out...
def find_missing_limits(minmax_h, effects, base_pvec):
    if np.all(np.isfinite(np.array(minmax_h))):
        return minmax_h, True

    minmax_h = minmax_h.copy()

    nolim = 1 - np.isfinite(np.array(minmax_h))  # is infinite
    missing_lims_h = np.where(nolim)[0]
    missing_lims_type = np.where(nolim)[1]
    len_missing_lims = np.isfinite(np.array(minmax_h)).sum()

    for nolimh, nolimtype in zip(missing_lims_h, missing_lims_type):
        for col in range(effects.shape[1]):
            coeff_self = effects[nolimh, col]

            if coeff_self == 0 or int(coeff_self < 0) != nolimtype:
                continue  # if no effect from point here, or if coeff sign doesn't match missing limit type

            if (effects[:, col] != 0).sum() == 1:
                continue  # other points do not have an effect, cannot derive from here

            other_hs = np.where((effects[:, col] != 0) & (np.arange(effects.shape[0]) != nolimh))[0]
            coeffs_other = effects[other_hs, col]

            newlim = None
            limtype_others = (coeffs_other > 0).astype(np.int8)  # if > 0: max (so 1), < 0: min (so 0)
            if all(np.isfinite(minmax_h[h][lt]) for h, lt in zip(other_hs, limtype_others)):
                coeff_mult = sum(
                    [-c * minmax_h[oh][ltype] for c, oh, ltype in zip(coeffs_other, other_hs, limtype_others)]
                )
                newlim = (coeff_mult - base_pvec[col]) / coeff_self

            if newlim is None:
                continue

            minmax_h[nolimh][nolimtype] = np.ceil(newlim).astype(np.int64)
            break

    if len_missing_lims == np.isfinite(np.array(minmax_h)).sum():  # nothing has changed
        return minmax_h, False

    return find_missing_limits(minmax_h, effects, base_pvec)


part1 = 0
part2 = 0
for i, (lights_vector, button_matrix, joltage_vector) in enumerate(machines):
    n_buttons = button_matrix.shape[1]
    range_n_buttons = [*range(n_buttons)]

    ## Part 1 ##
    found = False
    for n_press in range(1, 1000):  # doubt it's more than 1000
        button_presses = combinations_with_replacement(range_n_buttons, n_press)
        press_vector = np.zeros(n_buttons).T
        for presses in button_presses:
            press_vector = np.zeros(n_buttons).T
            for press in presses:
                press_vector[press] += 1

            result = (button_matrix @ press_vector) % 2
            if np.all(result == lights_vector):
                part1 += n_press
                found = True
                break

        if found:
            break

    ## Part 2 from here onewards ##
    if button_matrix.shape[0] == button_matrix.shape[1] and np.linalg.det(button_matrix) != 0:
        # square, non-singular matrix: single solution!!
        press_vector = np.linalg.inv(button_matrix) @ joltage_vector
        part2 += np.rint(np.sum(press_vector)).astype(np.int64)

    elif not np.isclose(np.linalg.det(button_matrix.T @ button_matrix), 0):
        # A^T A invertible => unique least-squares solution
        # we know there is an exact solution so the LSQ solution is already it!
        press_vector = np.linalg.inv(button_matrix.T @ button_matrix) @ button_matrix.T @ joltage_vector
        part2 += np.rint(np.sum(press_vector)).astype(np.int64)

    # we are essentially solving a system of linear Diophantine equations
    # the general solution (which includes negative solutions, and is not optimised) can be found using the smith normal form
    else:
        SNF, U, V = smith_normal_form(button_matrix)
        # we can rewrite button_matrix @ press_vector = joltage_vector
        # to SNF @ (inv(V) @ press_vector) = U @ joltage_vector
        k = np.where(np.diag(SNF) > 0)[0][-1] + 1
        D = U @ joltage_vector
        y_start = [D[i] // SNF[i, i] for i in range(k)]

        min_press = np.inf
        len_missing = V.shape[0] - k
        base_pvec = V @ np.array(y_start + [0 for _ in range(len_missing)])
        base_npress = np.sum(base_pvec)

        if len_missing == 1:  # only one 'free' value, easy to find best one
            effect = V @ np.array([0 for _ in range(k)] + [1])
            sum_effect = np.sum(effect)
            min_h = -np.inf
            max_h = np.inf
            for j, bp in enumerate(base_pvec):
                # effect[j]*h + bp >= 0 => h >= -bp/effect[j] (or <= if effect[j] < 0)
                lim = -bp / effect[j] if effect[j] != 0 else None
                if effect[j] < 0:
                    if lim < max_h:
                        max_h = np.floor(lim)
                elif effect[j] > 0:  # no condition for effect = 0
                    if lim > min_h:
                        min_h = np.ceil(lim)
            h = min_h if sum_effect > 0 else max_h
            pvec = V @ np.array(y_start + [h])
            min_press = np.rint(base_npress + sum_effect * h).astype(np.int64)

        else:
            effects = []
            sum_effects = []
            minmax_h = [[-np.inf, np.inf] for _ in range(len_missing)]

            for i in range(len_missing):
                y = [0 for _ in range(k + len_missing)]
                y[k + i] = 1
                effect = V @ np.array(y)
                effects.append(effect)
                sum_effects.append(np.sum(effect))

            effects = np.array(effects)

            for i, col in enumerate(effects.T):
                if np.sum(col != 0) == 1:  # only one h has an effect!
                    h_affected = np.where(col != 0)[0][0]
                    eff_loc = col[h_affected]  # won't be zero anyways
                    lim = -base_pvec[i] / eff_loc

                    if eff_loc < 0:
                        if lim < minmax_h[h_affected][1]:
                            minmax_h[h_affected][1] = np.floor(lim).astype(np.int64)

                    elif eff_loc > 0:  # no condition for effect = 0
                        if lim > minmax_h[h_affected][0]:
                            minmax_h[h_affected][0] = np.ceil(lim).astype(np.int64)

            if not np.all(np.isfinite(np.array(minmax_h))):
                minmax_h, result = find_missing_limits(minmax_h, effects, base_pvec)

                if not result:
                    print(f"Accurate limits could not be found for a button/joltage combo! Setting remaining limits to default ({INF_CORR_MAX})...")

                    for no_limh, nolimtype in zip(*np.where(1 - np.isfinite(np.array(minmax_h)))):
                        if nolimtype == 0:
                            minmax_h[no_limh][0] = -10
                        else:
                            minmax_h[no_limh][1] = 10

            ranges = [[*range(a, b + 1)] for a, b in minmax_h]
            for vals in product(*ranges):
                press_vec = V @ (y_start + list(vals))
                presses = np.rint(np.sum(press_vec)).astype(np.int64)
                if presses < min_press and (press_vec >= 0).all():
                    min_press = presses

        part2 += min_press

    press_vector = np.linalg.lstsq(button_matrix, joltage_vector)[0]
    presses = np.rint(np.sum(press_vector)).astype(np.int64)

print("Part 1:", part1)
print("Part 2:", part2)
