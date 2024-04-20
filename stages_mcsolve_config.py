import qutip
import numpy as np
from dataclasses import dataclass


@dataclass
class SimulationParameters:
    lmbd: float
    Nt: int
    T: float
    dt: float
    omegaS: float
    state0: qutip.Qobj
    HS : qutip.Qobj
    POVM : list[qutip.Qobj]


lmbd_list = [.7, 1.1, 2/np.sqrt(3), 1.5, 3]
Nt = 10**4
T = 10
dt = .01
omegaS = 1
state0 = qutip.basis(2, 0)
HS = omegaS * qutip.sigmax()
 

def get_povm(lmbd, omegaS): # ! Wrong nomenclature here.
    gamma = 4 * omegaS * lmbd
    spin1 = qutip.basis(2, 1)
    E1 = gamma * spin1 * spin1.dag()
    E0 = qutip.qeye(2) - E1
    M0 = E0.sqrtm()
    M1 = E1.sqrtm()

    return [M1]


sim_list = [SimulationParameters(lmbd, Nt, T, dt, omegaS, state0, HS, get_povm(lmbd, omegaS))
            for lmbd in lmbd_list]
