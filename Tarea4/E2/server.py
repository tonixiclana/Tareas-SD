import zmq
import pendulum
import socket
import time

CODING = "utf-8"

topics = ["Europe/Madrid", "Europe/London", "America/Mexico_City"]

context   = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://127.0.0.1:5555")

print("Servidor de horas mundiales ON")
while True:
    for i in topics:
        now = pendulum.now(i)
        topic = bytes(i, encoding = CODING)
        timeInTZ = bytes(now.to_datetime_string(), encoding = CODING)
        publisher.send_multipart([topic, timeInTZ])
    time.sleep(1)
    
# We never get here but clean up anyhow
publisher.close()
context.term()