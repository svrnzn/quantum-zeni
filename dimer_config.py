import numpy as np
import qutip
import dimer
import itertools


# lmbd_1_list = [0, .7, 1.1, 2/np.sqrt(3), 1.5, 3]
lmbd_1_list = [0]
# lmbd_2_list = [0, .7, 1.1, 2/np.sqrt(3), 1.5, 3., 3.2]
lmbd_2_list = [1.5]
ntraj_list= [10**2]
omega_S_list = [1]

T_list = [100]
dt_eval_list = [T/2/100 for T in T_list]
t_eval_list = [np.arange(T/2, T+dt_eval, dt_eval)
               for T, dt_eval in zip(T_list, dt_eval_list)]

# solver = "trsolve"
solver = "mcsolve"
if solver == "mcsolve":
    dt_list = [None]
elif solver == "trsolve":
    dt_list = [0.01]

no_click = False

psi0_list = [qutip.tensor(qutip.basis(2, 1), qutip.basis(2, 1))]