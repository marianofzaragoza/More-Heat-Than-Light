import time
#from alsa_midi import SequencerClient, READ_PORT, NoteOnEvent, NoteOffEvent

from tempsender import Tempsender, TempSource

from config import DynamicConfigIni
import logging
import mhlog 
import pathlib
import asyncio
import asyncio
from alsa_midi import (AsyncSequencerClient, READ_PORT, WRITE_PORT,
                       NoteOnEvent, NoteOffEvent, PortType)
import alsa_midi
from aalink import Link
class Thermometer():
    def __init__(self, testing=False, nodename='alice'):
        self.nodename = nodename
        self.temp = 0
    def read_total_temperature(self):
        return self.temp

    def set_temp(self, temp):
        print('setting: ' + str(temp))
        self.temp = temp
 
class Midi():
    async def bang(self, link, name, interval):
        while True:
            beat = await link.sync(interval)
            self.ts_a.send_temp()
            self.ts_b.send_temp()

            #print('bang', name, beat) 

    def __init__(self):
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("playerui", self)
        self.log.setLevel(logging.WARN)

        self.tm_a = Thermometer()
        self.ts_a = Tempsender(thermometer=self.tm_a, source='alice')
        self.tm_a.set_temp(23)
        self.ts_a.send_temp()

        self.tm_b = Thermometer()
        self.ts_b = Tempsender(thermometer=self.tm_b, source='bob')
        self.tm_b.set_temp(23)
        self.ts_b.send_temp()



        self.client = AsyncSequencerClient("mhtemp")

        self.input_port = self.client.create_port("input", WRITE_PORT)
        #sleep(0.1)
        #self.input_port.connect_to(self.client.list_ports(input=True)[0])
        #sleep(0.1)

        #self.input_port.connect_to(self.get_in_port())

        self.output_port = self.client.create_port("output", READ_PORT)
        #self.output_port.connect_to(self.get_out_port())

        print('out: ' + str(self.output_port) + ' in: ' + str(self.input_port))
        loop = asyncio.get_event_loop()
        link = Link(120, loop)
        link.enabled = True
        loop.run_until_complete(asyncio.gather(self.show_input(), self.bang(link, 'test', 1)))

    async def play_chord(self):
        
        for event in NoteOnEvent(note=60), NoteOnEvent(note=64), NoteOnEvent(note=67):
            await self.client.event_output(event, port=self.output_port)
        await self.client.drain_output()

        await asyncio.sleep(1)

        for event in NoteOffEvent(note=60), NoteOffEvent(note=64), NoteOffEvent(note=67):
            await self.client.event_output(event, port=self.output_port)
        await self.client.drain_output()

    async def show_input(self):
        while True:
                e = await self.client.event_input()
                if type(e) == alsa_midi.ControlChangeEvent:
                    # A: <ControlChangeEvent channel=0 param=19 value=127>
                    # B: <ControlChangeEvent channel=0 param=19 value=127>
                    param = e.param
                    value = float(e.value) / 2.0 - 10
                    print(repr(e))
                    print(param + value)
                    if param == 19:
                        self.tm_a.set_temp(value)
                        self.ts_a.send_temp()
                    if param == 23:
                        self.tm_b.set_temp(value)
                        self.ts_b.send_temp()



                else:
                    print(repr(e))

    def get_out_port(self): 
        out_ports = self.client.list_ports(output=True)
        print('op: ' + str(out_ports))
        for p in out_ports:
            print(type(p))
            print(p.name)
            if p.name == "MIDI Mix MIDI 1":
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
    p = Midi()

