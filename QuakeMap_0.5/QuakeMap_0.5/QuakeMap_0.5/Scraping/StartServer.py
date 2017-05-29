from multiprocessing import Process
from Scripts.Server import server

p = Process(target=server, args=())
p.start()
p.join()