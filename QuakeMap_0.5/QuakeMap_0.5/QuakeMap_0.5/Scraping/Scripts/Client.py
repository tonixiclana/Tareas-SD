# Cliente para obtencion de informacion de terremotos, se recive de algún worker en json
# lanzar python3 Cliente.py nombreCliente [v/nombreDelGroupPlace | nombreDelPlace] [T|F]paraListarTodasPag 
import zmq, platform, pendulum, json, time, sys

def client(nameClient, place, webServer, maxPages):
    
    # Prepare our context and sockets of scraping server
    context = zmq.Context()
    socket= context.socket(zmq.REQ)
    #connect to router server
    socket.connect("tcp://localhost:5500")
    
    nowDateTime = pendulum.now("Europe/Madrid").to_datetime_string()
    hostname = platform.node()
    message = {'hostname' : hostname, 'datetime' : nowDateTime, 'nameClient' : nameClient, 'place' : place, 'maxPages' : maxPages}
    
    #send the request place
    print("[Client " + nameClient + "]\tEnviando peticion")
    socket.send_json(json.dumps(message))
    print("[Client " + nameClient + "]\tSolicitando respuesta...")
    
    #wait to info of Quake place
    received = socket.recv_json()
    received = json.loads(received)
    #Print the reply info
    if(received["content"] == "FAIL"):
        print("[Client " + nameClient + "]\tEl worker:\t " + received['worker'] + "\t ha fallado")
    else:
        print("[Client " + nameClient + "]\tRespuesta Recibida de worker:\t " + received['worker'])