import os
import random
from config import DynamicConfigIni
import logging
import mhlog 



class Playlist():
    def __init__(self):

        self.conf = DynamicConfigIni()
        self.nodename = self.conf.DEFAULT.nodename
        self.playlist_category = eval('self.conf.' + self.nodename + '.playlist_category')
        self.videodir = self.conf.playlist.videodir

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("playlist", self)
        self.log.setLevel(logging.WARN)
        self.a_temp = 0
        self.b_temp = 0
        

    def update_temp(self, which, temp):
        #self.log.warning('temp_update ' + which + ' ' + str(temp))
        if which == 'A':
            self.a_temp = temp
        elif which == 'B':
            self.b_temp = temp

    def next(self, interrupt=False):
        video_path, entanglement, broken_channel = self.next_video( self.a_temp, self.b_temp)
        realpath = os.path.realpath(self.videodir + '/' + video_path)
        
        return realpath

    def next_video(self, a_temp, b_temp):
        videodir=self.videodir
        entanglement = False
        broken_channel = False

        if a_temp < 20 and b_temp < 20 and abs(a_temp - b_temp) < 1:
            entanglement = True
        elif abs(a_temp - b_temp) > 10:
            broken_channel = True
        
if __name__ == "__main__":
    print("Testing of the playlist happens here...")
 #   dir = "/home/agustina/More-Heat-Than-Light/testfile"
    dir = "testfile"
 

    playlist = Playlist(False,'a', dir)
    playlist.update_a_temp(20)
    playlist.update_b_temp(20)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    playlist = Playlist(False,'b', dir)
    playlist.update_a_temp(20)
    playlist.update_b_temp(20)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("Entanglement")
    playlist = Playlist(False,'a', dir)
    playlist.update_a_temp(9)
    playlist.update_b_temp(9)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("no entanglement but low temperatures")
    playlist = Playlist(False,'b', dir)
    playlist.update_a_temp(8)
    playlist.update_b_temp(0)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("Cold Broken Chanel")
    playlist = Playlist(False,'a', dir)
    playlist.update_a_temp(0)
    playlist.update_b_temp(20)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("Hot Broken Chanel")
    playlist = Playlist(False,'a', dir)
    playlist.update_a_temp(30)
    playlist.update_b_temp(50)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("Hot normal playing")
    playlist = Playlist(False,'a', dir)
    playlist.update_a_temp(35)
    playlist.update_b_temp(35)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 

    print("etanglement?")
    playlist = Playlist(False,'a', dir)
    playlist.update_a_temp(0)
    playlist.update_b_temp(1)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 




