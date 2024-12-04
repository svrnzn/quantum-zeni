import numpy as np
from qze import dimer
from qze import many_zeno
from qze import dimer_gutz_mc_qutip
import concurrent.futures
import dimer_config as c


def run_simulation(sp):
    if sp.solver == "mcsolve":
        results = many_zeno.mcsolve(sp.H_S,
                                    sp.psi0,
                                    sp.t_eval,
                                    sp.c_ops,
                                    sp.ntraj,
                                    map=c.mcsolve_map)

    elif sp.solver == "trsolve":
        results = many_zeno.trsolve(sp.H_S,
                                    sp.psi0,
                                    sp.dt,
                                    sp.t_eval,
                                    sp.c_ops,
                                    sp.ntraj,
                                    sp.no_click)
        
    elif sp.solver == "gutzwiller":
        results = dimer_gutz_mc_qutip.gusolve(sp.H_S,
                                              sp.psi0,
                                              sp.dt,
                                              sp.t_eval,
                                              sp.c_ops,
                                              sp.ntraj,
                                              sp.no_click)
    

    states = np.array(results.runs_final_states, dtype=object)

    # if sp.store_states:
    #     output['states'] = states

    print('Computing Bloch Sphere coordinates.')
    bloch_coords = dimer.state_to_yz_bloch(states)

    output = dict(simulation_parameters=sp,
                  bloch_coords=bloch_coords)

    if sp.solver == "mcsolve" or sp.solver == "trsolve":
        # if sp.compute_eentropy:
        print('Computing Entropy of Entanglement.')
        entropy_of_entanglement = dimer.entropy_of_entanglement(states)
        output['entropy_of_entanglement'] = entropy_of_entanglement

        # if sp.compute_fidelity:
        print('Computing Fidelity.')
        fidelity = dimer.fidelity(states)
        output['fidelity'] = fidelity


    # f = open(f"data/{str(sp)}.pkl", "wb")
    # dump(output, f)
    f = open(f"data/{str(sp)}.npz", "wb")
    np.savez(f,
             bloch_coords=bloch_coords,
             entropy_of_entanglement=entropy_of_entanglement,
             fidelity=fidelity)
    f.close()

    print(f"Simulation #{str(sp)} finished successfully.")


if __name__ == "__main__":
    import sys
    import dimer_config as c

    sim_list = dimer.get_sim_list(c.lambdas,
                                  c.omega_S,
                                  c.psi0,
                                  c.t_eval,
                                  c.ntraj,
                                  c.dt,
                                  c.solver,
                                  c.no_click,
                                  c.nsim)

    if len(sys.argv) == 1:
        with concurrent.futures.ProcessPoolExecutor(max_workers=c.max_workers) as executor:
            executor.map(run_simulation, sim_list)

    elif sys.argv[1] == '--debug':
        print('Running a single simulation for debugging purposes.')
        run_simulation(sim_list[-1])
    
    else:
        print('Invalid options. Try again.')