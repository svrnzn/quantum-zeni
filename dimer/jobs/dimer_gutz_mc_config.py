import numpy as np

# Maximum number of parallel processes to use in the simulation.
max_workers = 2

# Number of simulations with the same parameters.
Nsim = 1

# Simulation parameters.
nwalk = int(2 * 10**7)

lambdas = [[.25, .25],
           [.25, 1.75],
           [1.25, .25]]

T = 20
dt = .01
omega_S = 1
walk_pos0 = np.array(nwalk * [[np.pi, np.pi]])
# walk_pos0 = None