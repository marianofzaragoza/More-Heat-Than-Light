#!/usr/bin/python3
# This program is licensed under GPLv3.
# https://blogs.gnome.org/desrt/2012/05/09/glib-mainloop-sources-in-python-e-g-for-irclib/
#from os import path
import os
import gi
import pprint
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
#gi.require_version('Glib', '1.0')
gi.require_version('GdkX11', '3.0')
gi.require_version('GstVideo', '1.0')
gi.require_version("GLib", "2.0")
gi.require_version("GstNet", "1.0")
import sys
import gi
gi.require_version('Gst', '1.0')
import cairo
from gi.repository import GLib, GObject, Gst, Gtk, GstNet

#
# https://github.com/patrickkidd/pksampler/blob/master/pk/gst/gstsample.py
# https://gstreamer.freedesktop.org/documentation/additional/design/playback-gapless.html?gi-language=c
# https://coaxion.net/blog/2014/08/concatenate-multiple-streams-gaplessly-with-gstreamer/
import random
import argparse
import codecs
import threading
import socket
import threading
import socketserver
#
# Needed for get_xid(), set_window_handle()
from gi.repository import GdkX11, GstVideo

from datetime import datetime
import time
from playlist import Playlist
from tempsender import Tempsender, TempSource


class Player(Gtk.Window):
   
    def init_gui(self):
        Gtk.Window.__init__(self, title="More Heat Than Light")
        self.connect('destroy', self.quit)
        #self.set_default_size(800, 450)
        self.fullscreen()
        Gtk.Window.fullscreen(self)
        # Create DrawingArea for video widget
        self.drawingarea = Gtk.DrawingArea()
        # Create a grid for the DrawingArea and buttons
        grid = Gtk.Grid()
        self.add(grid)

        self.text_tempa = Gtk.Button(label="temp A")
        self.text_tempb = Gtk.Button(label="temp B")
        grid.attach(self.text_tempa, 0, 0, 1, 1)
        grid.attach(self.text_tempb, 1, 0, 1, 1)

        grid.attach(self.drawingarea, 0, 1, 2, 4)
        # Needed or else the drawing area will be really small (1px)
        self.drawingarea.set_hexpand(True)
        self.drawingarea.set_vexpand(True)


    def on_draw(self, _overlay, context, _timestamp, _duration):
        """Each time the 'draw' signal is emitted"""
        context.select_font_face('Open Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(40)
        context.move_to(100, 100)
        context.text_path('HELLO' + str(_timestamp) + ' ' + str(_duration))
        context.set_source_rgb(0.5, 0.5, 1)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(1)
        context.stroke()
    
    def on_fps_measurements(self, element, fps, droprate, avg, videosink):
        caps = videosink.get_static_pad('sink').get_current_caps()
        print('fps: {:.2f} avg: {:.2f} droprate: {:.2f} caps: {}'.format(fps, avg, droprate, caps))
        self.print_caps(caps)

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

    def init_gst(self):

        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.environ["GST_DEBUG_DUMP_DOT_DIR"] = current_dir
        os.putenv('GST_DEBUG_DUMP_DIR_DIR', current_dir)
        os.putenv('GST_DEBUG_NO_COLOR', "1")
        os.putenv('GST_DEBUG_FILE', current_dir + '/debug.log')
        print('debug: ' + current_dir)
        Gst.init(None)

        Gst.debug_set_active(True)
        Gst.debug_set_default_threshold(4)

       ############
        # Gst setup
        ############
        self.playbin = Gst.parse_launch('playbin3')
        self.playbin.set_property('instant-uri', True)
 
        vsink = Gst.ElementFactory.make('xvimagesink', 'videosink')
                #overlaysink = Gst.parse_bin_from_description("timeoverlay ! queue ! videoconvert ! textoverlay deltay=300 halignment=1 name=text text=temperature ! videoconvert ! queue  ! xvimagesink", 'overlaysink')
#        overlaysink = Gst.parse_bin_from_description("cairooverlay name=coverlay ! timeoverlay name=t1 ! videoconvert ! timeoverlay name=t2 text=hello halignment=2 ! timeoverlay text=lala ! queue ! videoconvert ! queue  ! glimagesink", 'overlaysink')
        #overlaysink = Gst.parse_launch("timeoverlay name=t1 ! videoconvert ! timeoverlay name=t2 text=hello halignment=2 ! timeoverlay text=lala ! queue ! videoconvert ! queue  ! glimagesink")
 #       overlaysink = Gst.parse_bin_from_description("cairooverlay name=coverlay ! queue ! glimagesink", 'overlaysink')

        cairo = False
        comp = False
        if cairo:
            print("USING CAIRO OVERLAY")
            overlaysink = Gst.parse_bin_from_description("cairooverlay name=coverlay ! queue ! glimagesink", 'overlaysink')
            cairo_overlay = overlaysink.get_by_name('coverlay')
            cairo_overlay.connect('draw', self.on_draw)
        elif comp:
            overlaysink = Gst.parse_bin_from_description("overlaycomposition name=coverlay ! queue ! glimagesink", 'overlaysink')
            cairo_overlay = overlaysink.get_by_name('coverlay')
            cairo_overlay.connect('draw', self.on_composition_draw)

        else: 
            #overlaysink = Gst.parse_bin_from_description("videoconvert ! queue ! timeoverlay ! queue ! videoconvert ! queue ! glimagesink", 'overlaysink')
            #    FPSSINK = 'fpsdisplaysink name=fps video-sink="appsink name=appsink"'

            overlaysink = Gst.parse_bin_from_description('videoconvert ! queue ! fpsdisplaysink name=fps video-sink="glimagesink name=glsink"', 'overlaysink')
            fps = overlaysink.get_by_name('fps')
            videosink = overlaysink.get_by_name('glsink')
            fps.set_property('text-overlay', True)
            fps.set_property('signal-fps-measurements', True)
            fps.set_property('fps-update-interval', 1000)
            fps.connect('fps-measurements', self.on_fps_measurements, videosink)

        asink = Gst.ElementFactory.make('fakesink', 'audiosink')
        self.playbin.set_property('video-sink', overlaysink)
        self.playbin.set_property('audio-sink', asink)
        ###########
        # clock
        #############
        '''
        #pipeline.set_clock(gst.system_clock_obtain())
        #pipeline.set_state(gst.STATE_PLAYING)
        clock = Gst.SystemClockObtain()
        #clock = self.playbin.get_clock()
        print('Using clock: ', clock)
        self.playbin.use_clock(clock)
        '''
        # this will start a server listening on a UDP port
        #clock_provider = GstNet.NetTimeProvider.new(clock, '0.0.0.0', 7123)
        '''

        client_clock = GstNet.NetClientClockNew(NULL,193.123.37.231,
        client_clock = gst_net_client_clock_new (NULL, "192.168.1.42", clock_port, 0);
        base_time = get_base_time ();
        /* Set up synchronisation */
        gst_pipeline_use_clock (GST_PIPELINE (playbin), client_clock);
        gst_element_set_start_time (playbin, GST_CLOCK_TIME_NONE);
        gst_element_set_base_time (playbin, base_time);
---
                                                '''
        # we explicitly manage our base time
        #base_time = clock.get_time()
        #print ('Start slave as: python ./play-slave.py %s [IP] %d %d' % (uri, port, base_time))
        
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

        
        # This is needed to make the video output in our DrawingArea:
        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message)

    '''
    // Connect to the overlaycomposition element's "draw" signal, which is emitted for
    // each videoframe piped through the element. The signal handler needs to
    // return a gst_video::VideoOverlayComposition to be drawn on the frame
    //
    // Signals connected with the connect(<name>, ...) API get their arguments
    // passed as array of glib::Value. For a documentation about the actual arguments
    // it is always a good idea to check the element's signals using either
    // gst-inspect, or the online documentation.
    //
    // In this case, the signal passes the gst::Element and a gst::Sample with
    // the current buffer
    '''
    #https://gitlab.freedesktop.org/gstreamer/gstreamer-rs/-/blob/main/examples/src/bin/overlay-composition.rs
    def  on_composition_draw(element, sample, userdata):
        print(element)
        print(sample)
        print(userdata)

        #<__main__.Player object at 0x7f84a2990a00 (__main__+Player at 0x1ddc270)>
        #<__gi__.GstOverlayComposition object at 0x7f84a31ec740 (GstOverlayComposition at 0x22ce340)>
        #<Gst.Sample object at 0x7f84967b3dd0 (GstSample at 0x7f84440b72d0)>


    def __init__(self):
        GObject.threads_init()
        self.init_gui()
        t = threading.Thread(target=self.th_test)
        t.daemon = True
        t.start()

        
        self.notemp = True
        #debug
        if not self.notemp:
            self.tempsender = Tempsender()

        self.playlist = Playlist(True, 'A', 'videos')
        
        self.init_gst()

    def start(self):
        #print('called: start()')
        self.interrupt_next()
   
    def pl_set_state(self,state):
        GLib.idle_add(lambda: self.pipeline.set_state(state))

    def state_change(self,state):
        self.pipeline.set_state(Gst.State.PLAYING)

    def th_test(self):
        time.sleep(random.randint(3,20))
        while True:
            print("interrupting.............")

            self.interrupt_next()
            time.sleep(random.uniform(1,20))
        #Glib.idle_add(lambda: self.th_test())
        #Glib.timeout_add(300, lambda: self.th_test())
 
    def interrupt_next(self):
        #print('called: interrupt_next()')

        # gstreamer stuff needs to be called from main thread, but this function can be called from any
        GLib.idle_add(lambda: self.mt_interrupt_next())



    def mt_interrupt_next(self):
        #print('called: MT_interrupt_next()')
        self.pipeline.set_state(Gst.State.NULL)
        nextfile = self.playlist.next()
        self.playbin.set_property("uri", "file://" + nextfile) 
        self.pipeline.set_state(Gst.State.PLAYING)

        # returning False  removes it from the glib event loop
        return False
       
    def next(self):
        #print('called: next()')
        nextfile = self.playlist.next()
        print('next() nextfile: ' + nextfile)
        self.playbin.set_property("uri", "file://" + nextfile) 
        return True

    #def update(self):
    #    #print('called: update()')

     #   #print('testing')
     #   appmsg = Gst.Structure.new_empty('user_text')
     #   appmsg.set_value('text', 'testing')

      #  bus = self.pipeline.get_bus()
      #  bus.post(Gst.Message.new_application(self.pipeline, appmsg))
      #  GLib.timeout_add(1000, self.update)

    def onnetmessage(self):

        while (msg := self.tempsender.retrieve_one()) is not None: 
            print('got message from net: ' + msg)
            self.text_tempa.set_label(msg)


    def run(self):

        #GLib.timeout_add(200, self.update)
        self.show_all()
        self.xid = self.drawingarea.get_property('window').get_xid()
        self.pipeline.set_state(Gst.State.PLAYING)
        

        #start the player
        self.start()
        if not self.notemp: 
            print("creating msgsource")
            msgsource = TempSource(self.tempsender, self.onnetmessage)
            #simple.ircobj.fn_to_add_socket = source.add_socket
            #simple.ircobj.fn_to_remove_socket = source.rm_socket
            msgsource.attach()
       
        print("starting gtk mainloop")
        Gtk.main()

    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    # for playing in a gtk window
    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            #print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)

    def on_msg(self, bus, msg):
        print('msg bus:' + str(bus)+ str(msg))

        pprint.pp(msg.type)
        pprint.pp(msg.src)
        if msg.type == Gst.MessageType.DURATION_CHANGED:
            print("DURATION CHANGED")
        if msg.type == Gst.MessageType.STATE_CHANGED:
            print("STATE CHANGED")
            if isinstance(message.src, Gst.Pipeline):
                old_state, new_state, pending_state = message.parse_state_changed()
                print(("Pipeline state changed from %s to %s." % (old_state.value_nick, new_state.value_nick)))
        if msg.type == Gst.MessageType.ERROR:
            err, dbg = msg.parse_error()
            print("ERROR:", msg.src.get_name(), ":", err)
            if dbg:
                print("Debug info:", dbg)
        if msg.type == Gst.MessageType.APPLICATION:
            #print("application msg")
            #if msg.get_structure().get_name() == 'user_text':
            structn = msg.get_structure().get_name()
            structv = msg.get_structure().get_value('text') 
            #print('appmsg: ' + str(structn) + ' v: ' + str(structv))
                #overlay.set_property('text', struct['text'])
            #overlay.set_property('text','asdfasdf')


    def on_eos(self, bus, msg):
        print("EOS")
        self.interrupt_next()

    def on_about_to_finish(self,*args):
        self.next()

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())
    
    def probe_block(self, pad, buf):
        print("probe blocked")
        return True

p = Player()
p.run()
