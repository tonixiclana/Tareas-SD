import socket

MAX_CLIENTS = 10

#creamos el socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 4000))
sock.listen(MAX_CLIENTS)
coding = "utf-8"

#extraemos el titulo del fichero, ademas de cuantas letras tiene el titulo 
nameFile = "serverFile.py"
sizeNameFile= len(nameFile)

#extraemos el contenido del fichero
fileContent = ""
with open(nameFile) as file:
    for line in file:
        fileContent += line

#esperamos a que un cliente se conecte y mandamos toda la informacion
while(True):
    (client, address) = sock.accept()
    
#convertimos toda la info a bytes, en el caso del sizeNameFile, lo pasamos con 2
#tamaño de 2 bytes y en little endian, en caso de los string lo codificamos en utf-8
    client.sendall((sizeNameFile).to_bytes(2, byteorder = "little" ) + 
        bytes(nameFile, encoding = coding) + bytes(fileContent, encoding = coding))

