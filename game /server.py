from threading import Thread
import random
from tkinter import *
from tkinter import messagebox

from socket import * 

# global variables
player = 0 # indicate which player has to play (1 me , 0 other )
ownerScore = 100 # indicate which turn used to show if we finish game or not 
oppositeScore = 100
#top = Tk()
top = Tk()
top.configure(background='black')
top.title("Server") # title

# labels one and two players
ownerLabel = Label(top,text="Me:100" ,font=('Helvetiica',35))
ownerLabel.grid(row = 0,column=0)
oppositeLabel = Label(top,text="Opposite:100" ,font=('Helvetiica',35))
oppositeLabel.grid(row = 0,column=2)
statusLabel = Label(top,text="Waiting" ,font=('Helvetiica',35))
statusLabel.grid(row = 2,column=1)



# session with server 
soc = socket(AF_INET , SOCK_STREAM)
soc.bind(("127.0.0.1" , 6001) )
soc.listen(2)
c = None
# check
def check():
    if ownerScore <= 0:
        win("Server")
    elif oppositeScore <= 0:
        win("Client")
	
	
def win(player):
	messagebox.showinfo("win", player +" is win")
	top.destroy()

#fun1
def roll():
	global player
	global ownerScore
	if(player==1):
		player=0 # make turn to other player
		# claculate rand value
		p = random.randint(1,6)
		ownerScore -= p
		sendPlay(p)	
		check()


def sendPlay(p):
    showStatus("You played -{}\n Opposite Turn".format(p))
    # display
    ownerLabel["text"] = "You:{}".format(ownerScore)
    n = str(ownerScore)
    n = n.encode()
    c.send(n)

def handlePlay(n):
    global player
    global oppositeScore
    oppositeScore = n 
    oppositeLabel["text"] = "Opposite:{}".format(oppositeScore)
    player = 1
    check()


def applayPlay(p):
    showStatus("opposite played \nYour Turn")
    p = p.decode()
    p = int(p)
    handlePlay(p)


def showStatus(msg):
    statusLabel["text"] = msg
    

def handleClient():
    global player
    global c 
    player = 1 
    c , ad = soc.accept()
    showStatus(" a player connected\n Your Turn")
    t = Thread(target = rec , args = [c,] )
    t.start()


def rec(c):
    while True:
      p = c.recv(10)
      applayPlay(p)


btn1=Button(top,text="Roll",fg="black",width=10,height=5,font='Helvetiica',command=roll)
btn1.grid(row=1,column=1)
acc = Thread(target = handleClient )
acc.start() 
   

showStatus("waiting....")

#to run the topow
top.mainloop()