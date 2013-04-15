import sys
sys.path.append('../..')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnStand
from SimulationKit.helpers import *
import time
from forward_kinematics import *
from inverse_kinematics import *
from joint_control import *
from trajectory import *

from math import *

d = {'offset': (0, 0, 0.67)}
s = Simulator(dt=1e-3,
              plane=1,
              pave=0,
              graphical=1,
              robot=LegOnStand,
              robot_kwargs=d,
              start_paused=True)

# Put up the goal posts
wickets = []
static_geoms = []
row_n = 6
x_off = .5
y_off = .5
i = 0
# Rack up the pins
for i in range(row_n):
    for j in range(i + 1):
        body, geom = s.createCapsule(mass=1.0e1,
                                     length=1.0,
                                     radius=0.1,
                                     pos=(i * x_off, -5.0 - y_off * j + i * (y_off / 2), 0.7))
        wickets.append(body)
        static_geoms.append(geom)

yaw_joint = s.robot.members['hip_yaw']
pitch_joint = s.robot.members['hip_pitch']
knee_joint = s.robot.members['knee_pitch']
shock_joint = s.robot.members['foot_shock']

# def jointAnglesFromFootPosition( hip_yaw_angle, hip_pitch_angle, knee_angle, robot ):
# def footPositionFromJointAngles( foot_x, foot_y, foot_z, robot ):
# class Trajectory:
#     def __init__( self, start_foot_pos, target_foot_pos, robot, start_sim_t, end_sim_t ):
#     def getTargetJointAngles( self, sim_t ):

state = 0
yaw_control = JointController(yaw_joint)
pitch_control = JointController(pitch_joint)
knee_control = JointController(knee_joint)

while True:
    start_t = s.getSimTime()

    shock_depth = shock_joint.getPosition()
    pos = footPositionFromJointAngles(yaw_joint.getAngle(), pitch_joint.getAngle(), knee_joint.getAngle(), shock_depth, s.robot)
    print "state", state
    print "start", pos
    print "shock", shock_depth

    if state == 0:
        target_pos = (pos[0], pos[1], -4.0)
        end_t = start_t + 4

    elif state == 1:
        target_pos = (pos[0], pos[1], pos[2] - shock_depth + 1.25)
        end_t = start_t + 1

    elif state == 2:
        target_pos = (1.2, -1.0, pos[2])
        end_t = start_t + 2

    elif state == 3:
        target_pos = (1.2, -1.0, -4.0)
        end_t = start_t + 1

    elif state == 4:
        target_pos = (1.2, 1.0, pos[2])
        end_t = start_t + 2

    print target_pos, start_t, end_t
    traj = Trajectory(pos, target_pos, s.robot, start_t, end_t)

    while True:
        s.step()

        sim_t = s.getSimTime()
        shock_depth = shock_joint.getPosition()
        #print "state", state, "shock", shock_depth
        if state == 0 or state == 3:
            if shock_depth <= -0.05:
                break
        else:
            if sim_t >= end_t:
                break
                
        #print yaw_joint.getAngle(), pitch_joint.getAngle(), knee_joint.getAngle()
        step_pos = traj.getTargetJointAngles(sim_t)
        #print sim_t, step_pos
        yaw_angle, pitch_angle, knee_angle = jointAnglesFromFootPosition(step_pos, shock_depth, s.robot)
        #print yaw_angle, pitch_angle, knee_angle

        yaw_control.updateJoint(sim_t, yaw_angle)
        pitch_control.updateJoint(sim_t, pitch_angle)
        knee_control.updateJoint(sim_t, knee_angle)

    if state == 4:
        state = 1
    else:
        state += 1
