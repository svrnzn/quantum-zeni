import numpy as np
import qutip

# Maximum number of parallel processes to use in the simulation.
max_workers = 4

# Number of simulations with the same parameters.
nsim = 4

# Statistics
ntraj = 10**2

# Physical parameters.
lambdas = [[.25, .25],
           [.25, 1.75],
           [1.25, .25]]

T = 20
dt = .01
omega_S = 1

t_eval = np.array([0, T])

# solver = "trsolve"
solver = "mcsolve"
# solver = "gutzwiller"

store_states = False
compute_eentropy = False
compute_fidelity = False

no_click = False

psi0 = qutip.tensor(qutip.basis(2, 1), qutip.basis(2, 1))