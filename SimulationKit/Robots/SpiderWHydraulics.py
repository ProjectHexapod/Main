from SimulationKit.MultiBody import MultiBody
from SimulationKit.helpers import *
from SimulationKit.pubsub import *
import ode

deg2rad = pi/180

class StompyLegPhysicalCharacteristics(object):
    """This class contains the physical characteristics of one of
    Stompy's legs"""
    def __init__(self):
        self.YAW_L   = 0.3   # Length of yaw link
        self.YAW_W   = 0.1   # Diameter of yaw link
        self.THIGH_L = 1.83  # Length of thigh link, 6 feet
        self.THIGH_W = 0.125 # Diameter of thigh link
        self.CALF_L  = 2.44  # Length of calf link 8 feet
        self.CALF_W  = 0.1   # Diameter of calf link
        self.YAW_M   = 10.0  # Yaw link mass, 22 lbs
        self.THIGH_M = 36.3  # Thigh link mass, 80 lbs
        self.CALF_M  = 36.3  # Calf link mass, 80 lbs

        # describe the neutral position of the leg
        self.YAW_OFFSET   = 0.0
        self.PITCH_OFFSET = 0.0
        self.KNEE_OFFSET  = deg2rad*90.0
        # Compliance of foot
        self.COMPLIANCE_K   = 87560  # newtons/meter deflection of foot = 1000 pounds/2 inches
        self.COMPLIANCE_LEN = 0.06  # how long til it bottoms out
        # Leg origin from robot origin, expressed in Stompy's coordinate frame
        self.OFFSET_FROM_ROBOT_ORIGIN   = (0,0,0)
        # Row major 3x3 rotation matrix
        self.ROTATION_FROM_ROBOT_ORIGIN = calcRotMatrix( (0,0,1), 0.0 )

class StompyPhysicalCharacteristics(object):
    """
    This class is a container for Stompy's physical layout, including
    link lengths, masses, offsets, actuator placements...
    """
    def __init__(self):
        self.BODY_W  = 0.4 # Body diameter
        self.BODY_T  = 0.3 # Thickness of the body capsule TODO: improve body model
        self.BODY_M  = 500  # Body mass
        self.LEGS = []
        # These are the rotation matrices we will use
        r_30z = calcRotMatrix( (0,0,1), pi/6.0 )
        r_60z = calcRotMatrix( (0,0,1), pi/3.0 )
        r_90z = calcRotMatrix( (0,0,1), pi/2.0 )
        # To start with, the layout of the body is perfectly hexagonal
        leg_origin = (self.BODY_W/2.0, 0, 0)
        leg_origin = rotate3( r_30z, leg_origin )
        leg_angle  = pi/6.0
        # Set their offsets and rotations from robot origin
        for i in range(6):
            leg = StompyLegPhysicalCharacteristics()
            leg.OFFSET_FROM_ROBOT_ORIGIN   = leg_origin
            leg.ROTATION_FROM_ROBOT_ORIGIN = calcRotMatrix( (0,0,1), leg_angle )
            leg_origin = rotate3( r_60z, leg_origin )
            leg_angle += pi/3.0
            self.LEGS.append(leg)
        # As a test, let's make one of the legs kind of stubby...
        #self.LEGS[0].OFFSET_FROM_ROBOT_ORIGIN = (.5,0,-.2)
        #self.LEGS[0].ROTATION_FROM_ROBOT_ORIGIN = calcRotMatrix( (0,0,1), pi/2 )
        #self.LEGS[0].THIGH_L = 1.0
        #self.LEGS[0].CALF_L = 1.0

