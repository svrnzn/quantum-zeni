# %%
import numpy as np
import qutip
import dimer
import matplotlib.pyplot as plt

# %%
# Statistics
ntraj = 10**7

# Physical parameters.
lambdas = [[.25, 1.75]]

omega_S = 1
dt = 0.01
T = 20
t_eval = np.array([0, T])

# solver = "trsolve"
solver = "mcsolve"
# solver = "gutzwiller"

store_states = False
compute_eentropy = False
compute_fidelity = False

no_click = False

psi0 = qutip.tensor(qutip.basis(2, 1), qutip.basis(2, 1))

# %%
sim_list = dimer.get_sim_list(lambdas,
                              omega_S,
                              psi0,
                              t_eval,
                              ntraj,
                              dt,
                              solver,
                              no_click)

# %%
data = []

for sim in sim_list:
    f = open(f"data/{str(sim)}.npz", "rb")
    data.append(np.load(f))
    # f.close()

# %%
# plt.style.use(["./config/stylelib/thesis.mplstyle", "./config/stylelib/manuscript_grid_1x3.mplstyle"])

bins = 72
binning_range = [[-np.pi, np.pi], [-np.pi, np.pi]]
ticks = np.linspace(-np.pi, np.pi, 3)
# tick_labels = [r"$-\pi$", r"$0$", r"$\pi$"]

fig, ax = plt.subplots()
for i, sim in enumerate(sim_list):
    tl = data[i]['bloch_coords'][:-1,0,1]
    tr = data[i]['bloch_coords'][:-1,1,1]
    
    ax.hist2d(tl, tr,
                  density=True,
                  range=binning_range,
                  bins=bins,
                  norm="log")
    ax.set_xticks(ticks)
    # axs[i].set_xticklabels(tick_labels)
    ax.set_yticks(ticks)
    # axs[i].set_yticklabels(tick_labels)
    # axs[i].set_title(rf"$\lambda_1 = {sim.lmbd_1}$, $\lambda_2 = {sim.lmbd_2}$")
    # axs[i].set(xlabel=r"$\theta_\mathrm{L}$", ylabel=r"$\theta_\mathrm{R}$")
    ax.set(aspect='equal')

# Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axs.flat:
#     ax.label_outer()

plt.savefig("dimer-full-p-infty-mc.pdf")
