import numpy as np
import qutip


class DimerStages():
    def __init__(self, HS, POVM, dt):
        self.HS = HS
        self.POVM = POVM
        self.dt = dt
        self.e_ops = self.compute_E_ops()
        self.H_eff = self.compute_H_eff()
        self.rng = np.random.default_rng()


    def compute_H_eff(self):
        H_eff = self.HS
        for E in self.e_ops:
            H_eff -= 1j/2 * E 

        return H_eff


    def compute_E_ops(self):
        e_ops = []
        for M in self.POVM:
            e_ops.append(M.dag() * M)

        return e_ops


    def compute_click_probs(self, state):
        probs = np.empty(len(self.POVM))
        for i, E in enumerate(self.e_ops):
            probs[i] = self.dt * E.overlap(state)

        return probs


    def no_click_step(self, state):
        U_eff = qutip.qeye( [2, 2] ) - 1j * self.dt * self.H_eff
        state_dt = U_eff * state

        return state_dt.unit()
        

    def run_step(self, state, force_no_click=False):
        if force_no_click:
            return self.no_click_step(state)
        
        else:
            r = self.rng.random()
            click_probs = self.compute_click_probs(state)
            for i, cum_prob in enumerate(np.cumsum(click_probs)):
                if r < cum_prob:
                    state_dt = self.POVM[i] * state

                    return state_dt.unit()
            
            return self.no_click_step(state)
            

    def run(self, state0, T, force_no_click=False):
        trajectory = [state0]
        state = state0

        for t in np.arange(0, T+self.dt, self.dt):
            state_dt = self.run_step(state, force_no_click)
            trajectory.append(state_dt)
            state = state_dt

        return trajectory