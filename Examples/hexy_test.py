import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import Hexy
import time

d = {'offset': (0, 0, 20e-2)}
s = Simulator(dt=0,
              plane=1,
              pave=0,
              graphical=1,
              robot=Hexy,
              robot_kwargs=d)

last_t = time.time()

rad2deg = 180. / 3.14159


def updateServo(j):
    j.servo.setPos(degrees=(j.servo_mult * rad2deg * j.getAngleTarget()) + j.servo_offset)

while True:
    s.step()
    s.robot.constantSpeedWalk()
    if time.time() - last_t > 50e-3:
        updateServo(s.robot.legs[0]['hip_yaw'])
        updateServo(s.robot.legs[0]['hip_pitch'])
        updateServo(s.robot.legs[0]['knee_pitch'])
        updateServo(s.robot.legs[1]['hip_yaw'])
        updateServo(s.robot.legs[1]['hip_pitch'])
        updateServo(s.robot.legs[1]['knee_pitch'])
        updateServo(s.robot.legs[2]['hip_yaw'])
        updateServo(s.robot.legs[2]['hip_pitch'])
        updateServo(s.robot.legs[2]['knee_pitch'])
        updateServo(s.robot.legs[3]['hip_yaw'])
        updateServo(s.robot.legs[3]['hip_pitch'])
        updateServo(s.robot.legs[3]['knee_pitch'])
        updateServo(s.robot.legs[4]['hip_yaw'])
        updateServo(s.robot.legs[4]['hip_pitch'])
        updateServo(s.robot.legs[4]['knee_pitch'])
        updateServo(s.robot.legs[5]['hip_yaw'])
        updateServo(s.robot.legs[5]['hip_pitch'])
        updateServo(s.robot.legs[5]['knee_pitch'])
        last_t = time.time()
        time.sleep(1e-6)
        # Give the other threads some time to run
