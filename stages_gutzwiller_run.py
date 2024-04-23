import stages_gutzwiller as stages
import pickle
import concurrent.futures
import stages_gutzwiller_config as config


def run_simulation(params):
    spin = stages.Spin(params.omegaS, params.dt, params.lmbd)
    states_infty = []
    for i in range(params.Nt):
        states_infty.append(spin.run(params.state0, params.T)[-1])
        # if i+1 % 10 == 0:
        #     print(f"Trajectory #{i+1} computed.")
        print(f"Trajectory #{i+1} computed.")

    f = open(f"data/gutzwiller-lambda={params.lmbd}-Nt={params.Nt}T={params.T}-dt={params.dt}-omega0={params.omegaS}.pkl", "wb")
    pickle.dump([params, states_infty], f)
    f.close()


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(run_simulation, config.sim_list)

# run_simulation(config.sim_list[0])