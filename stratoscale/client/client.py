__author__ = 'max'

import time
import socket
import select
import sys
import threading

from time_sender import TimeSender
from master_time import MasterTimeRecv


class Client(threading.Thread):
    def __init__(self, host="127.0.0.1", port=8888):
        super(Client, self).__init__()
        self.timeSender = TimeSender()
        self.masterTimeRecv = MasterTimeRecv()
        self.host = host
        self.port = port
        self.socket = None
        self.isRunning = False


    def run(self):
        self.connect()
        self.isRunning = True
        self.timeSender.start()
        self.masterTimeRecv.start()

        sys.stdout.write('>>> ')
        sys.stdout.flush()

        while self.isRunning :

            i, o, e = select.select( [sys.stdin], [], [], 3 )
            if i:
                command = sys.stdin.readline().strip()

                if command == 'time':
                    print self.masterTimeRecv.getTime()

                sys.stdout.write('>>> ')
                sys.stdout.flush()

    def connect(self):
        print "Connecting to {host}:{port}".format(host=self.host, port=self.port)
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print "Could not establish connection to {host}:{port}".format(host=self.host, port=self.port)
            sys.exit(1)
        print "Socket created"
        self.socket.settimeout(2)
        try:
            self.socket.connect((self.host, self.port))
        except Exception:
            print "Could not establish connection to {host}:{port}".format(host=self.host, port=self.port)
            sys.exit(1)


        self.timeSender.setSocket(self.socket)
        self.masterTimeRecv.setSocket(self.socket)

        print "Connection to {host}:{port} has been established".format(host=self.host, port=self.port)

    def stop(self):
        self.isRunning = False
        self.timeSender.close()
        self.masterTimeRecv.stop()
        self.socket.close()


    def getMasterTime(self):
        return self.masterTimeRecv.getTime()

