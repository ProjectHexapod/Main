from SimulationKit.MultiBody import MultiBody, LinearVelocityActuatedHingeJoint
from SimulationKit.helpers import *
from Utilities.pubsub import *
from SimulationKit.OpenGLLibrary import *
from math import *
import ode
from Utilities.ActuatorCharacteristics import *

# Convenience multipliers...
deg2rad    = pi/180
psi2pascal = 6894.76
inch2meter = 2.54e-2
pound2kilo = 0.455
gpm2cmps = 1/15850.4

class StompyLegPhysicalCharacteristics(object):
    """
    This class contains the physical characteristics of one of
    Stompy's legs
    """
    def __init__(self):
        self.YAW_L   = inch2meter*10.0 # Length of yaw link
        self.YAW_W   = 0.1             # Diameter of yaw link
        self.THIGH_L = inch2meter*54.0 # Length of thigh link
        self.THIGH_W = 0.1             # Diameter of thigh link
        self.CALF_L  = inch2meter*78.0 # Length of calf link
        self.CALF_W  = 0.1             # Diameter of calf link
        self.YAW_M   = pound2kilo*20   # Yaw link mass
        self.THIGH_M = pound2kilo*200  # Thigh link mass
        self.CALF_M  = pound2kilo*150  # Calf link mass

        # Describe the actuator placements at each joint
        self.YAW_ACT    = ActuatorCharacteristics(
                bore_diameter          = inch2meter*2.5,
                rod_diameter           = inch2meter*1.125,
                act_retracted_len      = inch2meter*14.25,
                act_extended_len       = inch2meter*18.25,
                pivot1_dist_from_joint = inch2meter*16.18,
                pivot2                 = (inch2meter*2.32,inch2meter*3.3),
                ang_offset             = deg2rad*-30.0,
                system_pressure        = psi2pascal*2300,
                axis                   = ( 0, 0, -1 ) )

        self.PITCH_ACT  = ActuatorCharacteristics(
                bore_diameter          = inch2meter*3.0,
                rod_diameter           = inch2meter*1.5,
                act_retracted_len      = inch2meter*20.25,
                act_extended_len       = inch2meter*30.25,
                pivot1_dist_from_joint = inch2meter*8.96,
                pivot2                 = (inch2meter*27.55,inch2meter*8.03),
                ang_offset             = deg2rad*-84.0,
                system_pressure        = psi2pascal*2300,
                axis                   = ( 0, -1, 0 ) )

        self.KNEE_ACT   = ActuatorCharacteristics(
                bore_diameter          = inch2meter*2.5,
                rod_diameter           = inch2meter*1.25,
                act_retracted_len      = inch2meter*22.25,
                act_extended_len       = inch2meter*34.25,
                pivot1_dist_from_joint = inch2meter*28.0,
                pivot2                 = (inch2meter*4.3,inch2meter*6.17),
                ang_offset             = deg2rad*61.84,
                system_pressure        = psi2pascal*2300,
                axis                   = ( 0, -1, 0 ) )
        #self.KNEE_ACT.BORE_DIAMETER           = inch2meter*2.5
        #self.KNEE_ACT.ROD_DIAMETER            = inch2meter*1.25
        #self.KNEE_ACT.ACT_RETRACTED_LEN       = inch2meter*22.250
        #self.KNEE_ACT.ACT_EXTENDED_LEN        = inch2meter*34.250
        #self.KNEE_ACT.PIVOT1_DIST_FROM_JOINT  = inch2meter*28
        #self.KNEE_ACT.PIVOT2                  = (inch2meter*4.3,inch2meter*6.17)
        #self.KNEE_ACT.ANG_OFFSET              = deg2rad*61.84
        #self.KNEE_ACT.SYSTEM_PRESSURE         = psi2pascal*2300
        #self.KNEE_ACT.AXIS                    = (0,-1,0)

        # Compliance of foot
        self.COMPLIANCE_K   = 87560  # newtons/meter deflection of foot = 1000 pounds/2 inches
        self.COMPLIANCE_LEN = 0.06  # how long til it bottoms out
        # Leg origin from robot origin, expressed in Stompy's coordinate frame
        self.OFFSET_FROM_ROBOT_ORIGIN   = (0,0,0)
        # Row major 3x3 rotation matrix
        # calcRotMatrix takes an axis and an angle
        self.ROTATION_FROM_ROBOT_ORIGIN = calcRotMatrix( (0,0,1), 0.0 )
    def setRotation( self, axis, angle ):
        """
        Sets the rotation of the leg in space.
        Axis is a 3-vector, angle is a scalar in radians
        """
        rot_matrix = calcRotMatrix( axis, angle )
        self.ROTATION_FROM_ROBOT_ORIGIN = rot_matrix

