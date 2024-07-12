import numpy as np
import many_zeno
import dimer
import pickle


# lambdas = [[.5, .5], [.5, 1.5], [1.5, 1.5]]
lambdas = [[.25, .25]]
ntraj_list= [10**4]
omega_S = 1

solver = "trsolve"
T = 100
dt = .01
t_eval = np.arange(0, T + dt, dt)

# no_click = False
no_click = True

# psi0_list = [qutip.tensor(qutip.basis(2, 1), qutip.basis(2, 1))]

Nth = 100
dth = 2*np.pi / Nth
tl0s = np.linspace(-np.pi + dth, np.pi, Nth)
psi0s = [dimer.thetas_to_state(tl, np.pi) for tl in tl0s]

for lmbd_1, lmbd_2 in lambdas:
    no_click_dynamics = []
    for i, psi0 in enumerate(psi0s):
        no_click_dynamics.append(many_zeno.trsolve(dimer.get_H_S(omega_S),
                                                psi0,
                                                dt,
                                                t_eval,
                                                dimer.get_c_ops(lmbd_1, lmbd_2, omega_S),
                                                ntraj=1,
                                                no_click=True))
    
    f_name = ("dimer-no-click-dynamics-"
              f"solver={solver}-"
              f"omega_S={omega_S:.2f}-"
              f"lmbd_1={lmbd_1:.2f}-"
              f"lmbd_2={lmbd_2:.2f}-"
              f"T={T}-"
              f"ntraj={1}-"
              f"dt={dt}")
    f = open(f"data/{f_name}.pkl", "wb")
    pickle.dump(no_click_dynamics, f)
    f.close()