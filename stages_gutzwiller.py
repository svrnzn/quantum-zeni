import numpy as np
import qutip
from dataclasses import dataclass


@dataclass
class SimulationParameters:
    lmbd: float
    Nt: int
    T: float
    dt: float
    omegaS: float
    state0: qutip.Qobj
    force_no_click : bool


def state_to_theta(state):
    rho = state * state.dag()
    y = 2 * rho[1, 0].imag
    z = (rho[0, 0] - rho[1, 1]).real
    theta = np.arctan2(y, z)
    
    return theta


def p_infty(lmbd, theta):
    pass


class Spin:


    def __init__(self, omegaS, dt, lmbd):
        self.omegaS = omegaS
        self.dt = dt
        self.lmbd = lmbd

        self.alpha = 4 * omegaS * lmbd
        self.HS = omegaS * qutip.sigmax()
        spin1 = qutip.basis(2, 1)
        self.projector1 = spin1 * spin1.dag()
        self.e1 = self.alpha * self.dt * self.projector1
        self.rng = np.random.default_rng()


    def get_U_eff(self, state):
        H_eff = (self.HS
                 -1j * self.alpha * self.projector1.overlap(state) * self.projector1 / 4)
        U_eff = qutip.qeye(2) - 1j * self.dt * H_eff

        return U_eff

    def click_probability(self, state):
        return self.alpha * self.dt * self.projector1.overlap(state)**2# Note that I'm taking the overlap with the projector.


    def step(self, state, force_no_click=False):
        def click_step():
            return qutip.basis(2, 1)
        

        def no_click_step(state):
            state_dt = self.get_U_eff(state) * state

            return state_dt.unit()
        

        if force_no_click:
            return no_click_step(state)
        
        else:
            r = self.rng.random()
            click = r < self.click_probability(state)
            if click:
                return click_step()
            
            else:
                return no_click_step(state)


    def run(self, state0, T, force_no_click=False):
        trajectory = [state0]
        state = state0
        for t in np.arange(0, T + self.dt, self.dt):
            state_dt = self.step(state, force_no_click)
            trajectory.append(state_dt)
            state = state_dt

        return trajectory