class ValveActuatedHingeJoint(LinearVelocityActuatedHingeJoint):
    """
    This class simulates an actuator attached to a hinge joint controlled by a spool valve.
    The valve being modeled is a Hydraforce SP10-47C
    """
    def __init__(self, sim, actuator_characteristics=None):
        #super(ValveActuatedHingeJoint, self).__init__(sim)
        LinearVelocityActuatedHingeJoint.__init__( self, sim )
        self.valve_command = 0.0
        self.actuator = actuator_characteristics

    def SP10_47CFlow( self, inlet_to_work_port_pressure, valve_command ):
        """
        Returns the flow to the work port in an SP10-47C spool valve
        given the inlet to work port pressure and the valve command.
        Pressure in pascal
        Valve command is float from 0 to 1, 0 being close, 1 being full open
        Returns flow in cubic meter/sec

        This is rough piecewise linear interpretation of the charts at:
        http://www.hydraforce.com/proport/Prop_html/2-112-1_SP10-47C/2-112-1_SP10-47C.htm
        """
        if valve_command > 1.0:
            valve_command = 1.0
        if inlet_to_work_port_pressure < psi2pascal*300:
            normalized_flow = (gpm2cmps*6.0)*(inlet_to_work_port_pressure/(psi2pascal*300.0))
        else:
            normalized_flow = (gpm2cmps*6.0) - ((inlet_to_work_port_pressure-(psi2pascal*300.0))*((gpm2cmps*1.5)/(psi2pascal*1700)))

        if normalized_flow < 0:
            normalized_flow = 0

        if valve_command > 0.25:
            normalized_command = (valve_command - .25)/0.75
        else:
            normalized_command = 0.0
        retval = normalized_command * normalized_flow
        return retval

    def getAngRate( self ):
        # Calculate the pressure on the work side of the actuator
        torque = self.getTorque()
        force = torque / self.getLeverArm()
        if self.valve_command > 0.0:
            cross_section = self.actuator.getExtensionCrossSectionM2()
        else:
            cross_section = self.actuator.getRetractionCrossSectionM2()
        if sign(self.valve_command) != sign(torque):
            # We are pulling against the work side
            work_pressure = 0.0
        else:
            work_pressure = force / cross_section
        inlet_to_work_pressure = self.actuator.SYSTEM_PRESSURE - abs(work_pressure)
        flow = self.SP10_47CFlow( inlet_to_work_pressure, abs(self.valve_command) )
        lenrate = (flow / cross_section)
        if self.valve_command<0:
            lenrate *= -1
        ang_vel = lenrate / self.getLeverArm()
        if self.getBody(0) == ode.environment:
            ang_vel = -1*ang_vel
        return ang_vel

    def setLengthRate(self, vel_mps):
        raise NotImplemented, "Cannot set Length Rate directly on a ValveActuatedHingeJoint"
    
    def setValveCommand( self, command ):
        """
        command is float between 1 and -1.  1 is full extend, -1 full retract.
        """
        if command > 1:
            command = 1
        elif command < -1:
            command = -1
        self.valve_command = command

import os.path as path
graphics_dir = path.dirname(path.realpath(__file__))+'/graphics'

class IIR(object):
    def __init__(self, k=.9, t_init=0, t_const=1):
        """
        By default, absorb .9 of the update value in 1 second
        """
        self.k = k**(1/t_const)
        self.state = 0.0
        self.t = t_init
    def getVal(self):
        return self.state
    def update(self, val, t):
        dt = t-self.t
        adjusted_k = self.k**dt
        self.state *= adjusted_k
        self.state += (1-adjusted_k)*val
        self.t = t

