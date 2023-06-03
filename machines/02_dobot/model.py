import time

import numpy as np
import pybullet as pb
import pybullet_data as pb_data
import cv2
from PIL import Image
import os

from camera import Camera

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

if not os.path.exists("./charuco/"):
    os.mkdir("./charuco/")
    
for i, delta in enumerate([[0, -.5, .1], [-.3, -.4, .1], [.3, -.4, .1]]):
    dest = inv_with_limits(robot, delta)
    print(dest)
    for joint, val in enumerate(dest):
        pb.resetJointState(robot, joint, val)
    # move(robot, dest)
    
    cam.set_pos(
        pb.getLinkState(robot, 3)[0],
        transform_vector(robot, [-1, 0, 0]),
        transform_vector(robot, [.1, -1, .1]),
    )
    frame = cam.get_frame()
    pb.stepSimulation()
    time.sleep(1/240)
cam.calibrate()
for frame in cam.captured_images:
    img = cam.process_charuko(frame)
    while True:
        cv2.imshow("window", img)
        key = cv2.waitKey(1)
        
        if key == ord('q'):
            break
        if key == ord('w'):
            cv2.destroyAllWindows()
            exit()
    
# cv2.imwrite(f"charuco/charuco_{i}.png", frame)
