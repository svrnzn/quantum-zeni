import numpy as np
import qutip


# lmbd_1_list = [0, .7, 1.1, 2/np.sqrt(3), 1.5, 3]
# lmbd_1_list = [0.5, 1.5]
lmbd_1_list = np.linspace(0, 2, 9)
# lmbd_2_list = [0, .7, 1.4, 1.75, 3.]
# lmbd_2_list = [0.5, 1.5]
lmbd_2_list = np.linspace(0, 2, 9)
ntraj_list= [10**5]
omega_S_list = [1]

T_list = [20]
t_eval_list = [np.array([0, T]) for T in T_list]
# t_eval_list = [np.linspace(T/2, T, 101) for T in T_list]

# solver = "trsolve"
solver = "mcsolve"
# solver = "gutzwiller"
if solver == "mcsolve":
    dt_list = [None]
elif solver == "trsolve" or solver == "gutzwiller":
    dt_list = [0.01]

no_click = False

psi0_list = [qutip.tensor(qutip.basis(2, 1), qutip.basis(2, 1))]