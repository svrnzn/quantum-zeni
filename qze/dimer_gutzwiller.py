import numpy as np
import qutip
from .many_zeno import ManyZenoTrotter, MZTrotterResult


class DimerGutzwiller(ManyZenoTrotter):


    def rho_to_theta(self, rho):
        y = 2 * rho[1, 0].imag
        z = (rho[0, 0] - rho[1, 1]).real
        theta = np.arctan2(y, z)
        
        return theta


    def theta_to_psi(self, theta):
        psi = (np.cos(theta/2)*qutip.basis(2, 0) +
               1j * np.sin(theta/2)*qutip.basis(2, 1))

        return psi


    def no_click_step(self, state):
        ns_state_dt = super().no_click_step(state)
        rho_l = ns_state_dt.ptrace(0)
        rho_r = ns_state_dt.ptrace(1)
        theta_l = self.rho_to_theta(rho_l)
        theta_r = self.rho_to_theta(rho_r)
        psi_l = self.theta_to_psi(theta_l)
        psi_r = self.theta_to_psi(theta_r)
        state_dt = qutip.tensor(psi_l, psi_r)

        return state_dt


class DimerGutzwillerLocked(ManyZenoTrotter):

    
    def __init__(self, H_S, c_ops, c_ops_multi, dt):
        self.H_S = H_S
        self.c_ops = c_ops
        self.c_ops_multi = c_ops_multi
        self.dt = dt
        self.e_ops = None
        self.H_eff = None
        self.rng = np.random.default_rng()


    def compute_e_ops(self, state=None):
        e_ops = []
        for M, multi in zip(self.c_ops, self.c_ops_multi):
            E = M.dag() * M
            gamma = E.tr()# This only works for rank 1 projectors
            if gamma == 0:
                gl_modifier = 0
            else:
                gl_modifier = (E.overlap(state))**(multi-1) / gamma
            E_gl = gl_modifier * E
            e_ops.append(E_gl)

        return e_ops


    def run_step(self, state, no_click=False):
        self.e_ops = self.compute_e_ops(state)
        self.H_eff = self.compute_H_eff()
        
        return super().run_step(state)


def gusolve(H_S, psi0, dt, tlist, c_ops, ntraj=500, no_click=False):
    dg = DimerGutzwiller(H_S, c_ops, dt)
    results = ntraj * [len(tlist) * [psi0]]
    for i in range(ntraj):
        traj = dg.run(psi0, tlist, no_click)
        results[i] = traj
        print(f"Trajectory #{i+1} of {ntraj} computed.")

    output = MZTrotterResult(results)

    return output


def glsolve(H_S, psi0, dt, tlist, c_ops, c_ops_multi, ntraj=500, no_click=False):
    gl = DimerGutzwillerLocked(H_S, c_ops, c_ops_multi, dt)
    results = ntraj * [len(tlist) * [psi0]]
    for i in range(ntraj):
        traj = gl.run(psi0, tlist, no_click)
        results[i] = traj
        print(f"Trajectory #{i+1} of {ntraj} computed.")

    output = MZTrotterResult(results)

    return output