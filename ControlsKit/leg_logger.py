import sys
sys.path.append('..')

import logging
import logging.handlers
from SimulationKit.pubsub import Publisher
from collections import defaultdict


class LegLog():
    def __init__(self):
        self.logger = logging.getLogger("hexapod")
        self.logger.setLevel(logging.DEBUG)

        csv = logging.Formatter("%(time)s,%(hip_yaw_command)s,%(hip_pitch_command)s,%(knee_pitch_command)s,%(hip_yaw_angle)s,%(hip_pitch_angle)s,%(knee_pitch_angle)s,%(shock_depth)s,%(hip_yaw_rate)s,%(hip_pitch_rate)s,%(knee_pitch_rate)s")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(csv)
        self.logger.addHandler(console_handler)

        socket_handler = logging.handlers.SocketHandler("127.0.0.1", 9020)  # default port
        socket_handler.setLevel(logging.INFO)
        self.logger.addHandler(socket_handler)

        file_handler = logging.FileHandler("eventLog.csv")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(csv)
        self.logger.addHandler(file_handler)

        self.state = {} 
        self.state["time"] = "Not set"
        self.state["hip_yaw_rate"] =  "Not set"
        self.state["hip_pitch_rate"] =  "Not set"
        self.state["knee_pitch_rate"] =  "Not set"
        self.state["hip_yaw_angle"] =  "Not set"
        self.state["hip_pitch_angle"] =  "Not set"
        self.state["knee_pitch_angle"] =  "Not set"
        self.state["shock_depth"] =  "Not set"
        self.state["hip_yaw_command"] =  "Not set"
        self.state["hip_pitch_command"] =  "Not set"
        self.state["knee_pitch_command"] =  "Not set"
        self.state[""] =  "Not set"

        self.next_publisher_port = 5056
        self.publisher = self.createPublisher(['time', 'hip_yaw_rate', 'hip_pitch_rate', 'knee_pitch_rate', 'hip_yaw_angle', 'hip_pitch_angle', 'knee_pitch_angle', 'shock_depth'])

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name[:3] == 'get' and name[4:] in self.state:
            return lambda: self.state[name]
        else:
            raise AttributeError(name+" not a get request or key not found.")

    def createPublisher(self, values_to_publish):
        pub = Publisher(self.next_publisher_port)
        self.next_publisher_port += 1
        for val in values_to_publish:
            pub.addToCatalog("logging."+val, self.__getattr__("get_"+val))
        pub.start()
        return pub

    def populate_state(self, kwargs):
        for k in kwargs:
            self.state[k] = kwargs[k]

    def debug(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.debug(msg.format(args), extra=self.state)

    def info(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.info(msg.format(args), extra=self.state)

    def warning(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.warning(msg.format(args), extra=self.state)

    def error(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.error(msg.format(args), extra=self.state)

    def critical(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.critical(msg.format(args), extra=self.state)

logger = LegLog()

