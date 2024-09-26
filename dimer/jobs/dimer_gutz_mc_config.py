import numpy as np

# Maximum number of parallel processes to use in the simulation.
max_workers = 4

# Number of simulations with the same parameters.
Nsim = 4

# Simulation parameters.
nwalk = 10**3
T = 20
dt = .01
lambdas = [[.25, .25], [1.25, .25], [.25, 1.75]]
omega_S = 1
walk_pos0 = np.array(nwalk * [[np.pi, np.pi]])
# walk_pos0 = None