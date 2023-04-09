# import modules
import socket
import threading
import sqlalchemy as db
import time
from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, func, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Create a SQLite database
engine = create_engine('sqlite:///messages.db')

# Define the Message model using SQLAlchemy declarative base

from messageDB import Message, Users, Base

Base.metadata.create_all(engine)

#ALLIPs= {"Rashid1":"192.168.1.6","Rashid2":"192.168.1.10","Osama":"0"}
PORT = 8001

class P2P():
    def __init__(self, username, ALLIPs):
        self.ALLIPs = ALLIPs
        self.clientIP = ALLIPs[username]    
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isserver=False
        self.clients=[]
        self.username=username
        self.otherUsername=''
        self.myMessages = Message()


    def receive(self):
        """
        Receives messages from the server and prints them to the console
        """
        if self.isserver:
            while True:
                client=self.clients[0]
                message = client.recv(1024).decode("utf-8")
                self.store_message(sender=self.otherUsername,recipient=self.username,message=message,sent_status=1)
                #message_db=Message(self.username,self.otherUser)
                print(f'{self.otherUsername}: {message}')
        else:
            while True:
                try:
                    message = self.s.recv(1024).decode("utf-8")
                    self.store_message(sender=self.otherUsername,recipient=self.username,message=message,sent_status=1)
                    print(f'{self.otherUsername}: {message}')
                except:
                    # Exit the thread if there's an error
                    break

    def send_offline(self):
        run=True
        while run:
            message = input()
            #print(f'echo message: {message}')
            self.store_message(sender=self.username,recipient=self.otherUsername,message=message,sent_status=0)
            if len(self.clients)>0:
                run=False


                
    def send(self):
        """
        Sends messages to the server
        """
        
        if self.isserver:
             #send offline messages
            messages_offline = self.myMessages.get_messages(engine,self.otherUsername)
            for message_offline in messages_offline:
                for client in self.clients:
                    client.send(message_offline.message.encode("utf-8"))
            self.myMessages.change_message_status(engine, self.otherUsername)
            while True:
                message = input()
                #print(f'echo message: {message}')
                for client in self.clients:
                    client.send(message.encode("utf-8"))
                
                self.store_message(sender=self.username,recipient=self.otherUsername,message=message,sent_status=1)
                
        else:
            messages_offline = self.myMessages.get_messages(engine,self.otherUsername)
            for message_offline in messages_offline:
                self.s.send(message_offline.message.encode("utf-8"))
            self.myMessages.change_message_status(engine, self.otherUsername)
                
            while True:
                message = input()
                self.s.send(message.encode("utf-8"))
                self.store_message(sender=self.username,recipient=self.otherUsername,message=message,sent_status=1)


    def connect(self, otheruser):
        self.otherIP = self.ALLIPs[otheruser]
        self.otherUsername = otheruser
        try:
            self.s.settimeout(20)
            self.s.connect((self.otherIP,PORT))
            
            recieve_thread=threading.Thread(target=self.receive)
            send_thread=threading.Thread(target=self.send)
            recieve_thread.start()
            send_thread.start()
            
            connected = True
            
            
        except:
            self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connected = False
            
        return connected

    def startSession(self):
        self.isserver=True
        #self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"IP: {self.clientIP}, PORT: {PORT}")
        self.s.bind((self.clientIP,PORT))
        self.s.listen()

        send_thread_offline=threading.Thread(target=self.send_offline)
        send_thread_offline.start()
        while True:
            client, address=self.s.accept()
            print(f"address: {address[0]}")
            self.otherUsername = [i for i in self.ALLIPs if self.ALLIPs[i]== address[0]][0]
            self.clients.append(client)

            recieve_thread=threading.Thread(target=self.receive)
            send_thread=threading.Thread(target=self.send)
            recieve_thread.start()
            send_thread.start()
        
    def store_message(self,sender,recipient,message,sent_status):
        self.myMessages.add_message(sender=sender,recipient=recipient,message=message,sent_status=sent_status, engine=engine) 

    


def main():
    # establish users DB
    myUsers= Users()
    login = input('Would you like to login [A] or Create An Account [B]?: ')
    allUsers = myUsers.get_users(engine)
    validUser = False

    if login.lower() == 'a':
        username = input('Please insert your username: ')
        for users in allUsers:
            if username == users.username:
                validUser = True
        if not validUser:
            print("Invalid Username")
            return 
    elif login.lower() == 'b':
        username = input('Please insert your username: ')
        # IP_add = input('Please insert your IP address: ')
        hostname=socket.gethostname()
        IPAddr=socket.gethostbyname(hostname)  
        print(IPAddr)   
        myUsers.add_user(username=username, IP_address=IPAddr, engine=engine)
    else:
        print('Invalid Selection')
        return
     
    print('\n\nYour Contacts List: ')
    for users in allUsers:
        if username != users.username:
                print(users.username)
    print('\n\n')
   

    addOrconn = input('Would you like to add a user [A] or connect to a user [B]?: ')
    friend_username = input("Please insert your friend's username: ")
    
    if addOrconn.lower() == 'a':
        friendIP_add = input("Please insert your friend's IP address: ")
        myUsers.add_user(username=friend_username, IP_address=friendIP_add, engine=engine)
    elif addOrconn.lower() != 'b':
        print('Invalid Selection')
        return
        
    allUsers = myUsers.get_users(engine)
    ALLIPs = {}

    for user in allUsers:
        ALLIPs[user.username] = user.IP_address

    # start p2p class:
    p2p = P2P(username, ALLIPs)

    p2p.otherUsername = friend_username
    print("..........Attempting to Connect..........")
    time.sleep(1)
    connected = p2p.connect(friend_username)
    # print(f"connected {connected}")
    if connected:
        print("Succesfuly connected")
    else:
        startSession = input("Friend is not online :(, would you like to start session [y]/[n]?: ")
        if startSession == 'y':
            p2p.startSession()
    

if __name__ == '__main__':
    main()