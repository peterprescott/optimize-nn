"""
PyTest tests for attempted improvements.
"""

from opt_nn import given, improved, kdtree, xyz


def check_solution(alternative_solution):
    '''
    Check that improved solution returns same values as given slow solution.
    '''

    df = given.make_data(100)

    # need to copy df to compare answers as `slow()` modifies inplace
    a0 = given.slow(df.copy())
    a1 = alternative_solution(df.copy())

    # compare equality of distances
    compare_distance = (a1.distance_km == a0.distance_km)
    # compare equality of neighbour indices
    compare_index = (a1.neighbour_index == a0.neighbour_index)

    assert len(compare_distance.unique()) == 1
    assert compare_distance.unique()[0] == True
    assert len(compare_index.unique()) == 1
    assert compare_index.unique()[0] == True


def wrong_solution(points_df):
    '''
    Return same answers as `slow()` solution,
    but change zeroth neighbour_index to impossible negative value.
    '''

    df = given.slow(points_df)
    df.loc[0, 'neighbour_index'] = -1

    return df


def test_check_solution():
    '''
    Test that check_solution passes for identical `given.slow` solution 
    and fails for `wrong_solution`.
    '''

    # check_solution passes for identical solution
    check_solution(given.slow)

    # check_solution fails for wrong_solution
    try:
        check_solution(wrong_solution)
    except Exception as e:
        # `wrong_solution` should throw an AssertionError
        assert isinstance(e, AssertionError)


def test_less_slow():
    '''
    Test `improved.less_slow()` solution.
    '''

    check_solution(improved.less_slow)

def test_use_kdtree():
    '''
    Test `kdtree.use_kdtree()` solution.
    '''

    check_solution(kdtree.use_kdtree)


def test_use_3dtree():
    '''
    Test `xyz.use_3dtree()` solution.
    '''

    check_solution(xyz.use_3dtree)

def test_transform_coords():
    '''
    Test that nearest neighbours are the same
    for euclidean metric in 3-d space
    and haversine metric on surface of the globe.
    '''

    from opt_nn.improved import h_distance, Distances
    from opt_nn.xyz import euclidean, transform_coords

    df = given.make_data(100)
    df = transform_coords(df)

    dist = Distances(df, h_distance)
    dist.find_all()
    a1 = dist.find_nn()

    eucl = Distances(df, euclidean)
    eucl.find_all()
    a2 = eucl.find_nn()

    compare = a1.neighbour_index == a2.neighbour_index
    assert len(compare.unique()) == 1
    assert compare[0] == True

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
