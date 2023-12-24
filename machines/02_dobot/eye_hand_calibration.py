from itertools import combinations

import cv2
import numpy as np
import scipy.optimize as optimize

def get_board2base_transform(twists_base2endeffector, twists_board2camera):
    base_to_end = twists_base2endeffector
    cam_to_checker = twists_board2camera
    As = [t[np.ix_([0, 1, 3], [0, 1, 3])] for t in base_to_end]
    n = calc_normal(cam_to_checker)
    Bs = [get_B(twist, n) for twist in cam_to_checker]

    lefts, rights = [], []
    for i, j in combinations(np.arange(len(base_to_end)), 2):
        lefts.append((np.linalg.inv(As[j]) @ As[i])[:2])
        rights.append((Bs[j] @ np.linalg.inv(Bs[i])))
    print(np.linalg.det(lefts[0][:2, :2]), np.linalg.det(rights[0][:2, :2]))
        
    left = np.vstack(lefts)
    optim = optimize.minimize(solver, [0, 0, 0], args=(left, rights))
    print("tsnei", optim.x)
    return As[0] @ get_X(*optim.x) @ Bs[0]

def calc_normal(twists):
    return np.mean([twist[:3, 2] for twist in twists], axis=0)

def get_B(twist, n):
    r_vec = n + [0, 0, 1]
    r_vec = r_vec / np.linalg.norm(r_vec) * np.pi
    R1 = cv2.Rodrigues(r_vec)[0]

    B = np.block([[R1, np.zeros((3, 1))], [0, 0, 0, 1]]) @ twist
    return B[np.ix_([0, 1, 3], [0, 1, 3])]

def get_X(phi, dx, dy):
    return np.array([
        [np.cos(phi), -np.sin(phi), dx],
        [np.sin(phi), np.cos(phi), dy],
        [0, 0, 1]
    ])

def solver(x, left, rights):
    X = get_X(*x)
    l = left @ X
    r = np.vstack([(X @ right)[:2] for right in rights])
    delta = l - r
    loss = np.linalg.norm(delta[:, :2], "fro") * .01 + np.linalg.norm(delta[:, -1:], "fro")
    return loss

