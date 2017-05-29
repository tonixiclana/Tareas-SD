import zmq, os, time, json, gmplot, os, time
import bottle, requests
from bs4 import BeautifulSoup
from bottle import route, template, run, error, SimpleTemplate

def media(lista):
    suma = 0
    for elem in lista:
        suma += elem
    return suma/len(lista)
    
def drawMap(data, mapName):
    longitude = []
    latitude = []

    for i in data:
     longitude.append(float(i['Longitude']))
     latitude.append(float(i['Latitude']))
     
    mediaLongitud = media(longitude)
    mediaLatitud = media(latitude)
    
    gmap = gmplot.GoogleMapPlotter(mediaLatitud, mediaLongitud, 8)
    gmap.heatmap(latitude, longitude)
    #gmap.scatter(latitude, longitude, '#3B0B39', size=80, marker=False)
    
    gmap.draw("maps/" + mapName.split(".")[0] + ".html")
    

if __name__ == "__main__":
    run(host='192.168.4.2', port=8080)


DIRECCIONWEBSERVER = "tcp://localhost:5551"

DIRECCIONSCRAPYCLIENT = ("tcp://localhost:5550")
DIRECCIONINTERMEDIARIO = ("tcp://localhost:5600")

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect(DIRECCIONINTERMEDIARIO)

scrapy = context.socket(zmq.PUSH)
scrapy.connect(DIRECCIONSCRAPYCLIENT)

@route("/")
def main():
    tpl = template("main.html", zoneDefault="zone/es-51-sevilla")
    
    tpl += template("template/zoneList_cab.tpl", tittle="Ciudades Guardadas", css="position: absolute; left: 10px; top: 65px;")
    tpl += template('<div id="{{id}}"></div>', id="resultSaveds")
    tpl += template("template/zoneList_foot.tpl", msg="")
    
    tpl += template("template/search_cab.tpl", tittle="Buscar Ciudad", css="position: absolute; left: 10px; top: 110px;")
    tpl += template('template/search_mid.tpl', id="search", id2="numPages")
    tpl += template("template/zoneList_foot.tpl", msg="")
    return tpl

@route("/search/<name>")
def search(name):
    req = requests.get("http://earthquaketrack.com/search?utf8=%E2%9C%93&q=" + name + "&commit=Go")
    # Comprobamos que la petición nos devuelve un Status Code = 200
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")
        entradas = html.find_all('li', {'class': 'search-result'})
        for i, entrada in enumerate(entradas):
            nombreCiudad = entrada.find('a').getText()
            enlace = entrada.find('a')["href"].split("/")[1]
            response = template('<li style="cursor: hand; cursor: pointer;"><a onclick=\'cargar("/getzone/{{url}}/" + numPages(), "#searchResult")\'>{{name}}</a></li>', {"url" : enlace, "name" : nombreCiudad})
            yield response
    else:
        return status_code

@route("/getSaveds")
def getSaveds():
    timeInit = time.time()
    print("Enviando petición al intermediario...")
    comandoListado = ("LIST", "")
    socket.send_json(json.dumps(comandoListado))
    receiveList = socket.recv_json()
    print("Recibiendo listado zonas disponibles:")
    info = {}
    tpl = template("{{nada}}", nada="")
    for i in range(len(receiveList)):
        info["url"] = "zone/" + receiveList[i]["jsonName"].split('.')[0]
        info["name"] = receiveList[i]["jsonName"].split('.')[0]
        tpl +=   template("template/zoneList_mid.tpl", info)
    
    print("Tiempo de respuesta: " + str(time.time() - timeInit) + "seg")

    return tpl
    
@route("/css/<name>")
def css(name):
    return open("css/main.css").read()

@route("/getzone/<mapName>/<maxPages>")
def zoneRequest(mapName, maxPages):
        mapName = mapName + ".json"
        print("enviando peticion de Scraping a StartClients")
        scrapy.send_json({"namePlace" : mapName.split(".")[0] , "place" : mapName.split(".")[0], "maxPages" : maxPages, "webServer" : DIRECCIONWEBSERVER})
        print("Peticion de Scraping mandada")
        return '<div class="alert alert-info"><strong>Info!</strong> El mapa estará disponible en breve.</div>'
      
@route("/zone/<mapName>")
def viewZone(mapName):
        mapName = mapName + ".json"
        print("Pidiendo datos a Intermediario para la zona: \t" + mapName)
        comandoDescarga = ("DOWN", mapName)
        socket.send_json(json.dumps(comandoDescarga))
        data = socket.recv_json()
        print(data["status"])
        
        if(data["status"] == "OK"):
            drawMap(data["data"], mapName)
            #Para mostrar datos
            map = open('maps/' + mapName.split(".")[0] + ".html", 'r')
            tpl =   template(map.read(), name='World')
            #for i in range(len(data["data"])):
            #    tpl += template('<p>{{DateTime}} {{Country}} {{City}} {{Location}} {{Latitude}} {{Longitude}} {{Magnitude}} {{Depth}}</p>', data["data"][i])
            return tpl
        else:
            if data["status"] == "ERROR_FICH":
                return "No existe la zona"
            else:
                if data["status"] == "OP_INVALID":
                    return "Operacion invalida"

@error(404)
def error404(error):
    return 'Nothing here, sorry'

app = bottle.default_app()
#run(host="0.0.0.0", port=8080, debug="true", server='gunicorn', workers=2)
