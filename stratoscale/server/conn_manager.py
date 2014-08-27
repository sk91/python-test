import time

__author__ = 'max'

import threading
from connection import Connection


class ConnManager(threading.Thread):
    def __init__(self):
        super(ConnManager, self).__init__()
        self.isRunning = False
        self.connections = []
        self.master = None
        self.daemon = True


    def run(self):
        self.isRunning = True
        while self.isRunning:
            tm = self.getMasterTime()
            if tm is not None:
                self.sendAll(tm)

            time.sleep(1)


    def getMasterTime(self):
        master = self.master
        if master is None or master.hasTimedOut():
            self.master = master = self.chooseMaster()

        if master is None:
            return None
        return master.getTime()


    def chooseMaster(self):
        for conn in self.connections:
            if not conn.hasTimedOut() and conn.isListening():
                return conn
        return None

    def sendAll(self, message):
        for conn in self.connections:
            if conn.isListening():
                conn.send(message)

    def stop(self):
        for conn in self.connections:
            conn.close()
        self.isRunning = False


    def push(self, conn, addr):
        connection = Connection(conn, addr)
        connection.handle()
        self.connections.append(connection)
