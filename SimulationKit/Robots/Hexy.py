from SimulationKit.MultiBody import MultiBody
from SimulationKit.helpers import *
from Utilities.pubsub import *
import ode
import math
# import serial
import threading

debug = False


class serHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.ser = None

        self.sendQueue = []
        self.sendLock = threading.Lock()

        self.recieveQueue = []
        self.recieveLock = threading.Lock()

        self.serOpen = False
        self.serNum = 0
        self.setDaemon(True)
        self.start()

    def run(self):
        self.connect()
        if self.serOpen:
            if self.ser.writable:
                if self.serOpen:

                    while(True):
                    # send waiting messages
                        send = False
                        if(len(self.sendQueue) > 0):
                            toSend = self.sendQueue.pop(0)
                            send = True
                        if send:
                            self.ser.write(str(toSend))
                        else:
                            time.sleep(1e-6)

    def connect(self):
        # auto attach to controller
        self.serOpen = False
        for i in range(1, 100):
            try:
                try:
                    # ser = serial.Serial(i, baudrate=115200, timeout=1)
                    ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
                except:
                    raise Exception
                ser.flush()
                time.sleep(0.1)
                ser.write("VER\r")
                time.sleep(0.1)
                readReply = ser.read(5)
                if readReply == 'SSC32':
                    print "controller found at port:", i + 1
                    ser.flush()
                    self.ser = ser
                    print "connected to port", i + 1
                    self.serNum = i
                    self.serOpen = True
                    break
                else:
                    ser.close()
                    pass
            except:
                pass
        if not self.serOpen:
            print "no serial ports available, just showing graphical"


class Servo:
    def __init__(self, servoNum, serHandler, servoPos=1500, offset=0, active=True):
        self.serHandler = serHandler
        self.active = active
        self.servoNum = servoNum

        # servo position and offset is stored in microseconds (uS)
        self.servoPos = servoPos
        self.offset = offset


    def setPos(self, timing="None", degrees="None", move=True):

        if timing != "None":
            self.servoPos = timing
        if degrees != "None":
            self.servoPos = int(1500.0 + float(degrees) * 11.1111111)
        if move:
            self.active = True
            self.move()
            if debug:
                print "moved ", self.servoNum
        if debug:
            print "servo", self.servoNum, "set to", self.servoPos

    def getPosDeg(self):
        return (self.servoPos - 1500) / 11.1111111

    def getPosuS(self):
        return self.servoPos

    def getOffsetDeg(self):
        return (self.offset - 1500) / 11.1111111

    def getOffsetuS(self):
        return self.offset

    def setOffset(self, timing=1500, degrees=0.0):
        if timing != 1500:
            pass
        if degrees != 0.0:
            pass

    def reset(self):
        self.setPos(timing=1500)
        self.active = False
        self.move()

    def kill(self):
        self.active = False
        self.move()

    def move(self):
        if self.active:
            if debug:
                print "sending command #%dP%dT0 to queue" % (self.servoNum, int(self.servoPos))
            # send the message the serial handler in a thread-safe manner
            toSend = "#%dP%dT0\r" % (self.servoNum, int(self.servoPos))
            self.serHandler.sendLock.acquire()
            self.serHandler.sendQueue.append(toSend)
            self.serHandler.sendLock.release()
        else:
            try:
                serMsg = serMsgSend(self.serHandler, "#%dL\r" % self.servoNum)
                if debug:
                    print "sending command #%dL to queue" % self.servoNum
            except:
                pass


class Controller:
    def __init__(self, servos=32):
        self.serialHandler = serHandler()
        timeout = time.time()
        while not (self.serialHandler.serOpen or (time.time() - timeout > 2.0)):
            time.sleep(0.01)
        print "initilizing servos"
        self.servos = {}
        for i in range(32):
            self.servos[i] = Servo(i, serHandler=self.serialHandler)
        print "servos initalizied"

    def killAll(self):
        if self.serialHandler.serOpen:
            for servo in self.servos:
                self.servos[servo].kill()
        print "SHUTTING. DOWN. EVERYTHING. All servos killed."


