import zmq
import msgpack
import time

class NetworkDriver: # for gps positioning communication
    ctx = zmq.Context()

    pub = ctx.socket(zmq.PUB)
    sub = ctx.socket(zmq.SUB)
    
    # atomic pi config
    transmitPort = 5552
    receivePort = 5551
    receiveIP = "localhost"

    def __init__(self, boatIP): # prob 192.168.3.1
        self.receiveIP = boatIP

        self.pub.bind("tcp://*:" + str(self.transmitPort))
        self.sub.connect("tcp://" + str(self.receiveIP) + ":" + str(self.receivePort))
        self.sub.subscribe("")

    def transmitPosition(self, lat, lon):
        #print(lat, lon)
        self.pub.send(msgpack.packb([lat, lon]))

    def receivePosition(self):
        d = []
        try:
            d = msgpack.unpackb(self.sub.recv(copy=False, flags=zmq.NOBLOCK))
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                pass
            else:
                print(e)
        return d