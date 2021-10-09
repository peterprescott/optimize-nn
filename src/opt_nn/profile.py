'''
Analyze solutions with insightful graphs.
'''

import time

import matplotlib.pyplot as plt

from opt_nn.given import make_data


def time_solution(solution, n):
    '''Time solution for dataset of given length.'''

    df = make_data(n)   # create dataframe of length n
    t0 = time.time()    # start timer
    solution(df)        # solve
    t1 = time.time()    # stop timer

    return t1 - t0      # return time taken
