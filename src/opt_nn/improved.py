'''
Improved methods for finding nearest neighbours.
'''

def less_slow():
    # simplest idea is to improve slow function
    # by not calculating d(x,y) if we know d(y,x)
    # since haversine metric is symmetric
    pass

def vectorize():
    # might be able to speed up method by treating columns
    # as vectors instead of looping through
    pass

def use_kd_tree():
    # the best method is probably to partition the space
    # with a kd_tree
    # cf. @Wikipedia2021, @StackOverflow2015, @KWeinberger2021
    pass
