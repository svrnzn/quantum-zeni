import qutip
import numpy as np
from dataclasses import dataclass


@dataclass
class DimerParameters:
    HS : qutip.Qobj
    lmbd_1 : float
    lmbd_2 : float
    POVM : list[qutip.Qobj] # ! Wrong nomenclature
    Nt : int
    T : float
    dt : float
    t_eval : np.array 
    state0: qutip.Qobj


def state_to_theta(rho):
    y = 2 * rho[1, 0].imag
    z = (rho[0, 0] - rho[1, 1]).real
    theta = np.arctan2(y, z)
    
    return theta