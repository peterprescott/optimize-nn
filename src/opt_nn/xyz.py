"""
Avoid complications of spherical geometry
by working in 3-d Cartesian space.

Unfortunately, this is only 90% accurate,
and I'm not sure where the bug is. 
(Perhaps it is numpy rounding errors?)
"""

from math import sqrt

import numpy as np

from opt_nn.improved import h_distance


def same_point(p1, p2):
    """
    Return True if points are equivalent.
    """

    if p1.point_index == p2.point_index:
        return True
    elif (p1.x == p2.x) and (p1.y == p2.y) and (p1.z == p2.z):
        return True
    else:
        return False


def closer_distance(pivot, p1, p2):
    """
    Return whichever point is closest to pivot,
    so long as point is not identical to pivot.
    """

    # if one point is None, return the other
    if p1 is None:
        return p2
    if p2 is None:
        return p1

    # if one point is identical, return the other
    if same_point(pivot, p1):
        return p2
    if same_point(pivot, p2):
        return p1

    # otherwise return whichever point is shorter distance away
    d1 = euclidean(pivot, p1)
    d2 = euclidean(pivot, p2)

    if d1 < d2 and d1 > 0:
        return p1
    else:
        return p2


class KDTree:
    """
    Recursive spatial index built by cycling through dimensional axes
    and splitting on median point.
    """

    axes = ("x", "y", "z")

    def __init__(self, points_df, depth=0):
        """Create new (branch of) tree with dataframe of points."""

        n = len(points_df)
        self.depth = depth
        self.axis = self.axes[depth % len(self.axes)]

        if n > 0:
            sorted_points = points_df.sort_values(self.axis)

            self.node = sorted_points.iloc[n // 2][["x", "y", "z", "point_index"]]
            self.left = KDTree(sorted_points.iloc[: n // 2], self.depth + 1)
            self.right = KDTree(sorted_points.iloc[n // 2 + 1 :], self.depth + 1)

        else:
            self.node = None

    def find_nn(self, point):
        """
        Find nearest neighbour on this (branch of) tree for given point.
        """

        if self.node is None:
            return None

        # first check what side of the boundary we are on
        if point[self.axis] < self.node[self.axis]:
            next_branch, opposite = self.left, self.right
        else:
            next_branch, opposite = self.right, self.left

        # check if point is closer to the current node
        # or a point on the next branch
        closest = closer_distance(point, self.node, next_branch.find_nn(point))

        # if we are closer to the boundary than the current closest
        # then we also need to check our current closest
        # is better than the nearest neighbour on the opposite branch
        if (
            euclidean(point, closest)
            > (
                # square of distance to axis boundary
                point[self.axis]
                - self.node[self.axis]
            )
            ** 2
        ):
            closest = closer_distance(point, closest, opposite.find_nn(point))

        # also need to make sure we don't bounce on same point
        if same_point(point, self.left.node):
            closest = closer_distance(point, closest,
                    self.left.find_nn(point))
        elif same_point(point, self.right.node):
            closest = closer_distance(point, closest,
                    self.right.find_nn(point))

        return closest


        return closest


def euclidean(p1, p2, square_root=False):
    """
    Return (sum of) Euclidean distance between 3-d points.
    """

    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dz = p1.z - p2.z

    sum_of_squares = dx ** 2 + dy ** 2 + dz ** 2

    if square_root:
        return sqrt(sum_of_squares)
    else:
        return sum_of_squares



def transform_coords(df):
    '''Transform lat/lng to cartesian'''

    df[["theta", "phi"]] = np.radians(df[["lng", "lat"]])
    df["x"] = np.cos(df.theta) * np.cos(df.phi)
    df["y"] = np.sin(df.theta) * np.cos(df.phi)
    df["z"] = np.sin(df.phi)

    return df


def use_3dtree(df):
    """Use 3-dimensional k-d tree to give solution"""

    
    df["point_index"] = df.index

    # first transform to 3-d cartesian coordinates
    df = transform_coords(df)

    # then construct kd-tree
    tree = KDTree(df)

    # then use to find nearest neighbours
    df.neighbour_index = df.apply(
            lambda x: tree.find_nn(x).point_index, axis=1)

    df["euclidean_square"] = df.apply(
        lambda x: euclidean(x, df.iloc[x.neighbour_index]), axis=1
    )

    # then find spherical distance using haversine formula
    df.distance_km = df.apply(
        lambda x: h_distance(x, df.iloc[x.neighbour_index]), axis=1
    )

    return df
