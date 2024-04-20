import qutip
import pickle
import concurrent.futures
import multi_stages_mcsolve_config as config


def run_simulation(params):
    results = qutip.mcsolve(params.HS, params.state0, [0, params.T], params.POVM, ntraj=params.Nt)

    f = open(f"data/mcsolve-Ns={params.Ns}-lambda={params.lmbd}-Nt={params.Nt}-T={params.T}-dt={params.dt}.pkl", "wb")
    pickle.dump([params, results], f)
    f.close()


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(run_simulation, config.sim_list)

# run_simulation(config.sim_list[0])
