#!/usr/bin/python3
# This program is licensed under GPLv3.
# https://blogs.gnome.org/desrt/2012/05/09/glib-mainloop-sources-in-python-e-g-for-irclib/
#from os import path
import os
import pprint
import sys
import gi
import cairo
from aalink import Link

gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
#gi.require_version('Glib', '1.0')
gi.require_version('GdkX11', '3.0')
gi.require_version('GstVideo', '1.0')
gi.require_version("GLib", "2.0")
gi.require_version("GstNet", "1.0")


from gi.repository import GLib, GObject, Gst, Gtk, GstNet, GdkX11, GstVideo, Gdk

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
#from gi.repository import GdkX11, GstVideo

from datetime import datetime
import time
from playlist import Playlist
from tempsender import Tempsender, TempSource

from config import DynamicConfigIni
import logging
import mhlog 

import asyncio
from mhgstreamer import MhGstPlayer 

class PlayerUi(Gtk.Window):
   
    def init_gui(self):
        Gtk.Window.__init__(self, title="More Heat Than Light")
        self.connect('destroy', self.quit)
        #self.set_default_size(800, 450)
        self.fullscreen_at_monitor(self, 0)
        self.fullscreen()
        self.maximize()
        #gtk_widget_set_size_request (GTK_WIDGET(window), 1366, 768);
        #Gtk.Window.fullscreen(self)
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



    def __init__(self):
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("playerui", self)
        self.log.setLevel(logging.WARN)
 
        self.notemp = False
        #debug
        if not self.notemp:
            self.tempsender = Tempsender()
            self.log.info("creating msgsource")
            msgsource = TempSource(self.tempsender, self.onnetmessage)
            #simple.ircobj.fn_to_add_socket = source.add_socket
            #simple.ircobj.fn_to_remove_socket = source.rm_socket
            msgsource.attach()
       

        GObject.threads_init()
        
        #gtk stuff
        self.init_gui()
        
        self.playlist = Playlist(True, 'A', 'videos')
        
        #GLib.timeout_add(200, self.update)
        self.show_all()
        self.xid = self.drawingarea.get_property('window').get_xid()
        
        #gstreamer player
        self.player = MhGstPlayer(playlist=self.playlist,xid=self.xid)

        t = threading.Thread(target=self.th_test)
        t.daemon = True
        t.start()

      
        #TODO start the player
        #self.start()

        self.log.info("starting gtk mainloop")
        Gtk.main()


         
    def pl_set_state(self,state):
        GLib.idle_add(lambda: self.pipeline.set_state(state))

    def state_change(self,state):
        self.pipeline.set_state(Gst.State.PLAYING)

    # this is where we compare state, and 
    async def beat_test(self):
        loop = asyncio.get_running_loop()

        link = Link(int(self.config.sync.bpm), loop)
        link.quantum = int(self.config.sync.quantum) 
        link.enabled = True

        #async def sequence(name):
        #    for i in range(4):
        #        await link.sync(1)
        #        self.log.critical('bang! ' + name)
        while True:
            beatno = await link.sync(float(self.config.sync.syncbeat), float(self.config.sync.offset))
            print('last from debian: ' + str(self.tempsender.get_stats("debian", "temperature", "last")))
            print('last from alice: ' + str(self.tempsender.get_stats("alice", "temperature", "last")))
            print(beatno % int(self.config.sync.modulo))

            bm = beatno % int(self.config.sync.modulo)
            #check
            if bm == 1:
                self.log.warning("check  ")

            #send
            if bm == 2:
                self.log.warning("send  ")

            #receive
            if bm == 3:
                self.log.warning("receive ")

            #play
            if bm == 4:
                self.log.warning("interrupting.............")

                self.player.interrupt_next()

            self.log.critical('bang! ' + str(beatno))



    def th_test(self):
        #time.sleep(random.randint(3,9))
        self.log.critical("hello from th_test")
        asyncio.run(self.beat_test())
        #while True:
        #    time.sleep(random.randint(20,300))
        #    self.log.warning("interrupting.............")
        #    self.interrupt_next()
        #Glib.idle_add(lambda: self.th_test())
        #Glib.timeout_add(300, lambda: self.th_test())
 
      
    def next(self):
        #print('called: next()')
        nextfile = self.playlist.next()
        self.log.warning('next() nextfile: ' + nextfile)
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
        self.log.critical("net message")
        atemp = self.tempsender.get_stats(self.config.playlist.tempa_node , "temperature", "last")
        btemp = self.tempsender.get_stats(self.config.playlist.tempb_node , "temperature", "last")
        self.text_tempa.set_label(str(atemp))
        self.text_tempb.set_label(str(btemp))

        #while (msg := self.tempsender.retrieve_one()) is not None: 
        #    print('got message from net: ' + msg)
        #    self.text_tempa.set_label(msg)


    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def fullscreen_at_monitor(self, window, n):
        screen = Gdk.Screen.get_default()

        monitor_n_geo = screen.get_monitor_geometry(n)
        x = monitor_n_geo.x
        y = monitor_n_geo.y

        window.move(x,y)

        window.fullscreen()

if __name__ == '__main__':
    p = PlayerUi()

