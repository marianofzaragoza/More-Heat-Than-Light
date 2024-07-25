import os

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



