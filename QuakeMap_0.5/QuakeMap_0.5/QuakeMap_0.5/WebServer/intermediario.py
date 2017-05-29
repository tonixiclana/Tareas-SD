import zmq 
import json
import dropbox
import tempfile

def listarFicheros():
    lista_ficheros = []
    for entry in dbx.files_list_folder('').entries:
            lista_ficheros.append({'jsonName': entry.name})
    return lista_ficheros
    
def estaEnLista(nombre):
    res = False
    listaComprobacion   =   listarFicheros()
    for fichero in listaComprobacion:
        if fichero["jsonName"] == nombre:
            res=True
            break
    
    return res

DIRECCION = ("tcp://*:5600")
CODING = "utf-8"

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(DIRECCION)

msgError1 = {"status" : "OP_INVALID"}
msgError2 = {"status" : "ERROR_FICH"}

token = "nQdGOjA2yTEAAAAAAAAQIGDRfFjQnVIxZnLUmNKpSUaF0e171AQPlDOPhA1x6NVc"
dbx = dropbox.Dropbox(token)

while True:
    print("******************************")
    peticion = json.loads(socket.recv_json())
    print("[Peticion]: ")
    print(peticion)
    
    if (peticion[0] == "LIST"):
        print("[Peticion para listar archivos recibida]")
        lista_aux = listarFicheros()
        socket.send_json(lista_aux)
        print("Lista enviada:")
        print(lista_aux)
        
    elif (peticion[0] == "DOWN"):
        
        if not estaEnLista(peticion[1]):
            print(msgError2)
            socket.send_json(msgError2)
        else:
            file_temp = tempfile.NamedTemporaryFile(suffix=".json")
            path = "/"+peticion[1]
            print(path)
            dbx.files_download_to_file(file_temp.name, path)
            print(file_temp.name)
            
            stream = file_temp.read(12000000)
            stream = stream.decode(CODING)

            msg = {"status" : "OK", 'data' : json.loads(stream) }
 
            socket.send_json(msg)
            print("Json enviado")
            
    else:
        print("[Se ha recibido una peticion con un comando no valido]")
        socket.send_json(msgError1)