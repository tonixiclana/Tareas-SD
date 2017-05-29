# usage: python3 StartWorkers numberOfWorkers
import sys
from multiprocessing import Process, Pool
from Scripts.Worker import worker

ps = []
for i in range(int(sys.argv[1])):
    ps.append(Process(target=worker, args=(str(i))))
    ps[i].start()
     
for p in ps:   
    p.join()
