import sys
sys.path.append("..")

import hashlib
import threading
import time

from ControlsKit import logger
from robotControl_pb2 import Command
from socket import socket, AF_INET, SOCK_STREAM, timeout

SOCKET_TIMEOUT = .5

class InputServer:
    """This class takes care of listening for incomming inputs and supplying an appropriate
    update functions to obey the inputs.  It also handles the mapping from raw input values
    to the controls they represent.
    """
    def __init__(self, password="", host='localhost', port=7337):
        self.host = host
        self.port = port
        self.sock = None
        self.conn = None
        self.password = password
        self.server_thread = None
        self.continue_serving = True
        self.last_command = None

    def startListening(self):
        self.continueServing = True
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind( (self.host, self.port) )
        self.sock.settimeout(SOCKET_TIMEOUT)
        self.sock.listen(True)
        self.server_thread = threading.Thread()
        self.server_thread.run = self.serve
        self.server_thread.start()

    def serve(self):
        while self.continue_serving:
            try:
                self.conn, addr = self.sock.accept()
                print "Got connection from " + str(addr)
                self.conn.settimeout(SOCKET_TIMEOUT)
                if self.authorizeConnection():
                    while self.continue_serving:  # redundant check here to quit on Ctrl+C
                        try:
                            proto_bin = self.conn.recv(4096)
                        except timeout:
                            continue  # do nothing, the timeout is only set so we can poll for Ctrl+C
                        if not proto_bin:  # successfully recving no data implies conn closed
                            break  # so break out of the conn specific loop to await another conn
                        command = Command()
                        command.ParseFromString(proto_bin)
                        self.last_command = command
                        if (command.HasField('intended_command') and
                            command.intended_command == Command.DISCONNECT):
                            self.conn.close()
                else:
                    self.conn.close()
                    logger.warning("Invalid login attempt from " + str(addr))
            except timeout:
                pass  # this just means an accept has timed out, which is expected
            except Exception, e:
                logger.error("Controls Server error!", error=e)

    def authorizeConnection(self):
        challenge = str(time.time())
        self.conn.send(challenge)
        response = self.conn.recv(64)
        expected_response = hashlib.sha1(self.password + challenge).hexdigest()
        return response == expected_response

    def stopListening(self):
        self.continue_serving = False
        if self.conn:
            self.conn.close()
        if self.sock:
            self.sock.close()

    def getLastCommand(self):
        return self.last_command


if __name__ == '__main__':
    server = InputServer()
    server.startListening()
    try:
        while server.continue_serving:
            time.sleep(.500)
    except:
        server.stopListening()
