# P2P-Chat-System

## Overview

This is a peer to peer chat system that allows clients to message one another without the need of connecting to a centralized server. There is no centralized server at all involved in this implementation. Instead, the system works by allowing a client to become a "temporary server" allowing other clients to connect to them for chatting purposes. This system has two databases that are stored for each client. One database called messages tracks the messaging history of the user while another database called Users tracks the current users contact list. This implementation allows for user discovery as well as message synchornization.

## Requirements

-socket

-threading

-sqlalchemy

## Installation Guide Lines

Install p2pFinal.py and messageDb.py and put them into the same directory. To run the system write this in the command line :

```python
python p2pFinal.py
```

## How it works

After running the above code in the command line you will be prompted with 2 options either to login(A) or to Create an account(B). If this is your first time running the code then you should proceed with option B and create an account in the database(which is just your name in this instance). 

After creating an account or logging into an existing one, you will be shown your current contact list of people you have added as friends. You will then be prompted with 2 options to either add a user(A) or to connect to a user(B). If you want to add a ser
