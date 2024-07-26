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
            print('count: ' + str(self.count)  + 'max: ' + str(self.max))
            self.count += 1
            if self.count > self.max:
                print("restarting playlist")
                self.count = 0
            filepath = self.playlist[self.count]
            return os.path.realpath(self.videodir + '/' + filepath)
        else:
            video_path, entanglement, broken_channel = self.next_video( self.a_temp, self.b_temp)
            
            return os.path.realpath(video_path)

       
    def choose_video(self, temp):
        folder_index = 0
        folders = [self.videodir + '/' + self.nodename + '_' + f"{i}" for i in range(11)]
        print(folders)
        if temp > 20:
            folder_index = min((temp - 20) // 2, len(folders) - 1) #increases by two each time
        video = random.choice(os.listdir(folders[folder_index]))
        videopath = folders[folder_index] + '/' + video
        print('choose_video: ' + videopath)
        return videopath

    def next_video(self, a_temp, b_temp):
        videodir=self.videodir
        entanglement = False
        broken_channel = False
        video_path = ""
        if a_temp < 20 and b_temp < 20 and abs(a_temp - b_temp) < 1:
            entanglement = True
            video_path = '??'
        elif abs(a_temp - b_temp) > 10:
            broken_channel = True
            video_path = '??'
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

    playlist = Playlist(True,'b', dir)
    playlist.update_a_temp(20)
    playlist.update_b_temp(20)
    print(playlist.next())
    print(playlist.next()) 
    print(playlist.next()) 


