from dataclasses import dataclass
import numpy as np


@dataclass
class DimerGutzMCParameters:
    omega_S : float
    lmbd_1 : float
    lmbd_2 : float
    walk_pos0 : np.array
    dt : float
    T : np.array
    nwalk : int
    simid : int


    def __str__(self):
        f_name = ("dimer-"
                  f"solver=gutz-mc-"
                  f"omega_S={self.omega_S:.2f}-"
                  f"lmbd_1={self.lmbd_1:.2f}-"
                  f"lmbd_2={self.lmbd_2:.2f}-"
                  f"dt={self.dt}-"
                  f"T={self.T}-"
                  f"nwalk={self.nwalk}-"
                  f"simid={self.simid}")
        
        return f_name


class DimerGutzMc():


    def __init__(self, dt, lmbd_1, lmbd_2, omega_S=1):
        self.dt = dt
        self.lmbd_1 = lmbd_1
        self.lmbd_2 = lmbd_2
        self.omega_S = omega_S
        self.rng = np.random.default_rng()


    def click_prob_1(self, th):
        cp = self.dt*4*self.omega_S*self.lmbd_1 * np.sin(th/2)**2

        return cp


    def click_prob_2(self, tl, tr):
        cp = (self.dt*4*self.omega_S*self.lmbd_2
              * np.sin(tl/2)**2 * np.sin(tr/2)**2)

        return cp


    def unitary_drift(self, walk_pos):
        return walk_pos - 2*self.omega_S*self.dt


    def m0_drift(self, walk_pos):
        tl, tr = walk_pos

        # Compute drifts.
        dl = (self.lmbd_1 + self.lmbd_2*np.sin(tr/2)**2) * np.sin(tl) * self.dt
        dr = (self.lmbd_1 + self.lmbd_2*np.sin(tl/2)**2) * np.sin(tr) * self.dt

        drift = - 2 * self.omega_S * np.array([dl, dr])

        return walk_pos + drift


    # def drift(self, walk_pos):
    #     '''Runge-Kutta'''
    #     tl = walk_pos[:, 0]
    #     tr = walk_pos[:, 1]
    #     k1 = -self.f_dimer(tl, tr)
    #     k2 = -self.f_dimer(tl + self.dt*k1[0]/2, tr + self.dt*k1[1]/2)
    #     k3 = -self.f_dimer(tl + self.dt*k2[0]/2, tr + self.dt*k2[1]/2)
    #     k4 = -self.f_dimer(tl + self.dt*k3[0], tr + self.dt*k3[1])
    #     output = walk_pos.T + self.dt/6 * (k1 + 2*k2 + 2*k3 + k4)

    #     return output.T


    def evolve(self, t, walk_pos0):
        walk_pos = walk_pos0
        for i in range(int(t/self.dt)):
            walk_pos = self.unitary_drift(walk_pos)
            tl = walk_pos[:, 0]
            tr = walk_pos[:, 1]
            cp_l = self.click_prob_1(tl)
            cp_r = self.click_prob_1(tr)
            cp_2 = self.click_prob_2(tl, tr)
            rs = self.rng.random(len(walk_pos))
            clicks_l = rs < cp_l
            clicks_r = np.logical_and(rs > cp_l, rs < cp_l + cp_r)
            clicks_2 = np.logical_and(rs > cp_l + cp_r, rs < cp_l + cp_r + cp_2)
            for j, (cl, cr, c2) in enumerate(zip(clicks_l, clicks_r, clicks_2)):
                if cl:
                    walk_pos[j, 0] = np.pi
                elif cr:
                    walk_pos[j, 1] = np.pi
                elif c2:
                    walk_pos[j] = np.pi * np.ones(2)
                else: # Apply M0
                    walk_pos[j] = self.m0_drift(walk_pos[j])

            if (i+1) % 100 == 0:
                print(f'Step #{i+1} of {int(t/self.dt)} completed.')

        return walk_pos


if __name__ == "__main__":
    nwalk = 1000
    T = 10
    dt = .01
    lmbd_1 = .7
    lmbd_2 = .7
    omega_S = 1

    walk_pos0 = np.array(nwalk * [[np.pi, np.pi]])

    dgmc = DimerGutzMc(dt, lmbd_1, lmbd_2)

    walk_pos = dgmc.evolve(T, walk_pos0)
    print(walk_pos)