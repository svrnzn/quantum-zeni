import numpy as np

Nsim = 1

nwalk = 10**3
T = 20
dt = .01
lambdas = [[.25, .25], [.25, 1.25], [1.75, .25]]
omega_S = 1
walk_pos0 = np.array(nwalk * [[np.pi, np.pi]])
# walk_pos0 = None