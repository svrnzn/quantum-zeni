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


@dataclass
class DimerGutzwillerLockedParameters(DimerParameters):
    c_ops_multi : list[int] = None
    solver = "gutzwiller-locked"


def states_to_yz_bloch(states):
    r_l = np.empty(len(states))
    t_l = np.empty(len(states))
    r_r = np.empty(len(states))
    t_r = np.empty(len(states))
    for j, psi in enumerate(states):
        pstate_l = psi.ptrace(0)
        pstate_r = psi.ptrace(1)
        r_l[j], t_l[j] = pstate_to_yz_bloch(pstate_l)
        r_r[j], t_r[j] = pstate_to_yz_bloch(pstate_r)

    output = np.array([[r_l, t_l], [r_r, t_r]])

    return output


def pstate_to_yz_bloch(pstate):
    y = 2 * pstate[1, 0].imag
    z = (pstate[0, 0] - pstate[1, 1]).real
    r = np.sqrt(y**2 + z**2)
    theta = np.arctan2(y, z)
    
    return r, theta


def thetas_to_state(tl, tr):
    o = qutip.basis(2, 0)
    i = qutip.basis(2, 1)
    psil = np.cos(tl/2) * o + 1j * np.sin(tl/2) * i
    psir = np.cos(tr/2) * o + 1j * np.sin(tr/2) * i

    return qutip.tensor(psil, psir)


def get_H_S(omega_S):
    H_S = omega_S * (qutip.tensor(qutip.sigmax(), qutip.qeye(2))
                    + qutip.tensor(qutip.qeye(2), qutip.sigmax()))
    
    return H_S


def get_c_ops(lmbd_1, lmbd_2, omega_S, multi=False):
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

    if multi:
        return [c1_L, c1_R, c11], [1, 1, 2]
    else:
        return [c1_L, c1_R, c11]


def get_H_S_1(omega_S):
    H_S = omega_S * qutip.sigmax()
    
    return H_S


def get_c_ops_1(lmbd_1, lmbd_2, omega_S, multi=False):
    gamma_1 = 4 * omega_S * lmbd_1
    gamma_2 = 4 * omega_S * lmbd_2
    E_1 = gamma_1 * (qutip.qeye(2)-qutip.sigmaz()) / 2
    E_2 = gamma_2 * (qutip.qeye(2)-qutip.sigmaz()) / 2
    c1 = E_1.sqrtm()
    c11 = E_2.sqrtm()

    if multi:
        return [c1, c11], [1, 2]
    else:
        return [c1, c11]


def get_gutz_locked_sim_list(lmbd_1_list,
                             lmbd_2_list,
                             omega_S_list,
                             psi0_list,
                             t_eval_list,
                             ntraj_list,
                             dt_list,
                             solver,
                             no_click):
    sim_list = [DimerGutzwillerLockedParameters(omega_S,
                                                lmbd_1,
                                                lmbd_2,
                                                get_H_S_1(omega_S),
                                                get_c_ops_1(lmbd_1, lmbd_2, omega_S),
                                                psi0,
                                                t_eval,
                                                ntraj,
                                                solver,
                                                dt,
                                                no_click,
                                                get_c_ops_1(lmbd_1, lmbd_2, omega_S, multi=True)[1])
                for lmbd_1, lmbd_2, omega_S, psi0, t_eval, ntraj, dt 
                in itertools.product(lmbd_1_list,
                                     lmbd_2_list,
                                     omega_S_list,
                                     psi0_list,
                                     t_eval_list,
                                     ntraj_list,
                                     dt_list)]
    
    return sim_list


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