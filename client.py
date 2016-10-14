
import sys
from socket import *

serverHost = 'localhost'          
serverPort = 50007               


sockobj = socket(AF_INET, SOCK_STREAM)      
sockobj.connect((serverHost, serverPort))  

print('Welcome to Hangman.  Good luck!')

while True:
    d = sockobj.recv(1024).decode('utf-8')
    print(d)

    dd = sockobj.recv(1024).decode('utf-8')
    print(dd)
    
    gs = input("\n\nEnter your guess: ")
    sockobj.send(gs.encode('utf-8'))

sockobj.close()                            
