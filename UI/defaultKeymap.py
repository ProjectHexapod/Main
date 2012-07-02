from robotControl_pb2 import Command

def getPlannerName(command):
    if command.controller == Command.PS3_CONTROLLER:
        for axis in command.raw_command:
            if axis.index == 15 and axis.value == 1:  # Square
                return "row_the_cart"

    # TODO: add more controls
    return "hold_position"
