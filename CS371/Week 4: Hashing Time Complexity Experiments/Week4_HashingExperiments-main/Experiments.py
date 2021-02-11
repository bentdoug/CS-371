import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse

def get_bin_trials(m, n):
    """
    Do a trial of throwing m balls into n bins
    Parameters
    ----------
    m: int
        Number of balls
    n: int
        Number of bins
    
    Returns
    -------
    trials: ndarray(m)
        The bin indices of each throw
    bins: ndarray(n)
        The bins with the counts of elements that landed in them
    """
    trials = np.random.randint(0, n, m)
    bins = sparse.coo_matrix( (np.ones(m), (trials, np.zeros(m)) ), shape=(n, 1))
    bins = bins.toarray()
    return trials, bins

def make_animation(m, n):
    """
    Make an animation of tossing m balls into n bins
    uniformly at random
    Parameters
    ----------
    m: int
        Number of balls
    n: int
        Number of bins
    """
    # Throw m balls into n bins and record
    # the indices of each trial
    trials, bins = get_bin_trials(m, n)
    # What is the maximum number of balls in any bin?
    # (This will be used to adjust the height of the plot)
    max_bin = np.max(bins)
    fac = 0.2
    plt.figure(figsize=(fac*m, fac*(max_bin+2)))
    for i in range(len(trials)):
        plt.clf()
        # First plot all of the trials up to this point
        # As blue dots
        binsi = np.zeros(n)
        for idx in trials[0:i]:
            binsi[idx] += 1
        for x, h in enumerate(binsi):
            for y in range(int(h)):
                plt.scatter([x], [y], c='C0')
        # Plot the this trial as an orange dot
        x = trials[i]
        y = binsi[x]
        binsi[x] += 1
        plt.scatter([x], [y], c='C1')
        plt.xticks(np.arange(n), ["{}".format(i) for i in range(n)])
        plt.xlim([-0.2, n+0.2])
        plt.ylim([-1, max_bin])
        plt.title("Max height = {}, Num Empty = {}, Average Height = {}".format(
            int(np.max(binsi)), np.sum(binsi == 0), np.mean(binsi)
        ))
        plt.savefig("{}.png".format(i), bbox_inches='tight')


def experiment_fixedbins(n, max_m, trials_per_m):
    """
    Do a series of experiments to count the maximum height
    after tossing an increasing amount of m balls into n
    bins, and plot the results
    Parameters
    ----------
    n: int
        Number of bins
    max_m: int
        The maximum number of balls in a bin
    trials_per:m: int
        Number of trials per number of objects
    """
    ms = np.arange(1, max_m)
    max_counts = np.zeros_like(ms)
    for i, m in enumerate(ms):
        ## TODO: Fill this in
        ## For this m, do trials_per_m trials using the method
        ## get_bin_trials, average the number of throws this
        ## takes, and save the result in max_counts at index i
        fin = 0
        tot = 0
        for x in range(trials_per_m):
            trials, bins = get_bin_trials(m, n)
            fin+=np.max(bins)
            tot+=1
        #print(fin/tot)
        max_counts[i] = fin/tot
        pass
    plt.plot(ms, max_counts)
    plt.xlabel("m")
    plt.ylabel("Average Max Height")

def experiment_varyingbins(max_n, trials_per_n):
    """
    Make an animation of tossing m balls into n bins
    uniformly at random
    Parameters
    ----------
    max_n: int
        The maximum number of balls/bins to consider
    trials_per_n: int
        Number of trials per bin number
    """
    ## TODO: Fill this in
    pass

    
experiment_fixedbins(100, 200, 100)
plt.show()