class LegOnColumn(MultiBody):
    def __init__( self, *args, **kwargs ):
        self.dimensions = StompyLegPhysicalCharacteristics()
        super(self.__class__, self).__init__(*args, **kwargs)
        self.foot_IIR = IIR(k=.9,t_const=0.2,t_init=self.sim.getSimTime())
        self.flow_IIR = IIR(k=.5, t_const=1.0, t_init=self.sim.getSimTime())
    def buildBody( self ):
        """ Build a hexapod according to the dimensions laid out
        in self.dimensions """
        # This is the constant offset for aligning with the physics element
        # This is a 4x4 opengl style matrix, expressing an offset and a rotation
        self.publisher.addToCatalog(\
            "body.totalflow_gpm",\
            self.getTotalHydraulicFlowGPM)
        self.publisher.addToCatalog(\
            "body.totalflow_gpm_filt",\
            self.getTotalHydraulicFlowGPMFiltered)

        yaw_act_dim   = self.dimensions.YAW_ACT
        pitch_act_dim = self.dimensions.PITCH_ACT
        knee_act_dim  = self.dimensions.KNEE_ACT
        hip_offset    = self.dimensions.OFFSET_FROM_ROBOT_ORIGIN
        leg_rot       = self.dimensions.ROTATION_FROM_ROBOT_ORIGIN
        # Anchor of the hip yaw
        yaw_p         = hip_offset
        # Anchor of the hip pitch
        hip_p         = mul3( (1,0,0), self.dimensions.YAW_L )
        hip_p         = rotateAxisAngle( hip_p, \
            yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
        hip_p         = rotate3( leg_rot, hip_p )
        hip_p         = add3(hip_p, yaw_p)
        # Anchor of the knee
        knee_p         = mul3( (1,0,0), self.dimensions.THIGH_L )
        knee_p         = rotateAxisAngle( knee_p, \
            pitch_act_dim.AXIS, -pitch_act_dim.ANG_OFFSET )
        knee_p         = rotateAxisAngle( knee_p, \
            yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
        knee_p         = rotate3( leg_rot, knee_p )
        knee_p         = add3(knee_p, hip_p)
        # Anchor of the foot
        foot_p         = mul3( (1,0,0), self.dimensions.CALF_L )
        foot_p         = rotateAxisAngle( foot_p, \
            knee_act_dim.AXIS, -knee_act_dim.ANG_OFFSET )
        foot_p         = rotateAxisAngle( foot_p, \
            pitch_act_dim.AXIS, -pitch_act_dim.ANG_OFFSET )
        foot_p         = rotateAxisAngle( foot_p, \
            yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
        foot_p         = rotate3( leg_rot, foot_p )
        foot_p         = add3(foot_p, knee_p)
        # Calculate the middle of the shin so we can place our shock joint
        midshin_p = div3(add3(foot_p, knee_p), 2)

        # Add hip yaw
        act_axis = rotate3(leg_rot,yaw_act_dim.AXIS)
        yaw_link = self.addBody( \
            p1     = yaw_p, \
            p2     = hip_p, \
            radius = self.dimensions.YAW_W, \
            mass   = self.dimensions.YAW_M,\
            collide= False)
        # glObjPath will be used by the simulator to populate the body
        yaw_link.glObjPath   = graphics_dir+'/Yaw.obj'
        # This is the constant offset for aligning with the physics element
        # This is a 4x4 opengl style matrix, expressing an offset and a rotation
        offset = (-1.52,+.13,-0.15)
        rot    = calcRotMatrix( (0,1,0), 3*pi/2 )
        scale = (39,39,39)
        yaw_link.glObjOffset = makeOpenGLMatrix( rot, offset, scale )
        yaw_link.shape = 'capsule'
        yaw_transfer = self.addTransferBody(yaw_p)
        hip_yaw = self.addLinearVelocityActuatedHingeJoint( \
            body1  = ode.environment,\
            body2  = yaw_transfer,\
            anchor = yaw_p,\
            axis   = act_axis,\
            a1x    = yaw_act_dim.PIVOT1_DIST_FROM_JOINT,\
            a2x    = yaw_act_dim.PIVOT2[0],\
            a2y    = yaw_act_dim.PIVOT2[1],\
            subclass = ValveActuatedHingeJoint)
        hip_yaw_backlash = self.addSpringyHingeJoint(\
            body1  = yaw_transfer,\
            body2  = yaw_link,\
            anchor = yaw_p,\
            axis   = act_axis,\
            bounce = 0.8,\
            loStop = -1.25*deg2rad,\
            hiStop =  1.25*deg2rad,\
            spring_const = -2e1,
            damping      = -2e2)
        hip_yaw.actuator = yaw_act_dim
        #hip_yaw.setParam(ode.ParamLoStop, 0.0)
        hip_yaw.setParam(ode.ParamLoStop, -yaw_act_dim.getRangeOfMotion())
        hip_yaw.setParam(ode.ParamHiStop, 0.0)
        #hip_yaw.setParam(ode.ParamHiStop, yaw_act_dim.getRangeOfMotion())
        hip_yaw.setExtendForceLimit(yaw_act_dim.getMaxExtensionForceNewtons())
        hip_yaw.setRetractForceLimit(yaw_act_dim.getMaxRetractionForceNewtons())
        hip_yaw.setExtendCrossSection(yaw_act_dim.getExtensionCrossSectionM2())
        hip_yaw.setRetractCrossSection(yaw_act_dim.getRetractionCrossSectionM2())
        hip_yaw.setMaxHydraulicFlow(gpm2cmps*5)
        hip_yaw.setAngleOffset(yaw_act_dim.ANG_OFFSET )

        # Add thigh and hip pitch
        # Calculate the axis of rotation for hip pitch
        act_axis   = rotateAxisAngle( pitch_act_dim.AXIS, \
            yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
        act_axis = rotate3(leg_rot,act_axis)
        thigh = self.addBody(\
            p1     = hip_p, \
            p2     = knee_p, \
            radius = self.dimensions.THIGH_W, \
            mass   = self.dimensions.THIGH_M,\
            collide= False)
        # glObjPath will be used by the simulator to populate the body
        thigh.glObjPath   = graphics_dir+'/Thigh.obj'
        # This is the constant offset for aligning with the physics element
        # This is a 4x4 opengl style matrix, expressing an offset and a rotation
        offset = (0.09,0.10,-2.23)
        rot    = calcRotMatrix( (0,0,1), pi )
        rot2   = calcRotMatrix( (0,1,0), -pi/26 )
        rot3   = calcRotMatrix( (1,0,0), pi )
        rot    = mul3x3Matrices( rot, rot2 ) 
        rot    = mul3x3Matrices( rot, rot3 ) 
        scale  = (39,39,39)
        thigh.glObjOffset = makeOpenGLMatrix( rot, offset, scale )
        thigh.shape = 'capsule'
        thigh_transfer = self.addTransferBody( hip_p )
        hip_pitch = self.addLinearVelocityActuatedHingeJoint( \
            body1  = yaw_link, \
            body2  = thigh_transfer, \
            anchor = hip_p, \
            axis   = act_axis, \
            a1x    = pitch_act_dim.PIVOT1_DIST_FROM_JOINT,\
            a2x    = pitch_act_dim.PIVOT2[0],\
            a2y    = pitch_act_dim.PIVOT2[1],\
            subclass = ValveActuatedHingeJoint)
        hip_pitch_backlash = self.addSpringyHingeJoint(\
            body1  = thigh_transfer,\
            body2  = thigh,\
            anchor = yaw_p,\
            axis   = act_axis,\
            bounce = 0.5,\
            loStop = -1.0*deg2rad,\
            hiStop =  1.0*deg2rad,\
            spring_const = 0.0,
            damping      = 0.0)
        hip_pitch.actuator = pitch_act_dim
        hip_pitch.setParam(ode.ParamLoStop, 0.0)
        hip_pitch.setParam(ode.ParamHiStop, pitch_act_dim.getRangeOfMotion())
        hip_pitch.setExtendForceLimit(pitch_act_dim.getMaxExtensionForceNewtons())
        hip_pitch.setRetractForceLimit(pitch_act_dim.getMaxRetractionForceNewtons())
        hip_pitch.setExtendCrossSection(pitch_act_dim.getExtensionCrossSectionM2())
        hip_pitch.setRetractCrossSection(pitch_act_dim.getRetractionCrossSectionM2())
        hip_pitch.setMaxHydraulicFlow(gpm2cmps*5)
        hip_pitch.setAngleOffset(pitch_act_dim.ANG_OFFSET )

        # Add calf and knee bend
        act_axis   = rotateAxisAngle( knee_act_dim.AXIS, \
            pitch_act_dim.AXIS, -pitch_act_dim.ANG_OFFSET )
        act_axis   = rotateAxisAngle( act_axis, \
            yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
        act_axis = rotate3(leg_rot,act_axis)
        calf = self.addBody( \
            p1     = knee_p, \
            p2     = midshin_p, \
            radius = self.dimensions.CALF_W, \
            mass   = self.dimensions.CALF_M/2.0 )
        # glObjPath will be used by the simulator to populate the body
        calf.glObjPath   = graphics_dir+'/Calf.obj'
        # This is the constant offset for aligning with the physics element
        # This is a 4x4 opengl style matrix, expressing an offset and a rotation
        offset = (-0.45,0.11,2.35)
        rot    = calcRotMatrix( (0,0,1), 0 )
        scale  = (39,39,39)
        calf.glObjOffset = makeOpenGLMatrix( rot, offset, scale )
        calf.shape = 'capsule'
        calf_transfer = self.addTransferBody( knee_p )
        knee_pitch = self.addLinearVelocityActuatedHingeJoint( \
            body1  = thigh, \
            body2  = calf_transfer, \
            anchor = knee_p, \
            axis   = act_axis, \
            a1x    = knee_act_dim.PIVOT1_DIST_FROM_JOINT,\
            a2x    = knee_act_dim.PIVOT2[0],\
            a2y    = knee_act_dim.PIVOT2[1],\
            subclass = ValveActuatedHingeJoint)
        knee_pitch_backlash = self.addSpringyHingeJoint(\
            body1  = calf_transfer,\
            body2  = calf,\
            anchor = yaw_p,\
            axis   = act_axis,\
            bounce = 0.5,\
            loStop = -1.0*deg2rad,\
            hiStop =  1.0*deg2rad,\
            spring_const = 0.0,
            damping      = 0.0)
        knee_pitch.actuator = knee_act_dim
        knee_pitch.setParam(ode.ParamLoStop, 0.0)
        knee_pitch.setParam(ode.ParamHiStop, knee_act_dim.getRangeOfMotion())
        knee_pitch.setExtendForceLimit(knee_act_dim.getMaxExtensionForceNewtons())
        knee_pitch.setRetractForceLimit(knee_act_dim.getMaxRetractionForceNewtons())
        knee_pitch.setExtendCrossSection(knee_act_dim.getExtensionCrossSectionM2())
        knee_pitch.setRetractCrossSection(knee_act_dim.getRetractionCrossSectionM2())
        knee_pitch.setMaxHydraulicFlow(gpm2cmps*5)
        knee_pitch.setAngleOffset(knee_act_dim.ANG_OFFSET )

        # Create the foot
        # Add the compliant joint
        act_axis   = rotateAxisAngle( knee_act_dim.AXIS, \
            knee_act_dim.AXIS, -knee_act_dim.ANG_OFFSET )
        act_axis   = rotateAxisAngle( act_axis, \
            pitch_act_dim.AXIS, -pitch_act_dim.ANG_OFFSET )
        act_axis   = rotateAxisAngle( act_axis, \
            yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
        act_axis = rotate3(leg_rot,act_axis)
        foot = self.addBody( \
            p1     = midshin_p, \
            p2     = foot_p, \
            radius = self.dimensions.CALF_W, \
            mass   = self.dimensions.CALF_M/2 )
        # glObjPath will be used by the simulator to populate the body
        foot.glObjPath   = graphics_dir+'/Compliant.obj'
        # This is the constant offset for aligning with the physics element
        # This is a 4x4 opengl style matrix, expressing an offset and a rotation
        offset = (-0.55,0.06,1.5)
        rot    = calcRotMatrix( (0,0,1), 0 )
        scale  = (39,39,39)
        foot.glObjOffset = makeOpenGLMatrix( rot, offset, scale )
        foot.shape = 'capsule'
        calf_axis  = norm3(sub3(midshin_p, foot_p))
        foot_shock = self.addPrismaticSpringJoint( \
            body1        = calf, \
            body2        = foot, \
            axis         = mul3(calf_axis,-1),\
            #spring_const = 0,\
            spring_const = -80e3,\
            hi_stop      = 0.1,\
            lo_stop      = 0.0,\
            neutral_position = 0.0,\
            damping          = -6e3)
        def populatePublisher( dof_name, joint, backlash ):
            self.publisher.addToCatalog(\
                "%s.torque"%(dof_name),\
                joint.getTorque)
            self.publisher.addToCatalog(\
                "%s.torque_lim"%(dof_name),\
                joint.getTorqueLimit)
            self.publisher.addToCatalog(\
                "%s.ang"%(dof_name),\
                lambda: joint.getAngle()+backlash.getAngle())
            self.publisher.addToCatalog(\
                "%s.ang_deg"%(dof_name),\
                lambda: (joint.getAngle()+backlash.getAngle())/deg2rad)
            self.publisher.addToCatalog(\
                "%s.bl_pos_deg"%(dof_name),\
                lambda: backlash.getAngle()/deg2rad)
            self.publisher.addToCatalog(\
                "%s.len"%(dof_name),\
                joint.getLength)
            self.publisher.addToCatalog(\
                "%s.len_rate"%(dof_name),\
                joint.getLengthRate)
            self.publisher.addToCatalog(\
                "%s.flow_gpm"%(dof_name),\
                joint.getHydraulicFlowGPM)
            #self.publisher.addToCatalog(\
            #    "%s.lever_arm"%(dof_name),\
            #    joint.getLeverArm)
            #self.publisher.addToCatalog(\
            #    "%s.extend_force"%(dof_name),\
            #    joint.getExtendForceLimit)
            #self.publisher.addToCatalog(\
            #    "%s.retract_force"%(dof_name),\
            #    joint.getRetractForceLimit)
            self.publisher.addToCatalog(\
                "%s.ang_target"%(dof_name),\
                joint.getAngleTarget)

        populatePublisher('hy' , hip_yaw    , hip_yaw_backlash)
        populatePublisher('hp' , hip_pitch  , hip_pitch_backlash)
        populatePublisher('kp' , knee_pitch , knee_pitch_backlash)
        self.publisher.addToCatalog(\
            "fs.shock_deflection",\
            foot_shock.getPosition)
            
        d                 = {}
        d['hip_yaw']      = hip_yaw
        d['hip_pitch']    = hip_pitch
        d['knee_pitch']   = knee_pitch
        d['foot_shock']   = foot_shock
        d['hip_yaw_bl']   = hip_yaw_backlash
        d['hip_pitch_bl'] = hip_pitch_backlash
        d['knee_pitch_bl']= knee_pitch_backlash
        d['hip_yaw_link'] = yaw_link
        d['thigh']        = thigh
        d['calf']         = calf
        d['foot']         = foot
        self.joints       = d
    def getEncoderAngleMatrix( self ):
        """
        Returns a list of tuples containing the joint angles at each joint.
        Outer index is leg index
        Inner index is joint index
        So retval[0][0] is hip yaw for leg 0,
        retval[1][0] is hip yaw for leg 1,
        retval[0][2] is knee angle for leg 0, etc.
        """
        retval = []
        for i in range(6):
            retval.append( (\
                self.joints['hip_yaw'].getAngle(),\
                self.joints['hip_pitch'].getAngle(),\
                self.joints['knee_pitch'].getAngle(),\
                self.joints['foot_shock'].getPosition()) )
        return retval
    def setLenRateMatrix( self, len_rate_matrix ):
        """
        Provides an interface to set the length rates of the actuators
        at all joints at the same time.
        len_rate_matrix outer indices are leg indices
        inner indices specify joints
        len_rate_matrix[0][1] is leg 0 hip pitch
        len_rate_matrix[1][2] is leg 1 knee pitch
        """
        for i in range(6):
            self.joints['hip_yaw'   ].setLengthRate(len_rate_matrix[i][0])
            self.joints['hip_pitch' ].setLengthRate(len_rate_matrix[i][1])
            self.joints['knee_pitch'].setLengthRate(len_rate_matrix[i][2])
    def getTotalHydraulicFlowGPM( self ):
        total = 0
        for i in range(6):
            total += abs(self.joints['hip_yaw'].getHydraulicFlowGPM())
            total += abs(self.joints['hip_pitch'].getHydraulicFlowGPM())
            total += abs(self.joints['knee_pitch'].getHydraulicFlowGPM())
        return total
    def getTotalHydraulicFlowGPMFiltered( self ):
        self.flow_IIR.update(self.getTotalHydraulicFlowGPM(), self.sim.getSimTime())
        return self.flow_IIR.getVal()
    def setDesiredFootPositions( self, positions ):
        """
        positions should be a 3-vector in the robot coordinate frame
        """
        yaw_p = self.dimensions.OFFSET_FROM_ROBOT_ORIGIN
        # Move the target point from the robot coordinate frame
        # to the leg coordinate frame
        target_p         = sub3(target_p, yaw_p)
        rot              = invert3x3(self.dimensions.ROTATION_FROM_ROBOT_ORIGIN)
        target_p         = rotate3( rot, target_p )
        # Calculate hip yaw target angle
        hip_yaw_angle    = atan2( target_p[1], target_p[0] )
        # Move target_p to the coordinate frame based at hip pitch
        target_p = rotateAxisAngle( target_p,\
            self.dimensions.YAW_ACT.AXIS, hip_yaw_angle )
        target_p         = sub3( target_p, (self.dimensions.YAW_L,0,0) )
        # Assign outputs
        # Calculate leg length
        leg_l            = len3( target_p )
        # Compensate for shock in shin length
        # Low pass the shock deflection to prevent bouncing
        shock_deflection = self.joints['foot_shock'].getPosition()
        self.foot_IIR.update(shock_deflection, self.sim.getSimTime())
        shock_deflection = self.foot_IIR.getVal()
        calf_l = self.dimensions.CALF_L-shock_deflection
        # Use law of cosines on leg length to calculate knee angle 
        knee_angle       = pi-thetaFromABC(\
            self.dimensions.THIGH_L,\
            calf_l, leg_l )
        # Calculate hip pitch
        knee_comp_angle  = thetaFromABC( leg_l, self.dimensions.THIGH_L, self.dimensions.CALF_L )
        depression_angle = -atan2(target_p[2], target_p[0])
        hip_pitch_angle  = depression_angle-knee_comp_angle
        def controlLenRate( joint, target_ang, gain=10.0 ):
            error = target_ang - joint.getAngle()
            joint.setLengthRate( error*gain )
            joint.setAngleTarget(target_ang)
        controlLenRate(self.joints['hip_yaw'   ],  hip_yaw_angle   )
        controlLenRate(self.joints['hip_pitch' ],  hip_pitch_angle )
        controlLenRate(self.joints['knee_pitch'],  knee_angle      )
    def getBodyHeight( self ):
        return self.core.getPosition()[2]
    def getPosition( self ):
        return self.offset
        #return self.core.getPosition()
    def getAcceleration( self ):
        return div3(self.core.getForce(), self.dimensions.BODY_M) # FIXME: Returns (0,0,0)
    def getOrientation( self ):
        return self.core.getRotation()
    def getAngularRates( self ):
        return self.core.getAngularVel()
    def getVelocity( self ):
        return self.core.getLinearVel()
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
        # Color overtorque
        self.colorJointByTorque(     self.joints['hip_yaw'] )
        self.colorJointByTorque(     self.joints['hip_pitch'] )
        self.colorJointByTorque(     self.joints['knee_pitch'] )
        self.colorShockByDeflection( self.joints['foot_shock'])
    def update( self ):
        MultiBody.update(self)
