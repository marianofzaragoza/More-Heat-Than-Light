import os
import random
from config import DynamicConfigIni
from videochooser import Videochooser
import logging
import mhlog 
import asyncio
from midi import MidiSender

class Playlist():
    def __init__(self):

        self.conf = DynamicConfigIni()
        self.nodename = self.conf.DEFAULT.nodename
        self.playlist_category = eval('self.conf.' + self.nodename + '.playlist_category')
        self.videodir = self.conf.playlist.videodir_final

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("playlist", self)
        self.log.setLevel(logging.WARN)
        
        self.midi = MidiSender()
        self.a_temp = 24
        self.b_temp = 22
        self.mhstate = 'INVALID'
        self.mhcategory = 'invalid'
        self.nowplaying = 'invalid'
        self.channel = 'C'

        if self.nodename == self.conf.playlist.vida_node:
            self.othernode = self.conf.playlist.vidb_node
            self.channel = 'A'
            self.gsheet = True
        elif self.nodename == self.conf.playlist.vidb_node:
            self.othernode = self.conf.playlist.vida_node
            self.channel = 'B'
            self.gsheet = True
        else:
            self.gsheet = False
            self.log.critical("this player has no channel assigned")

      
        self.vc = Videochooser(gsheet=self.gsheet)
        #self.vc.load_data_gsheet()
        #p.save_data_file()
        #self.vc.load_data_file()
        self.check_files()

    def get_other_node(self):
        return self.othernode

    def check_files(self):
        # TODO check everything in gsheet

        files = [ 'VIDEO_MISSING.mov', 'ENTANGLEMENT.mov', "BROKENCHANNEL_A.mov", "BROKENCHANNEL_B.mov" ]
        for file in files:
            if not os.path.isfile(self.videodir + '/' + file):
                self.log.critical('file missing: ' + file)


    def get_playlist_state(self):
        s = dict()
        s['channel'] = self.channel
        if self.channel == 'A':
            s['temp'] = self.a_temp
        elif self.channel == 'B':
            s['temp'] = self.b_temp
        s['mhstate'] = self.mhstate
        s['mhcategory'] = self.mhcategory
        s['nowplaying'] = self.nowplaying
        return s

    def update_temp(self, which, temp):
        #self.log.warning('temp_update ' + which + ' ' + str(temp))
        if which == 'A':
            self.a_temp = temp
        elif which == 'B':
            self.b_temp = temp
        self.mhstate = self.vc.state_from_temp(self.a_temp, self.b_temp)
        if self.channel == 'A':
            self.mhcategory = self.vc.cat_from_temp(self.a_temp)
        elif self.channel == 'B':
            self.mhcategory = self.vc.cat_from_temp(self.b_temp)

    def get_overlay(self):
        video_file = self.vc.get_broken_channel_file(self.channel)
        realpath = os.path.realpath(self.videodir + '/' + video_file)

        self.log.info("get_overlay: " + realpath) 
        return realpath

    def next(self, interrupt=False, entanglement=False):
        

        video_file = self.vc.get_random_file(self.channel, self.a_temp, self.b_temp, entanglement=entanglement)
        self.nowplaying = video_file
        realpath = os.path.realpath(self.videodir + '/' + video_file)
        self.log.info("file: " + realpath)
        #print(p.get_broken_channel_file('A'))
        
        return realpath
     
    def send_specific_midi(self, note):
        self.midi.send_note(note)

    def send_midi(self, interrupt=False):
        #if interrupt == True:
        #    note = 19
        #else:
        note = self.vc.get_midi_note(self.channel, self.a_temp, self.b_temp)
        #asyncio.run(self.midi.send_note_async(note))
        self.midi.send_note(note)


        #self.log.info("midinote: " + str(note))
        #print(p.get_broken_channel_file('A'))
        
        return True
 
       
if __name__ == "__main__":
    print("Testing of the playlist happens here...")
 #   dir = "/home/agustina/More-Heat-Than-Light/testfile"
    dir = "testfile"
    playlist = Playlist()
    playlist.update_temp('A', 20)
    playlist.update_temp('A', 20)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    playlist.update_temp('B',20)
    playlist.update_temp('B', 20)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("Entanglement")
    playlist.update_temp('A', 9)
    playlist.update_temp('B', 9)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("no entanglement but low temperatures")
    playlist.update_temp('A', 8)
    playlist.update_temp('B', 0)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("Cold Broken Chanel")
    playlist.update_temp('A',0)
    playlist.update_temp('B', 20)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("Hot Broken Chanel")
    playlist.update_temp('A', 30)
    playlist.update_temp('B', 50)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("Hot normal playing")
    playlist.update_temp('A', 35)
    playlist.update_temp('B', 35)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("etanglement?")
    playlist.update_temp('A', 0)
    playlist.update_temp('B', 1)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 




