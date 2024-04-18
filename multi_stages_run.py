import multi_stages as ms
import pickle
import concurrent.futures
import multi_stages_config as config


def run_simulation(params):
    spins = ms.Spins(params.Ns, params.HS, params.POVM, params.dt)
    states_infty = []
    for i in range(params.Nt):
        states_infty.append(spins.run(params.state0, params.T)[-1])
        if (i+1) % 10 == 0:
            print(f"Trajectory #{i+1} computed.")
        # print(f"Trajectory #{i+1} computed.")

    f = open(f"data/Ns={params.Ns}-lambda={params.lmbd}-Nt={params.Nt}T={params.T}-dt={params.dt}.pkl", "wb")
    pickle.dump([params, states_infty], f)
    f.close()


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(run_simulation, config.sim_list)

# run_simulation(config.sim_list[0])
