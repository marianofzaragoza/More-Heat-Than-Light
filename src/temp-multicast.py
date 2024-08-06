# UDP multicast examples, Hugo Vincent, 2005-05-14.
import sys
import re
import socket
import time
import struct
from netifaces import interfaces, ifaddresses, AF_INET
from mcast import Mcast  

class Tempsender():
    host = 'A'
    addr = '239.192.1.100'
    port = 50000

    def __init__(self):

        self.socket = Mcast()
        print(self.socket)
        #self.socket.send(b'test')



ts = Tempsender()

print(sys.argv)
time.sleep(1)
if len(sys.argv) > 1 and sys.argv[1] == "recv":

    while True:
        print('receiving')
        print(ts.socket.recv())
        #time.sleep(1)

else:
    while True:
        print('testing')         
        ts.socket.send(b"hello")
        #ts.socket.recv()
        print('adsf')
        ts.socket.send(b"hello2")
        #ts.socket.recv()
        time.sleep(1)



