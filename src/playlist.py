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

    def __init__(self):
        self.count=0
        self.max=len(self.playlist) - 1
    def next(self):
        print('count: ' + str(self.count)  + 'max: ' + str(self.max))
        self.count += 1
        if self.count > self.max:
            print("restarting playlist")
            self.count = 0
        filepath = self.playlist[self.count]
        return os.path.realpath(self.videodir + filepath)

    def choose_video(self, temp, dir):
        folder_index = 0
        folders = [dir + f"/cat{i}" for i in range(11)]
        if temp > 20:
            folder_index = min((temp - 20) // 2, len(folders) - 1) #increases by two each time
        video = random.choice(os.listdir(folders[folder_index]))
        return video

    def next_video(self, name, a_temp, b_temp, dir):
        entanglement = False
        broken_channel = False
        video_path = ""
        if a_temp < 20 and b_temp < 20 and abs(a_temp - b_temp) < 1:
            entanglement = True
        elif abs(a_temp - b_temp) > 10:
            broken_channel = True
        else: 
            if name == "A":
                video_path = playlist.choose_video(a_temp, dir)
            else:
                video_path = playlist.choose_video(b_temp, dir)    
        return video_path, entanglement, broken_channel

if __name__ == "__main__":
    print("Testing of the playlist happens here...")
    dir = "/home/agustina/More-Heat-Than-Light/testfile"
    playlist = Playlist()
    print(playlist.next_video('A', 10, 40, dir))
    print(playlist.next_video('B', 9, 9, dir))
    


 


