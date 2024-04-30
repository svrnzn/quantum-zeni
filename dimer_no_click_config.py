import qutip
import numpy as np
import itertools
import dimer_stages as stages

# lmbd_1_list = np.array([0, .7, 1.1, 2/np.sqrt(3), 1.5, 3])
lmbd_1_list = np.array([0])
# lmbd_2_list = np.array([0, .7, 1.5, 3, 3.2, 4.5, 6, 7.5])
lmbd_2_list = np.array([.7, .75, .8, .9, 1.1, 1.5, 3])
# lmbd_2_list = np.array([1.1])
Nt = 1
T = 1000
dt = .01
omegaS = 1
force_no_click = True


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


sim_list = [stages.DimerParameters(HS,
                                   lmbd_1,
                                   lmbd_2,
                                   get_povm(lmbd_1, lmbd_2, omegaS),
                                   Nt,
                                   T,
                                   dt,
                                   state0,
                                   force_no_click)
            for lmbd_1, lmbd_2 in itertools.product(lmbd_1_list, lmbd_2_list)]
