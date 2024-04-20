import qutip
import multi_stages as ms
import numpy as np


lmbd_list = np.array([.7, 1.1, 2/np.sqrt(3), 1.5, 3])
# lmbd_list = np.array([4.5, 6, 8, 10])
# lmbd_list = np.array([.7])
Ns = 2
Nt = 10**4
T = 10
dt = .01
omegaS = 1

spin0 = qutip.basis(2, 0)
spin1 = qutip.basis(2, 1)
state0 = qutip.tensor(Ns * [spin0])

HS = qutip.tensor([qutip.sigmax()] + (Ns-1)*[qutip.qeye(2)])
for i in range(1, Ns):
    padding_l = i * [qutip.qeye(2)]
    padding_r = (Ns-i-1) * [qutip.qeye(2)]
    HS += omegaS * qutip.tensor(padding_l + [qutip.sigmax()] + padding_r)

def get_povm(lmbd, omegaS): # ! Wrong nomenclature here.
    gamma = 4 * omegaS * lmbd
    E1 = gamma * qutip.tensor(Ns * [spin1]) * qutip.tensor(Ns * [spin1]).dag()
    E0 = qutip.qeye([2, Ns]) - E1
    M0 = E0.sqrtm()
    M1 = E1.sqrtm()

    return [M1]


sim_list = [ms.SimulationParameters(Ns, HS, lmbd, get_povm(lmbd, omegaS), Nt, T, dt, state0)
            for lmbd in lmbd_list]
