import dimer_config as c
import dimer
import many_zeno
import dimer_gutzwiller
from pickle import dump
import concurrent.futures


def run_simulation(sp):
    if sp.solver == "mcsolve":
        results = many_zeno.mcsolve(sp.H_S,
                                    sp.psi0,
                                    sp.t_eval,
                                    sp.c_ops,
                                    sp.ntraj)

    elif sp.solver == "trsolve":
        results = many_zeno.trsolve(sp.H_S,
                                    sp.psi0,
                                    sp.dt,
                                    sp.t_eval,
                                    sp.c_ops,
                                    sp.ntraj,
                                    sp.no_click)
        
    elif sp.solver == "gutzwiller":
        results = dimer_gutzwiller.gusolve(sp.H_S,
                                           sp.psi0,
                                           sp.dt,
                                           sp.t_eval,
                                           sp.c_ops,
                                           sp.ntraj,
                                           sp.no_click)
    

    f = open(f"data/{str(sp)}.pkl", "wb")
    dump([sp, results], f)
    f.close()

    print(f"Sumulation #{str(sp)} finished successfully.")


if __name__ == "__main__":
    sim_list = dimer.get_sim_list(c.lmbd_1_list,
                                  c.lmbd_2_list,
                                  c.omega_S_list,
                                  c.psi0_list,
                                  c.t_eval_list,
                                  c.ntraj_list,
                                  c.dt_list,
                                  c.solver,
                                  c.no_click)
    

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(run_simulation, sim_list)

    # run_simulation(sim_list[0])