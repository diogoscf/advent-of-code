import os
import time

from itertools import combinations, pairwise

from frozendict import frozendict
from functools import cache

filename = "day09.txt"
txt = open(os.path.join(os.path.dirname(__file__), filename)).read()

class Point:  # should be hashable!
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __hash__(self):
        return hash((self._x, self._y))

    def __eq__(self, other):
        if isinstance(other, tuple):
            return (self._x, self._y) == other
        if not isinstance(other, Point):
            return False
        return (self._x, self._y) == (other._x, other._y)

    def __repr__(self):  # makes debugging a lot easier :))
        return f"Point({self._x}, {self._y})"


class VertexPoint(Point):
    def __init__(self, x, y, convex=None, prv=None, nxt=None):
        super().__init__(x, y)
        self.convex = convex
        self.prv = prv
        self.nxt = nxt

    def direction(self):  # return dir_x, dir_y
        if self.nxt.x == self.x:
            dir_y = 1 if self.nxt.y > self.y else -1
            dir_x = 1 if self.prv.x > self.x else -1
        else:
            dir_y = 1 if self.prv.y > self.y else -1
            dir_x = 1 if self.nxt.x > self.x else -1

        return dir_x, dir_y


class EdgePoint(Point):
    def __init__(self, x, y, nearest_vertices=(None, None)):
        super().__init__(x, y)
        self.nearest_vertices = nearest_vertices


redtiles = [VertexPoint(*(int(x) for x in l.split(","))) for l in txt.split("\n")]
outerloop = {}

minx, maxx = min([p.x for p in redtiles]), max([p.x for p in redtiles])
miny, maxy = min([p.y for p in redtiles]), max([p.y for p in redtiles])


def genedge_points(p1: Point, p2: Point):  # note: does not include vertices themselves
    if p1.x == p2.x:  # same x
        larger, smaller = (p1.y, p2.y) if p1.y > p2.y else (p2.y, p1.y)
        return [EdgePoint(p1.x, y, (p1, p2)) for y in range(smaller + 1, larger)]
    elif p1.y == p2.y:  # same y
        larger, smaller = (p1.x, p2.x) if p1.x > p2.x else (p2.x, p1.x)
        return [EdgePoint(x, p1.y, (p1, p2)) for x in range(smaller + 1, larger)]
    else:
        raise ValueError("Only horizontal or vertical edges supported!")


def is_convex(B: Point, A: Point, C: Point):  # note: returns as convex if flat!!, assumes CCW shape
    BA = (A.x - B.x), (A.y - B.y)
    BC = (C.x - B.x), (C.y - B.y)
    vec_det = BA[0] * BC[1] - BA[1] * BC[0]
    return vec_det <= 0


direction_n = 0
y_values_horedge = set()

for p1, p2 in pairwise(redtiles + [redtiles[0]]):
    y_values_horedge.update([p1.y, p2.y])
    edge = genedge_points(p1, p2)
    direction_n += (p2.x - p1.x) * (p2.y + p1.y)
    outerloop[p1] = p1  # add vertex (p2 added in next iteration)
    if (edge[0].x - p1.x) == 1 or (edge[0].y - p1.y) == 1:  # first edge point is next
        p1.nxt = edge[0]
        p2.prv = edge[-1]
    else:
        p1.nxt = edge[-1]
        p2.prv = edge[0]
    for ep in edge:
        outerloop[ep] = ep

y_values_horedge = sorted(list(y_values_horedge), reverse=True)

outerloop = frozendict(outerloop)

if direction_n > 0:  # ccw point sequence if negative, cw if positive
    raise ValueError("Points are not in CCW order! Simply invert the order (e.g. [::-1]) to make it work :)")


ntiles = len(redtiles)
for i, rt in enumerate(redtiles):
    rt.convex = is_convex(rt, redtiles[i - 1], redtiles[(i + 1) % ntiles])

@cache
def point_in_shape(pt: Point, perimeter: frozendict[Point, Point] = outerloop) -> bool:
    if pt in perimeter:
        return True

    closest_in_dir = None
    for y in y_values_horedge:
        if y >= pt.y:
            continue
        if (testpt := (pt.x, y)) in perimeter:
            closest_in_dir = perimeter[testpt]  # we want the actual point instance
            break

    if closest_in_dir is None:
        return False

    # if convex and DIRECTLY above/below => outside, if concave and DIRECTLY above/below => inside
    if isinstance(closest_in_dir, VertexPoint):
        return not closest_in_dir.convex

    else:  # edge point => need to check one vertex (sufficient!) and check if it is convex and 'turning towards' or concave and 'turning away'
        vtx = closest_in_dir.nearest_vertices[0]
        # we know nv1.y = closest_above.y < pt.y
        vert = vtx.prv if vtx.nxt.y == vtx.y else vtx.nxt
        # horizontal is coming 'towards us' anyways, vertical one matters!
        inside = None
        if vert.y < vtx.y:  # vertical going away from us
            inside = not vtx.convex
        else:  # vertical coming towards us
            inside = vtx.convex

        return inside


start = time.time()
part1 = 0
part2 = 0

rectangles = []

for p1, p2 in combinations(redtiles, 2):
    area = (abs(p2.x - p1.x) + 1) * (abs(p2.y - p1.y) + 1)
    rectangles.append((area, p1, p2))

rectangles.sort(reverse=True, key=lambda x: x[0])

part1 = rectangles[0][0]

for i, (area, p1, p2) in enumerate(rectangles):
    dir_x = 1 if p2.x > p1.x else -1
    dir_y = 1 if p2.y > p1.y else -1

    if (dir_x, dir_y) == p1.direction():
        if not p1.convex:  # must be convex for rest of rectangle to be inside
            continue
    else:  # must be concave for rest of rectangle to be inside
        if p1.convex:
            continue
    if (-dir_x, -dir_y) == p2.direction():
        if not p2.convex:  # must be convex for rest of rectangle to be inside
            continue
    else:  # must be concave for rest of rectangle to be inside
        if p2.convex:
            continue

    # now we just need to check if the edges are all inside the shape
    # first step: check if other two corners are inside the shape
    p3 = Point(p1.x, p2.y)
    p4 = Point(p2.x, p1.y)

    if not point_in_shape(p3) or not point_in_shape(p4):
        continue

    # check if we hit an edge point when going along edges => would mean we are crossing beyond boundaries
    continue_flag = False
    for x in range(p1.x + dir_x, p2.x - 2 * dir_x, dir_x):
        # first step in point_in_shape is checking if in perimeter so should be okay speed-wise
        if (x, p1.y) in outerloop and not point_in_shape(Point(x + dir_x, p1.y)):
            continue_flag = True
            break
        if (x, p2.y) in outerloop and not point_in_shape(Point(x + dir_x, p2.y)):
            continue_flag = True
            break

    if continue_flag:  # no point in checking y as well
        continue

    for y in range(p1.y + dir_y, p2.y - 2 * dir_y, dir_y):
        if (p1.x, y) in outerloop and not point_in_shape(Point(p1.x, y + dir_y)):
            continue_flag = True
            break
        if (p2.x, y) in outerloop and not point_in_shape(Point(p2.x, y + dir_y)):
            continue_flag = True
            break

    if continue_flag:
        continue

    part2 = area
    break

print("Part 1:", part1)
print("Part 2:", part2)

print(f"Time taken: {time.time() - start} s")
