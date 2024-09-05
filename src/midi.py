import time
import sys
#from alsa_midi import SequencerClient, READ_PORT, NoteOnEvent, NoteOffEvent

from tempsender import Tempsender, TempSource

from config import DynamicConfigIni
import logging
import mhlog 
import pathlib
import asyncio
import asyncio
from alsa_midi import (SequencerClient, AsyncSequencerClient, READ_PORT, WRITE_PORT,
                       NoteOnEvent, NoteOffEvent, PortType)
import alsa_midi
from aalink import Link

class MidiSender():
    def __init__(self, mtype="temp"):
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("playerui", self)
        self.log.setLevel(logging.WARN)
       
        self.client = SequencerClient("mhplayer")
        self.output_port = self.client.create_port("output", READ_PORT)
        
        self.cport = self.get_out_port()
        self.output_port.connect_to(self.cport)

        self.log.critical('hello from midi')
        
    async def send_note_async(self,note):
        self.log.critical('send_note_async'+ str(note))
        event = NoteOnEvent(note=note)
        await self.client.event_output(event, port=self.output_port)
        await self.client.drain_output()

    def send_note(self,note):
        self.log.critical('send_note'+ str(note))
        event = NoteOnEvent(note=note)
        self.client.event_output(event, port=self.output_port)
        self.client.drain_output()



    def get_out_port(self): 
        out_ports = self.client.list_ports(output=True)
        #print('op: ' + str(out_ports))
        for p in out_ports:
            #print(type(p))
            #print(p.name)
            if p.name == "stroom":
                out_port = p
        return out_port

    def get_in_port(self):
        in_ports = self.client.list_ports(input=True)
        print('ip: ' + str(in_ports))
        for p in in_ports:
            print(type(p))
            print(p.name)
            if p.name == "MIDI Mix MIDI 1":
                print('se')
                in_port = p
        return in_ports[0]
 
if __name__ == '__main__':
    
        p = MidiSender()
        while True:
            print('hello')
            p.send_note(12)
 
            #asyncio.run(p.send_note_async(12))
            time.sleep(1)

