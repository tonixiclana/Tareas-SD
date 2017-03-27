import zmq
import socket
import sys

CODING = "utf-8"

# Prepare our context and publisher
context    = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5555")

if(sys.argv[1] == "spain"):
    topic = "Europe/Madrid"
if(sys.argv[1] == "england"):
    topic = "Europe/London"
if(sys.argv[1] == "mexico"):
    topic = "America/Mexico_City"
    
subscriber.setsockopt(zmq.SUBSCRIBE, bytes(topic, encoding = CODING))

while True:
    # Read envelope with address
    [topic, data] = subscriber.recv_multipart()
    print(topic.decode(CODING) + "\t" + data.decode(CODING))

# We never get here but clean up anyhow
subscriber.close()
context.term()