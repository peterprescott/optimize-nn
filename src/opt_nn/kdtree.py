"""
K-D Tree, adapted for sphere from example by @Tsoding2017.
See also @Wikipedia2021, @KWeinberger2021, and @D.W.2015.

The main changes are:
    - input takes a dataframe with `lat` and `lng` columns,
        instead of a list of tuples,
    - 'pivot' point is included in tree, so `closer_distance()`
        must ignore point if distance is zero
    - haversine distance used instead of euclidean
    - need to account for wrapping of the globe at east-west extrema;
        @CScheidegger2013 suggests three tricks of which the third,
        'multiple covering' seems simplest.
    - want to add a visualization of divided plane
"""

from math import asin, sin, cos

import pandas as pd

from opt_nn.improved import h_distance


def build_kdtree(points_df, depth=0):
    """
    Build (branch of) kd-tree with points from dataframe.
    """

    n = len(points_df)
    k = 2  # we are working on sphere, and don't need to generalize

    if n == 0:
        return None

    axis = ("lat", "lng")[depth % k]  # cycle through dimensions

    sorted_points = points_df.sort_values(axis)

    return {
        "point": sorted_points.iloc[n // 2][["lat", "lng", "point_index"]],
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


def min_distance_to_lng_circle(angle, point):
    '''
    Return the min. distance between given point and 
    circle of longitude of given angle.

    For proof of general case see @LStrous2018.
    '''

    r = 6371  # radius of earth in km
    # following `given.haversine()`

    theta = asin(
        cos(point.lat) *
        (cos(angle) * sin(point.lng) - sin(angle) * cos(point.lng)))

    return r * theta


def min_distance_to_lat_circle(angle, point):
    '''
    Return the min. distance between given point
    and circle of latitude of given angle.

    Since circles of latitude are not great circles,
    this is easy.
    '''

    r = 6371  # radius of earth in km
    # following `given.haversine()`

    theta = abs(angle - point.lat)

    return r * theta


def axis_distance(axis, angle, point):
    '''
    Return appropriate distance for given axis.
    '''

    assert axis in ('lat', 'lng')

    if axis == 'lat':
        return min_distance_to_lat_circle(angle, point)
    else:
        return min_distance_to_lng_circle(angle, point)


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

    if h_distance(point, best) > axis_distance(axis, 
                                                root["point"][axis],
                                                point):
        best = closer_distance(
            point, kdtree_closest_point(opposite_branch, point, depth + 1),
            best)

    return best


def use_kdtree(points_df):
    '''Find nearest neighbours for all points in df using kd-tree'''

    # make `point_index` explicit column
    points_df['point_index'] = points_df.index

    # # create covering on both sides of the globe
    # left_cover = points_df.copy()
    # left_cover['lng'] = points_df['lng'] - 360
    # right_cover = points_df.copy()
    # right_cover['lng'] = points_df['lng'] + 360
    # covered_df = pd.concat([points_df, left_cover, right_cover])

    # build tree from covered_df
    # tree = build_kdtree(covered_df)

    # TODO: Debug covering. 
    # At the moment, adding the left and right covers leads to the
    # algorithm suggesting that the nearest neighbour for most (but not
    # all??) points is itself.

    tree = build_kdtree(points_df)

    # find nearest neighbours
    for i in range(len(points_df)):
        current_point = points_df.iloc[i]
        nearest = kdtree_closest_point(tree, current_point)
        points_df.loc[i, 'neighbour_index'] = nearest.point_index
        points_df.loc[i, 'distance_km'] = h_distance(current_point,
                nearest)

    return points_df


def visualize(kdtree):
    # TODO...
    pass


if __name__ == "__main__":

    from opt_nn.given import make_data

    df = make_data(100)
    a = find_all_nn(df)
    print(a)
