import numpy as np

def compute_longest_survival(survivals):
    found_survivor_at = -1
    t = len(survivals)-1
    while found_survivor_at == -1 and t >= 0:
        if np.count_nonzero(survivals[t]):
            found_survivor_at = t
        t -= 1
    return found_survivor_at

def compute_num_survivors_at_the_end(survivals):
    return np.count_nonzero(survivals[-1])
