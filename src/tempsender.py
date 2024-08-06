import os
import gi
import pprint
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
#gi.require_version('Glib', '1.0')
gi.require_version('GdkX11', '3.0')
gi.require_version('GstVideo', '1.0')
gi.require_version("GLib", "2.0")
gi.require_version("GstNet", "1.0")


from gi.repository import GLib
from gi.repository import GObject, Gst, Gtk, GstNet

import numpy as np


###
import sys
import re
import socket
import time
import struct
from netifaces import interfaces, ifaddresses, AF_INET
from mcast import Mcast  
from collections import deque
import moreheat_pb2

class Tempsender():
    def __init__(self):
        self.testtemp = 21.9
        self.rxqueue = deque([])
        self.appqueue = deque([])
        self.socket = Mcast()
        print(self.socket)
        #self.socket.send(b'test')

    def poll(self):
        gotdata = False
        while (data := self.socket.recv()) is not None:
            self.rxqueue.append(data) 
            gotdata = True
        return gotdata

    def retrieve_one(self):
        self.process_messages()
        try:
            msg = self.appqueue.popleft()
            return str(msg)
        except IndexError:
            return None

    def process_messages(self):
        ql = len(self.rxqueue)
        while ql > 0:
            try:
                msg = self.rxqueue.popleft()
                # decode, update temperature, reject broken, keep stats
                msglen = len(msg.SerializeToString())
                print("length bits: " + str(msglen * 8))
                self.appqueue.append(msg.temperature)
                print(str(msg))
            except IndexError:
                return True
        


    def get_last_temperature(self):
        self.process_messages()

        return temperature

    def send_temp(self):
        msg = moreheat_pb2.Temperature()
        msg.source = "alice"
        self.testtemp = random_walk(self.testtemp)
        msg.temperature = self.testtemp
        ts.socket.send(msg.encode(encoding='utf-8'))
 
    def random_walk(y):
        # put some stuff here to make it stay within normal range
           y += np.random.normal(scale=1)
        return y


class TempSource(GLib.Source):
    def __init__(self, tempsender, callback):
        self.tempsender = tempsender
        GLib.Source.__init__(self)
        self.callback = callback
        #self.pollfds = []

    def prepare(self):
        return False

    def check(self):
        #print('checking')
        return self.tempsender.poll()

    def dispatch(self, callback, args):
        self.callback()
        return True

'''
    def add_socket(self, socket):
        pollfd = GLib.PollFD(socket.fileno(), GLib.IO_IN)
        self.pollfds.append(pollfd)
        self.add_poll(pollfd)

    def rm_socket(self, socket):
        fd = socket.fileno()
        for pollfd in self.pollfds:
            if pollfd.fd == fd:
                self.remove_poll(pollfd)
                self.pollfds.remove(pollfd)
'''


if __name__ == "__main__":
    print("testing tempsender")
     
    ts = Tempsender()

    print(sys.argv)
    time.sleep(1)
    if len(sys.argv) > 1 and sys.argv[1] == "recv":

        while True:
            #print('receiving')
            #data = ts.socket.recv()
            #while data is not None:
            # read until empty
            while (data := ts.socket.recv()) is not None:
                print('received: ' + str(data))
            print('socket empty')
            time.sleep(10)

    else:
        count = 0
        while True:
            #print('testing')         
            msg =  "counting: " + str(count)

            ts.socket.send(msg.encode(encoding='utf-8'))
            count += 1
            #ts.socket.recv()
            #print('adsf')
            #ts.socket.send(b"hello2")
            #ts.socket.recv()
            time.sleep(0.5)



