import numpy as np
import qutip
from dataclasses import dataclass


@dataclass
class MZTrotterResult:
    states : list[list[qutip.Qobj]]


class ManyZeno():


    def __init__(self, H_S, c_ops):
        self.H_S = H_S
        self.c_ops = c_ops
    

class ManyZenoMcsolve(ManyZeno):


    def __init__(self, H_S, c_ops):
        super().__init__(H_S, c_ops)


    def run(self, psi0, tlist, ntraj):
        return qutip.mcsolve(self.H_S,
                             psi0,
                             tlist,
                             self.c_ops,
                             ntraj=ntraj,
                             options={"keep_runs_results" : True,
                                      "norm_steps" : 10})


class ManyZenoTrotter(ManyZeno):


    def __init__(self, H_S, c_ops, dt):
        super().__init__(H_S, c_ops)
        self.dt = dt
        self.e_ops = self.compute_e_ops()
        self.H_eff = self.compute_H_eff()
        self.rng = np.random.default_rng()


    def compute_e_ops(self):
        e_ops = []
        for M in self.c_ops:
            e_ops.append(M.dag() * M)

        return e_ops


    def compute_H_eff(self):
        H_eff = self.H_S
        for E in self.e_ops:
            H_eff -= 1j/2 * E

        return H_eff


    def compute_click_probs(self, state):
        probs = np.empty(len(self.c_ops))
        for i, E in enumerate(self.e_ops):
            probs[i] = self.dt * E.overlap(state).real

        return probs


    def no_click_step(self, state):
        U_eff = qutip.qeye_like(self.H_S) - 1j * self.dt * self.H_eff
        state_dt = U_eff * state

        return state_dt.unit()
        

    def run_step(self, state, no_click=False):
        if no_click:
            return self.no_click_step(state)
        
        else:
            r = self.rng.random()
            click_probs = self.compute_click_probs(state)
            for i, cum_prob in enumerate(np.cumsum(click_probs)):
                if r < cum_prob:
                    state_dt = self.c_ops[i] * state

                    return state_dt.unit()
            
            return self.no_click_step(state)
            

    def run(self, psi0, tlist, no_click=False):
        state = psi0
        traj = len(tlist) * [psi0]
        t_idx = 0
        if np.isclose(0, tlist[0]):
            traj[0] = state
            t_idx += 1
        for i, t in enumerate(np.arange(0, tlist[-1]+self.dt/2, self.dt)):
            if np.isclose(t, tlist[t_idx]):
                traj[t_idx] = state
                t_idx += 1

            state_dt = self.run_step(state, no_click)
            state = state_dt

        return traj
    

def trsolve(H_S, psi0, dt, tlist, c_ops, ntraj=500, no_click=False):
    mzt = ManyZenoTrotter(H_S, c_ops, dt)
    results = ntraj * [len(tlist) * [psi0]]
    for i in range(ntraj):
        traj = mzt.run(psi0, tlist, no_click)
        results[i] = traj
        print(f"Trajectory #{i+1} of {ntraj} computed.")

    output = MZTrotterResult(results)

    return output


def mcsolve(H_S, psi0, tlist, c_ops, ntraj=500):
    mzm = ManyZenoMcsolve(H_S, c_ops)
    results = mzm.run(psi0, tlist, ntraj)

    return results