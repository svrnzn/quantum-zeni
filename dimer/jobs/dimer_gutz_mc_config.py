import numpy as np

nwalk = 10**7
T = 20
dt = .01
# lambdas = [[.25, .25], [.5, 1.5], [1.5, .5]]
lambdas = [[.25, .25]]
omega_S = 1

walk_pos0 = np.array(nwalk * [[np.pi, np.pi]])
# walk_pos0 = None
