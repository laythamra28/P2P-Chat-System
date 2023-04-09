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
