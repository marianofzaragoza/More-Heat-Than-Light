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
import datetime
from google.protobuf.timestamp_pb2 import Timestamp

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
from thermometer import Thermometer
from config import DynamicConfigIni
import logging
import mhlog 

'''
* encodeds / decodes temp messages
* sends receives udp messages with temperatures
* keeps track of last termperature received
'''
class Tempsender():
    def __init__(self, enable_appqueue=False, thermometer=False, source=False, node=False):
        self.enable_appqueue=enable_appqueue
        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("tempsender", self)
        self.log.setLevel(logging.CRITICAL)
 
        self.config = DynamicConfigIni()
        if not node == False:
            self.nodename = node
        else:
            if source:
                self.nodename = source
            else:
                self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        if thermometer:
            self.thermometer = thermometer
        else:
            if self.nodename == 'alice' or self.nodename == 'bob':
                self.thermometer = Thermometer()
            else:
                self.thermometer = Thermometer(testing=True)

        # stats (last / avg)
        # [node].type.value
        self.stats = dict()
    
        # incoming messages (whatever is in the udp packet)
        self.rxqueue = deque([])
        
        # outgoing messages for app (python dict with values), not used atm. is for logging all messages eventually
        if self.enable_appqueue:
            self.appqueue = deque([])

        self.socket = Mcast()
        #self.socket.send(b'test')

    def update_stats(self, node, mtype, value, seconds, nanos):
        if node not in self.stats:
            self.stats[node] = dict()
        if mtype not in self.stats[node]:
            self.stats[node][mtype] = dict()
        
        #TODO: check here if we have to switch states
        self.stats[node][mtype]["last_seconds"] = seconds
        self.stats[node][mtype]["last_nanos"] = nanos
        self.stats[node][mtype]["last"] = value

    def get_stats(self, node, mtype, stype):
        self.process_messages()
        #if stype == "last":
        try:
            return round(self.stats[node][mtype][stype], 2)
        except KeyError as e:
            self.log.warning("no STATS: node: " + node + ' mtype: ' + mtype + ' stype: ' + stype + ' err: '+ str(e))
            return 23
        #else:
        #    return 232323


    def poll(self):
        gotdata = False
        while (data := self.socket.recv()) is not None:
            #print('receiving' + str(self.stats))
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
        #ql = len(self.rxqueue)
        self.log.debug("quelenght in process_messages" + str(len(self.rxqueue)))
        while len(self.rxqueue) > 1:
            #try:
            #if True:
            #self.log.critical("quel before" + str(len(self.rxqueue)))

            msg = self.rxqueue.popleft()
            #self.log.critical("quel after" + str(len(self.rxqueue)))

            # decode, update temperature, reject broken, keep stats
            decoded = moreheat_pb2.MhMessage()
            decoded.ParseFromString(msg)
            #msglen = len(msg)
            self.update_stats(decoded.source, decoded.type, decoded.value, decoded.seconds, decoded.nanos)

            #self.log.debug(str(decoded.source) + ' ' + str(decoded.type) + ' ' + str(decoded.value))
            if self.enable_appqueue: 
                self.appqueue.append(decoded.value)
            #except IndexError:
            #    self.log.critical("indexerror in process_messages")
            #    return True
        
    def send_temp(self, entanglement=False):
        msg = moreheat_pb2.MhMessage()
        t = datetime.datetime.now().timestamp()
        seconds = int(t)
        nanos = int(t % 1 * 1e9)
        #proto_timestamp = Timestamp(seconds=seconds, nanos=nanos)

        msg.seconds = seconds
        msg.nanos = nanos
        msg.source = self.nodename
        if entanglement:
            msg.type = "entanglement"
        else:
            msg.type = "temperature"

        if entanglement:
            msg.value = 127
        else:
            msg.value = self.thermometer.read_total_temperature()

        msglen = len(msg.SerializeToString())
        #self.log.debug("length bits: " + str(msglen * 8))
        
        #self.log.critical(msg)
        #self.log.debug(msg.SerializeToString())

        self.socket.send(msg.SerializeToString())
 
    def random_walk(y):
        # put some stuff here to make it stay within normal range
        y += np.random.normal(scale=1)
        return y

# glib socketsource
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
class StaticThermometer():
    def __init__(self, temp=1):
        self.temp = temp
    def read_total_temperature(self):
        return self.temp

    def set_temp(self, temp):
        print('setting: ' + str(temp))
        self.temp = temp
 

if __name__ == "__main__":
     
    aq = False
    if os.environ.get('TESTTEMP') is not None: 
        print("RANDOM temperatures (not real)")
        tm = Thermometer(testing=True)
    else:
        tm = Thermometer()



    ts = Tempsender(enable_appqueue=aq, thermometer=tm)


    ts.log.info("testing tempsender" + str(sys.argv))
    time.sleep(1)
    if len(sys.argv) > 1 and sys.argv[1] == "recv":

        while True:
            #ts.log.debug('receiving')
            ts.poll()
            #data = ts.socket.recv()
            #while data is not None:
            # read until empty

            # test appqueue
            if aq:
                while (data := ts.retrieve_one()) is not None:
                    ts.log.info('received: ' + str(data))
            
    
            print('last from debian: ' + str(ts.get_stats("debian", "temperature", "last")))
            print('last from alice: ' + str(ts.get_stats("alice", "temperature", "last")))
            print('last from bob: ' + str(ts.get_stats("bob", "temperature", "last")))



            #ts.log.debug('socket empty')
            time.sleep(1)

    elif len(sys.argv) > 1 and sys.argv[1] == "static":

        ta = StaticThermometer(temp=int(sys.argv[2]))
        tb = StaticThermometer(temp=int(sys.argv[3]))
        tsa = Tempsender(enable_appqueue=aq, thermometer=ta, node='alice')
        tsb = Tempsender(enable_appqueue=aq, thermometer=tb, node='bob')

        while True:
            tsa.send_temp()
            tsb.send_temp() 

            time.sleep(0.5)

    else:
        count = 0
        while True:
            #print('testing')         
            #msg =  "temp: " + str(ts.thermometer.read_total_temperature())
            ts.send_temp()
            #ts.socket.send(msg.encode(encoding='utf-8'))
            count += 1
            #ts.socket.recv()
            #print('adsf')
            #ts.socket.send(b"hello2")
            #ts.socket.recv()
            time.sleep(0.5)



