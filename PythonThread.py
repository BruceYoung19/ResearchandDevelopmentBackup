import logging
import threading
import time
import random 

#learning how to use a threaded constructor
def __init__(self,Objid):
    thread.__init__(self)
    f = random.random()
    self.objid = f

def printid(self):
    print(x.objid)     

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(10)
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
	#pill2kill = threading.Event()
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    printid(self)
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    x.join()
    logging.info("Main    : all done")




