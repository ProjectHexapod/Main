import hashlib
import random
import threading

from ControlsKit import logger
from robotControl_pb2 import Command

class InputServer:
    """This class takes care of listening for incomming inputs and supplying an appropriate
    update functions to obey the inputs.  It also handles the mapping from raw input values
    to the controls they represent.
    """
    def __init__(self, host='localhost', port=7337, password=None):
        self.host = host
        self.port = port
        self.sock = None
        self.conn = None
        self.password = password  #  TODO: use this field
        self.serverThread = None
        self.continueServing = True

    def startListening(self):
        self.continueServing = True
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind( (host, port) )
        self.sock.listen(True)
        self.serverThread = threading.Thread()
        self.serverThread.run = self.serve
        self.serverThread.start()

    def serve(self):
        while self.continueServing:
            try:
                self.conn = self.sock.accept()
                if self.authorizeConnection():
                    continueConnection = True
                    while continueConnection:
                        command = Command()
                        command.ParseFromString(self.conn.recv(4096))
                        self.handleCommand(command)
                        if (command.HasField('intended_command') and
                            command.intended_command == Command.DISCONNECT):
                            continueConnection = False
                else:
                    self.conn.close()
                    logger.warning("Invalid login attempt!")
            except error, msg:
                logger.error(msg, error=error)

    def authorizeConnection(self):
        try:
            challenge = str(random.random())
            self.conn.send(challenge)
            response = self.conn.recv(64)
            expected_response = hashlib.sha1(self.password + challenge).hexdigest()
            return response == expected_response
        except error, msg:
            logger.error(msg, error=error)
            return False

    def handleCommand(self, command):
        if command.HasField('intended_command'):
            # TODO: switch on command.intended_command and map to planners appropriately
            pass
        elif command.HasField('raw_command'):
            # TODO: use the controls dictionary to look up the mapping from raw commands
            # to intended_commands, and then set the appropriate planner
            pass

    def stopListening(self):
        self.continueServing = False
        self.conn.close()
        self.sock.close()

    def getUpdateFunction(self):
        pass
