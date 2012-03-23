from MultiBody import MultiBody
from helpers import *
import ode
from pubsub import *

BODY_W  = 0.4
BODY_T  = 0.3
YAW_L   = 0.3
YAW_W   = 0.1
THIGH_L = 1.83 # 6 feet
THIGH_W = 0.125
CALF_L  = 2.44  # 8 feet
CALF_W  = 0.1

BODY_M  = 454  # 1000 lbs
#BODY_M  = 1000  # 2200 lbs
YAW_M   = 10.0 # 22 lbs
THIGH_M = 36.3 # 80 lbs
CALF_M  = 36.3 # 80 lbs

class SpiderWHydraulics(MultiBody):
    def buildBody( self ):
        """ Build an equilateral hexapod """
        # These are the rotation matrices we will use
        r_30z = calcRotMatrix( (0,0,1), pi/6.0 )
        r_60z = calcRotMatrix( (0,0,1), pi/3.0 )
        r_90z = calcRotMatrix( (0,0,1), pi/2.0 )
        # p_hip is the point where the hip is located.
        # We want to start it 30 degrees into a rotation around Z
        p_hip = (BODY_W/2.0, 0, 0)
        #p_hip = rotate3( r_30z, p_hip )
        self.core = [0,0,0]
        self.core[0] = self.addBody( p_hip, mul3(p_hip, -1), BODY_T, mass=BODY_M )

        self.publisher.addToCatalog(\
            "body.totalflow_gpm",\
            self.getTotalHydraulicFlowGPM)

        # Start another rotation
        p = (1, 0, 0)
        p = rotate3( r_30z, p )
        self.legs                  = [0,0,0,0,0,0]
        for i in range(6):
            yaw_p  = mul3( p, (BODY_W/2.0) )
            hip_p  = mul3( p, (BODY_W/2.0)+YAW_L )
            knee_p = mul3( p, (BODY_W/2.0)+YAW_L+THIGH_L )
            foot_p = mul3( p, (BODY_W/2.0)+YAW_L+THIGH_L+CALF_L )
            # Add hip yaw
            yaw_link = self.addBody( \
                p1     = yaw_p, \
                p2     = hip_p, \
                radius = YAW_W, \
                mass   = YAW_M )
            hip_yaw = self.addLinearControlledHingeJoint( \
                body1        = self.core[0], \
                body2        = yaw_link, \
                anchor       = yaw_p, \
                axis         = (0,0,1),\
                a1x          = 0.25,\
                a2x          = 0.25,\
                a2y          = 0.25)
            hip_yaw.setForceLimit(2.8e4)# 2 inch bore @ 2000 psi
            hip_yaw.setGain(10.0)
            self.publisher.addToCatalog(\
                "l%d.hy.torque"%i,\
                hip_yaw.getTorque)
            self.publisher.addToCatalog(\
                "l%d.hy.torque_lim"%i,\
                hip_yaw.getTorqueLimit)
            self.publisher.addToCatalog(\
                "l%d.hy.ang"%i,\
                hip_yaw.getAngle)
            self.publisher.addToCatalog(\
                "l%d.hy.ang_target"%i,\
                hip_yaw.getAngleTarget)
            self.publisher.addToCatalog(\
                "l%d.hy.len"%i,\
                hip_yaw.getLength)
            self.publisher.addToCatalog(\
                "l%d.hy.len_rate"%i,\
                hip_yaw.getLengthRate)
            hip_yaw.cross_section = 2.02e-3 # 2 inch bore
            self.publisher.addToCatalog(\
                "l%d.hy.flow_gpm"%i,\
                hip_yaw.getHydraulicFlowGPM)

            # Add thigh and hip pitch
            # Calculate the axis of rotation for hip pitch
            axis = rotate3( r_90z, p )
            thigh = self.addBody(\
                p1     = hip_p, \
                p2     = knee_p, \
                radius = THIGH_W, \
                mass   = THIGH_M )
            hip_pitch = self.addLinearControlledHingeJoint( \
                body1        = yaw_link, \
                body2        = thigh, \
                anchor       = hip_p, \
                axis         = axis, \
                a1x          = 0.25,\
                a2x          = 0.25,\
                a2y          = 0.25)
            hip_pitch.setParam(ode.ParamLoStop, -pi/3)
            hip_pitch.setParam(ode.ParamHiStop, +pi/3)
            p1 = mul3( p, (BODY_W/2.0)+YAW_L )
            p1 = (p1[0], p1[1], 0.355)
            p2 = mul3( p, (BODY_W/2.0)+YAW_L+THIGH_L/2 )
            hip_pitch.setForceLimit(2.8e4)# 2 inch bore @ 2000 psi
            hip_pitch.setGain(10.0)
            self.publisher.addToCatalog(\
                "l%d.hp.torque"%i,\
                hip_pitch.getTorque)
            self.publisher.addToCatalog(\
                "l%d.hp.torque_lim"%i,\
                hip_pitch.getTorqueLimit)
            self.publisher.addToCatalog(\
                "l%d.hp.ang"%i,\
                hip_pitch.getAngle)
            self.publisher.addToCatalog(\
                "l%d.hp.ang_target"%i,\
                hip_pitch.getAngleTarget)
            self.publisher.addToCatalog(\
                "l%d.hp.len"%i,\
                hip_pitch.getLength)
            self.publisher.addToCatalog(\
                "l%d.hp.len_rate"%i,\
                hip_pitch.getLengthRate)
            hip_pitch.cross_section = 2.02e-3 # 2 inch bore
            self.publisher.addToCatalog(\
                "l%d.hp.flow_gpm"%i,\
                hip_pitch.getHydraulicFlowGPM)

            # Add calf and knee bend
            calf = self.addBody( \
                p1     = knee_p, \
                p2     = foot_p, \
                radius = CALF_W, \
                mass   = CALF_M )
            knee_pitch = self.addLinearControlledHingeJoint( \
                body1        = thigh, \
                body2        = calf, \
                anchor       = knee_p, \
                axis         = axis, \
                a1x          = 0.25,\
                a2x          = 0.25,\
                a2y          = 0.25)
            knee_pitch.setParam(ode.ParamLoStop, -2*pi/3)
            knee_pitch.setParam(ode.ParamHiStop, 0.0)
            p1 = mul3( p, (BODY_W/2.0)+YAW_L+(THIGH_L/4) )
            p1 = (p1[0], p1[1], -0.1)
            p2 = mul3( p, (BODY_W/2.0)+YAW_L+THIGH_L-.355 )
            knee_pitch.setForceLimit(2.8e4)# 2 inch bore @ 2000 psi
            knee_pitch.setGain(10.0)
            self.publisher.addToCatalog(\
                "l%d.kp.torque"%i,\
                knee_pitch.getTorque)
            self.publisher.addToCatalog(\
                "l%d.kp.torque_lim"%i,\
                knee_pitch.getTorqueLimit)
            self.publisher.addToCatalog(\
                "l%d.kp.ang"%i,\
                knee_pitch.getAngle)
            self.publisher.addToCatalog(\
                "l%d.kp.ang_target"%i,\
                knee_pitch.getAngleTarget)
            self.publisher.addToCatalog(\
                "l%d.kp.len"%i,\
                knee_pitch.getLength)
            self.publisher.addToCatalog(\
                "l%d.kp.len_rate"%i,\
                knee_pitch.getLengthRate)
            knee_pitch.cross_section = 2.02e-3 # 2 inch bore
            self.publisher.addToCatalog(\
                "l%d.kp.flow_gpm"%i,\
                knee_pitch.getHydraulicFlowGPM)

            d                 = {}
            d['hip_yaw']      = hip_yaw
            d['hip_pitch']    = hip_pitch
            d['knee_pitch']   = knee_pitch
            d['hip_yaw_link'] = yaw_link
            d['thigh']        = thigh
            d['calf']         = calf
            self.legs[i]      = d

            p = rotate3( r_60z, p )
    def getTotalHydraulicFlowGPM( self ):
        total = 0
        for i in range(6):
            total += abs(self.legs[i]['hip_yaw'].getHydraulicFlowGPM())
            total += abs(self.legs[i]['hip_pitch'].getHydraulicFlowGPM())
            total += abs(self.legs[i]['knee_pitch'].getHydraulicFlowGPM())
        return total
    def setDesiredFootPositions( self, positions ):
        """
        positions should be an iterable of 6 positions relative to the body
        """
        # These are the rotation matrices we will use
        r_30z = calcRotMatrix( (0,0,1), pi/6.0 )
        r_60z = calcRotMatrix( (0,0,1), pi/3.0 )
        r_90z = calcRotMatrix( (0,0,1), pi/2.0 )
        p = (1,0,0)
        p = rotate3( r_30z, p )

        i = 0


        for target_p in positions:
            yaw_p = mul3(p, (BODY_W/2))
            # Calculate hip yaw
            hip_yaw_offset_angle     = atan2(yaw_p[1], yaw_p[0])
            hip_yaw_angle            = atan2( target_p[1], target_p[0] ) - hip_yaw_offset_angle
            yaw_link_offset = mul3(p, YAW_L)
            yaw_link_offset = ( yaw_link_offset[0]*cos(hip_yaw_angle),\
                                yaw_link_offset[1]*sin(hip_yaw_angle),\
                                0)
            hip_p = add3(yaw_p, yaw_link_offset)
            # Assign outputs
            # Calculate leg length
            leg_l                    = dist3( target_p, hip_p )
            # Use law of cosines on leg length to calculate knee angle 
            knee_angle               = pi-thetaFromABC( THIGH_L, CALF_L, leg_l )
            # Calculate target point relative to hip origin
            target_p                 = sub3( target_p, hip_p )
            # Calculate hip pitch
            hip_offset_angle         = -thetaFromABC( THIGH_L, leg_l,  CALF_L )
            hip_depression_angle     = -atan2( target_p[2], len3((target_p[0], target_p[1], 0)) )
            hip_pitch_angle          = hip_offset_angle + hip_depression_angle
            self.legs[i]['hip_yaw'   ].setAngleTarget( -hip_yaw_angle   )
            self.legs[i]['hip_pitch' ].setAngleTarget( -hip_pitch_angle )
            self.legs[i]['knee_pitch'].setAngleTarget( -knee_angle      )
            # Calculate the hip base point for the next iteration
            p                    = rotate3( r_60z, p )
            i+=1
    def getBodyHeight( self ):
        return self.core[0].getPosition()[2]
    def getPosition( self ):
        return self.core[0].getPosition()
    def getVelocity( self ):
        return self.core[0].getLinearVel()
    def naiveWalk( self, sim_t ):
        gait_cycle=5.0
        foot_positions = []
        x_off =  1.00*cos(2*pi*sim_t/gait_cycle)
        z_off =  1.5*sin(2*pi*sim_t/gait_cycle)
        if z_off<0:
            z_off *= -1
        for i in range(6):
            z = -2.0
            if (i%2) ^ (sim_t%gait_cycle<(gait_cycle/2.0)):
                z += z_off
            p = ( sign(i%2)*x_off + 2.29*cos(pi/6 + (i*pi/3)), 2.29*sin(pi/6 + (i*pi/3)), z )
            foot_positions.append(p)
        self.setDesiredFootPositions( foot_positions )
        return foot_positions
    def standUp( self, sim_t ):
        """Don't walk, just sort of try to stand up"""
        gait_cycle      = 3.0     # time in seconds
        step_cycle      = gait_cycle/2.0
        neutral_r       = 2.5     # radius from body center or foot resting, m
        stride_length   = 2.00    # length of a stride, m
        body_h          = 2.20    # height of body off the ground, m
        foot_lift_h     = 1.00     # how high to lift feet in m

        foot_positions = []
        z_off        =  foot_lift_h*sin(2*pi*sim_t/gait_cycle)
        if z_off<0:
            z_off *= -1
        for i in range(6):
            x = neutral_r*cos(pi/6 + (i*pi/3))
            y = neutral_r*sin(pi/6 + (i*pi/3))
            z = -body_h
            if (i%2) ^ (sim_t%gait_cycle<(step_cycle)):
                z += z_off
            p = ( x, y, z )
            foot_positions.append(p)
        self.setDesiredFootPositions( foot_positions )
        return foot_positions
    def constantSpeedWalk( self, sim_t ):
        gait_cycle      = 3.0     # time in seconds
        step_cycle      = gait_cycle/2.0
        swing_overshoot = 1.00
        neutral_r       = 2.5     # radius from body center or foot resting, m
        stride_length   = 2.00    # length of a stride, m
        body_h          = 2.20    # height of body off the ground, m
        foot_lift_h     = 0.45     # how high to lift feet in m

        #gait_cycle      = 1.8     # time in seconds
        #step_cycle      = gait_cycle/2.0
        #swing_overshoot = 1.00
        #neutral_r       = 1.7     # radius from body center or foot resting, m
        #stride_length   = 1.4     # length of a stride, m
        #body_h          = 1.5     # height of body off the ground, m
        #foot_lift_h     = 0.1     # how high to lift feet in m
        foot_positions = []
        x_off_swing  =  swing_overshoot*(stride_length/2.0)*cos(2*pi*(sim_t%step_cycle)/gait_cycle)
        x_off_stance =  stride_length*(((sim_t%step_cycle)/step_cycle)-0.5)
        z_off        =  foot_lift_h*sin(2*pi*sim_t/gait_cycle)
        if z_off<0:
            z_off *= -1
        for i in range(6):
            x = neutral_r*cos(pi/6 + (i*pi/3))
            y = neutral_r*sin(pi/6 + (i*pi/3))
            z = -body_h
            if (i%2) ^ (sim_t%gait_cycle<(step_cycle)):
                x += x_off_swing
                z += z_off
            else:
                x += x_off_stance
            p = ( x, y, z )
            foot_positions.append(p)
        self.setDesiredFootPositions( foot_positions )
        return foot_positions
    def colorJointByTorque( self, joint ):
            b = joint.getBody(1)
            r = abs(joint.getTorque()/joint.getTorqueLimit())
            if r >= 0.99:
                b.color = (0,0,0,255)
            else:
                b.color = (255*r,255*(1-r),0,255)
    def colorTorque( self ):
        for i in range(6):
            # Color overtorque
            self.colorJointByTorque( self.legs[i]['hip_yaw'] )
            self.colorJointByTorque( self.legs[i]['hip_pitch'] )
            self.colorJointByTorque( self.legs[i]['knee_pitch'] )
    def update( self ):
        MultiBody.update(self)

