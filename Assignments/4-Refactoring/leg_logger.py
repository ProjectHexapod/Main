import logging

class LegLog():
    def __init__(self):
        self.logger = logging.getLogger("hexapod")
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.setHandler(self.console_handler

        self.state = {}

    def populate_state(self, kwargs):
        for k,v in kwargs:
            self.state[k] = v

    def debug(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.debug(msg, args, extra=self.state)

    def info(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.info(msg, args, extra=self.state)

    def warning(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.warning(msg, args, extra=self.state)

    def error(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.error(msg, args, extra=self.state)

    def critical(self, msg, *args, **kwargs):
        self.populate_state(kwargs)
        self.logger.critical(msg, args, extra=self.state)

logger = LegLog()

