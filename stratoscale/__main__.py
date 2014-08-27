__author__ = 'max'

import sys
import time
from server import server
import signal
from client import client

def run_server(host, port):
    host = host if host else server.Server.HOST
    port = port if port else server.Server.PORT

    serv = server.Server(host, port)
    serv.start()

    return serv


def run_client(host, port):
    cl = client.Client(host,port)

    cl.start()

    return cl

def parse_args(argv):
    argc = len(argv)
    if argc < 2 or argc > 4:
        return "help", False, False

    command = argv[1]

    ip = argv[2] if argc > 2 else False
    port = int(argv[3]) if argc > 3 else False

    if command not in ("client", "server", "help"):
        command = "help"

    if command == 'client' and not (ip and port):
        command = "help"

    return command, ip, port


def print_help():
    print '''
        Help:
        -----------------------------------------------------------
        You mast use the program with a command help|client|server
        Example: ./stratoscale server 120.0.0.1 8888

        help ------- Show this help
        client ----- Start client. Usage: ./stratoscale ip port
                     While running client in an interactive mode
                     (not a deamon)  type 't' to see the current
                     master time.
        server ----- start server. Usage: ./stratoscale [ip] [port]
                     Defaults: ip = 0.0.0.0 , port = 8888
    '''


def sigint_handler(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    print ""
    print('You pressed Ctrl+C!')
    print "Closing..."
    if running is not None:
        running.stop()


    sys.exit(1)


def main(argv):
    command, host, port = parse_args(argv)

    if command == "server":
        return run_server(host, port)
    elif command == "client":
        return run_client(host, port)
    if command == 'help':
        print_help()
        sys.exit(1)
    return None


if __name__ == "__main__":
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, sigint_handler)
    running = main(sys.argv)

    while True:
        time.sleep(1)
        if not running.isRunning:
            sys.exit(1)