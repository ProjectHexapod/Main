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
    def __init__(self, input_handler, password="", host='localhost', port=7337):
        self.host = host
        self.port = port
        self.sock = None
        self.conn = None
        self.password = password
        self.serverThread = None
        self.continueServing = True
        self.input_handler = input_handler

    def startListening(self):
        self.continueServing = True
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind( (self.host, self.port) )
        self.sock.settimeout(SOCKET_TIMEOUT)
        self.sock.listen(True)
        self.serverThread = threading.Thread()
        self.serverThread.run = self.serve
        self.serverThread.start()

    def serve(self):
        while self.continueServing:
            try:
                self.conn, addr = self.sock.accept()
                print "Got connection from " + str(addr)
                self.conn.settimeout(SOCKET_TIMEOUT)
                if self.authorizeConnection():
                    while self.continueServing:  # redundant check here to quit on Ctrl+C
                        try:
                            proto_bin = self.conn.recv(4096)
                        except timeout:
                            continue  # do nothing, the timeout is only set so we can poll for Ctrl+C
                        if not proto_bin:  # successfully recving no data implies conn closed
                            break  # so break out of the conn specific loop to await another conn
                        command = Command()
                        command.ParseFromString(proto_bin)
                        self.input_handler(command)
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
        self.continueServing = False
        if self.conn:
            self.conn.close()
        if self.sock:
            self.sock.close()


if __name__ == '__main__':
    server = InputServer()
    server.startListening()
    try:
        while server.continueServing:
            time.sleep(.500)
    except:
        server.stopListening()
