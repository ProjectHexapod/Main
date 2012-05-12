from SimulationKit.MultiBody import MultiBody
from SimulationKit.helpers import *
from SimulationKit.pubsub import *
import ode

deg2rad = pi/180

class LegOnStand(MultiBody):
    YAW_W   = 0.10
    THIGH_W = 0.10
    CALF_W  = 0.10
    YAW_L   = 0.211
    THIGH_L = 1.372
    CALF_L  = 1.283

    YAW_M   =  9.72
    THIGH_M = 17.41
    CALF_M  = 14.17

    # describe the neutral position
    YAW_OFFSET   = deg2rad*-43
    PITCH_OFFSET = deg2rad*-37
    KNEE_OFFSET  = deg2rad*69.5

    # describe the cart
    CART_DIMS = (0.91, 1.27, 0.4)
    CART_M  = 249.5

    HIP_FROM_CART_OFFSET = (-0.16, 0.27, -0.33)

    # radius of the wheels
    WHEEL_R = 0.1

    # Compliance of foot
    COMPLIANCE_K   = 8756  # newtons/meter deflection of foot = 100 pounds/2 inches
    COMPLIANCE_LEN = 0.06  # how long til it bottoms out

    # The vertical stackup to the hip is WHEEL_R + CART_DIMS[2]/2 - HIP_FROM_CART_OFFSET[2]
    HIP_FROM_GROUND_HEIGHT = WHEEL_R + CART_DIMS[2]/2 - HIP_FROM_CART_OFFSET[2]
    
    def buildBody( self ):
        """ Build a single leg anchored to the universe """
        #self.publisher.addToCatalog(\
        #    "body.totalflow_gpm",\
        #    self.getTotalHydraulicFlowGPM)

        # build the cart
        cart = self.addBox( \
            self.CART_DIMS[0], \
            self.CART_DIMS[1], \
            self.CART_DIMS[2], \
            self.HIP_FROM_CART_OFFSET, \
            self.CART_M )
        # Add wheels to the cart
        wheel_p1 = ( self.CART_DIMS[0]/2.0, self.CART_DIMS[1]/2.0, -self.CART_DIMS[2]/2.0)
        wheel_p1 = add3( wheel_p1, self.HIP_FROM_CART_OFFSET )
        wheel_p2 = (-self.CART_DIMS[0]/2.0, self.CART_DIMS[1]/2.0, -self.CART_DIMS[2]/2.0)
        wheel_p2 = add3( wheel_p2, self.HIP_FROM_CART_OFFSET )

        wheel0 = self.addBody(\
            p1     = wheel_p1, \
            p2     = wheel_p2, \
            radius = self.WHEEL_R, \
            mass = 0.5)
        cart_bearing0 = self.addHingeJoint( \
            body1  = cart,\
            body2  = wheel0,\
            anchor = wheel_p1,\
            axis   = (1,0,0))

        wheel_p1 = ( self.CART_DIMS[0]/2.0, -self.CART_DIMS[1]/2.0, -self.CART_DIMS[2]/2.0)
        wheel_p1 = add3( wheel_p1, self.HIP_FROM_CART_OFFSET )
        wheel_p2 = (-self.CART_DIMS[0]/2.0, -self.CART_DIMS[1]/2.0, -self.CART_DIMS[2]/2.0)
        wheel_p2 = add3( wheel_p2, self.HIP_FROM_CART_OFFSET )

        wheel1 = self.addBody(\
            p1     = wheel_p1, \
            p2     = wheel_p2, \
            radius = self.WHEEL_R, \
            mass = 0.5)
        cart_bearing1 = self.addHingeJoint( \
            body1  = cart,\
            body2  = wheel1,\
            anchor = wheel_p1,\
            axis   = (1,0,0))

        p = (1, 0, 0)
        yaw_p  = (0,0,0)
        hip_p  = mul3( p, self.YAW_L )
        knee_p = add3(hip_p, (self.THIGH_L*cos(self.PITCH_OFFSET), 0, -1*self.THIGH_L*sin(self.PITCH_OFFSET)))
        f_ang = self.PITCH_OFFSET+self.KNEE_OFFSET
        midshin_p = add3(knee_p, (.5*self.CALF_L*cos(f_ang), 0, -.5*self.CALF_L*sin(f_ang)))
        foot_p    = add3(midshin_p, (.5*self.CALF_L*cos(f_ang), 0, -.5*self.CALF_L*sin(f_ang)))
        def yaw_offset_around_negz(p):
            a = self.YAW_OFFSET
            s = sin(a)
            c = cos(a)
            return (c*p[0]+s*p[1],-s*p[0]+c*p[1],p[2])
        hip_p     = yaw_offset_around_negz(hip_p)
        knee_p    = yaw_offset_around_negz(knee_p)
        midshin_p = yaw_offset_around_negz(midshin_p)
        foot_p    = yaw_offset_around_negz(foot_p)
        # Add hip yaw
        yaw_link = self.addBody( \
            p1     = yaw_p, \
            p2     = hip_p, \
            radius = self.YAW_W, \
            mass   = self.YAW_M )
        hip_yaw = self.addLinearVelocityActuatedHingeJoint( \
            body1        = cart, \
            body2        = yaw_link, \
            anchor       = yaw_p, \
            axis         = (0,0,1),\
            a1x          = 0.368,\
            a2x          = 0.076,\
            a2y          = 0.086)
        hip_yaw.setParam(ode.ParamLoStop, 0.0)
        hip_yaw.setParam(ode.ParamHiStop, deg2rad*87.28)
        hip_yaw.setForceLimit(maxForce(1.0))
        hip_yaw.setAngleOffset( self.YAW_OFFSET )
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
        axis = yaw_offset_around_negz((0,-1,0))
        thigh = self.addBody(\
            p1     = hip_p, \
            p2     = knee_p, \
            radius = self.THIGH_W, \
            mass   = self.THIGH_M )
        hip_pitch = self.addLinearVelocityActuatedHingeJoint( \
            body1        = yaw_link, \
            body2        = thigh, \
            anchor       = hip_p, \
            axis         = axis, \
            a1x          = 0.203,\
            a2x          = 0.203,\
            a2y          = 0.279)
        hip_pitch.setParam(ode.ParamLoStop, 0.0)
        hip_pitch.setParam(ode.ParamHiStop, deg2rad*29.7)
        p1 = mul3( p, self.YAW_L )
        p1 = (p1[0], p1[1], 0.355)
        p2 = mul3( p, self.YAW_L+self.THIGH_L/2 )
        hip_pitch.setForceLimit(maxForce(1.5))
        hip_pitch.setAngleOffset( self.PITCH_OFFSET )
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

        axis = yaw_offset_around_negz((0,-1,0))
        # Add calf and knee bend
        calf = self.addBody( \
            p1     = knee_p, \
            p2     = midshin_p, \
            radius = self.CALF_W, \
            mass   = self.CALF_M/2 )
        knee_pitch = self.addLinearVelocityActuatedHingeJoint( \
            body1        = thigh, \
            body2        = calf, \
            anchor       = knee_p, \
            axis         = axis, \
            a1x          = 0.359,\
            a2x          = 0.077,\
            a2y          = 0.116)
        knee_pitch.setParam(ode.ParamLoStop, 0.0)
        knee_pitch.setParam(ode.ParamHiStop, deg2rad*70.8)
        knee_pitch.setForceLimit(maxForce(1.0))
        knee_pitch.setAngleOffset( self.KNEE_OFFSET )
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

        # Create the foot
        # Add the compliant joint
        foot = self.addBody( \
            p1     = midshin_p, \
            p2     = foot_p, \
            radius = self.CALF_W, \
            mass   = self.CALF_M/2 )
        calf_axis  = norm3(sub3(midshin_p, foot_p))
        foot_shock = self.addPrismaticSpringJoint( \
            body1        = calf, \
            body2        = foot, \
            axis         = mul3(calf_axis,-1),\
            spring_const = -5e3,\
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
        self.members      = d
    def getVelocity( self ):
	return (0,0,0)
    def getTotalHydraulicFlowGPM( self ):
        total = 0
        total += abs(self.members['hip_yaw'].getHydraulicFlowGPM())
        total += abs(self.members['hip_pitch'].getHydraulicFlowGPM())
        total += abs(self.members['knee_pitch'].getHydraulicFlowGPM())
        return total
    def jointAnglesFromFootPosition( self, foot_pos ):
        # Calculate hip yaw
        hip_yaw_angle   = -atan2( foot_pos[1], foot_pos[0] )
        # Calculate hip yaw offset
        hip_p = norm2( (foot_pos[0], foot_pos[1]) )
        hip_p = (self.YAW_L*hip_p[0], self.YAW_L*hip_p[1], 0.0)
        # Calculate leg length
        leg_l                    = dist3( foot_pos, hip_p )
        # Use law of cosines on leg length to calculate knee angle 
        knee_angle               = pi-thetaFromABC( self.THIGH_L, self.CALF_L, leg_l )
        # Calculate hip pitch
        hip_offset_angle         = thetaFromABC( self.THIGH_L, leg_l,  self.CALF_L )
        target_p                 = sub3(foot_pos, hip_p)
        hip_depression_angle     = atan2( -target_p[2], len2((target_p[0], target_p[1])) )
        hip_pitch_angle          = hip_depression_angle - hip_offset_angle
        return (hip_yaw_angle, hip_pitch_angle, knee_angle)
    def setDesiredFootPosition( self, position ):
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
    def getPosition( self ):
        return self.members['hip_yaw'].getAnchor()
    def colorJointByTorque( self, joint ):
            b = joint.getBody(1)
            r = abs(joint.getTorque()/joint.getTorqueLimit())
            if r >= 0.99:
                b.color = (0,0,0,255)
            else:
                b.color = (255*r,255*(1-r),0,255)
    def colorShockByDeflection( self, joint ):
            b = joint.getBody(1)
            r = abs(joint.getPosition()/joint.getHiStop())
            if r >= 0.99:
                b.color = (0,0,0,255)
            else:
                b.color = (255*r,255*(1-r),0,255)
    def colorTorque( self ):
        # Color overtorque
        self.colorJointByTorque( self.members['hip_yaw'] )
        self.colorJointByTorque( self.members['hip_pitch'] )
        self.colorJointByTorque( self.members['knee_pitch'] )
        self.colorShockByDeflection( self.members['foot_shock'])
    def update( self ):
        MultiBody.update(self)