class Hexy(MultiBody):
    BODY_W  = 200e-3
    BODY_T  = 10e-3
    YAW_L   = 26e-3
    YAW_W   = 10e-3
    THIGH_L = 50e-3
    THIGH_W = 10e-3
    CALF_L  = 43e-3
    CALF_W  = 10e-3
    BODY_M  = 0.2
    YAW_M   = 0.05
    THIGH_M = 0.05
    CALF_M  = 0.05

    def connectToHexy(self):
        """Connect to the real hexy"""
        self.hexy_conn = Controller()

    def buildBody(self):
        """ Build an equilateral hexapod """
        # Connect to the real hexy
        self.connectToHexy()
        # These are the rotation matrices we will use
        r_30z = calcRotMatrix((0, 0, 1), pi / 6.0)
        r_45z = calcRotMatrix((0, 0, 1), pi / 4.0)
        r_60z = calcRotMatrix((0, 0, 1), pi / 3.0)
        r_90z = calcRotMatrix((0, 0, 1), pi / 2.0)
        # p_hip is the point where the hip is located.
        # We want to start it 30 degrees into a rotation around Z
        p_hip = (self.BODY_W / 2.0, 0, 0)
        self.core = [0, 0, 0]
        self.core[0] = self.addBody(p_hip, mul3(p_hip, -1), self.BODY_T, mass=self.BODY_M)

        self.publisher.addToCatalog(
            "body.totalflow_gpm",
            self.getTotalHydraulicFlowGPM)

        p = (1, 0, 0)
        p = rotate3(r_45z, p)
        self.legs                  = [0, 0, 0, 0, 0, 0]
        for i in range(6):
            yaw_p  = mul3(p, (self.BODY_W / 2.0))
            hip_p  = mul3(p, (self.BODY_W / 2.0) + self.YAW_L)
            knee_p = mul3(p, (self.BODY_W / 2.0) + self.YAW_L + self.THIGH_L)
            foot_p = mul3(p, (self.BODY_W / 2.0) + self.YAW_L + self.THIGH_L + self.CALF_L)
            # Add hip yaw
            yaw_link = self.addBody(
                p1=yaw_p,
                p2=hip_p,
                radius=self.YAW_W,
                mass=self.YAW_M)
            hip_yaw = self.addControlledHingeJoint(
                body1=self.core[0],
                body2=yaw_link,
                anchor=yaw_p,
                axis=(0, 0, 1))
            hip_yaw.setTorqueLimit(0.157)  # Limit of HXT900
            hip_yaw.setGain(10.0)
            self.publisher.addToCatalog(
                "l%d.hy.torque" % i,
                hip_yaw.getTorque)
            self.publisher.addToCatalog(
                "l%d.hy.torque_lim" % i,
                hip_yaw.getTorqueLimit)
            self.publisher.addToCatalog(
                "l%d.hy.ang" % i,
                hip_yaw.getAngle)
            self.publisher.addToCatalog(
                "l%d.hy.ang_target" % i,
                hip_yaw.getAngleTarget)

            # Add thigh and hip pitch
            # Calculate the axis of rotation for hip pitch
            axis = rotate3(r_90z, p)
            thigh = self.addBody(
                p1=hip_p,
                p2=knee_p,
                radius=self.THIGH_W,
                mass=self.THIGH_M)
            hip_pitch = self.addControlledHingeJoint(
                body1=yaw_link,
                body2=thigh,
                anchor=hip_p,
                axis=axis)
            # hip_pitch.setParam(ode.ParamLoStop, -pi/3)
            # hip_pitch.setParam(ode.ParamHiStop, +pi/3)
            p1 = mul3(p, (self.BODY_W / 2.0) + self.YAW_L)
            p1 = (p1[0], p1[1], 0.355)
            p2 = mul3(p, (self.BODY_W / 2.0) + self.YAW_L + self.THIGH_L / 2)
            # hip_pitch.setTorqueLimit(0.157) # Limit of HXT900
            hip_pitch.setTorqueLimit(0.157)  # testing
            hip_pitch.setGain(10.0)
            self.publisher.addToCatalog(
                "l%d.hp.torque" % i,
                hip_pitch.getTorque)
            self.publisher.addToCatalog(
                "l%d.hp.torque_lim" % i,
                hip_pitch.getTorqueLimit)
            self.publisher.addToCatalog(
                "l%d.hp.ang" % i,
                hip_pitch.getAngle)
            self.publisher.addToCatalog(
                "l%d.hp.ang_target" % i,
                hip_pitch.getAngleTarget)

            # Add calf and knee bend
            calf = self.addBody(
                p1=knee_p,
                p2=foot_p,
                radius=self.CALF_W,
                mass=self.CALF_M)
            knee_pitch = self.addControlledHingeJoint(
                body1=thigh,
                body2=calf,
                anchor=knee_p,
                axis=axis)
            # knee_pitch.setParam(ode.ParamLoStop, -2*pi/3)
            # knee_pitch.setParam(ode.ParamHiStop, 0.0)
            p1 = mul3(p, (self.BODY_W / 2.0) + self.YAW_L + (self.THIGH_L / 4))
            p1 = (p1[0], p1[1], -0.1)
            p2 = mul3(p, (self.BODY_W / 2.0) + self.YAW_L + self.THIGH_L - .355)
            knee_pitch.setTorqueLimit(0.157)  # Limit of HXT900
            knee_pitch.setGain(10.0)
            self.publisher.addToCatalog(
                "l%d.kp.torque" % i,
                knee_pitch.getTorque)
            self.publisher.addToCatalog(
                "l%d.kp.torque_lim" % i,
                knee_pitch.getTorqueLimit)
            self.publisher.addToCatalog(
                "l%d.kp.ang" % i,
                knee_pitch.getAngle)
            self.publisher.addToCatalog(
                "l%d.kp.ang_target" % i,
                knee_pitch.getAngleTarget)

            d                 = {}
            d['hip_yaw']      = hip_yaw
            d['hip_pitch']    = hip_pitch
            d['knee_pitch']   = knee_pitch
            d['hip_yaw_link'] = yaw_link
            d['thigh']        = thigh
            d['calf']         = calf
            self.legs[i]      = d

            p = rotate3(r_45z, p)
            if i == 2:
                p = rotate3(r_45z, p)
        # Assign the servo numbers for interfacing with the real Hexy
        self.legs[0]['hip_yaw'].servo    = self.hexy_conn.servos[0]
        self.legs[0]['hip_pitch'].servo  = self.hexy_conn.servos[1]
        self.legs[0]['knee_pitch'].servo = self.hexy_conn.servos[2]
        self.legs[1]['hip_yaw'].servo    = self.hexy_conn.servos[4]
        self.legs[1]['hip_pitch'].servo  = self.hexy_conn.servos[5]
        self.legs[1]['knee_pitch'].servo = self.hexy_conn.servos[6]
        self.legs[2]['hip_yaw'].servo    = self.hexy_conn.servos[8]
        self.legs[2]['hip_pitch'].servo  = self.hexy_conn.servos[9]
        self.legs[2]['knee_pitch'].servo = self.hexy_conn.servos[10]
        self.legs[3]['hip_yaw'].servo    = self.hexy_conn.servos[24]
        self.legs[3]['hip_pitch'].servo  = self.hexy_conn.servos[25]
        self.legs[3]['knee_pitch'].servo = self.hexy_conn.servos[26]
        self.legs[4]['hip_yaw'].servo    = self.hexy_conn.servos[20]
        self.legs[4]['hip_pitch'].servo  = self.hexy_conn.servos[21]
        self.legs[4]['knee_pitch'].servo = self.hexy_conn.servos[22]
        self.legs[5]['hip_yaw'].servo    = self.hexy_conn.servos[16]
        self.legs[5]['hip_pitch'].servo  = self.hexy_conn.servos[17]
        self.legs[5]['knee_pitch'].servo = self.hexy_conn.servos[18]

        self.legs[0]['hip_yaw'].servo_offset    = 0.0
        self.legs[0]['hip_pitch'].servo_offset  = 0.0
        self.legs[0]['knee_pitch'].servo_offset = -90.0
        self.legs[1]['hip_yaw'].servo_offset    = 0.0
        self.legs[1]['hip_pitch'].servo_offset  = 0.0
        self.legs[1]['knee_pitch'].servo_offset = -90.0
        self.legs[2]['hip_yaw'].servo_offset    = 0.0
        self.legs[2]['hip_pitch'].servo_offset  = 0.0
        self.legs[2]['knee_pitch'].servo_offset = -90.0
        self.legs[3]['hip_yaw'].servo_offset    = 0.0
        self.legs[3]['hip_pitch'].servo_offset  = 0.0
        self.legs[3]['knee_pitch'].servo_offset = -90.0
        self.legs[4]['hip_yaw'].servo_offset    = 0.0
        self.legs[4]['hip_pitch'].servo_offset  = 0.0
        self.legs[4]['knee_pitch'].servo_offset = -90.0
        self.legs[5]['hip_yaw'].servo_offset    = 0.0
        self.legs[5]['hip_pitch'].servo_offset  = 0.0
        self.legs[5]['knee_pitch'].servo_offset = -90.0

        self.legs[0]['hip_yaw'].servo_mult    = 1.0
        self.legs[0]['hip_pitch'].servo_mult  = 1.0
        self.legs[0]['knee_pitch'].servo_mult = -1.0
        self.legs[1]['hip_yaw'].servo_mult    = 1.0
        self.legs[1]['hip_pitch'].servo_mult  = 1.0
        self.legs[1]['knee_pitch'].servo_mult = -1.0
        self.legs[2]['hip_yaw'].servo_mult    = 1.0
        self.legs[2]['hip_pitch'].servo_mult  = 1.0
        self.legs[2]['knee_pitch'].servo_mult = -1.0
        self.legs[3]['hip_yaw'].servo_mult    = 1.0
        self.legs[3]['hip_pitch'].servo_mult  = 1.0
        self.legs[3]['knee_pitch'].servo_mult = -1.0
        self.legs[4]['hip_yaw'].servo_mult    = 1.0
        self.legs[4]['hip_pitch'].servo_mult  = 1.0
        self.legs[4]['knee_pitch'].servo_mult = -1.0
        self.legs[5]['hip_yaw'].servo_mult    = 1.0
        self.legs[5]['hip_pitch'].servo_mult  = 1.0
        self.legs[5]['knee_pitch'].servo_mult = -1.0

    def getTotalHydraulicFlowGPM(self):
        total = 0
        for i in range(6):
            total += abs(self.legs[i]['hip_yaw'].getHydraulicFlowGPM())
            total += abs(self.legs[i]['hip_pitch'].getHydraulicFlowGPM())
            total += abs(self.legs[i]['knee_pitch'].getHydraulicFlowGPM())
        return total

    def setDesiredFootPositions(self, positions):
        """
        positions should be an iterable of 6 positions relative to the body
        Hexy is not a perfect hexapod.  He is actually an octogon with two positions not populated
        """
        # These are the rotation matrices we will use
        r_30z = calcRotMatrix((0, 0, 1), pi / 6.0)
        r_45z = calcRotMatrix((0, 0, 1), pi / 4.0)
        r_60z = calcRotMatrix((0, 0, 1), pi / 3.0)
        r_90z = calcRotMatrix((0, 0, 1), pi / 2.0)
        p = (1, 0, 0)
        p = rotate3(r_45z, p)

        i = 0


        for target_p in positions:
            yaw_p = mul3(p, (self.BODY_W / 2))
            # Calculate hip yaw
            hip_yaw_offset_angle     = atan2(yaw_p[1], yaw_p[0])
            hip_yaw_angle            = atan2(target_p[1], target_p[0]) - hip_yaw_offset_angle
            yaw_link_offset = mul3(p, self.YAW_L)
            yaw_link_offset = (yaw_link_offset[0] * cos(hip_yaw_angle),
                               yaw_link_offset[1] * sin(hip_yaw_angle),
                               0)
            hip_p = add3(yaw_p, yaw_link_offset)
            # Assign outputs
            # Calculate leg length
            leg_l                    = dist3(target_p, hip_p)
            # Use law of cosines on leg length to calculate knee angle 
            knee_angle               = pi - thetaFromABC(self.THIGH_L, self.CALF_L, leg_l)
            # Calculate target point relative to hip origin
            target_p                 = sub3(target_p, hip_p)
            # Calculate hip pitch
            hip_offset_angle         = -thetaFromABC(self.THIGH_L, leg_l,  self.CALF_L)
            hip_depression_angle     = -atan2(target_p[2], len3((target_p[0], target_p[1], 0)))
            hip_pitch_angle          = hip_offset_angle + hip_depression_angle
            self.legs[i]['hip_yaw'].setAngleTarget(-hip_yaw_angle)
            self.legs[i]['hip_pitch'].setAngleTarget(-hip_pitch_angle)
            self.legs[i]['knee_pitch'].setAngleTarget(-knee_angle)
            # Calculate the hip base point for the next iteration
            p                    = rotate3(r_45z, p)
            i += 1
            if i == 3:
                p = rotate3(r_45z, p)

    def getBodyHeight(self):
        return self.core[0].getPosition()[2]

    def getPosition(self):
        return self.core[0].getPosition()

    def getVelocity(self):
        return self.core[0].getLinearVel()

    def __getLegAngleOffset(self, i):
        if i < 3:
            return (pi / 4) + i * (pi / 4)
        elif i < 6:
            return (pi / 2) + i * (pi / 4)
        else:
            raise

    def constantSpeedWalk(self):
        gait_cycle      = 4.0     # time in seconds
        step_cycle      = gait_cycle / 2.0
        swing_overshoot = 1.00
        neutral_r       = 14e-2     # radius from body center or foot resting, m
        stride_length   = 10e-2    # length of a stride, m
        body_h          = 6e-2    # height of body off the ground, m
        foot_lift_h     = 3e-2     # how high to lift feet in m

        foot_positions = []
        x_off_swing  = swing_overshoot * (stride_length / 2.0) * cos(2 * pi * (self.sim.sim_t % step_cycle) / gait_cycle)
        x_off_stance = stride_length * (((self.sim.sim_t % step_cycle) / step_cycle) - 0.5)
        z_off        = foot_lift_h * sin(2 * pi * self.sim.sim_t / gait_cycle)
        if z_off < 0:
            z_off *= -1
        for i in range(6):
            x = neutral_r * cos(self.__getLegAngleOffset(i))
            y = neutral_r * sin(self.__getLegAngleOffset(i))
            z = -body_h
            if (i % 2) ^ (self.sim.sim_t % gait_cycle < (step_cycle)):
                x += x_off_stance
            else:
                x += x_off_swing
                z += z_off
            p = (x, y, z)
            foot_positions.append(p)
        self.setDesiredFootPositions(foot_positions)
        return foot_positions

    def colorJointByTorque(self, joint):
            b = joint.getBody(1)
            r = abs(joint.getTorque() / joint.getTorqueLimit())
            if r >= 0.99:
                b.color = (0, 0, 0, 255)
            else:
                b.color = (255 * r, 255 * (1 - r), 0, 255)

    def colorTorque(self):
        for i in range(6):
            # Color overtorque
            self.colorJointByTorque(self.legs[i]['hip_yaw'])
            self.colorJointByTorque(self.legs[i]['hip_pitch'])
            self.colorJointByTorque(self.legs[i]['knee_pitch'])

    def update(self):
        MultiBody.update(self)
