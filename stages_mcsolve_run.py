import qutip
import pickle
import concurrent.futures
import stages_mcsolve_config as config


def run_simulation(params):
    results = qutip.mcsolve(params.HS, params.state0, [0, params.T], params.POVM, ntraj=params.Nt,
                            options={'store_states' : False,
                                     'store_final_state' : True,
                                     'keep_runs_results' : True,
                                    #  'map' : map,
                                     'norm_steps' : 10})

    f = open(f"data/mcsolve-lambda={params.lmbd}-Nt={params.Nt}-T={params.T}-dt={params.dt}-omega0={params.omegaS}.pkl", "wb")
    pickle.dump([params, results], f)
    f.close()


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(run_simulation, config.sim_list)

# run_simulation(config.sim_list[0])
