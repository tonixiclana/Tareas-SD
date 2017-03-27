import zmq
import sys
import platform
import pendulum
import json

CODING = "utf-8"

response = {'response': 'worker' + sys.argv[1]}
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5501")
while True:
    message = json.loads(socket.recv().decode(CODING))
    print("[Worker2]\thostname: " + message['hostname'] + ", time: " + message['datetime'])
    print("[Worker2]\tRespuesta enviada")
    socket.send_string(json.dumps(response))