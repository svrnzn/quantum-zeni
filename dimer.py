import numpy as np
import qutip
from dataclasses import dataclass
import itertools


@dataclass
class DimerParameters:
    omega_S : float
    lmbd_1 : float
    lmbd_2 : float
    H_S : qutip.Qobj
    c_ops : list[qutip.Qobj]
    psi0 : qutip.Qobj
    t_eval : np.array
    ntraj : int
    solver : str
    dt : float = None
    no_click : bool = False


    def __str__(self):
        f_name = ("dimer-"
                  f"solver={self.solver}-"
                  f"omega_S={self.omega_S:.2f}-"
                  f"lmbd_1={self.lmbd_1:.2f}-"
                  f"lmbd_2={self.lmbd_2:.2f}-"
                  f"T={self.t_eval[-1]}-"
                  f"ntraj={self.ntraj}-"
                  f"dt={self.dt}")
        
        return f_name


def pstate_to_yz_bloch(pstate):
    y = 2 * pstate[1, 0].imag
    z = (pstate[0, 0] - pstate[1, 1]).real
    r = np.sqrt(y**2 + z**2)
    theta = np.arctan2(y, z)
    
    return r, theta


def get_H_S(omega_S):
    H_S = omega_S * (qutip.tensor(qutip.sigmax(), qutip.qeye(2))
                    + qutip.tensor(qutip.qeye(2), qutip.sigmax()))
    
    return H_S


def get_c_ops(lmbd_1, lmbd_2, omega_S):
    gamma_1 = 4 * omega_S * lmbd_1
    gamma_2 = 4 * omega_S * lmbd_2
    E_1_L = gamma_1 * qutip.tensor((qutip.qeye(2)-qutip.sigmaz())/2,
                                   qutip.qeye(2))
    E_1_R = gamma_1 * qutip.tensor(qutip.qeye(2),
                                   (qutip.qeye(2)-qutip.sigmaz())/2)
    E_2 = gamma_2 * qutip.tensor((qutip.qeye(2)-qutip.sigmaz())/2,
                                 (qutip.qeye(2)-qutip.sigmaz())/2)
    c1_L = E_1_L.sqrtm()
    c1_R = E_1_R.sqrtm()
    c11 = E_2.sqrtm()

    return [c1_L, c1_R, c11]


def get_sim_list(lmbd_1_list,
                 lmbd_2_list,
                 omega_S_list,
                 psi0_list,
                 t_eval_list,
                 ntraj_list,
                 dt_list,
                 solver,
                 no_click):
    sim_list = [DimerParameters(omega_S,
                                lmbd_1,
                                lmbd_2,
                                get_H_S(omega_S),
                                get_c_ops(lmbd_1, lmbd_2, omega_S),
                                psi0,
                                t_eval,
                                ntraj,
                                solver,
                                dt,
                                no_click)
                for lmbd_1, lmbd_2, omega_S, psi0, t_eval, ntraj, dt 
                in itertools.product(lmbd_1_list,
                                     lmbd_2_list,
                                     omega_S_list,
                                     psi0_list,
                                     t_eval_list,
                                     ntraj_list,
                                     dt_list)]
    
    return sim_list