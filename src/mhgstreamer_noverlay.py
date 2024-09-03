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




#from gi.repository import GLib, GObject, Gst, Gtk, GstNet
# Needed for get_xid(), set_window_handle()
#from gi.repository import GdkX11, GstVideo


gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
#gi.require_version('Glib', '1.0')
gi.require_version('GdkX11', '3.0')
gi.require_version('GstVideo', '1.0')
gi.require_version("GLib", "2.0")
gi.require_version("GstNet", "1.0")
from gi.repository import GLib, GObject, Gst, Gtk, GstNet, GdkX11, GstVideo

class MhGstPlayer():
    def __init__(self, xid=None, playlist=None):
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("GstPlayer", self)
        self.log.setLevel(logging.WARN)
        
        self.playlist = playlist
        self.xid = xid

        self.init_gst()

        self.start()
 
    def init_gst(self):
       
        Gst.init(None)
       ############
        # Gst setup
        ############
        #video/x-raw,format=AYUV,framerate=\(fraction\)5/1,width=320,height=240

    #glvideomixer name=videomix latency=1000 sink_1::alpha=0.5 message-forward=false start-time-selection=2  ! glimagesink sync=false\
    #uridecodebin uri="file://${SRC}" name=demux1 ! queue leaky=0 ! videoconvert ! videorate ! queue ! glupload !glcolorconvert ! glcolorscale ! videomix. \
    #uridecodebin uri="file://${SRC2}" name=demux2 ! \
    #queue leaky=0 ! decodebin ! queue  ! videoconvert ! queue ! videorate ! glupload ! glcolorconvert  ! glcolorscale ! videomix.



        ############## old
        self.playbin = Gst.parse_launch('playbin3')
        self.playbin.set_property('instant-uri', True)
 
        vsink = Gst.ElementFactory.make('xvimagesink', 'videosink')
        overlaysink = Gst.parse_bin_from_description('videoconvert ! queue ! fpsdisplaysink name=fps video-sink="glimagesink name=glsink"', 'overlaysink')
        fps = overlaysink.get_by_name('fps')
        glsink = overlaysink.get_by_name('glsink')

        #glist = Gst.ValueList([0,0,1920,1080])
        #array = Gst.ValueArray (glist)
        # https://github.com/GStreamer/gst-python/blob/master/testsuite/test_types.py
        #a = Gst.ValueArray((1,2,3))
        #rect = Gst.ValueArray((0,0,1920,1080))
        #glsink.set_property('render-rectangle', rect)

        videosink = overlaysink.get_by_name('glsink')
        fps.set_property('text-overlay', True)
        fps.set_property('signal-fps-measurements', True)
        fps.set_property('fps-update-interval', 1000)
        fps.connect('fps-measurements', self.on_fps_measurements, videosink)

        asink = Gst.ElementFactory.make('fakesink', 'audiosink')
        self.playbin.set_property('video-sink', overlaysink)
        self.playbin.set_property('audio-sink', asink)
        ############
        # bus
        ###############
        bus = self.playbin.get_bus()
        bus.add_signal_watch()
        #bus.connect('message::error', self._error)
        self.playbin.connect('about-to-finish', self.on_about_to_finish) 
        bus.connect('message::eos', self.on_eos)
        #bus.connect('message::application', self.on_msg)
        #bus.connect('message::state_changed', self.on_msg)
        #bus.connect('message::duration_changed', self.on_msg)
 
        #bus.connect('message::async-done', self._async_done)
        self.pipeline = self.playbin 
        
        # This is needed to make the video output in gtk DrawingArea:
        if self.xid:
            bus.enable_sync_message_emission()
            bus.connect('sync-message::element', self.on_sync_message)

    def interrupt_next(self, start=False, almostfinished=False):
        #print('called: interrupt_next()')

        # gstreamer stuff needs to be called from main thread, but this function can be called from any
        GLib.idle_add(lambda: self.mt_interrupt_next(start=start))


    # this function needs to be called from main thread, do not use directly, use interrupt_next
    def mt_interrupt_next(self, start=False):
        #print('called: MT_interrupt_next()')
        self.pipeline.set_state(Gst.State.NULL)
        
        if start:
            nextfile = self.playlist.next(interrupt=False)
        else: 
            nextfile = self.playlist.next(interrupt=True)
        
        self.playbin.set_property("uri", "file://" + nextfile) 
        self.pipeline.set_state(Gst.State.PLAYING)

        # returning False  removes it from the glib event loop
        return False
 
    def start(self):
        #print('called: start()')
        self.interrupt_next(start=True)
 
    # for playing in a gtk window
    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            #print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)

    def on_eos(self, bus, msg):
        print("EOS")
        #self.interrupt_next()

    def next(self):

        print('called: next()')
        self.interrupt_next(almostfinished=True)
        #nextfile = self.playlist.next()
        #self.log.warning('next() nextfile: ' + nextfile)
        #self.playbin.set_property("uri", "file://" + nextfile) 
        #return True


    def on_about_to_finish(self,*args):
        self.next()

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())
    
    def probe_block(self, pad, buf):
        print("probe blocked")
        return True
   
    def on_fps_measurements(self, element, fps, droprate, avg, videosink):
        self.log.info("fps: ", str(fps) + "droprate: " + str(droprate))
        #caps = videosink.get_static_pad('sink').get_current_caps()
        #print('fps: {:.2f} avg: {:.2f} droprate: {:.2f} caps: {}'.format(fps, avg, droprate, caps))
        #self.print_caps(caps)

    def print_field(self, field, value, pfx):
        str = Gst.value_serialize(value)
        print("{0:s}  {1:15s}: {2:s}".format(
            pfx, GLib.quark_to_string(field), str))
        return True

    def print_caps(self, caps):
        pfx = "     "
        if not caps:
            return

        if caps.is_any():
            print("{0:s}ANY".format(pfx))
            return

        if caps.is_empty():
            print("{0:s}EMPTY".format(pfx))
            return

        for i in range(caps.get_size()):
            structure = caps.get_structure(i)
            print("{0:s}{1:s}".format(pfx, structure.get_name()))
            structure.foreach(self.print_field, pfx) 

    def on_msg(self, bus, msg):
        self.log.debug('msg bus:' + str(bus)+ str(msg) + str(msg.type) )

        if msg.type == Gst.MessageType.DURATION_CHANGED:
            self.log.debug("DURATION CHANGED")
        if msg.type == Gst.MessageType.STATE_CHANGED:
            self.log.debug("STATE CHANGED")
            if isinstance(message.src, Gst.Pipeline):
                old_state, new_state, pending_state = message.parse_state_changed()
                self.log.debug(("Pipeline state changed from %s to %s." % (old_state.value_nick, new_state.value_nick)))
        if msg.type == Gst.MessageType.ERROR:
            err, dbg = msg.parse_error()
            self.log.critical("ERROR:", msg.src.get_name(), ":", err)
            if dbg:
                self.log.critical("Debug info:", dbg)
        if msg.type == Gst.MessageType.APPLICATION:
            #print("application msg")
            #if msg.get_structure().get_name() == 'user_text':
            structn = msg.get_structure().get_name()
            structv = msg.get_structure().get_value('text') 
            #print('appmsg: ' + str(structn) + ' v: ' + str(structv))
                #overlay.set_property('text', struct['text'])
            #overlay.set_property('text','asdfasdf')


if __name__ == '__main__':

    playlist = Playlist(True, 'A', 'videos')
    GObject.threads_init()
    mainloop = GObject.MainLoop()

    p = MhGstPlayer(playlist=playlist)
    mainloop.run()

