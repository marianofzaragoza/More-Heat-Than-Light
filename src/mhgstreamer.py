import os
import pprint
import sys
import gi
import cairo
from config import DynamicConfigIni
import logging
import mhlog 
from datetime import datetime
import time
from playlist import Playlist
from tempsender import Tempsender, TempSource
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('GdkX11', '3.0')
gi.require_version('GstVideo', '1.0')
gi.require_version("GLib", "2.0")
gi.require_version("GstNet", "1.0")
from gi.repository import GLib, GObject, Gst, Gtk, GstNet, GdkX11, GstVideo

class MhGstPlayer():
    def __init__(self, xid=None, playlist=None):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.putenv('GST_DEBUG_DUMP_DIR_DIR', current_dir + '/../debug/')

        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("GstPlayer", self)
        self.log.setLevel(logging.WARN)
        
        self.playlist = playlist
        self.xid = xid
        self.overlay = True

        self.hdfile = "video/quality/HD PRORESS.mov"
        self.overlayfile = "video/animation/alice_hd.mov"
        self.tfile = "video/random/305_24p.mp4"

        #GST
        Gst.init(None)

        self.videomixer = self.create_mixerpipeline() 
        self.videomixer.set_state(Gst.State.PLAYING)

        self.videoplayer = self.create_pb('_video', self.tfile)
        self.videoplayer.set_state(Gst.State.PLAYING)

        if self.overlay:
            self.overlayplayer = self.create_pb('_overlay', self.overlayfile)
            self.overlayplayer.set_state(Gst.State.PLAYING)
        # This is needed to make the video output in gtk DrawingArea:
        self.bus = self.videomixer.get_bus()

        if self.xid:
            self.bus.enable_sync_message_emission()
            self.bus.connect('sync-message::element', self.on_sync_message)


        #self.interrupt_next(start=True)

    def log_stuff(self):
        Gst.debug_bin_to_dot_file(self.videoplayer, Gst.DebugGraphDetails.ALL, 'gstdebug_videoplayer_' )
        Gst.debug_bin_to_dot_file(self.videomixer, Gst.DebugGraphDetails.ALL, 'gstdebug_videomixer_' + '3' )


        self.log.critical( 'video, dur: ' + str(self.videoplayer.query_duration(Gst.Format.TIME)) + ' pos: '+ str(self.videoplayer.query_position(Gst.Format.TIME)) )
        if self.overlay:

            Gst.debug_bin_to_dot_file(self.overlayplayer, Gst.DebugGraphDetails.ALL, 'gstdebug_overlayplayer_' + '2' )
            self.log.critical( 'overlay, dur: ' + str(self.overlayplayer.query_duration(Gst.Format.TIME)) + ' pos: '+ str(self.overlayplayer.query_position(Gst.Format.TIME)) )
     

    def quit(self):
        self.videomixer.set_state(Gst.State.NULL)
        self.videoplayer.set_state(Gst.State.NULL)
        if self.overlay:
            self.overlayplayer.set_state(Gst.State.NULL)



    def create_mixerpipeline(self):
        videomixer = Gst.parse_launch(
           "intervideosrc name=video_src_1 channel=channel_video ! queue  !  clocksync sync-to-first=true sync=true !  videoconvert ! queue ! videoconvert !  video/x-raw,width=1920,height=1080,framerate=24/1 ! videomix. " +
            "intervideosrc name=video_src_2 channel=channel_overlay ! queue ! clocksync sync-to-first=true sync=true ! videoconvert ! queue ! videoconvert ! video/x-raw,width=1920,height=1080,framerate=24/1 ! videomix. " +
            "glvideomixer " + 
            "sink_1::blend-constant-color-alpha=0 "+
            "sink_1::blend-function-src-alpha=14 "+
            #"sink_1::blend-function-dst-alpha=0 "+
            "sink_1::blend-function-src-rgb=6 "+
            "sink_1::blend-function-dst-rgb=7 "+

            "sink_0::blend-constant-color-alpha=0 "+
            "sink_0::blend-function-src-alpha=14 "+
            #"sink_0::blend-function-dst-alpha=0"+
            "sink_0::blend-function-src-rgb=6 "+ 
            "sink_0::blend-function-dst-rgb=7 "+
            "sink_1::alpha=1 sink_0::alpha=1 "+
            "name=videomix ! glcolorconvert ! glimagesink sync=true "
            )
        return videomixer

    def on_eos(self, bus, msg):
        # gstreamer stuff needs to be called from main thread, but this function can be called from any
        GLib.idle_add(lambda: self.mt_on_eos(bus, msg))


    # this should not be called normally, maybe could be used when the interrupt video is played in separate playbin (so it can be preloaded and mixed in)
    def mt_on_eos(self, bus, msg):
        self.log.critical("EOS received from %s " /  str(msg.src))
        '''
        pb = msg.src
        pb.set_state(Gst.State.NULL)
        uri = Gst.filename_to_uri(overlayfile)
        pb.set_property("uri", uri) 
        pb.set_state(Gst.State.PLAYING)
        '''

    def on_about_to_finish(self, pb):
        # gstreamer stuff needs to be called from main thread, but this function can be called from any
        GLib.idle_add(lambda: self.mt_on_about_to_finish(pb))


    def mt_on_about_to_finish(self, pb):
        # FIXME: do this in main thread
        name = pb.get_property("name")
        uri = pb.get_property("uri")
        #state = pb.get_state() 
        self.log.critical(name + " about to finish " + uri)
        #print(str(name)+ ' ' + str(state) + ' '  + str(uri))
        self.log_stuff()
        if name == "playbin_overlay":
            self.log.warning("playbinoverlay about to finish")
            uri = Gst.filename_to_uri(self.overlayfile)
        elif name == "playbin_video":
            self.log.warning("playbinvideo about to fi")
            uri = Gst.filename_to_uri(self.tfile)
        else:
            uri = Gst.filename_to_uri(self.hdfile)

        pb.set_property("uri", uri) 
        pb.set_state(Gst.State.PLAYING)

    def create_ob(self, name):

        ob = Gst.Bin.new(name + "output")

        #queue (input)
        q1 = Gst.ElementFactory.make("queue", "q1")
        ob.add(q1)
        pad = q1.get_static_pad("sink")
        ghostpad = Gst.GhostPad.new("sink", pad)
        ob.add_pad(ghostpad)

        #convert
        convert = Gst.ElementFactory.make("videoconvert", "convert")
        #ob.add(convert)
        #q1.link(convert)

        #rate
        rate = Gst.ElementFactory.make("videorate", "videorate")
        ob.add(rate)
        q1.link(rate)


        #capsfilter (seems needed for alpha)
        capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
        caps_str = "video/x-raw,format=BGRA,width=1920,height=1080,framerate=(fraction)24/1"
        caps = Gst.Caps.from_string(caps_str)
        capsfilter.set_property("caps", caps)
        #ob.add(capsfilter)
        #rate.link(capsfilter)
         
        #queue
        q2 = Gst.ElementFactory.make("queue", "q2")
        ob.add(q2)
        #q2.link(capsfilter)
        rate.link(q2)
       
        #intersink
        intersink = Gst.ElementFactory.make("intervideosink", "video_sink" + name)
        intersink.set_property('channel', 'channel' + name)
        intersink.set_property('sync', True)
        ob.add(intersink)
        q2.link(intersink)

        return ob


    # We make the two pipelines
    def create_pb(self, name, file):
        uri = Gst.filename_to_uri(file)

        #create playbin
        pb = Gst.parse_launch('playbin3 name=playbin' + name)
        pb.set_property('instant-uri', True)
        pb.set_property("uri", uri) 

        obsink = self.create_ob(name)
        pb.set_property('video-sink', obsink)

        asink = Gst.ElementFactory.make("fakesink", "audiosink")
        pb.set_property('audio-sink', asink)

        #signals
        pb.connect('about-to-finish', self.on_about_to_finish) 

        bus = pb.get_bus()
        bus.connect('message::eos', self.on_eos)

        #playsink = pb.get_by_name('playsink')
        #pb.set_state(Gst.State.PAUSED)
        return pb


    # loads next file in main thread, almostfinished=True will not reset playback
    def interrupt_next(self, start=False, almostfinished=False):
        # gstreamer stuff needs to be called from main thread, but this function can be called from any
        GLib.idle_add(lambda: self.mt_interrupt_next(start=start))


    # this function needs to be called from main thread, do not use directly, use interrupt_next
    def mt_interrupt_next(self, start=False):
        #print('called: MT_interrupt_next()')
        self.videoplayer.set_state(Gst.State.NULL)
        
        if start:
            nextfile = self.playlist.next(interrupt=False)
        else: 
            nextfile = self.playlist.next(interrupt=True)
        
        self.videoplayer.set_property("uri", "file://" + nextfile) 
        self.videoplayer.set_state(Gst.State.PLAYING)

        # returning False  removes it from the glib event loop
        return False

    # for playing in a gtk window
    def on_sync_message(self, bus, msg):
        self.log.critical("sync message")
        if msg.get_structure().get_name() == 'prepare-window-handle':
            #print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)

   

if __name__ == '__main__':

    playlist = Playlist()
    GObject.threads_init()
    mainloop = GObject.MainLoop()

    p = MhGstPlayer(playlist=playlist)

    mainloop.run()

