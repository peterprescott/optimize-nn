"""
PyTest tests for attempted improvements.
"""

from opt_nn import given, improved


def test_less_slow():

    df = given.make_data(100)

    # need to copy df to compare answers as `slow()` modifies inplace
    a0 = given.slow(df.copy())
    a1 = improved.less_slow(df.copy())

    compare_distance = a1.distance_km == a0.distance_km
    compare_index = a1.neighbour_index == a0.neighbour_index

    assert len(compare_distance.unique()) == 1
    assert compare_distance.unique()[0] == True
    assert len(compare_index.unique()) == 1
    assert compare_index.unique()[0] == True


def test_h_distance():
    '''
    Test that h_distance() is equal to haversine() for any two points.
    '''

    df = given.make_data(2)

    p0 = df.iloc[0]
    p1 = df.iloc[1]

    assert improved.h_distance(p0, p1) == given.haversine(
        p0.lng, p0.lat, p1.lng, p1.lat
    )
