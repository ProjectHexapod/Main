import logging
import logging.handlers

class LegLog():
    def __init__(self):
        self.logger = logging.getLogger("hexapod")
        self.logger.setLevel(logging.DEBUG)

        csv = logging.Formatter("%(time)s,%(hip_yaw_rate)s,%(hip_pitch_rate)s,%(knee_pitch_rate)s,%(hip_yaw_angle)s,%(hip_pitch_angle)s,%(knee_pitch_angle)s,%(shock_depth)s")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(csv)
        self.logger.addHandler(console_handler)

        socket_handler = logging.handlers.SocketHandler("127.0.0.1", 9020)  # default port
        socket_handler.setLevel(logging.INFO)
        self.logger.addHandler(socket_handler)

        file_handler = logging.FileHandler("gimpy.csv")
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

