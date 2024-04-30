import pickle
import concurrent
import dimer_stages_myte_config as config
# import dimer_no_click_config as config
import dimer_stages_myte as ds


def run_simulation(params):
    dimer = ds.DimerStages(params.HS, params.POVM, params.dt)
    trajectories = []

    t_steps = int(params.T / params.dt)
    del_t_steps = int(t_steps/2/100)

    for i in range(params.Nt):
        traj = dimer.run(params.state0, params.T, params.force_no_click)
        if params.force_no_click:
            trajectories.append(traj)
        else:
            trajectories.append(traj[int(t_steps/2)::del_t_steps])

        print(f"Trajectory #{i+1} of {params.Nt} computed.")

    f = open(f"data/dimer-myte-lmbd_1={params.lmbd_1:.1f}-lmbd_2={params.lmbd_2:.1f}-Nt={params.Nt}-T={params.T}-dt={params.dt}-no_click={params.force_no_click}.pkl", "wb")
    pickle.dump([params, trajectories], f)
    f.close()


# with concurrent.futures.ProcessPoolExecutor() as executor:
#     executor.map(run_simulation, config.sim_list)

run_simulation(config.sim_list[0])