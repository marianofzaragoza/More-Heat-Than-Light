import os
import random
from config import DynamicConfigIni
import logging
import mhlog 



class Playlist():

    playlist_la = [
        #'testfile/test.mp4',
        '1920x1080_1.mp4',
        '1920x1080_2.mp4',
        '3840x2160_1.mp4',
        '3840x2160_2.mp4',
            ]
    interruptfilepath = '../quality/NINJA_S001_S001_T114.mxf'  
    testlist = [
            'test1.mp4',
            '../quality/HD PRORESS.mov',
            'test2.mp4',
            '../quality/HD PRORESS.mov',
            #'../quality/NINJA_S001_S001_T114.mxf',
            'test3.mp4',
            '../quality/HD PRORESS.mov',
            #'../quality/4k-prores.mov',
            'test4.mp4',
            '../quality/HD PRORESS.mov',
            'test5.mp4',
            '../quality/HD PRORESS.mov',
            ]

    def __init__(self):

        self.conf = DynamicConfigIni()
        self.nodename = self.conf.DEFAULT.nodename

        self.playlist_category = eval('self.conf.' + self.nodename + '.playlist_category')



        self.videodir = self.conf.playlist.videodir

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("playlist", self)
        self.log.setLevel(logging.WARN)
 

        self.testing = self.conf.playlist.testing == 'True'

        self.videoext = self.conf.playlist.videoext 

        self.a_temp = 0
        self.b_temp = 0
        if self.testing:
            self.log.critical("playlist in testing mode !")
            self.count=0
            self.max=len(self.testlist) - 1

            self.videodir = self.conf.playlist.videodir_testing
        else:
            self.videodir = self.conf.playlist.videodir



    def update_temp(self, which, temp):
        #self.log.warning('temp_update ' + which + ' ' + str(temp))
        if which == 'A':
            self.a_temp = temp
        elif which == 'B':
            self.b_temp = temp

    def next(self, interrupt=False):
        if self.testing:
            if interrupt:
                return os.path.realpath(self.videodir + '/' + self.interruptfilepath)
            self.count += 1
            if self.count > self.max:
                self.count = 0
            filepath = self.testlist[self.count]
            realpath = os.path.realpath(self.videodir + '/' + filepath)
        else:
            self.log.warning("next: ")
            video_path, entanglement, broken_channel = self.next_video( self.a_temp, self.b_temp)
            realpath = os.path.realpath(self.videodir + '/' + video_path)
        
        self.log.critical("next() " + realpath)
        return realpath

       
    def choose_video(self, temp):
        folder_index = 0
        folders = [self.playlist_category + '_' + f"{i}" for i in range(11)]

        #FIXME
        if temp > 20:
            folder_index = min((temp - 20) // 2, len(folders) - 1) #increases by two each time

        folder_contents = os.listdir(self.videodir + '/' + folders[folder_index])
        #only_mov = list(filter(lambda k: 'ab' in k, lst))
        only_mov = list(filter(lambda x: x.endswith('.mov'), folder_contents))
    
        try:
            video = random.choice(only_mov)
        except IndexError:
            self.log.critical("no mov files found !")
            video = random.choice(folder_contents)

        videopath = folders[folder_index] + '/' + video

        self.log.critical("choose_video return: " + videopath)
        return videopath

    def next_video(self, a_temp, b_temp):
        videodir=self.videodir
        entanglement = False
        broken_channel = False

        '''
        video_path = ""
        if a_temp < 20 and b_temp < 20 and abs(a_temp - b_temp) < 1:
            entanglement = True
            video_path = videodir + '/' + "entanglement." + self.videoext ## Put a valid video path
        elif abs(a_temp - b_temp) > 10:
            broken_channel = True
            video_path = videodir + '/' + "broken_channel." + self.videoext ## Put a valid video path
        else:
        '''
    
        if self.playlist_category == "a":
            video_path = self.choose_video(a_temp)
        elif self.playlist_category == "b":
            video_path = self.choose_video(b_temp)    
        else:
            self.log.critical("no valid playlist category")
        self.log.warning( "next video return: " + str(video_path) + ' ' + str(a_temp) + ' ' + str(b_temp))
        return video_path, entanglement, broken_channel

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




