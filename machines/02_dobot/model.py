import time

import numpy as np
import pybullet as pb
import pybullet_data as pb_data
import cv2
from PIL import Image
import os

from camera import Camera
import pickle

np.set_printoptions(suppress=True)

p = pb

physicsClient = pb.connect(pb.GUI)
pb.setAdditionalSearchPath(pb_data.getDataPath())

checker = pb.loadURDF(
    "checker.urdf",
    basePosition=[0, 0, 0.001],
    baseOrientation=p.getQuaternionFromEuler([np.pi / 2, 0, 0]),
    globalScaling=0.2,
    useFixedBase=True
)
_ = pb.loadURDF(
    "black.urdf",
    basePosition=[0, 0, 0],
    baseOrientation=p.getQuaternionFromEuler([np.pi / 2, 0, 0]),
    globalScaling=0.25,
    useFixedBase=True
)
robot = pb.loadURDF(
    "dobot.urdf", 
    basePosition=[0, +0.3, 0],
    baseOrientation=[0, 0, -1, 0],
    useFixedBase=1
)
pb.setTimeStep(0.01)  # no idea what this does
pb.setRealTimeSimulation(0)  # to iterate normally

def inv_with_limits(robot_id, delta):
    base = np.array(pb.getBasePositionAndOrientation(robot)[0])
    coords = pb.calculateInverseKinematics(robot_id, 3, targetPosition=base + delta)
    coords = np.array(coords)
    coords[3] = coords[2] - coords[1]
    return coords


cam = Camera()

def transform_vector(robot_id, vec):
    vec = np.array(vec)
    rot = np.array(pb.getMatrixFromQuaternion(pb.getLinkState(robot_id, 3)[1])).reshape(3, 3)
    return np.dot(rot, vec)

def get_pos_data(robot_id, link):
    if link == "base":
        pos, orient = pb.getBasePositionAndOrientation(robot_id)
    else:
        pos, orient = pb.getLinkState(robot_id, link)[: 2]
    orient = np.reshape(pb.getMatrixFromQuaternion(orient), (3, 3))
    return np.array(pos), orient

def get_twist(R, p):
    return np.block([[R, p.reshape(-1, 1)], [0] * len(p) + [1]])

def get_inv_twist(R, p):
    return np.block([[R.T, -R.T@p.reshape(-1, 1)], [0] * len(p) + [1]])

end_effector_poses = []
cam_to_checker = []
base_pos, base_orient = get_pos_data(robot, "base")
deltas = [[.4, -.4, .1], [-.3, -.4, .1], [.2, -.3, .1], [.3, -.3, .15]]
    
for i, delta in enumerate(deltas):
    dest = inv_with_limits(robot, delta)
    print(dest)
    for joint, val in enumerate(dest):
        pb.resetJointState(robot, joint, val)
        
    ef_pos, ef_orient  = get_pos_data(robot, 3)
    
    end_effector_poses.append(get_inv_twist(base_orient, base_pos) @ get_twist(ef_orient, ef_pos))
    last_twist = end_effector_poses[-1]
    # print(np.dot(get_twist(base_orient, base_pos),
    #              np.dot(last_twist, [.1, 0, 0, 1])), ef_pos)
    
    cam.set_pos(
        pb.getLinkState(robot, 3)[0],
        transform_vector(robot, [-1, 0, 0]),
        transform_vector(robot, [.4, -1, .1]),
    )
    frame = cam.get_frame()
    # input()
    
cam.calibrate()
for frame in cam.captured_images:
    img, rvec, tvec = cam.process_charuko(frame)
    cam_to_checker.append((rvec, tvec))
    
    while True:
        cv2.imshow("window", img)
        key = cv2.waitKey(1)
        
        if key == ord('q'):
            break
        if key == ord('w'):
            cv2.destroyAllWindows()
            exit()
            
with open("charuco_1/poses.pickle", "wb") as f:
    pickle.dump({"base_to_end": end_effector_poses, "cam_to_checker": cam_to_checker}, f)
    
cam.save("charuco_1")
