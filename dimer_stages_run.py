import qutip
import pickle
import concurrent
import dimer_stages_config as config


def run_simulation(params):
    trajectories = qutip.mcsolve(params.HS,
                                 params.state0,
                                 params.t_eval,
                                 params.POVM,
                                 ntraj=params.Nt)
    
    f = open(f"data/dimer-check-lmbd_1={params.lmbd_1:.1f}-lmbd_2={params.lmbd_2:.1f}-Nt={params.Nt}-T={params.T}-dt={params.dt}.pkl", "wb")
    pickle.dump([params, trajectories], f)
    f.close()


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(run_simulation, config.sim_list)

# run_simulation(config.sim_list[0])