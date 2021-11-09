import DobotDllType as dType


class Robot:
    def __init__(self, dll_path):
        self.api = dType.load(dll_path)

    def connect(self):
        state = dType.ConnectDobot(self.api, "", 115200)[0]
        assert state == 0  # success code
        dType.SetQueuedCmdClear(self.api)
        dType.SetQueuedCmdStartExec(self.api)

    def disconnect(self):
        dType.DisconnectDobot(self.api)


class RobotCommunicator:
    def __init__(self, robot):
        self.robot = robot
        self.api = robot.api
        self.home_xyzr = (200, 0, 0, 0)

        dType.SetHOMEParams(self.api, *self.home_xyzr, isQueued=1)
        dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued=1)
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued=1)

    def move_xyz(self, xyz: list):
        dType.SetPTPCmd(
            self.api,
            dType.PTPMode.PTPMOVLXYZMode,
            xyz[0] + self.home_xyzr[0],
            xyz[1] + self.home_xyzr[1],
            xyz[2] + self.home_xyzr[2],
            0,
            isQueued=1
        )

    def clear_alarms(self):
        dType.ClearAllAlarmsState(self.api)
