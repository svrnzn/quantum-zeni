import numpy as np
import qutip
import pickle
import stages

# lmbd = .7
# lmbd = 1.1
# lmbd = 2 / np.sqrt(3)
# lmbd = 1.5
lmbd = 3
Nt = 5 * 10**3
T = 10
omega0 = 1
dt = .01

f = open(f"data/lambda={lmbd}-Nt={Nt}T={T}-dt={dt}-omega0={omega0}.pkl", "rb")
states_infty = pickle.load(f)
f.close()

def state_to_theta(state):
    rho = state * state.dag()
    y = 2 * rho[1, 0].imag
    z = (rho[0, 0] - rho[1, 1]).real
    theta = np.arctan2(y, z)
    
    return theta

thetas = []
for state in states_infty:
    thetas.append(state_to_theta(state))

import matplotlib.pyplot as plt


plt.style.use(["./config/stylelib/thesis.mplstyle", "./config/stylelib/manuscript_fullwidth.mplstyle"])

counts, bins = np.histogram(thetas, 36)
bin_width = bins[1] - bins[0]
freqs = counts / Nt / bin_width

plt.plot(bins[:-1] + bin_width/2, freqs, ".", label=r"MC")
plt.plot(np.arange(-np.pi, np.pi, .01), stages.p_infty(lmbd, np.arange(-np.pi, np.pi, .01)), label=r"Analitical")

plt.xlim((-np.pi, np.pi))
xticks = [-np.pi, -np.pi/2, 0, np.pi/2, np.pi]
xlabels = [r"$-\pi$", r"$-\pi/2$", r"$0$", r"$\pi/2$", r"$\pi$"]
plt.xticks(xticks, xlabels)
plt.xlabel(r"$\theta$")
plt.ylabel(r"$P_\infty(\theta)$")
plt.legend()

plt.tight_layout()

plt.savefig(f"plots/lambda={lmbd}-Nt={Nt}T={T}-dt={dt}-omega0={omega0}.pdf")
