import stages_gutzwiller as stages
import qutip
import pickle
import concurrent.futures
import stages_gutzwiller_config as config


def run_simulation(params):
    params.force_no_click = True
    params.state0 = qutip.basis(2, 1)
    spin = stages.Spin(params.omegaS, params.dt, params.lmbd)
    nc_trajectory = spin.run(params.state0, params.T, params.force_no_click)

    f = open(f"data/no-click-gutzwiller-lambda={params.lmbd}-T={params.T}-dt={params.dt}-omega0={params.omegaS}.pkl", "wb")
    pickle.dump([params, nc_trajectory], f)
    f.close()


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(run_simulation, config.sim_list)

# run_simulation(config.sim_list[0])