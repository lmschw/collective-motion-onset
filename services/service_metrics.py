import numpy as np

def compute_longest_survival(agents, num_predators):
    found_survivor_at = -1
    t = len(agents)-1
    while found_survivor_at == -1 and t >= 0:
        agents_t = np.array(agents[t])
        if len(agents_t[agents_t >= num_predators]) > 0:
            found_survivor_at = t
        t -= 1
    return found_survivor_at

def compute_num_survivors_at_the_end(agents, num_predators):
    agents_t = np.array(agents[len(agents)-1])
    return len(agents_t[agents_t >= num_predators])
