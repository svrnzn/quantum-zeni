import qutip
import stages
import numpy as np


# lmbd_list = [1.1, 2/np.sqrt(3), 1.5, 3]
lmbd_list = [.7, 1.5, 3, 4.5]
# lmbd_list = [.7]
# Nt = 1000
Nt = 10**4
# T = 100
T = 10
dt = .01
omegaS = 1
state0 = qutip.basis(2, 0)

sim_list = [stages.SimulationParameters(lmbd, Nt, T, dt, omegaS, state0) for lmbd in lmbd_list]
