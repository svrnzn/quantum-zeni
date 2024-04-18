import numpy as np
import qutip
from dataclasses import dataclass


@dataclass
class SimulationParameters:
    Ns : int
    HS : qutip.Qobj
    lmbd : float
    POVM : list[qutip.Qobj] # ! Wrong nomenclature
    Nt: int
    T: float
    dt: float
    state0: qutip.Qobj


def state_to_theta(rho):
    y = 2 * rho[1, 0].imag
    z = (rho[0, 0] - rho[1, 1]).real
    theta = np.arctan2(y, z)
    
    return theta


class Spins:


    def __init__(self, Ns, HS, POVM, dt):
        self.Ns = Ns
        self.HS = HS
        self.POVM = POVM # ! Wrong nomenclature
        self.dt = dt
        self.rng = np.random.default_rng()
        self.U = (qutip.qeye([2, self.Ns]) - 1j*self.HS*self.dt)


    def povm_probabilities(self, state):
        probs = []
        for M in self.POVM:
            E = M.dag() * M
            probs.append(qutip.expect(E, state))

        return probs


    def step(self, state, MF=False):


        def which_M(r, probs_cumsum, POVM):
            for cp, M in zip(probs_cumsum, POVM):
                if r < cp:
                    return M


        r = self.rng.random()
        click_probs = self.povm_probabilities(state)
        probs_cumsum = np.cumsum(click_probs)
        M = which_M(r, probs_cumsum, self.POVM)
        state_dt = self.U * state
        state_dt = M * state_dt

        return state_dt.unit()


    def run(self, state0, T, MF=False):
        trajectory = [state0]
        state = state0
        for t in np.arange(0, T + self.dt, self.dt):
            state_dt = self.step(state, MF)
            trajectory.append(state_dt)
            state = state_dt

        return trajectory
