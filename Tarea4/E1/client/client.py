import zmq
import os
import time
import json

DIRECCION = ("tcp://*:5556")
DIRECCIONSERV = ("tcp://localhost:5555")
CODING = "utf-8"

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.bind(DIRECCION)

socket.connect(DIRECCIONSERV)

while True:
    print("Enviando LIST")
    
    comandoListado = ("LIST", "")
    socket.send(bytes(json.dumps(comandoListado), encoding = CODING))
    
    receiveList = json.loads(socket.recv().decode(CODING))
    
    print("Escribe fichero a descargar:")
    
    for i in receiveList:
        print (i)
    
    fichero = input()
    
    print("Enviando DCG " + fichero)
    comandoDescarga = ("DCG", fichero)
    socket.send(bytes(json.dumps(comandoDescarga), encoding = CODING))
    
    print("recibiendo fichero")
    dest = open("Files/" + fichero, 'w')
    
    while True:
        # Start grabing data
        data = socket.recv().decode(CODING) 
        if(data == "ERR0"):
            print("fichero no encontrado")
        else:
            # Write the chunk to the file
            print(data)
            dest.write(data)
            if not socket.getsockopt(zmq.RCVMORE):
                # If there is not more data to send, then break
                break
    
    print("fichero: " + fichero + " guardado con exito")
    dest.close()