class LegOnStand(MultiBody):
    YAW_L   = 0.25
    THIGH_L = 1.00
    CALF_L  = 1.00
    YAW_M   = 10.0
    THIGH_M = 20.0
    CALF_M  = 20.0
    def buildBody( self ):
        """ Build a single leg anchored to the universe """
        #self.publisher.addToCatalog(\
        #    "body.totalflow_gpm",\
        #    self.getTotalHydraulicFlowGPM)

        p = (1, 0, 0)
        yaw_p  = (0,0,0)
        hip_p  = mul3( p, self.YAW_L )
        knee_p = mul3( p, self.YAW_L+self.THIGH_L )
        foot_p = mul3( p, self.YAW_L+self.THIGH_L+self.CALF_L )
        # Add hip yaw
        yaw_link = self.addBody( \
            p1     = yaw_p, \
            p2     = hip_p, \
            radius = 0.05, \
            mass   = self.YAW_M )
        hip_yaw = self.addLinearControlledHingeJoint( \
            body1        = ode.environment, \
            body2        = yaw_link, \
            anchor       = yaw_p, \
            axis         = (0,0,1),\
            a1x          = 0.25,\
            a2x          = 0.25,\
            a2y          = 0.25)
        hip_yaw.setForceLimit(2.8e4)# 2 inch bore @ 2000 psi
        hip_yaw.setGain(-10.0) # FIXME: ode has a weird bug that makes servo joints apply backwards force when anchored to environment.  Compensate by inverting gain.
        self.publisher.addToCatalog(\
            "hy.torque",\
            hip_yaw.getTorque)
        self.publisher.addToCatalog(\
            "hy.torque_lim",\
            hip_yaw.getTorqueLimit)
        self.publisher.addToCatalog(\
            "hy.ang",\
            hip_yaw.getAngle)
        self.publisher.addToCatalog(\
            "hy.ang_target",\
            hip_yaw.getAngleTarget)
        self.publisher.addToCatalog(\
            "hy.ang_error",\
            hip_yaw.getAngleError)
        self.publisher.addToCatalog(\
            "hy.len",\
            hip_yaw.getLength)
        self.publisher.addToCatalog(\
            "hy.len_rate",\
            hip_yaw.getLengthRate)
        hip_yaw.cross_section = 2.02e-3 # 2 inch bore
        self.publisher.addToCatalog(\
            "hy.flow_gpm",\
            hip_yaw.getHydraulicFlowGPM)

        # Add thigh and hip pitch
        # Calculate the axis of rotation for hip pitch
        axis = (0,1,0)
        thigh = self.addBody(\
            p1     = hip_p, \
            p2     = knee_p, \
            radius = THIGH_W, \
            mass   = self.THIGH_M )
        hip_pitch = self.addLinearControlledHingeJoint( \
            body1        = yaw_link, \
            body2        = thigh, \
            anchor       = hip_p, \
            axis         = axis, \
            a1x          = 0.25,\
            a2x          = 0.25,\
            a2y          = 0.25)
        hip_pitch.setParam(ode.ParamLoStop, -pi/3)
        hip_pitch.setParam(ode.ParamHiStop, +pi/3)
        p1 = mul3( p, (BODY_W/2.0)+self.YAW_L )
        p1 = (p1[0], p1[1], 0.355)
        p2 = mul3( p, (BODY_W/2.0)+self.YAW_L+self.THIGH_L/2 )
        hip_pitch.setForceLimit(2.8e4)# 2 inch bore @ 2000 psi
        hip_pitch.setGain(10.0)
        self.publisher.addToCatalog(\
            "hp.torque",\
            hip_pitch.getTorque)
        self.publisher.addToCatalog(\
            "hp.torque_lim",\
            hip_pitch.getTorqueLimit)
        self.publisher.addToCatalog(\
            "hp.ang",\
            hip_pitch.getAngle)
        self.publisher.addToCatalog(\
            "hp.ang_target",\
            hip_pitch.getAngleTarget)
        self.publisher.addToCatalog(\
            "hp.ang_error",\
            hip_pitch.getAngleError)
        self.publisher.addToCatalog(\
            "hp.len",\
            hip_pitch.getLength)
        self.publisher.addToCatalog(\
            "hp.len_rate",\
            hip_pitch.getLengthRate)
        hip_pitch.cross_section = 2.02e-3 # 2 inch bore
        self.publisher.addToCatalog(\
            "hp.flow_gpm",\
            hip_pitch.getHydraulicFlowGPM)

        # Add calf and knee bend
        calf = self.addBody( \
            p1     = knee_p, \
            p2     = foot_p, \
            radius = CALF_W, \
            mass   = self.CALF_M )
        knee_pitch = self.addLinearControlledHingeJoint( \
            body1        = thigh, \
            body2        = calf, \
            anchor       = knee_p, \
            axis         = axis, \
            a1x          = 0.25,\
            a2x          = 0.25,\
            a2y          = 0.25)
        knee_pitch.setParam(ode.ParamLoStop, -2*pi/3)
        knee_pitch.setParam(ode.ParamHiStop, 0.0)
        p1 = mul3( p, (BODY_W/2.0)+self.YAW_L+(self.THIGH_L/4) )
        p1 = (p1[0], p1[1], -0.1)
        p2 = mul3( p, (BODY_W/2.0)+self.YAW_L+self.THIGH_L-.355 )
        knee_pitch.setForceLimit(2.8e4)# 2 inch bore @ 2000 psi
        knee_pitch.setGain(10.0)
        self.publisher.addToCatalog(\
            "kp.torque",\
            knee_pitch.getTorque)
        self.publisher.addToCatalog(\
            "kp.torque_lim",\
            knee_pitch.getTorqueLimit)
        self.publisher.addToCatalog(\
            "kp.ang",\
            knee_pitch.getAngle)
        self.publisher.addToCatalog(\
            "kp.ang_target",\
            knee_pitch.getAngleTarget)
        self.publisher.addToCatalog(\
            "kp.ang_error",\
            knee_pitch.getAngleError)
        self.publisher.addToCatalog(\
            "kp.len",\
            knee_pitch.getLength)
        self.publisher.addToCatalog(\
            "kp.len_rate",\
            knee_pitch.getLengthRate)
        knee_pitch.cross_section = 2.02e-3 # 2 inch bore
        self.publisher.addToCatalog(\
            "kp.flow_gpm",\
            knee_pitch.getHydraulicFlowGPM)

        d                 = {}
        d['hip_yaw']      = hip_yaw
        d['hip_pitch']    = hip_pitch
        d['knee_pitch']   = knee_pitch
        d['hip_yaw_link'] = yaw_link
        d['thigh']        = thigh
        d['calf']         = calf
        self.members      = d
    def getTotalHydraulicFlowGPM( self ):
        total = 0
        for i in range(6):
            total += abs(self.legs[i]['hip_yaw'].getHydraulicFlowGPM())
            total += abs(self.legs[i]['hip_pitch'].getHydraulicFlowGPM())
            total += abs(self.legs[i]['knee_pitch'].getHydraulicFlowGPM())
        return total
    def setDesiredFootPositions( self, positions ):
        """
        positions should be an iterable of 6 positions relative to the body
        """
        # These are the rotation matrices we will use
        for target_p in positions:
            yaw_p = (0,0,0)
            # Calculate hip yaw
            hip_yaw_offset_angle     = atan2(yaw_p[1], yaw_p[0])
            hip_yaw_angle            = atan2( target_p[1], target_p[0] ) - hip_yaw_offset_angle
            yaw_link_offset = mul3(p, self.YAW_L)
            yaw_link_offset = ( yaw_link_offset[0]*cos(hip_yaw_angle),\
                                yaw_link_offset[1]*sin(hip_yaw_angle),\
                                0)
            hip_p = add3(yaw_p, yaw_link_offset)
            # Assign outputs
            # Calculate leg length
            leg_l                    = dist3( target_p, hip_p )
            # Use law of cosines on leg length to calculate knee angle 
            knee_angle               = pi-thetaFromABC( self.THIGH_L, self.CALF_L, leg_l )
            # Calculate target point relative to hip origin
            target_p                 = sub3( target_p, hip_p )
            # Calculate hip pitch
            hip_offset_angle         = -thetaFromABC( self.THIGH_L, leg_l,  self.CALF_L )
            hip_depression_angle     = -atan2( target_p[2], len3((target_p[0], target_p[1], 0)) )
            hip_pitch_angle          = hip_offset_angle + hip_depression_angle
            self.members['hip_yaw'   ].setAngleTarget( -hip_yaw_angle   )
            self.members['hip_pitch' ].setAngleTarget( -hip_pitch_angle )
            self.members['knee_pitch'].setAngleTarget( -knee_angle      )
            # Calculate the hip base point for the next iteration
            p                    = rotate3( r_60z, p )
    def getBodyHeight( self ):
        return self.offset[2]
    def getPosition( self ):
        return self.offset
    def getVelocity( self ):
        return self.core[0].getLinearVel()
    def colorJointByTorque( self, joint ):
            b = joint.getBody(1)
            r = abs(joint.getTorque()/joint.getTorqueLimit())
            if r >= 0.99:
                b.color = (0,0,0,255)
            else:
                b.color = (255*r,255*(1-r),0,255)
    def colorTorque( self ):
        # Color overtorque
        self.colorJointByTorque( self.members['hip_yaw'] )
        self.colorJointByTorque( self.members['hip_pitch'] )
        self.colorJointByTorque( self.members['knee_pitch'] )
    def update( self ):
        MultiBody.update(self)
