import hashlib
import network_args
import sys

#from ControlsKit.leg_logger import logger
from robotControl_pb2 import Command
from socket import socket, AF_INET, SOCK_STREAM, timeout


def getSocket():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(.5)
    try:
        sock.connect( (network_args.host, network_args.port) )
        challenge = sock.recv(64)
        response = hashlib.sha1(network_args.password + challenge).hexdigest()
        sock.send(response)
        return sock
    except Exception, ex:
        #logger.error("Could not connect to InputServer.", error=ex)
        return None

def sendCommand(command):
    sock = getSocket()
    try:
        sock.send(command.SerializeToString())
        sock.close()
    except Exception, ex:
        #logger.error("Could not send command to InputServer.", error=ex)
        return None

def sendCommandFromEventKey(event_key):
    command = Command()
    command.controller = Command.PYGAME
    raw = command.raw_command.add()
    raw.index = event_key
    raw.value = 1
    try:
        raw.name = chr(event_key)
        sendCommand(command)
    except ValueError:
	pass

def sendCommandFromCommandName(name, val=1):
    command = Command()
    command.controller = Command.COMMAND_LINE
    raw = command.raw_command.add()
    raw.name = name
    raw.value = val
    sendCommand(command)

if __name__ == "__main__":
    command_name = ""
    for arg in sys.argv:
        if "--cmd=" in arg:
            command_name = arg[len("--cmd="):]
    sendCommandFromCommandName(command_name)
