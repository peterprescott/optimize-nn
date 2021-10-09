'''
Improved methods for finding nearest neighbours,
as well as some other tweaks to `.given` to better suit me.
'''

from opt_nn.given import haversine


def h_distance(p1, p2):
    '''
    Return haversine distance between two points.
    (This wraps the given.haversine() function,
    allowing us to more intuitively feed in the 
    two points (with `lng` and `lat` attributes)
    that we are interested in finding the distance for.
    '''

    return haversine(p1.lng, p1.lat, p2.lng, p2.lat)


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


def vectorize():
    # might be able to speed up method by treating columns
    # as vectors instead of looping through
    pass


def use_kdtree(df):
    # the best method is probably to partition the space
    # with a kd_tree
    # cf. @Wikipedia2021, @D.W.2015, @KWeinberger2021
    pass
