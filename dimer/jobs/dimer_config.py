import numpy as np
import qutip

# Maximum number of parallel processes to use in the simulation.
max_workers = 2

# Run qutip.mcsolve in series or parallel.
mcsolve_map = 'serial'
# mcsolve_map = 'parallel'

# Number of simulations with the same parameters.
nsim = 1

# Statistics
ntraj = 10**3

# Physical parameters.
# lambdas = [[.25, .25],
#            [.25, 1.75],
#            [1.25, .25]]


Nl1 = 16
Nl2 = 31
l1s = np.linspace(0, 1.5, Nl1)
l2s = np.linspace(0, 3, Nl2)
lambdas = [[l1, l2] for l1 in l1s for l2 in l2s]

T = 20
dt = .01
omega_S = 1

t_eval = np.array([0, T])

# solver = "trsolve"
solver = "mcsolve"
# solver = "gutzwiller"

# store_states = False
# compute_eentropy = False
# compute_fidelity = False

no_click = False

psi0 = qutip.tensor(qutip.basis(2, 1), qutip.basis(2, 1))