class SpiderWHydraulics(MultiBody):
    def __init__( self, *args, **kwargs ):
        self.dimensions = StompyPhysicalCharacteristics()
        super(self.__class__, self).__init__(*args, **kwargs)
    def buildBody( self ):
        """ Build a hexapod according to the dimensions laid out
        in self.dimensions """
        self.core = self.addBody( (self.dimensions.BODY_W/2,0,0),\
            (-1*self.dimensions.BODY_W/2,0,0),\
            self.dimensions.BODY_T,\
            mass=self.dimensions.BODY_M )

        self.publisher.addToCatalog(\
            "body.totalflow_gpm",\
            self.getTotalHydraulicFlowGPM)

        # Start another rotation
        self.legs                  = [0,0,0,0,0,0]
        for i in range(6):
            hip_offset = self.dimensions.LEGS[i].OFFSET_FROM_ROBOT_ORIGIN
            leg_rot    = self.dimensions.LEGS[i].ROTATION_FROM_ROBOT_ORIGIN
            yaw_p     = hip_offset
            hip_p     = add3(yaw_p,\
                mul3( rotate3( leg_rot, (1,0,0) ),\
                self.dimensions.LEGS[i].YAW_L) )
            knee_p     = add3(hip_p,\
                mul3( rotate3( leg_rot, (1,0,0) ),\
                self.dimensions.LEGS[i].THIGH_L ))
            midshin_p = add3( knee_p, \
                rotate3(leg_rot, (0,0,-0.5*self.dimensions.LEGS[i].CALF_L)))
            foot_p = add3( midshin_p, \
                rotate3(leg_rot, (0,0,-0.5*self.dimensions.LEGS[i].CALF_L)))

            # Add hip yaw
            yaw_link = self.addBody( \
                p1     = yaw_p, \
                p2     = hip_p, \
                radius = self.dimensions.LEGS[i].YAW_W, \
                mass   = self.dimensions.LEGS[i].YAW_M )
            hip_yaw = self.addLinearVelocityActuatedHingeJoint( \
                body1        = self.core, \
                body2        = yaw_link, \
                anchor       = yaw_p, \
                axis         = (0,0,1),\
                a1x          = 0.25,\
                a2x          = 0.25,\
                a2y          = 0.25)
            hip_yaw.setForceLimit(2.8e4)# 2 inch bore @ 2000 psi
            hip_yaw.setAngleOffset(0.0)
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
            axis = rotate3( leg_rot, (0,-1,0) )
            thigh = self.addBody(\
                p1     = hip_p, \
                p2     = knee_p, \
                radius = self.dimensions.LEGS[i].THIGH_W, \
                mass   = self.dimensions.LEGS[i].THIGH_M )
            hip_pitch = self.addLinearVelocityActuatedHingeJoint( \
                body1        = yaw_link, \
                body2        = thigh, \
                anchor       = hip_p, \
                axis         = axis, \
                a1x          = 0.35,\
                a2x          = 0.35,\
                a2y          = 0.35)
            #hip_pitch.setParam(ode.ParamLoStop, -pi/3)
            #hip_pitch.setParam(ode.ParamHiStop, +pi/3)
            hip_pitch.setForceLimit(2.8e4)# 2 inch bore @ 2000 psi
            hip_pitch.setAngleOffset(0.0)
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
                p2     = midshin_p, \
                radius = self.dimensions.LEGS[i].CALF_W, \
                mass   = self.dimensions.LEGS[i].CALF_M/2.0 )
            knee_pitch = self.addLinearVelocityActuatedHingeJoint( \
                body1        = thigh, \
                body2        = calf, \
                anchor       = knee_p, \
                axis         = axis, \
                a1x          = 0.25,\
                a2x          = 0.25,\
                a2y          = 0.25)
            knee_pitch.setParam(ode.ParamLoStop, -pi/2)
            knee_pitch.setParam(ode.ParamHiStop, pi/3)
            knee_pitch.setForceLimit(2.8e4)# 2 inch bore @ 2000 psi
            knee_pitch.setAngleOffset(deg2rad*90.0)
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
            # Create the foot
            # Add the compliant joint
            foot = self.addBody( \
                p1     = midshin_p, \
                p2     = foot_p, \
                radius = self.dimensions.LEGS[i].CALF_W, \
                mass   = self.dimensions.LEGS[i].CALF_M/2 )
            calf_axis  = norm3(sub3(midshin_p, foot_p))
            foot_shock = self.addPrismaticSpringJoint( \
                body1        = calf, \
                body2        = foot, \
                axis         = mul3(calf_axis,-1),\
                spring_const = -20e3,\
                hi_stop      = 0.1,\
                lo_stop      = 0.0,\
                neutral_position = 0.0,\
                damping          = -1e2)
                
            d                 = {}
            d['hip_yaw']      = hip_yaw
            d['hip_pitch']    = hip_pitch
            d['knee_pitch']   = knee_pitch
            d['foot_shock']   = foot_shock
            d['hip_yaw_link'] = yaw_link
            d['thigh']        = thigh
            d['calf']         = calf
            d['foot']         = foot
            self.legs[i]      = d
    def getEncoderAngleMatrix( self ):
        retval = []
        for i in range(6):
            retval.append( (\
                self.legs[i]['hip_yaw'].getAngle(),\
                self.legs[i]['hip_pitch'].getAngle(),\
                self.legs[i]['knee_pitch'].getAngle(),\
                self.legs[i]['foot_shock'].getPosition()) )
        return retval


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
            yaw_p = mul3(p, (self.dimensions.BODY_W/2))
            # Calculate hip yaw
            hip_yaw_offset_angle     = atan2(yaw_p[1], yaw_p[0])
            hip_yaw_angle            = atan2( target_p[1], target_p[0] ) - hip_yaw_offset_angle
            yaw_link_offset = mul3(p, self.dimensions.LEGS[i].YAW_L)
            yaw_link_offset = ( yaw_link_offset[0]*cos(hip_yaw_angle),\
                                yaw_link_offset[1]*sin(hip_yaw_angle),\
                                0)
            hip_p = add3(yaw_p, yaw_link_offset)
            # Assign outputs
            # Calculate leg length
            leg_l                    = dist3( target_p, hip_p )
            # Use law of cosines on leg length to calculate knee angle 
            knee_angle               = pi-thetaFromABC( self.dimensions.LEGS[i].THIGH_L, self.dimensions.LEGS[i].CALF_L, leg_l )
            # Calculate target point relative to hip origin
            target_p                 = sub3( target_p, hip_p )
            # Calculate hip pitch
            hip_offset_angle         = -thetaFromABC( self.dimensions.LEGS[i].THIGH_L, leg_l,  self.dimensions.LEGS[i].CALF_L )
            hip_depression_angle     = -atan2( target_p[2], len3((target_p[0], target_p[1], 0)) )
            hip_pitch_angle          = hip_offset_angle + hip_depression_angle
            def controlLenRate( joint, target_ang, gain=10.0 ):
                error = target_ang - joint.getAngle()
                joint.setLengthRate( error*gain )
            controlLenRate(self.legs[i]['hip_yaw'   ], -hip_yaw_angle   )
            controlLenRate(self.legs[i]['hip_pitch' ],  hip_pitch_angle )
            controlLenRate(self.legs[i]['knee_pitch'],  knee_angle      )
            # Calculate the hip base point for the next iteration
            p                    = rotate3( r_60z, p )
            i+=1
    def getBodyHeight( self ):
        return self.core.getPosition()[2]
    def getPosition( self ):
        return self.core.getPosition()
    def getAcceleration( self ):
        return div3(self.core.getForce(), self.dimensions.BODY_M) # FIXME: Returns (0,0,0)
    def getOrientation( self ):
        return self.core.getRotation()
    def getAngularRates( self ):
        return self.core.getAngularVel()
    def getVelocity( self ):
        return self.core.getLinearVel()
    def naiveWalk( self ):
        gait_cycle=5.0
        foot_positions = []
        x_off =  1.00*cos(2*pi*self.sim.sim_t/gait_cycle)
        z_off =  1.5*sin(2*pi*self.sim.sim_t/gait_cycle)
        if z_off<0:
            z_off *= -1
        for i in range(6):
            z = -2.0
            if (i%2) ^ (self.sim.sim_t%gait_cycle<(gait_cycle/2.0)):
                z += z_off
            p = ( sign(i%2)*x_off + 2.29*cos(pi/6 + (i*pi/3)), 2.29*sin(pi/6 + (i*pi/3)), z )
            foot_positions.append(p)
        self.setDesiredFootPositions( foot_positions )
        return foot_positions
    def standUp( self ):
        """Don't walk, just sort of try to stand up"""
        gait_cycle      = 3.0     # time in seconds
        step_cycle      = gait_cycle/2.0
        neutral_r       = 2.5     # radius from body center or foot resting, m
        stride_length   = 2.00    # length of a stride, m
        body_h          = 2.20    # height of body off the ground, m
        foot_lift_h     = 1.00     # how high to lift feet in m

        foot_positions = []
        z_off        =  foot_lift_h*sin(2*pi*self.sim.sim_t/gait_cycle)
        if z_off<0:
            z_off *= -1
        for i in range(6):
            x = neutral_r*cos(pi/6 + (i*pi/3))
            y = neutral_r*sin(pi/6 + (i*pi/3))
            z = -body_h
            if (i%2) ^ (self.sim.sim_t%gait_cycle<(step_cycle)):
                z += z_off
            p = ( x, y, z )
            foot_positions.append(p)
        self.setDesiredFootPositions( foot_positions )
        return foot_positions
    def constantSpeedWalk( self ):
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
        x_off_swing  =  swing_overshoot*(stride_length/2.0)*cos(2*pi*(self.sim.sim_t%step_cycle)/gait_cycle)
        x_off_stance =  stride_length*(((self.sim.sim_t%step_cycle)/step_cycle)-0.5)
        z_off        =  foot_lift_h*sin(2*pi*self.sim.sim_t/gait_cycle)
        if z_off<0:
            z_off *= -1
        for i in range(6):
            x = neutral_r*cos(pi/6 + (i*pi/3))
            y = neutral_r*sin(pi/6 + (i*pi/3))
            z = -body_h
            if (i%2) ^ (self.sim.sim_t%gait_cycle<(step_cycle)):
                x += x_off_swing
                z += z_off
            else:
                x += x_off_stance
            p = ( x, y, z )
            foot_positions.append(p)
        self.setDesiredFootPositions( foot_positions )
        return foot_positions
    def colorShockByDeflection( self, joint ):
            b = joint.getBody(1)
            r = abs(joint.getPosition()/joint.getHiStop())
            if r >= 0.99:
                b.color = (0,0,0,255)
            else:
                b.color = (255*r,255*(1-r),0,255)
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
            self.colorJointByTorque(     self.legs[i]['hip_yaw'] )
            self.colorJointByTorque(     self.legs[i]['hip_pitch'] )
            self.colorJointByTorque(     self.legs[i]['knee_pitch'] )
            self.colorShockByDeflection( self.legs[i]['foot_shock'])
    def update( self ):
        MultiBody.update(self)
