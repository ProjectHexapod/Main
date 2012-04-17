from SimulationKit.MultiBody import MultiBody
from SimulationKit.helpers import *
from SimulationKit.pubsub import *
import ode

class LegOnStand(MultiBody):
    YAW_W   = 0.15
    THIGH_W = 0.10
    CALF_W  = 0.10
    YAW_L   = 0.211
    THIGH_L = 1.372
    CALF_L  = 1.283

    # TODO(dan): accurate masses
    LIN_DENS = 15.0  # kg/m
    YAW_M   = LIN_DENS * YAW_L
    THIGH_M = LIN_DENS * THIGH_L
    CALF_M  = LIN_DENS * CALF_L
    
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
        hip_yaw = self.addLinearVelocityActuatedHingeJoint( \
            body1        = ode.environment, \
            body2        = yaw_link, \
            anchor       = yaw_p, \
            axis         = (0,0,1),\
            a1x          = 0.368,\
            a2x          = 0.076,\
            a2y          = 0.086)
        hip_yaw.setForceLimit(maxForce(1.0))
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
            radius = self.THIGH_W, \
            mass   = self.THIGH_M )
        hip_pitch = self.addLinearVelocityActuatedHingeJoint( \
            body1        = yaw_link, \
            body2        = thigh, \
            anchor       = hip_p, \
            axis         = axis, \
            a1x          = 0.359,\
            a2x          = 0.116,\
            a2y          = 0.077)
        hip_pitch.setParam(ode.ParamLoStop, -pi/3)
        hip_pitch.setParam(ode.ParamHiStop, +pi/3)
        p1 = mul3( p, self.YAW_L )
        p1 = (p1[0], p1[1], 0.355)
        p2 = mul3( p, self.YAW_L+self.THIGH_L/2 )
        hip_pitch.setForceLimit(maxForce(1.5))
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
            radius = self.CALF_W, \
            mass   = self.CALF_M )
        knee_pitch = self.addLinearVelocityActuatedHingeJoint( \
            body1        = thigh, \
            body2        = calf, \
            anchor       = knee_p, \
            axis         = axis, \
            a1x          = 0.203,\
            a2x          = 0.203,\
            a2y          = 0.279)
        knee_pitch.setParam(ode.ParamLoStop, -2*pi/3)
        knee_pitch.setParam(ode.ParamHiStop, 0.0)
        p1 = mul3( p, self.YAW_L+(self.THIGH_L/4) )
        p1 = (p1[0], p1[1], -0.1)
        p2 = mul3( p, self.YAW_L+self.THIGH_L-.355 )
        knee_pitch.setForceLimit(maxForce(1.0))
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
    def getVelocity( self ):
	return (0,0,0)
    def getTotalHydraulicFlowGPM( self ):
        total = 0
        total += abs(self.members['hip_yaw'].getHydraulicFlowGPM())
        total += abs(self.members['hip_pitch'].getHydraulicFlowGPM())
        total += abs(self.members['knee_pitch'].getHydraulicFlowGPM())
        return total
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
        return self.offset
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
