
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

def handleClient(connection):                    # in spawned thread: reply
    time.sleep(1)                                # simulate a blocking activity
    #while True:                                  # read, write a client socket
        #data = connection.recv(1024)
        #if not data: break
        #connection.send(data)
    hangman(connection)
    #connection.close()


def hangman(connection):
    #word = random.choice(WORDS)   # the word to be guessed
    word= 'CUNT'
    so_far = "-" * len(word)      # one dash for each letter in word to be guessed
    wrong = 0                     # number of wrong guesses player has made
    used = ['v']                     # letters already guessed

    welcome = [b'Welcome to Hangman.  Good luck!']
    entr = [b'\n\nEnter your guess: ']
    #guess = "\nYou've used the following letters:\n"
    sofar = "\nSo far, the word is:\n"
    
    sendSB(connection, welcome)

    while wrong < MAX_WRONG and so_far != word:
        connection.send(HANGMAN[wrong].encode('utf-8'))
        #gss = guess.join
        #connection.send(gss.encode('utf-8'))
        #sendSB(connection, entr)
        gs = connection.recv(1024).decode('utf-8')

        print(gs)

        if gs in word:
            sendSB(connection, [b'yes'])
            new = ""
            for i in range(len(word)):
                if gs == word[i]:
                    new += gs
                else:
                    new += so_far[i]              
            so_far = new
            
        else:
            sendSB(connection, [b'lol'])
            wrong += 1

    if wrong == MAX_WRONG:
        connection.send(HANGMAN[wrong].encode('utf-8'))
        sendSB(connection, [b'ripip'])
    else:
        sendSB(connection, [b'gg'])
        

def sendSB(connection, thing):
    for b in thing:
        connection.send(b)


def dispatcher():                                # listen until process killed
    while True:                                  # wait for next connection,
        connection, address = sockobj.accept()   # pass to thread for service
        print('Server connected by', address, end=' ')
        print('at', now())
        thread.start_new_thread(handleClient, (connection,))

dispatcher()
