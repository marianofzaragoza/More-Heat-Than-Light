#!/usr/bin/env python
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os
from time import sleep
import time
from threading import Thread

Gst.init(None)
mainloop = GObject.MainLoop()

hdfile = "video/quality/HD PRORESS.mov"
overlayfile = "video/animation/alice_hd.mov"
#overlayfile = "video/animation/animation_low.webm"
#overlayfile = "video/animation/alice_high.webm"


#overlayfile = "video/animation/animation.mxf"
#overlayfile = "video/animation/LONLEY.mov"
#overlayfile = "video/random/transparent-video.webm"
tfile = "video/random/305_24p.mp4"
#overlayfile = ""

current_dir = os.path.dirname(os.path.realpath(__file__))
print(current_dir)
os.putenv('GST_DEBUG_DUMP_DIR_DIR', current_dir + '/../debug/')
print('debug: ' + current_dir)
#Gst.debug_set_active(True)
#Gst.debug_set_default_threshold(4)


#intervideosrc gstintervideosrc.c:411:gst_inter_video_src_create:<video_src_2> Failed to negotiate caps video/x-raw, format=(string)A444_10LE, width=(int)1920, height=(int)1080, interlace-mode=(string)progressive, pixel-aspect-ratio=(fraction)1/1, colorimetry=(string)bt709, framerate=(fraction)30/1

def on_about_to_finish(pb):
    name = pb.get_property("name")
    uri = pb.get_property("uri")
    #state = pb.get_state() 

    #print(str(name)+ ' ' + str(state) + ' '  + str(uri))

    if name == "playbin_overlay":
        print("playbinoverlay")
        uri = Gst.filename_to_uri(overlayfile)
    elif name == "playbin_video":
        print("playbinvideo")
        uri = Gst.filename_to_uri(tfile)
    else:
        uri = Gst.filename_to_uri(hdfile)

    pb.set_property("uri", uri) 
    pb.set_state(Gst.State.PLAYING)

def get_ob(name):

    ob = Gst.Bin.new(name + "output")

    #queue (input)
    q1 = Gst.ElementFactory.make("queue", "q1")
    ob.add(q1)
    pad = q1.get_static_pad("sink")
    ghostpad = Gst.GhostPad.new("sink", pad)
    ob.add_pad(ghostpad)

    #convert
    convert = Gst.ElementFactory.make("videoconvert", "convert")
    ob.add(convert)
    q1.link(convert)

    #rate
    rate = Gst.ElementFactory.make("videorate", "videorate")
    ob.add(rate)
    convert.link(rate)


    #capsfilter (seems needed for alpha)
    '''
    capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
    caps_str = "video/x-raw,width=1920,height=1080,framerate=(fraction)24/1"
    caps = Gst.Caps.from_string(caps_str)
    capsfilter.set_property("caps", caps)
    ob.add(capsfilter)
    rate.link(capsfilter)
    '''
    #queue

    q2 = Gst.ElementFactory.make("queue", "q2")
    ob.add(q2)
    #q2.link(capsfilter)
    convert.link(q2)
   
    #intersink
    intersink = Gst.ElementFactory.make("interpipesink", "video_sink" + name)
    intersink.set_property('name', 'channel' + name)
    #intersink.set_property('channel', 'channel' + name)
    #intersink.set_property('sync', False)
    
    ob.add(intersink)
    q2.link(intersink)

    return ob


# We make the two pipelines
def get_pb(name, file):
    uri = Gst.filename_to_uri(file)

    #create playbin
    pb = Gst.parse_launch('playbin3 name=playbin' + name)
    #pb.set_property('instant-uri', True)
    pb.set_property("uri", uri) 
    pb.set_property('video-sink', get_ob(name))

    #signals
    pb.connect('about-to-finish', on_about_to_finish) 
    #bus.connect('message::eos', self.on_eos)

    #playsink = pb.get_by_name('playsink')
    pb.set_state(Gst.State.PLAYING)
    return pb

videopl = get_pb('_video', tfile)
#overlaypl = get_pb('_overlay', overlayfile)

