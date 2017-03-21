import socket
import pendulum
import sys
import time

# lista de  clientes a sincronizar(he utilizado mismo pc, con diferentes puertos)

clientAddress = {
                    ("127.0.0.1", 5001),
                    ("127.0.0.1", 5002),
                    ("127.0.0.1", 5003),
                    ("127.0.0.1", 5004)
                }
    
PUERTOESCUCHA = ("127.0.0.1", 5000)
MAX_CLIENT = len(clientAddress)
BUFFER_SIZE = 1024
DESVIOMAX = 5
CODING = "utf-8"


def mediaRelojes(clocks):
    
    sumaRelojes = 0
    for i in clocks:
        sumaRelojes += float(i)
        
    return sumaRelojes / len(clocks)

def ajusteReloj(clocks, received):
    
    #lista de relojes que han pasado el filtro de desvio
    clocksFilter = clocks
    #calculamos la media
    horaMedia = mediaRelojes(clocks)
    #eliminar horas muy desviadas
    for i in clocks:
        if(float(abs(i - horaMedia)) > DESVIOMAX):
            clocksFilter.remove(i)
            print("!! Cliente descartado\t" + pendulum.from_timestamp(float(i)).to_time_string() )
            #recalcular media
            horaMedia = mediaRelojes(clocksFilter)
            print("!! Hora media actualizada:\t" + pendulum.from_timestamp(float(i)).to_time_string() )
    
    
    #calcular la correccion
    correccion = []
    for i in clocks:
        correccion.append(i - horaMedia)
        
    return correccion
            
#se pone puerto a la escucha
puertoEscucha = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
puertoEscucha.bind(PUERTOESCUCHA)



# Obtengo la hora actual (para espanoles)
horaInicioPeticion = pendulum.now("Europe/Madrid")

# Peticion de sincronización con los clientes
for i in clientAddress :
    puertoEscucha.sendto(bytes("sync", encoding = CODING), i)
    print("Peticion de sincronizacion enviada:\t" + str(i))

#lista de relojes recibidos 
clocks = []
#lista de direcciones que han enviado reloj
received = []
#agregamos en la lista la hora del servidor
clocks.append(horaInicioPeticion.timestamp())
received.append(PUERTOESCUCHA)

print("leyendo relojes...")
time.sleep(2)
for i in range(MAX_CLIENT):
   data, address = puertoEscucha.recvfrom(BUFFER_SIZE)
   timestampResponse = data.decode(CODING)
   print("##################################")
   print("Recibido\t" + pendulum.from_timestamp(float(timestampResponse)).to_time_string() +"\tde:\t" + str(address))
   
   tiempoRespuesta = abs(clocks[0] - pendulum.now("Europe/Madrid").timestamp())
   tiempoTotal = float(timestampResponse) + tiempoRespuesta
   print("Sumamos el tiempo de respuesta:\t" + str(tiempoRespuesta) + "seg\t=\t" + pendulum.from_timestamp(tiempoTotal).to_time_string())
   print("##################################\n")
   clocks.append(float(timestampResponse) + tiempoRespuesta)
   received.append(address)
   
print("\nHora media de los relojes(sin descarte):\t" + pendulum.from_timestamp(mediaRelojes(clocks)).to_time_string())
#Calculamos la media de la muestra de relojes
correccion = ajusteReloj(clocks, received)

print("\nEnviando correcciones...\n")
#enviamos la correccion a los clientes
for i, u in zip(correccion, received):
    puertoEscucha.sendto(bytes(str(i), encoding = CODING), u)
time.sleep(3)

print("##################################")
for i, u, j in zip(clocks, received, correccion):
    print("Direccion host:\t" + str(u) + "\thora:\t" + pendulum.from_timestamp(i).to_time_string() + "\tCorreccion:\t" + str(j))
print("##################################")

puertoEscucha.close()