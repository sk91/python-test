import time
import socket
from time import sleep

__author__ = 'max'

from threading import Thread


class Connection(Thread):
    TIME_OUT = 10

    def __init__(self, conn, addr):
        super(Connection, self).__init__()
        self.conn = conn
        self.addr = addr
        self.lastUpdate = None
        self.time = None
        self.listening = False
        self.daemon = True


    def getTime(self):
        return self.time

    def handle(self):
        self.start()

    def run(self):
        self.listen()
        self.close()

    def listen(self):
        self.listening = True

        while self.listening:
            try:
                data = self.conn.recv(2048)
                self.timeReceived(data)
            except socket.error:
                return self.close()

    def timeReceived(self, tm):
        try:
            tm = int(tm)
            if tm <= 0:
                raise ValueError("Not a timestamp")
        except ValueError:
            pass
        else:
            self.time = tm
            self.lastUpdate = time.time()

    def send(self, data):
        try:
            self.conn.sendall(str(data))
        except socket.error, msg:
            self.close()

    def hasTimedOut(self):
        if self.lastUpdate is None:
            return True

        return time.time() - self.lastUpdate >= self.TIME_OUT

    def close(self):
        self.listening = False
        self.conn.close()
        print "Disconnected from {host}:{port}".format(host=self.addr[0], port=self.addr[1])

    def isListening(self):
        return self.listening