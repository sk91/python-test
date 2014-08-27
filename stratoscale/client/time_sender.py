import socket

__author__ = 'max'

import threading
import time


class TimeSender(threading.Thread):

    def __init__(self):
        super(TimeSender,self).__init__()
        self.socket = None
        self.running = False

    def setSocket(self, socket):
        self.socket = socket


    def run(self):
        self.running = True
        while self.running:
            self.send(int(time.time()))
            time.sleep(1)


    def close(self):
        self.running = False

    def send(self,message):
        message = str(message)
        try:
            self.socket.sendall(message)
        except socket.error, msg:
            print "Disconnected from server"
            self.close()


