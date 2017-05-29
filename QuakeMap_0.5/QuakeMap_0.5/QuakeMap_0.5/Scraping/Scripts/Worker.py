import scrapy, time, zmq, os, json, sys, platform, dropbox, tempfile

CODING = "utf-8"

#prepare and open dropbox
token = "nQdGOjA2yTEAAAAAAAAQIGDRfFjQnVIxZnLUmNKpSUaF0e171AQPlDOPhA1x6NVc"
dbx = dropbox.Dropbox(token)

def worker(number):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:5501")
    
    while True:
        
        print("[Worker" + number + "]\tEsperando Peticion")
        message = socket.recv_json()
        message = json.loads(message)
        print("[Worker" + number + "]\thostname: " + message['hostname'] + ", time: " + message['datetime'])
        
        os.system("scrapy runspider Scraping/Scripts/Spider.py -a maxPages=" + message['maxPages'] + " -a place=" + message['place'] + " -o " + "/tmp/" + message['place'] + ".json")
        print("----------------------------spider stop")
            
        #convertimos a json la salida del spider
        try:
            with open("/tmp/" + message['place'] + ".json") as f:
                data = json.load(f)
                msg = json.dumps(data)
        except ValueError:
            socket.send_json(json.dumps({'worker': number, 'content' : 'fail'}))
            print("[Worker" + number + "]\tConfirmacion tarea no terminada enviada a:\t" + message['hostname'])
        else:
            #Save the info in DropBox
            dbx.files_upload(bytes(msg, encoding='utf-8'), "/" + message["nameClient"] + ".json", mode=dropbox.files.WriteMode.overwrite)
            os.remove("/tmp/" + message['place'] + ".json")
            #mandamos la respuesta con la confirmacion de tarea realizada al cliente
            socket.send_json(json.dumps({'worker': number, 'content' : 'ok'}))
            print("[Worker" + number + "]\tGuardado en archivo:\t" + message["nameClient"] + ".json\tConfirmacion tarea terminada enviada a:\t" + message['hostname'])
            
