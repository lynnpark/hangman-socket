
import sys
from socket import *              # portable socket interface plus constants
serverHost = 'localhost'          
serverPort = 50007                # non-reserved port used by the server

message = [b'Ready to hang men']          # default text to send to server

                                            # requires bytes: b'' or str,encode()
if len(sys.argv) > 1:       
    serverHost = sys.argv[1]                # server from cmd line arg 1
    if len(sys.argv) > 2:                   # text from cmd line args 2..n
        message = (x.encode() for x in sys.argv[2:])  

sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
sockobj.connect((serverHost, serverPort))   # connect to server machine + port

#for line in message:
    #sockobj.send(line)                      # send line to server over socket
    #data = sockobj.recv(1024)               # receive line from server: up to 1k
    #print(data)                             # bytes are quoted, was `x`, repr(x)


while True:
    data = sockobj.recv(1024)
    print(data.decode('utf-8'))
    gs = input("\n\nEnter your guess: ")
    gs = gs.upper()
    print(gs)
    sockobj.send(gs.encode('utf-8'))


sockobj.close()                             # close socket to send eof to server
