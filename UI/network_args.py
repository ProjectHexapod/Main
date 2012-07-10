import sys

password = ""
host = "localhost"
port = 7337

for arg in sys.argv:
    if "--password=" in arg:
        password = arg[len("--password="):]
    elif "--host=" in arg:
        host = arg[len("--host="):]
    elif "--port=" in arg:
        port = arg[len("--port="):]
