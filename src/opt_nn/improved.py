'''
Improved methods for finding nearest neighbours,
as well as some other tweaks to `.given` to better suit me.
'''


import pandas as pd
import numpy as np

from opt_nn.given import haversine, slow, make_data


def h_distance(p1, p2):
    '''
    Return haversine distance between two points.
    (This wraps the given.haversine() function,
    allowing us to more intuitively feed in the 
    two points (with `lng` and `lat` attributes)
    that we are interested in finding the distance for.
    '''

    return haversine(p1.lng, p1.lat, p2.lng, p2.lat)


def compare_solutions(sol1, sol2=slow, df=None):
    '''
    Compare nearest neighbour indices returned by two solutions.
    '''

    if df is None:
        df = make_data(100)

    # need to copy df to compare answers as `slow()` modifies inplace
    df1 = df.copy()
    df2 = df.copy()

    # use solution to generate answers
    a1 = sol1(df1)
    a2 = sol2(df2)

    # compare equality of neighbour indices
    return {'First': a1.neighbour_index,
            'Second': a2.neighbour_index,
            'Agreed': (a1.neighbour_index == a2.neighbour_index)}


class Distances():
    '''
    Make sure we never calculate a distance twice.
    '''

    def __init__(self, points_df, metric=h_distance):
        '''
        Initialize with dataframe of points.
        '''

        self.metric = metric
        self.points = points_df
        self.n = len(points_df)
        self.table = np.zeros((self.n, self.n), float)

    def lookup(self, i, j):
        '''
        Lookup distance between points i and j,
        as indexed in the points dataframe.
        '''

        # take advantage of symmetry
        if i > j:
            i, j = j, i

        # if points are the same point, no need to look
        if i == j:
            return 0
        # if we have found the answer before, no need to again
        elif self.table[i,j]:
            return self.table[i,j]
        # otherwise calculate, save, and return
        else:
            self.table[i,j] = self.metric(
                    self.points.iloc[i],
                    self.points.iloc[j])
            return self.table[i,j]

    def find_all(self):
        '''Find all distances.'''

        for i in range(self.n):
            for j in range(i, self.n):
                self.lookup(i,j)

    def find_nn(self):
        '''
        Find all nearest neighbours and return index
        and distance.
        '''

        self.find_all()
        # fill in empty half of matrix
        self.table = np.maximum(self.table.T, self.table)
        # prevent zero distance between same point looking like minimum
        self.table = np.where(self.table > 0, self.table, np.inf)

        nn_df = pd.DataFrame([
            np.min(self.table, axis=0),
            np.argmin(self.table, axis=0)
            ]).T
        nn_df.columns = ['distance_km', 'neighbour_index']

        return nn_df


def less_slow(df):
    '''
    The simplest idea is to improve slow function
    by not calculating d(x,y) if we know d(y,x)
    since haversine metric is symmetric.

    So we start the `j` loop from `i`, and also compare
    whether the distance is the nearest for j.
    '''

    # Loop over each point in the dataframe
    for i in range(len(df)):
        # compare it to each other point in the dataframe
        # (ADDITION:) that we have not yet compared it to
        for j in range(i, len(df)):

            # Calculate the distance
            distance = haversine(df.loc[i, "lng"], df.loc[i, "lat"],
                                 df.loc[j, "lng"], df.loc[j, "lat"])

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

            # (ADDITION: We also need to do the symmetric bit)
            if df.loc[j, "distance_km"] is None:
                df.loc[j, "distance_km"] = distance
                df.loc[j, "neighbour_index"] = i
            # if this distance is closer than the previous best then
            # lets use this one
            elif df.loc[j, "distance_km"] > distance:
                df.loc[j, "distance_km"] = distance
                df.loc[j, "neighbour_index"] = i
            # (end ADDITION)

    return df

