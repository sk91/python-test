__author__ = 'max'

import threading

class MasterTimeRecv(threading.Thread):

    def __init__(self):
        super(MasterTimeRecv, self).__init__()
        self.running = False
        self.socket = None
        self.time = None

    def run(self):
        self.running = True
        while self.running:
            data = self.socket.recv(2046)

            try:
                tm = int(data)
                if tm <= 0:
                    raise ValueError
            except ValueError:
                pass
            else:
                self.time = tm

    def getTime(self):
        return self.time

    def setSocket(self, socket):
        self.socket = socket

    def stop(self):
        self.running = False