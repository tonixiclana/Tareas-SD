import socket
import sys

# creamos el socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), 4000))
coding = "utf-8"

#cogemos los 2 primeros bytes del buffer de entrada del socket y lo convertimos a int
sizeNameFile = sock.recv(2)
sizeNameFile = int.from_bytes(sizeNameFile, byteorder='little')

#extraemos del buffer de entrada del socket el nombre, segun el numero de Bytes que tenga
nameFile = sock.recv(sizeNameFile).decode(coding)

#Extraemos el contenido del fichero, como máximo 2Mb
fileContent = sock.recv(2048).decode(coding)

#Abrimos el fichero en modo escritura w y escribimos el contenido del fichero
archi=open(nameFile,'w')
archi.write(fileContent)
archi.close()
