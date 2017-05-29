import sys, zmq, json, time
from multiprocessing import Process, Pool
from Scripts.Client import client

#prepare context of webserver connection
context = zmq.Context()
webServer = context.socket(zmq.PULL)
webServer.bind("tcp://*:5550")

while True:
    print("esperando peticion")
    request = webServer.recv_json()
    ps = Process(target=client, args=(request["namePlace"], request["place"], request["webServer"],  request["maxPages"]))
    
    ps.start()
    #webServer.send_json({'status' : ps.exitcode})
ps.join()



