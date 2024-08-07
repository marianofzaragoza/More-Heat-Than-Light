import os
import random

class Playlist():
    videodir = 'testfile/'

    playlist_la = [
        #'testfile/test.mp4',
        '1920x1080_1.mp4',
        '1920x1080_2.mp4',
        '3840x2160_1.mp4',
        '3840x2160_2.mp4',
            ]
            
    playlist = [
            'test1.mp4',
            'test2.mp4',
            'test3.mp4',
            'test4.mp4',
            'test5.mp4',
            ]

    def __init__(self, testing, node, vdir):
        self.testing=testing
        self.nodename=node
        self.videodir=vdir
        self.videoext="mp4"
        self.count=0
        self.max=len(self.playlist) - 1
        self.a_temp = 0
        self.b_temp = 0

    def update_a_temp(self, temp):
        self.a_temp = temp

    def update_b_temp(self, temp):
        self.b_temp = temp


    def next(self):
        if self.testing:
            self.count += 1
            if self.count > self.max:
                self.count = 0
            filepath = self.playlist[self.count]
            return os.path.realpath(self.videodir + '/' + filepath)
        else:
            video_path, entanglement, broken_channel = self.next_video( self.a_temp, self.b_temp)
            return os.path.realpath(video_path)

       
    def choose_video(self, temp):
        folder_index = 0
        folders = [self.videodir + '/' + self.nodename + '_' + f"{i}" for i in range(11)]
        if temp > 20:
            folder_index = min((temp - 20) // 2, len(folders) - 1) #increases by two each time
        video = random.choice(os.listdir(folders[folder_index]))
        videopath = folders[folder_index] + '/' + video
        return videopath

    def next_video(self, a_temp, b_temp):
        videodir=self.videodir
        entanglement = False
        broken_channel = False
        video_path = ""
        if a_temp < 20 and b_temp < 20 and abs(a_temp - b_temp) < 1:
            entanglement = True
            video_path = videodir + '/' + "entanglement." + self.videoext ## Put a valid video path
        elif abs(a_temp - b_temp) > 10:
            broken_channel = True
            video_path = videodir + '/' + "broken_channel." + self.videoext ## Put a valid video path
        else: 
            if self.nodename == "a":
                video_path = playlist.choose_video(a_temp)
            else:
                video_path = playlist.choose_video(b_temp)    
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




