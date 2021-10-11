'''
Analyze solutions with insightful graphs.
'''

import time
import os

import matplotlib.pyplot as plt

from opt_nn.given import make_data


def time_solution(solution, n):
    '''Time solution for dataset of given length.'''

    df = make_data(n)  # create dataframe of length n
    t0 = time.time()  # start timer
    solution(df)  # solve
    t1 = time.time()  # stop timer

    return t1 - t0  # return time taken


def compare_solutions(solution_list, dataset_sizes=range(10, 200, 50)):
    '''Compare solutions on datasets of different sizes.'''

    results = dict()

    for solution in solution_list:
        # ugly but better than '<function slow at 0x7fb168680310>'
        solution_name = str(solution).split(' ')[1]

        results[solution_name] = dict()
        for n in dataset_sizes:
            results[solution_name][n] = time_solution(solution, n)

    return results


def plot_comparison(results, figsize=(10, 10)):
    '''
    Line graph plotting dataset-size vs time-taken for each solution.
    '''

    fig, ax = plt.subplots(figsize=figsize)

    for solution in results.keys():
        ax.plot(results[solution].keys(),
                results[solution].values(),
                label=solution)

    ax.set_xlabel('n')
    ax.set_ylabel('t')
    ax.set_title('Time taken (t) by solutions on datasets of varying size (n)')
    plt.legend()
    try:
        plt.savefig(os.path.join('img','comparison.png'))
    except Exception as e:
        print(e)
    plt.show()


if __name__=='__main__':

    from opt_nn.given import slow
    from opt_nn.improved import less_slow
    from opt_nn.kdtree import use_kdtree
    from opt_nn.xyz import use_3dtree

    solutions = [slow, less_slow, use_kdtree, use_3dtree]

    results = compare_solutions(solutions)
    plot_comparison(results)

