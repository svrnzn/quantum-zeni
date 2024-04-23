import qutip
import multi_stages as ms
import numpy as np
import itertools


lmbd_1_list = np.array([0, .7, 1.1, 2/np.sqrt(3), 1.5, 3])
# lmbd_1_list = np.array([.7, 1.1, 2/np.sqrt(3), 1.5, 3])
# lmbd_1_list = np.array([0])
lmbd_2_list = np.array([0, .7, 1.5, 3, 3.2, 4.5, 6])
Ns = 2
Nt = 10**4
T = 10
dt = .01
omegaS = 1

spin0 = qutip.basis(2, 0)
spin1 = qutip.basis(2, 1)
state0 = qutip.tensor(Ns * [spin0])

HS = 0 * qutip.tensor(Ns * [qutip.sigmax()])
for i in range(Ns):
    padding_l = i * [qutip.qeye(2)]
    padding_r = (Ns-i-1) * [qutip.qeye(2)]
    HS += omegaS * qutip.tensor(padding_l + [qutip.sigmax()] + padding_r)

def get_povm(lmbd_1, lmbd_2, omegaS): # ! Wrong nomenclature here.
    POVM = []
    gamma_1 = 4 * omegaS * lmbd_1
    gamma_2 = 4 * omegaS * lmbd_2
    
    for i in range(Ns):
        padding_l = i * [qutip.qeye(2)]
        padding_r = (Ns-i-1) * [qutip.qeye(2)]
        projector1 = spin1 * spin1.dag()
        E1_1 = gamma_1 * qutip.tensor(padding_l + [projector1] + padding_r)
        M1_1 = E1_1.sqrtm()
        POVM.append(M1_1)

    E1_2 = gamma_2 * qutip.tensor(Ns * [spin1]) * qutip.tensor(Ns * [spin1]).dag()
    M1_2 = E1_2.sqrtm()
    POVM.append(M1_2)

    return POVM


sim_list = [ms.SimulationParameters(Ns, HS, f"({lmbd_1:.1f}, {lmbd_2:.1f})", get_povm(lmbd_1, lmbd_2, omegaS), Nt, T, dt, state0)
            for lmbd_1, lmbd_2 in itertools.product(lmbd_1_list, lmbd_2_list)]

# sim_list = [ms.SimulationParameters(Ns, HS, f"{lmbd_1}", get_povm(lmbd_1, lmbd_1, omegaS), Nt, T, dt, state0)
#             for lmbd_1 in lmbd_1_list]