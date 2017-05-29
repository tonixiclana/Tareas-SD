import zmq
import platform
import pendulum
import json

ROUTER = ("tcp://127.0.0.1:5500")
DEALER = ("tcp://127.0.0.1:5501")

CODING = "utf-8"

def server():
    # Prepare our context and sockets
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)
    frontend.bind(ROUTER)
    backend.bind(DEALER)
    
    # Initialize poll set
    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)
    
    print("[Server 0]\t Init Router Server")
    # Switch messages between sockets
    while True:
        socks = dict(poller.poll())
        if socks.get(frontend) == zmq.POLLIN:
            message = frontend.recv()
            more = frontend.getsockopt(zmq.RCVMORE)
            if more:
                backend.send(message, zmq.SNDMORE)
            else:
                backend.send(message)
        if socks.get(backend) == zmq.POLLIN:
            message = backend.recv()
            more = backend.getsockopt(zmq.RCVMORE)
            if more:
                frontend.send(message, zmq.SNDMORE)
            else:
                frontend.send(message)