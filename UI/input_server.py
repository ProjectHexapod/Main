import hashlib
import random
import robotControl_pb2
import threading

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
                    pass
                else:
                    # TODO: log the bad login attempt
                    self.conn.close()
            except error, msg:
                # TODO: log the msg
                pass

    def authorizeConnection(self):
        try:
            challenge = str(random.random())
            self.conn.send(challenge)
            response = self.conn.recv(64)
            expected_response = hashlib.sha1(self.password + challenge).hexdigest()
            return response == expected_response
        except error, msg:
            # TODO: log the msg
            return False

    def stopListening(self):
        self.continueServing = False
        self.conn.close()
        self.sock.close()

    def getUpdateFunction(self):
        pass
