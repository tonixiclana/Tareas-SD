import random
import socket
import pendulum

PUERTOESCUCHA = ("localhost", 5004)
BUFFER_SIZE = 1024
DESVIOALEATORIO = 23
CODING = "utf-8"

# Obtengo la hora actual (para espanoles)
current = pendulum.now("Europe/Madrid")
# Le meto un incremento aleatorio 
offset = random.randrange(-DESVIOALEATORIO, DESVIOALEATORIO)
tiempoActualDesviado = current.add(seconds=offset)

# Me pongo a la escucha
puertoEscucha = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
puertoEscucha.bind(PUERTOESCUCHA)

# Espero la peticion de sincronizacion
data = ""
address = ()
while(data != b'sync'):
     data, address = puertoEscucha.recvfrom(BUFFER_SIZE)
     
print("!!" + str(PUERTOESCUCHA) + "\tRespuesta enviada:\t" + pendulum.from_timestamp(tiempoActualDesviado.timestamp()).to_time_string())

#mandamos el timestamp actual
puertoEscucha.sendto(bytes((str)(tiempoActualDesviado.timestamp()), encoding = CODING), address)

#escuchamos para correccion
data, address = puertoEscucha.recvfrom(BUFFER_SIZE)

print("!!" + str(PUERTOESCUCHA) + "Correccion recibida:\t" + data.decode(CODING))