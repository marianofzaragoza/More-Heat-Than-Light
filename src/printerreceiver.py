import time
from print_test2 import Printer
from videochooser import Videochooser
from tempsender import Tempsender, TempSource
from config import DynamicConfigIni
import logging
import mhlog 
import pathlib
import asyncio
from aalink import Link


class PrinterReceiver():
    async def print_line(self, link):
        while True:
            beat = await link.sync(self.print_interval)
            self.print_on_clock()
            #print('print', beat) 

    async def receive_msg(self, link):
        while True:
            beat = await link.sync(self.receive_interval)
            self.tempsender.poll()
            self.tempsender.process_messages()
            self.a_temp = self.tempsender.get_stats('alice', 'temperature', 'last')
            self.b_temp = self.tempsender.get_stats('bob', 'temperature', 'last')
            #print('receive a: ' + str(self.a_temp) + ' b: ' + str(self.b_temp) + ' beat: ' + str(beat)) 


    def print_on_clock(self):
        state = self.vc.state_from_temp(self.a_temp, self.b_temp)
        ebob = int(self.tempsender.get_stats('bob_vid', 'entanglement', 'last'))
        ealice = int(self.tempsender.get_stats('alice_vid', 'entanglement', 'last'))

        #and ebob == 127 and ealice == 127
        if state == "ENTANGLEMENT" :
            entanglement = True
            brokenchannel = False
        elif state == "BROKENCHANNEL":
            entanglement = False
            brokenchannel = True
        elif state == "TRANSMISSION":
            entanglement = False
            brokenchannel = False
        else:
            print("unknown state: " + state)
            entanglement = False
            brokenchannel = False 
 
        text_matrix = self.printer.text_to_matrix(self.printer.margin_text, self.printer.font_height_5, self.printer.text_scale)
        print('A: ' + str(self.a_temp) + ' B:' + str(self.b_temp) + ' entanglement: ' + str(entanglement) + ' broken: ' + str(brokenchannel) + ' ebob: ' + str(ebob) + ' eali: ' + str(ealice))
        self.printer.check_time_and_print(self.printer.last_print_time_stamp, self.a_temp, self.b_temp, entanglement, brokenchannel, text_matrix, self.printer.counter)


    def __init__(self):
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("printerreceiver", self)
        self.log.setLevel(logging.WARN)

        self.print_interval = 1
        self.receive_interval = 0.25

        self.vc = Videochooser()
        self.vc.load_data_file()

        self.tempsender = Tempsender()
        self.printer = Printer()
        
        #check_time_and_print(self, last_print_time_stamp, a_temp, b_temp, entanglement, broken_channel, text_matrix, counter):

        loop = asyncio.get_event_loop()
        link = Link(120, loop)
        link.quantum = 12
        link.enabled = True
        loop.run_until_complete(asyncio.gather(self.receive_msg(link), self.print_line(link)))

if __name__ == '__main__':
    p = PrinterReceiver()

