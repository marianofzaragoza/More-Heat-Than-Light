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

from gi.repository import GLib
from gi.repository import GObject, Gst, Gtk
#

import argparse
import codecs

import socket
import threading
import socketserver
#
# Needed for get_xid(), set_window_handle()
from gi.repository import GdkX11, GstVideo

from datetime import datetime
#GObject.threads_init()
Gst.init(None)
from playlist import Playlist

class Player(Gtk.Window):
    def __init__(self):

        #debug

        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.environ["GST_DEBUG_DUMP_DOT_DIR"] = current_dir
        os.putenv('GST_DEBUG_DUMP_DIR_DIR', current_dir)
        os.putenv('GST_DEBUG_NO_COLOR', "1")
        os.putenv('GST_DEBUG_FILE', current_dir + '/debug.log')
        '''
        Gst.debug_set_active(True)
        Gst.debug_set_default_threshold(6)
        '''

        self.playlist = Playlist()
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
        grid.attach(self.drawingarea, 0, 1, 2, 1)
        # Needed or else the drawing area will be really small (1px)
        self.drawingarea.set_hexpand(True)
        self.drawingarea.set_vexpand(True)

        '''
        # Quit button
        quit = Gtk.Button(label="Quit")
        quit.connect("clicked", Gtk.main_quit)
        grid.attach(quit, 0, 0, 1, 1)
        '''
        # Create GStreamer pipeline
       # self.pipeline = Gst.parse_launch("playbin name=playbin ! tee name=tee ! queue name=videoqueue ! videoconvert ! xvimagesink")
        #self.pipeline = Gst.parse_launch("playbin name=playbin")
        self.playbin = Gst.ElementFactory.make("playbin", "player")
        vsink = Gst.ElementFactory.make('xvimagesink', 'videosink')
        self.duration = Gst.CLOCK_TIME_NONE

        #overlaysink = Gst.parse_bin_from_description("timeoverlay ! queue ! videoconvert ! textoverlay deltay=300 halignment=1 name=text text=temperature ! videoconvert ! queue  ! xvimagesink", 'overlaysink')
        overlaysink = Gst.parse_bin_from_description("timeoverlay ! queue ! videoconvert ! queue  ! glimagesink", 'overlaysink')



        #self.pipeline.get_by_name("tee").link(self.recordpipe)
 

        asink = Gst.ElementFactory.make('autoaudiosink', 'audiosink')
        self.playbin.set_property('video-sink', overlaysink)
        self.playbin.set_property('audio-sink', asink)

        bus = self.playbin.get_bus()
        bus.add_signal_watch()
        #bus.connect('message::error', self._error)
        self.playbin.connect('about-to-finish', self.on_about_to_finish) 
        bus.connect('message::eos', self.on_eos)
        bus.connect('message::application', self.on_msg)
        bus.connect('message::state_changed', self.on_msg)
        bus.connect('message::duration_changed', self.on_msg)
 
        #bus.connect('message::async-done', self._async_done)
        self.pipeline = self.playbin 

        
        # This is needed to make the video output in our DrawingArea:
        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message)

    def start(self):
        self.interrupt_next()
 
    def interrupt_next(self):
        self.pipeline.set_state(Gst.State.NULL)
        nextfile = self.playlist.next()
        print('huh' + nextfile)
        self.playbin.set_property("uri", "file://" + nextfile) 
        self.pipeline.set_state(Gst.State.PLAYING)
        return True

       
    def next(self):
        #self.pipeline.set_state(Gst.State.NULL)
        nextfile = self.playlist.next()
        print('huh' + nextfile)
        self.playbin.set_property("uri", "file://" + nextfile) 
        #self.pipeline.set_state(Gst.State.PLAYING)
        return True

    def update(self):
        print('testing')
        appmsg = Gst.Structure.new_empty('user_text')
        appmsg.set_value('text', 'testing')

        bus = self.pipeline.get_bus()
        bus.post(Gst.Message.new_application(self.pipeline, appmsg))


        GLib.timeout_add(1000, self.update)

    def run(self):

        GLib.timeout_add(200, self.update)
        self.show_all()
        self.xid = self.drawingarea.get_property('window').get_xid()
        self.pipeline.set_state(Gst.State.PLAYING)
        self.start()
        Gtk.main()

    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)

    def on_msg(self, bus, msg):
        print('msg bus:' + str(bus)+ str(msg))
        pprint.pp(msg.type)
        pprint.pp(msg.src)
        if msg.type == Gst.MessageType.DURATION_CHANGED:
            print("DURATION CHANGED")
        if msg.type == Gst.MessageType.ERROR:
            err, dbg = msg.parse_error()
            print("ERROR:", msg.src.get_name(), ":", err)
            if dbg:
                print("Debug info:", dbg)
        if msg.type == Gst.MessageType.APPLICATION:
            print("application msg")
            #if msg.get_structure().get_name() == 'user_text':
            structn = msg.get_structure().get_name()
            structv = msg.get_structure().get_value('text') 
            print('appmsg: ' + str(structn) + ' v: ' + str(structv))
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
        print("blocked")
        return True

p = Player()
p.run()
