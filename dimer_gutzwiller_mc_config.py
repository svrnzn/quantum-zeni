import numpy as np

nwalk = 10**4
T = 10
dt = .01
lambdas = [[.5, .5], [.5, 1.5], [1.5, 1.5]]
omega_S = 1

walk_pos0 = np.array(nwalk * [[np.pi, np.pi]])