import numpy as np
import dimer_gutzwiller_mc_config as c
from qze.dimer_gutzwiller_mc import DimerGutzwillerMCParameters, DimerGutzwillerMc
from pickle import dump
import concurrent.futures


def run_simulation(sp):
    
    dgmc = DimerGutzwillerMc(sp.dt, sp.lmbd_1, sp.lmbd_2, sp.omega_S)
    walk_pos = dgmc.evolve(sp.T, sp.walk_pos0)
    # The following is the right way to periodicise. The more naiive ways fail.
    # The way to see it is the fact that edges always collapse to the left.
    # If we want them to collapse to the right we have to mirror the calculation twice.
    walk_pos = -((-walk_pos+np.pi) % (2*np.pi) - np.pi)

    f = open(f"data/{str(sp)}.pkl", "wb")
    dump([sp, walk_pos], f)
    f.close()

    print(f"Sumulation #{str(sp)} finished successfully.")


if __name__ == "__main__":
    sim_list = [DimerGutzwillerMCParameters(c.omega_S,
                                            lmbd_1,
                                            lmbd_2,
                                            c.walk_pos0,
                                            c.dt,
                                            c.T,
                                            c.nwalk)
                for lmbd_1, lmbd_2 in c.lambdas]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(run_simulation, sim_list)

    # run_simulation(sim_list[0])