"""
These are the initial functions given for the exercise.
"""

from math import radians, cos, sin, asin, sqrt

import pandas as pd
import numpy as np


def make_data(list_length: int = 1000):
    """
    Generate Random Points on the globe for distance checking. All
    points are specified in decimal degrees.  The returned dataframe
    also contains two additional columns, distance_km which should be
    filled in with the distance in kilometers between this point and
    it's nearest neighbour and neighbour_index which should be filled in
    with the zero based index of the point that is closest to this
    point.

    Parameters
    ----------
    list_length: int
        The number of points to generate

    Returns
    -------
    pd.DataFrame
        The dataframe containing the random points and distance_km and
        neighbour_index columns.
    """
    return pd.DataFrame(
        data={
            "lat": (np.random.rand(list_length) - 0.5) * 180,
            "lng": (np.random.rand(list_length) - 0.5) * 360,
            "distance_km": None,
            "neighbour_index": None,
        }
    )


def haversine(lon1: float, lat1: float, lon2: float, lat2: float):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def slow(df: pd.DataFrame):
    """
    Given a dataframe of points in decimal degrees calculate the two
    additional columns, distance_km is filled in with the distance in
    kilometers between each point and it's nearest neighbour and
    neighbour_index which is filled in with the zero based index of the
    point that is closest to each point.

    This implementation is deliberately slow, how much better can you do?

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe containing the points to work with

    Returns
    -------
    pd.DataFrame
        The dataframe same dataframe returned with extra columns calculated
    """

    # Loop over each point in the dataframe
    for i in range(len(df)):
        # compare it to each other point in the dataframe
        for j in range(len(df)):

            # Calculate the distance
            distance = haversine(
                df.loc[i, "lng"],
                df.loc[i, "lat"],
                df.loc[j, "lng"],
                df.loc[j, "lat"]
            )

            # If the distance is 0 then it's the same point
            if distance == 0:
                continue

            # If there is no distance set then this is the closest so far
            if df.loc[i, "distance_km"] is None:
                df.loc[i, "distance_km"] = distance
                df.loc[i, "neighbour_index"] = j
            # if this distance is closer than the previous best then
            # lets use this one
            elif df.loc[i, "distance_km"] > distance:
                df.loc[i, "distance_km"] = distance
                df.loc[i, "neighbour_index"] = j

    return df
