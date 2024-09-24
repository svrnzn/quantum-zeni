import numpy as np

nwalk = 10**5
T = 20
dt = .01
lambdas = [[.25, .25], [.25, 1.25], [1.75, .25]]
# lambdas = [[.25, 1.75]]
omega_S = 1

walk_pos0 = np.array(nwalk * [[np.pi, np.pi]])
# walk_pos0 = None
