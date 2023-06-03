import time

import numpy as np
import pybullet as pb
import pybullet_data as pb_data
import cv2
from PIL import Image

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

def move(robot_id, coords):
    coords = np.array(coords)
    coords[3] = coords[2] - coords[1]

    pb.setJointMotorControlArray(
        robot_id,
        np.arange(4),
        targetPositions=coords,
        controlMode=pb.POSITION_CONTROL
    )

cam = Camera()
base = np.array(pb.getBasePositionAndOrientation(robot)[0])

def transform_vector(robot_id, vec):
    vec = np.array(vec)
    rot = np.array(pb.getMatrixFromQuaternion(pb.getLinkState(robot_id, 3)[1])).reshape(3, 3)
    return np.dot(rot, vec)

dest = pb.calculateInverseKinematics(
    robot, 
    3, 
    targetPosition=base + [-.3, -.4, .1]
)
print(dest)
move(robot, dest)
draw_frame = 1
print()
while True:
    cam.set_pos(
        pb.getLinkState(robot, 3)[0],
        transform_vector(robot, [-1, 0, 0])
    )
    frame = cam.get_frame()
    img = cam.get_arucos(frame)
    
    if draw_frame:
        cv2.imshow("window", img)
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        cam.get_arucos(cam.get_frame(), True)
        draw_frame = 0
    if key == ord('w'):
        break
    pb.stepSimulation()
    time.sleep(1/240)
cv2.destroyAllWindows()