import time
import zmq



class Server:
    
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind("tcp://*:5555")
        self.message = ""


    def listening(self):
        self.message = self.socket.recv_json()
        return self.message

