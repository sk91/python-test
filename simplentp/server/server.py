__author__ = 'max'

import socket
import sys
import threading
import time
from conn_manager import ConnManager


class Server(threading.Thread):

    HOST = '0.0.0.0'
    PORT = 8888
    def __init__(self, host=HOST, port=PORT, max_conn=100):
        super(Server, self).__init__()
        self.host = host
        self.port = port
        self.maxConn = max_conn
        self.connManager = ConnManager()
        self.socket = None
        self.isRunning = False



    def run(self):
        self.listen()
        print "Listening on {host}:{port}".format(host=self.host, port=self.port)
        self.connManager.start()
        print 'Running'
        self.isRunning = True
        while self.isRunning:
            try:
                conn, addr = self.socket.accept()
                print "Connected with {host}:{port}".format(host=addr[0], port=addr[1])
                self.connManager.push(conn, addr)
            except socket.error, msg:
                pass


    def stop(self):
        self.isRunning = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.connManager.stop()
        print "Stopping server"


    def listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.host, self.port))
        except socket.error, msg:
            print "Could not bind socket"
            sys.exit(1)

        self.socket.listen(self.maxConn)
