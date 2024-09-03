import os
import random
from config import DynamicConfigIni
from videochooser import Videochooser
import logging
import mhlog 



class Playlist():
    def __init__(self):

        self.conf = DynamicConfigIni()
        self.nodename = self.conf.DEFAULT.nodename
        self.playlist_category = eval('self.conf.' + self.nodename + '.playlist_category')
        self.videodir = self.conf.playlist.videodir_final

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("playlist", self)
        self.log.setLevel(logging.WARN)
        self.a_temp = 24
        self.b_temp = 22
        self.mhstate = 'INVALID'
        self.mhcategory = 'invalid'
        self.nowplaying = 'invalid'
        self.channel = 'C'
        if self.nodename == self.conf.playlist.vida_node:
            self.channel = 'A'
        elif self.nodename == self.conf.playlist.vidb_node:
            self.channel = 'B'
        else:
            self.log.critical("this player has no channel assigned")

      
        self.vc = Videochooser()
        #self.vc.load_data_gsheet()
        #p.save_data_file()
        self.vc.load_data_file()

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

        self.log.warning("get_overlay: " + realpath) 
        return realpath

    def next(self, interrupt=False):
        

        video_file = self.vc.get_random_file(self.channel, self.a_temp, self.b_temp)
        self.nowplaying = video_file
        realpath = os.path.realpath(self.videodir + '/' + video_file)
        self.log.warning("file: " + realpath)
        #print(p.get_broken_channel_file('A'))
        
        return realpath
       

       
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




