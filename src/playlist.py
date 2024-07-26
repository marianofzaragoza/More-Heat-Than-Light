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

    def __init__(self, testing, node):
        self.testing=testing
        self.node=node
        self.count=0
        self.max=len(self.playlist) - 1

    def next(self):
        if self.testing:
            print('count: ' + str(self.count)  + 'max: ' + str(self.max))
            self.count += 1
            if self.count > self.max:
                print("restarting playlist")
                self.count = 0
            filepath = self.playlist[self.count]
            return os.path.realpath(self.videodir + filepath)
        else:
            a_temp = 20
            b_temp = 20
            video_path, entanglement, broken_channel = next_video(self.node, 20, 20)
            
            return os.path.realpath(self.videodir + video_path)

    def choose_video(temp):
        if temp <= 20:
            cat_files = os.listdir("/cat1")
            video = random.choice(cat_files)
            return os.path(video)
        elif 20 < temp <= 22:
            cat_files = os.listdir("/cat2")
            video = random.choice(cat_files)
            return os.path(video)
        elif 22 < temp <= 24:
            cat_files = os.listdir("/cat3")
            video = random.choice(cat_files)
            return os.path(video)
        elif 24 < temp <= 26:
            cat_files = os.listdir("/cat4")
            video = random.choice(cat_files)
            return os.path(video)
        elif 26 < temp <= 28:
            cat_files = os.listdir("/cat5")
            video = random.choice(cat_files)
            return os.path(video)
        elif 28 < temp <= 30:
            cat_files = os.listdir("/cat6")
            video = random.choice(cat_files)
            return os.path(video)
        elif 30 < temp <= 32:
            cat_files = os.listdir("/cat7")
            video = random.choice(cat_files)
            return os.path(video)
        elif 32 < temp <= 34:
            cat_files = os.listdir("/cat8")
            video = random.choice(cat_files)
            return os.path(video)
        elif 34 < temp <= 36:
            cat_files = os.listdir("/cat9")
            video = random.choice(cat_files)
            return os.path(video)
        elif 36 < temp <= 38:
            cat_files = os.listdir("/cat10")
            video = random.choice(cat_files)
            return os.path(video)
        elif 38 < temp:
            cat_files = os.listdir("/cat11")
            video = random.choice(cat_files)
            return os.path(video)
        
    def next_video(self, name, a_temp, b_temp):
        entanglement = False
        broken_channel = False
        if a_temp < 20 and b_temp < 20 and abs(a_temp - b_temp) < 1:
            entanglement = True
            video_path = '??'
        elif abs(a_temp - b_temp) > 10:
            broken_channel = True
            video_path = '??'
        else: 
            if name == "alice":
                video_path = choose_video(a_temp)
            else:
                video_path = choose_video(b_temp)    
        return video_path, entanglement, broken_channel

if __name__ == "__main__":

    print("Testing of the playlist happens here...")
    playlist = Playlist(True,'A')

    print(playlist.next_video('A', 20.34, 123.111))
    print(playlist.next_video('B', 20.34, 123.111))


 


