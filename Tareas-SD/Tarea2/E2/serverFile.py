import socket
import time

# creamos el socket, lo vinculamos al puerto 4001 y nos conectamos a la direccion remota con puerto 4000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((socket.gethostname(), 4000))
sock.connect((socket.gethostname(), 4001))
coding = "utf-8"

sock.settimeout(10)

while(True):
    try:
        inBuff = sock.recv(1000).decode(coding)
        
        if(inBuff == "Como te llamas?"):
            while(inBuff != "ack"):
                try:
                    inBuff = sock.recv(1000).decode(coding)
                    sock.send(bytes("Servidor", encoding = coding))
                except OSError as err:
                    print("no se recive ack, mandando respuesta de nuevo")
            print("respuesta enviada y recivida por el cliente") 
    except OSError as err:
        print("Peticion no recivida")
    