import numpy as np


def thetas_flow(t_l, t_r, lmbd_1, lmbd_2, omega_S=1):
    flow = -2*omega_S * (1 + np.outer((lmbd_1 + lmbd_2*np.sin(t_r/2)**2), np.sin(t_l)))    

    return flow


def flow_potential(t_l, t_r, lmbd_1, lmbd_2):
    fir = 2 * (t_l + t_r)
    sec = - (2*lmbd_1 + lmbd_2) * np.cos(t_l)
    thi = - (2*lmbd_1 + lmbd_2) * np.cos(t_r)
    fou = lmbd_2 * np.cos(t_l) * np.cos(t_r)

    return fir + sec + thi + fou


def flow_potential_diag(t, lmbd_1, lmbd_2):

    return flow_potential(t, t, lmbd_1, lmbd_2)


def flow_potential_hessian(t_l, t_r, lmbd_1, lmbd_2):
    h00 = ((2*lmbd_1 + lmbd_2) * np.cos(t_l)
           - lmbd_2 * np.cos(t_l) * np.cos(t_r))
    h01 = lmbd_2 * np.sin(t_l) * np.sin(t_r)
    h10 = h01
    h11 = ((2*lmbd_1 + lmbd_2) * np.cos(t_r)
           - lmbd_2 * np.cos(t_l) * np.cos(t_r))
    H = np.array([[h00, h01], [h10, h11]])

    return H


def omegal(lamb1, lamb2, tl, tr):
        out = 2 * (1 + (lamb1 + lamb2*np.sin(tr/2)**2) * np.sin(tl))
        
        return out
    

def f_dimer(lamb1, lamb2, tl, tr):
    oml = omegal(lamb1, lamb2, tl, tr)
    omr = omegal(lamb1, lamb2, tr, tl)

    return -np.array([oml, omr])