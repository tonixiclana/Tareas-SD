import zmq
import socket
import time
import os
import json


DIRECCION = ("tcp://*:5555")
CODING = "utf-8"

def listarFicheros():
    lista = []
    for archivos in os.listdir("Files"):
        lista.append(archivos)
    return lista

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(DIRECCION)

while True :
    message =json.loads(socket.recv().decode(CODING))
    print("Recibido: %s" % message)
    
    if(message[0] == "LIST"):
        msg = json.dumps(listarFicheros())
        socket.send(bytes(msg, encoding = CODING))
        
    if(message[0] == "DCG"):
        # Verificar que el fichero existe
        if not os.path.isfile("Files/" + message[1]):
            socket.send(bytes("ERR0", encoding = CODING))
        else:
            # Open the file for reading
            fn = open("Files/" + message[1], 'rb')
            
            stream = True
            # Start reading in the file
            while stream:
                # Read the file bit by bit
                stream = fn.read(128)
                if stream:
                    # If the stream has more to send then send more
                    socket.send(stream, zmq.SNDMORE)
                else:
                    # Finish it off
                    socket.send(stream)
    
    time.sleep(1)
    