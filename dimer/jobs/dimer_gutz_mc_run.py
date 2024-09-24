import numpy as np
import dimer_gutz_mc_config as c
from qze.dimer_gutz_mc import DimerGutzMCParameters, DimerGutzMc
from pickle import dump
import concurrent.futures


def run_simulation(sp):
    
    dgmc = DimerGutzMc(sp.dt, sp.lmbd_1, sp.lmbd_2, sp.omega_S)
    walk_pos = dgmc.evolve(sp.T, sp.walk_pos0)
    # The following is the right way to periodicise. The more naiive ways fail.
    # The way to see it is the fact that edges always collapse to the left.
    # If we want them to collapse to the right we have to mirror the calculation twice.
    walk_pos = -((-walk_pos+np.pi) % (2*np.pi) - np.pi)

    f = open(f"data/{str(sp)}.pkl", "wb")
    dump([sp, walk_pos], f)
    f.close()

    print(f"Simulation #{str(sp)} finished successfully.")


if __name__ == "__main__":
    import sys

    sim_list = [DimerGutzMCParameters(c.omega_S,
                                      lmbd_1,
                                      lmbd_2,
                                      c.walk_pos0,
                                      c.dt,
                                      c.T,
                                      c.nwalk,
                                      simid)
                for (lmbd_1, lmbd_2) in c.lambdas
                for simid in range(c.Nsim)]

    if len(sys.argv) == 1:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(run_simulation, sim_list)

    elif sys.argv[1] == '--debug':
        print('Running a single simulation for debugging purposes.')
        run_simulation(sim_list[0])
    
    else:
        print('Invalid options. Try again.')