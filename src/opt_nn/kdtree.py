"""
K-D Tree, adapted for sphere from example by @Tsoding2017.
See also @Wikipedia2021, @KWeinberger2021, and @StackOverflow2015.

The main changes are:
    - input takes a dataframe with `lat` and `lng` columns,
        instead of a list of tuples,
    - 'pivot' point is included in tree, so `closer_distance()`
        must ignore point if distance is zero
    - haversine distance used instead of euclidean
    - need to account for wrapping of the globe at east-west extrema
    - want to add a visualization of divided plane
"""

from opt_nn.improved import h_distance


def build_kdtree(points_df, depth=0):
    """Build (branch of) kd-tree with points from dataframe."""

    n = len(points_df)
    k = 2  # we are working on sphere, and don't need to generalize

    if n == 0:
        return None

    axis = ("lat", "lng")[depth % k]  # cycle through dimensions

    sorted_points = points_df.sort_values(axis)

    return {
        "point": sorted_points.iloc[n // 2][["lat", "lng"]],
        "left": build_kdtree(sorted_points[:n // 2], depth + 1),
        "right": build_kdtree(sorted_points[n // 2 + 1:], depth + 1),
    }


def closer_distance(pivot, p1, p2):
    if p1 is None:
        return p2

    if p2 is None:
        return p1

    d1 = h_distance(pivot, p1)
    d2 = h_distance(pivot, p2)

    # if distance is zero, point is the same
    # and we must ignore it
    if d1 == 0:
        return p2
    elif d2 == 0:
        return p1
    # otherwise return smaller distance
    elif d1 < d2:
        return p1
    else:
        return p2


def kdtree_closest_point(root, point, depth=0):
    if root is None:
        return None

    k = 2  # number of dimensions
    axis = ("lat", "lng")[depth % k]  # cycle through dimensions

    next_branch = None
    opposite_branch = None

    if point[axis] < root["point"][axis]:
        next_branch = root["left"]
        opposite_branch = root["right"]
    else:
        next_branch = root["right"]
        opposite_branch = root["left"]

    best = closer_distance(point,
                           kdtree_closest_point(next_branch, point, depth + 1),
                           root["point"])

    # TODO: the line below is wrong, still comparing euclidean distance
    # squares, instead of great-circle distance
    if h_distance(point, best) > (point[axis] - root["point"][axis])**2:
        best = closer_distance(
            point, kdtree_closest_point(opposite_branch, point, depth + 1),
            best)

    return best

def visualize(kdtree):
    # TODO...
    pass

if __name__ == "__main__":

    from opt_nn.given import make_data

    df = make_data(100)

    tree = build_kdtree(df)

    print(kdtree_closest_point(tree, df.iloc[10]))

    print(df.iloc[10])
