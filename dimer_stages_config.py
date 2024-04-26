import qutip
import numpy as np
import itertools
import dimer_stages as stages

# lmbd_1_list = np.array([0, .7, 1.1, 2/np.sqrt(3), 1.5, 3])
lmbd_1_list = np.array([0])
# lmbd_1_list = np.array([.7, 1.1, 1.5, 3])
# lmbd_2_list = np.array([0, .7, 1.5, 3, 3.2, 4.5, 6, 7.5])
# lmbd_2_list = np.array([.7, 1.5, 3, 4.5])
lmbd_2_list = np.array([1.1])
Nt = 10**2
T = 100
dt = .01
delT = T/2/100
omegaS = 1


t_eval = np.arange(T/2, T+delT, delT)
# t_eval = np.array([0, T])
state0 = qutip.tensor(qutip.basis(2, 1), qutip.basis(2, 1))
HS = omegaS * (qutip.tensor(qutip.sigmax(), qutip.qeye(2))
               + qutip.tensor(qutip.qeye(2), qutip.sigmax()))


def get_povm(lmbd_1, lmbd_2, omegaS): # ! Wrong nomenclature here.
    gamma_1 = 4 * omegaS * lmbd_1
    gamma_2 = 4 * omegaS * lmbd_2

    E_1_L = gamma_1 * qutip.tensor((qutip.qeye(2)-qutip.sigmaz())/2, qutip.qeye(2))
    E_1_R = gamma_1 * qutip.tensor(qutip.qeye(2), (qutip.qeye(2)-qutip.sigmaz())/2)
    E_2 = gamma_2 * qutip.tensor((qutip.qeye(2)-qutip.sigmaz())/2, (qutip.qeye(2)-qutip.sigmaz())/2)

    M1_1_L = E_1_L.sqrtm()
    M1_1_R = E_1_R.sqrtm()
    M1_2 = E_2.sqrtm()

    return [M1_1_L, M1_1_R, M1_2]


sim_list = [stages.DimerParameters(HS, lmbd_1, lmbd_2, get_povm(lmbd_1, lmbd_2, omegaS), Nt, T, dt, t_eval, state0)
            for lmbd_1, lmbd_2 in itertools.product(lmbd_1_list, lmbd_2_list)]
