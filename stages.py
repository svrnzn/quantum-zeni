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


def state_to_theta(state):
    rho = state * state.dag()
    y = 2 * rho[1, 0].imag
    z = (rho[0, 0] - rho[1, 1]).real
    theta = np.arctan2(y, z)
    
    return theta


def p_infty(lmbd, theta):
    if lmbd < 1:
        gamma = 1 / np.sqrt(1 - lmbd**2)
        arg_tan = gamma * (lmbd + np.tan(theta/2))
        arg_exp = 2*lmbd*gamma * (np.arctan(arg_tan) - np.pi/2)
        N = lmbd * np.exp(arg_exp)
        D = (1 + lmbd*np.sin(theta))**2 * (1 - np.exp(- 2*np.pi*lmbd*gamma))

        return N / D

    elif lmbd > 1:
        gamma = np.sqrt(lmbd**2 - 1)
        theta_plus = 2 * np.arctan(-lmbd + gamma)

        def foo(theta):
            n = np.tan(theta/2) + lmbd - gamma
            d = np.tan(theta/2) + lmbd + gamma
            N = lmbd * np.power(n/d, lmbd/gamma)
            D = (1 + lmbd * np.sin(theta))**2

            return N / D

        return np.where(theta > theta_plus, foo(theta), 0)

    else:
        print("You're out of luck, mi amigo!")


class Spin:


    def __init__(self, omegaS, dt, lmbd):
        self.omegaS = omegaS
        self.dt = dt
        self.lmbd = lmbd

        self.alpha = 4 * omegaS * lmbd
        self.HS = omegaS * qutip.sigmax()
        spin1 = qutip.basis(2, 1)
        projector1 = spin1 * spin1.dag()
        self.e1 = self.alpha * self.dt * projector1
        self.U_eff = qutip.qeye(2) - 1.j * (self.HS - 1.j * self.alpha * projector1 / 2) * dt
        self.rng = np.random.default_rng()


    def click_probability(self, state):
        return self.e1.overlap(state)


    def step(self, state):
        r = self.rng.random()
        click = r < self.click_probability(state)
        if click:

            return qutip.basis(2, 1)
        
        else:
            state_dt = self.U_eff * state

            return state_dt.unit()


    def run(self, state0, T):
        trajectory = [state0]
        state = state0
        for i, t in enumerate(np.arange(0, T + self.dt, self.dt)):
            state_dt = self.step(state)
            trajectory.append(state_dt)
            state = state_dt

        return trajectory
