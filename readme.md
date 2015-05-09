Python assignment
================

Please write a Python (version 2.7.X) time sync program that will consist of a server and clients.
I should be able to run the server on one machine, and few (<100) clients on different machines in the same network.
Each client should send it's time every second to the server.
The server must choose one client from all the clients, whose clock will be the master clock. This choice ( of which client is the master clock ) can be done by any algorithm of your choice.
The server must send the master clock to each client every second.
If the master client does not send it's time for one minute, the server must choose a new client from the other clients to be the master clock.
Each client should implement a command line interface, in which the user can ask the the client for the last master clock it received from the server.
You can use whatever Python libraries that are included by default with the installation.
No GUI is needed, the UI should be console based, and as simple as possible.



Usage:
======

You mast use the program with a command client|server
Example: `python ./simplentp server 120.0.0.1 8888`

## Commands:

### client
Starts client. Usage: `python ./simplentp client ip port`. While running client in an interactive mode (not a deamon)  type `time` to see the current master time.
### server
Starts server. Usage: `python ./simplentp server [ip] [port]`
Defaults: ip = 0.0.0.0 , port = 8888
