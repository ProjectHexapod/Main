import threading

class InputServer:
    """This class takes care of listening for incomming inputs and supplying an appropriate
    update functions to obey the inputs.  It also handles the mapping from raw input values
    to the controls they represent.
    """
    def __init__(self, port=7337, password=None):
        self.port = port
        self.sock = None
        self.conn = None
        self.serverThread = None
        self.continueServing = True

    def startListening(self):
        self.continueServing = True
        self.serverThread = threading.Thread()
        self.serverThread.run = self.serve
        self.serverThread.start()

    def serve(self):
        pass

    def stopListening(self):
        self.continueServing = False
        self.conn.close()
        self.sock.close()

    def getUpdateFunction(self):
        pass
