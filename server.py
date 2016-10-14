
import time, _thread as thread           # or use threading.Thread().start()
from socket import *                     # get socket constructor and constants
from theman import HANGMAN
import random

# constants
MAX_WRONG = len(HANGMAN) - 1
WORDS = open("wordlist.txt", "r").readlines()


myHost = ''                              # server machine, '' means local host
myPort = 50007                           # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.listen(5)                                # allow up to 5 pending connects

def now():
    return time.ctime(time.time())               # current time on the server

def handleClient(connection):                   
    time.sleep(1)                               
    hangman(connection)


def hangman(connection):
    word = str(random.choice(WORDS))   
    so_far = "\nSo far, the word is:\n" + ("-"* len(word))      
    wrong = 0                     
    used = ["\nYou've used the following letters:\n"]                     

    sofar = '\nSo far, the word is:\n'
    
    while wrong < MAX_WRONG and so_far != word:
        connection.send(HANGMAN[wrong].encode('utf-8'))
        connection.send(so_far.encode('utf-8'))
        connection.send(''.join(used).encode('utf-8'))
        
        gs = connection.recv(1024).decode('utf-8')
        used.append(gs)
        used.append('\n')
        if gs in word:
            connection.send(''.join(['\nYes! ', gs,' is in the word!']).encode('utf-8'))
            new = ""
            for i in range(len(word)):
                if gs == word[i]:
                    new += gs
                else:
                    new += so_far[i]              
            so_far = new
            
        else:
            connection.send(''.join(['\nNo ', gs,' is in not the word']).encode('utf-8'))
            wrong += 1

    if wrong == MAX_WRONG:
        connection.send(HANGMAN[wrong].encode('utf-8'))
        connection.send('\nYou have been hanged!'.encode('utf-8'))
    else:
        connection.send('\nYou guessed it!'.encode('utf-8'))


def dispatcher():                                
    while True:                                  
        connection, address = sockobj.accept()  
        print('Server connected by', address, end=' ')
        print('at', now())
        thread.start_new_thread(handleClient, (connection,))

dispatcher()
