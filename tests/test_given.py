'''
PyTest tests for given functions.
'''

from random import randint

from opt_nn import given


def test_make_data():
    '''
    Test make_data() function returns appropriate dataframe.
    '''

    n = randint(10, 20)
    df = given.make_data(n)

    assert len(df) == n
    assert set(df.columns) == {'lat', 'lng', 'distance_km', 'neighbour_index'}
    assert max(df.lat) <= 90
    assert min(df.lat) >= -90
    assert max(df.lng) <= 180
    assert min(df.lng) >= -180


def test_haversine():
    '''
    TODO...
    '''
    pass


def test_slow():
    '''
    TODO...
    '''
    pass
