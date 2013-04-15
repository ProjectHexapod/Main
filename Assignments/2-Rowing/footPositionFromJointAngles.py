from transformations import *


def footPositionFromJointAngles(hip_yaw_angle, hip_pitch_angle, knee_angle, foot_extension, robot):
    yawTransform = multiplyMatrices(createRotation((0.0, 0.0, 1.0), hip_yaw_angle),
                                    createTranslation((robot.YAW_L, 0.0, 0.0)))

    hipTransform = multiplyMatrices(createRotation((0.0, 1.0, 0.0), hip_pitch_angle),
                                    createTranslation((robot.THIGH_L, 0.0, 0.0)))

    kneeTransform = multiplyMatrices(createRotation((0.0, 1.0, 0.0), knee_angle),
                                     createTranslation((robot.CALF_L - foot_extension, 0.0, 0.0)))

    return multiplyMatrixVector(multiplyMatrices(yawTransform, hipTransform, kneeTransform), (0, 0, 0))