pipe3 = Gst.parse_launch(
    "interpipesrc name=video_src_1 listen-to=channel_video ! timeoverlay ! queue ! video/x-raw,width=1920,height=1080 !  videoconvert ! queue ! glupload ! glcolorconvert ! videomix. " +
    "interpipesrc name=video_src_2 listen-to=channel_overlay ! timeoverlay ! queue !  video/x-raw,width=1920,height=1080 ! videoconvert ! queue ! glupload ! glcolorconvert! videomix. " +
    "glvideomixer latency=10000 name=videomix ! glupload ! glcolorconvert ! glimagesink"
    )

#
#pipe3 = gst.parse_launch(
#    "intervideosrc name=video_src_1 channel=channel_1 ! queue ! video/x-raw,width=1920,height=1080 ! videoconvert ! queue ! glupload ! glcolorconvert ! videomix. " +
#    "intervideosrc name=video_src_2 channel=channel_2 ! queue ! video/x-raw,width=1920,height=1080 ! videoconvert ! queue ! glupload ! glcolorconvert! videomix. " +
#    "glvideomixer latency=10000 name=videomix ! glupload ! glcolorconvert ! glimagesink"
#    )
#glvideomixer name=videomix latency=1000 sink_1::alpha=0.5 message-forward=false start-time-selection=2  ! glimagesink sync=false\
#uridecodebin uri="file://${SRC}" name=demux1 ! queue leaky=0 ! videoconvert ! videorate ! queue ! glupload !glcolorconvert ! glcolorscale ! videomix. \
#uridecodebin uri="file://${SRC2}" name=demux2 ! \
#queue leaky=0 ! decodebin ! queue  ! videoconvert ! queue ! videorate ! glupload ! glcolorconvert  ! glcolorscale ! videomix.
'''
pipe33 = Gst.parse_launch(
        "glvideomixer name=videomix ! queue ! glcolorscale ! glimagesink " + 
        "intervideosrc name=video_src_1 ! queue ! videoconvert ! queue ! videorate ! queue !  video/x-raw,format=ARGB,width=1920,height=1080  ! glupload ! glcolorconvert ! glcolorscale ! videomix. " +
        "intervideosrc name=video_src_2 ! queue  ! videoconvert ! queue ! videorate !  queue !video/x-raw,format=ARGB,width=1920,height=1080 !  glupload ! glcolorconvert  ! glcolorscale ! videomix."
        )
'''

#video_src_1 = pipe3.get_by_name('video_src_1')
#video_src_2 = pipe3.get_by_name('video_src_2')

pipe3.set_state(Gst.State.PLAYING)
videopl.set_state(Gst.State.PLAYING)
#pipe2.set_state(Gst.State.PLAYING)

def separate_thread():
    sleep(3)
    Gst.debug_bin_to_dot_file(videopl, Gst.DebugGraphDetails.ALL, 'gstdebug_' + '1' )
    #Gst.debug_bin_to_dot_file(overlaypl, Gst.DebugGraphDetails.ALL, 'gstdebug_' + '2' )
    Gst.debug_bin_to_dot_file(pipe3, Gst.DebugGraphDetails.ALL, 'gstdebug_' + '3' )

    while True:
        time.sleep(5)
        print("video")
        print(videopl.query_duration(Gst.Format.TIME))
        print(videopl.query_position(Gst.Format.TIME))
 
        #print(overlaypl.query_duration(Gst.Format.TIME))
        #print(overlaypl.query_position(Gst.Format.TIME))
 


        """
        if duration == Gst.CLOCK_TIME_NONE:
            ret, duration = self.playbin.query_duration(Gst.Format.TIME)
            if not ret:
                print("ERROR: Could not query current duration")
            else:
                print("duration: " + str(self.duration/Gst.SECOND))
                # set the range of the slider to the clip duration (in seconds)
                #self.slider.set_range(0, self.duration / Gst.SECOND)
        
        ret, current = self.playbin.query_position(Gst.Format.TIME)
        print("ret" + str(ret) + ' ' + str(current))
        """
        '''
        if ret:
            # block the "value-changed" signal, so the on_slider_changed
            # callback is not called (which would trigger a seek the user
            # has not requested)
            self.slider.handler_block(self.slider_update_signal_id)

            # set the position of the slider to the current pipeline position
            # (in seconds)
            self.slider.set_value(current / Gst.SECOND)

            # enable the signal again
            self.slider.handler_unblock(self.slider_update_signal_id)
        '''
        #pipe1.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, Gst.SECOND * int(seconds))


myThread = Thread(target=separate_thread, args=())
myThread.start()

mainloop.run()
