import zmq
import platform
import pendulum
import json
import time

nowDateTime = pendulum.now("Europe/Madrid").to_datetime_string()
hostname = platform.node()
message = {'hostname' : hostname, 'datetime' : nowDateTime}

# Prepare our context and sockets
context = zmq.Context()
socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5500")

while True:
    socket.send_string(json.dumps(message))
    print("[Client0]\tPidiendo respuesta...")
    received = socket.recv()
    print("[Client0]\tRespuesta Recibida:\t " + received.decode())
    time.sleep(5)

