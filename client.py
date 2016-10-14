
import sys
from socket import *

serverHost = 'localhost'          
serverPort = 50007               


sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
sockobj.connect((serverHost, serverPort))   # connect to server machine + port

#d = sockobj.recv(1024).decode('utf-8')
print('Welcome to Hangman.  Good luck!')


while True:
    d = sockobj.recv(1024).decode('utf-8')
    print(d)

    dd = sockobj.recv(1024).decode('utf-8')
    print(dd)
    
    gs = input("\n\nEnter your guess: ")
    sockobj.send(gs.encode('utf-8'))

    



sockobj.close()                             # close socket to send eof to server
