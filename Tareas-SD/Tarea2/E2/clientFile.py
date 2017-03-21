import socket
import time

# creamos el socket, lo vinculamos al puerto 4001 y nos conectamos a la direccion remota con puerto 4000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((socket.gethostname(), 4001))
sock.connect((socket.gethostname(), 4000))

sock.settimeout(5)

coding = "utf-8"

while(True):
    try:
        #preguntamos como te llamas
        sock.send(bytes("Como te llamas?", encoding = coding))
        #miramos si hay respuesta si no se crea excepcion y empezamos de nuevo
        inBuff = sock.recv(1000).decode(coding)
        #se ha recivido algo, lo imprimimos como nombre
        print("El nombre es: " + inBuff)
        #mandamos ack confimacion
        sock.send(bytes("ack", encoding = coding))
        print("ack enviado")
        time.sleep(5)
    except OSError as err:
        print(err)

