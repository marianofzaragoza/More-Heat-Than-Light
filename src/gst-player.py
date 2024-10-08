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
from osc_test import OscSender


gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
#gi.require_version('Glib', '1.0')
gi.require_version('GdkX11', '3.0')
gi.require_version('GstVideo', '1.0')
gi.require_version("GLib", "2.0")
gi.require_version("GstNet", "1.0")

import asyncio, gbulb
from gi.repository import GLib, GObject, Gst, Gtk, GstNet, GdkX11, GstVideo, Gdk, Gio

#
# https://github.com/patrickkidd/pksampler/blob/master/pk/gst/gstsample.py
# https://gstreamer.freedesktop.org/documentation/additional/design/playback-gapless.html?gi-language=c
# https://coaxion.net/blog/2014/08/concatenate-multiple-streams-gaplessly-with-gstreamer/
import random
import argparse
import codecs
import socket
#import threading
import socketserver
#
# Needed for get_xid(), set_window_handle()
#from gi.repository import GdkX11, GstVideo

from datetime import datetime
import time
#from testplaylist import Playlist
from playlist import Playlist


from tempsender import Tempsender, TempSource

from config import DynamicConfigIni
import logging
import mhlog 
import pathlib
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
        #FIXME: possible fix for awesome fullscreen
        #gtk_window_set_geometry_hints(main_window, NULL, NULL, 0);
        provider = Gtk.CssProvider()
        srcdir = pathlib.Path(__file__).parent.resolve()
        provider.load_from_file(Gio.File.new_for_path(str(srcdir) + "/style.css"))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
       

        if self.nodename == "debian":
            self.dw = False
            bar_up = True
        elif self.nodename == "test_vid":
            self.dw = True
            bar_up = True
        elif self.nodename == "rivest":
            self.dw = True
            bar_up = True
        else:
            self.dw = False
            bar_up = False


        vbox = Gtk.VBox()
        vbox.get_style_context().add_class('red-background')

        self.add(vbox)
        #vbox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1,0,1,1))
 
        hbox = Gtk.HBox()
        hbox.set_size_request(int(self.config.player.barwidth), int(self.config.player.barheight) / 2.0) 
        hbox.get_style_context().add_class('red-background')

        hbox2 = Gtk.HBox()
        hbox2.set_size_request(int(self.config.player.barwidth), int(self.config.player.barheight) / 2.0) 
        hbox2.get_style_context().add_class('red-background')


        #hbox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1,0,1,1))

        if self.dw:
            self.text_tempa = Gtk.Button(label="temp A")
            self.text_tempa.get_style_context()
            hbox.pack_start(self.text_tempa, True, True, 0)

            self.text_tempb = Gtk.Button(label="temp B")
            hbox.pack_start(self.text_tempb, True, True, 0)

            self.text_sm = Gtk.Button(label="beatcount")
            hbox.pack_start(self.text_sm, True, True, 0)


            self.text_beatno = Gtk.Button(label="beatcount")
            hbox.pack_start(self.text_beatno, True, True, 0)

            self.text_clock = Gtk.Button(label="clock")
            hbox2.pack_start(self.text_clock, True, True, 0)

            self.text_clocknet = Gtk.Button(label="clocknet")
            hbox2.pack_start(self.text_clocknet, True, True, 0)

            self.text_state = Gtk.Button(label="state")
            hbox2.pack_start(self.text_state, True, True, 0)

            self.text_olstate = Gtk.Button(label="olstate")
            hbox2.pack_start(self.text_olstate, True, True, 0)


            self.text_cstate = Gtk.Button(label="cstate")
            hbox2.pack_start(self.text_cstate, True, True, 0)



        # Add canvas to vbox
        # Create DrawingArea for video widget
        self.drawingarea = Gtk.DrawingArea()
        self.drawingarea.set_size_request(int(self.config.player.width), int(self.config.player.height)) 

        if bar_up:
            vbox.pack_start(hbox, True, True, 0)
            vbox.pack_start(hbox2, True, True, 0)
            vbox.pack_start(self.drawingarea, False, False, 0)
        else:
            vbox.pack_start(self.drawingarea, False, False, 0)
            vbox.pack_start(hbox, True, True, 0)
            vbox.pack_start(hbox2, True, True, 0)

                #GLib.timeout_add(200, self.update)
       
        #header_bar = Gtk.HeaderBar()
        #header_bar.set_show_close_button(True)
        #self.set_titlebar(header_bar)  # Place 2


    def __init__(self):
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("playerui", self)
        self.log.setLevel(logging.WARN)
 
        # asyncio for glib
        gbulb.install(gtk=True)

        self.notemp = False
        self.cstate = 'sleep'
        #debug
        if not self.notemp:
            self.tempsender = Tempsender()
            self.tempsender.send_temp(cancel_entanglement=True)

            self.log.info("creating msgsource")
            msgsource = TempSource(self.tempsender, self.onnetmessage)
            #simple.ircobj.fn_to_add_socket = source.add_socket
            #simple.ircobj.fn_to_remove_socket = source.rm_socket
            msgsource.attach()
       

        #GObject.threads_init()
        
        #gtk stuff
        self.init_gui() 
        self.show_all()
        self.xid = self.drawingarea.get_property('window').get_xid()
        self.osc = OscSender()

        self.playlist = Playlist()
        
                #gstreamer player

        self.player = MhGstPlayer(playlist=self.playlist,xid=self.xid, osc=self.osc)

        #t = threading.Thread(target=self.th_test)
        #t.daemon = True
        #t.start()

      
        #TODO start the player
        #self.start()
        #drawingarea.connect('configure-event', on_widget_configure, glsink)
        #window.connect('delete-event', Gtk.main_quit)
        asyncio.run(self.beat_test())

        asyncio.get_event_loop().run_forever()

        self.log.info("starting gtk mainloop")
        Gtk.main()

    async def asas(self):
        # beatloop
        task1 = asyncio.create_task(self.beat_test())

    '''        
    def pl_set_state(self,state):
        GLib.idle_add(lambda: self.player.pipeline.set_state(state))

    def state_change(self,state):
        self.player.pipeline.set_state(Gst.State.PLAYING)

    '''
    def update_playlist_temp(self, which, temp):
        #self.log.warning('called: update_temp ' + which + str(temp))

        # gstreamer stuff needs to be called from main thread, but this function can be called from any
        GLib.idle_add(lambda: self.playlist.update_temp(which=which, temp=temp))


    # this is where we compare state, and 
    async def beat_test(self):
        loop = asyncio.get_running_loop()
        #time.sleep(1)
        link = Link(int(self.config.sync.bpm), loop)
        link.quantum = int(self.config.sync.quantum) 
        link.enabled = True

        #async def sequence(name):
        #    for i in range(4):
        #        await link.sync(1)
        #        self.log.critical('bang! ' + name)
        pos1 = 1
        pos2 = 2
        pos3 = 3
        entseconds = 0
        rxtime = 999999
        while True:
            beatno = await link.sync(float(eval(self.config.sync.syncbeat)), float(self.config.sync.offset))
           
            #if beatno > 100 < 150:
            #    # test fix error
            #    self.player.fix_error(self.player)

            sstr = str(self.player.statemachine())
            if self.dw:
                GLib.idle_add(lambda: self.text_sm.set_label('sm: ' + sstr))

            await asyncio.sleep(0)

               #self.text_beatno.set_label('beat: ' + str(beatno))
            #self.text_clock.set_label('clock: ' + str(beatno))
            nowt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            state = self.playlist.mhstate
            playing = self.playlist.nowplaying
            cat = self.playlist.mhcategory
            await asyncio.sleep(0)
            pos = self.player.get_pos()
            await asyncio.sleep(0)
            olpos = self.player.get_olpos()
            await asyncio.sleep(0)



            if self.dw:
                GLib.idle_add(lambda: self.text_clock.set_label('beatcl: ' + nowt))
                GLib.idle_add(lambda: self.text_beatno.set_label('P: ' + str(link.num_peers) + ' bpm: ' + str(int(link.tempo)) + ' bt: ' + str(int(beatno)) + ' ph: ' + str(int(link.phase)) + ' time: ' + str(link.time)))

                GLib.idle_add(lambda: self.text_state.set_label('s: ' + state + ' f: ' + playing + ' c: ' + cat + ' ' + str(pos)))
                GLib.idle_add(lambda: self.text_olstate.set_label('s:' + str(pos)))

            await asyncio.sleep(0)
            self.update_playlist_temp('A', self.tempsender.get_stats(self.config.playlist.tempa_node, "temperature", "last"))
            await asyncio.sleep(0)
            self.update_playlist_temp('B', self.tempsender.get_stats(self.config.playlist.tempb_node, "temperature", "last"))


            #print('last from debian: ' + str(self.tempsender.get_stats("debian", "temperature", "last")))
            #print('last from alice: ' + str(self.tempsender.get_stats("alice", "temperature", "last")))
            self.log.info(beatno % int(self.config.sync.modulo))
            
            # we need to be on the whole beat, but also in the right phase (beat numbers are not the same on each node.....)
            bm = beatno % int(self.config.sync.modulo)
            bp = int(link.phase)
            await asyncio.sleep(0)



            #print(str(beatno) + ' ' + str(int(link.phase)))
            #check
            if bm == 1 and bp == 1:
                #self.player.toggle_overlay()
                self.cstate = "check"
                
                if self.player.pre_entanglement and not self.player.in_entanglement:
                    t = datetime.now().timestamp()
                    entseconds = int(t)
                    #self.tempsender.send_temp(entanglement=True)
             
                #self.log.warning("check  ")
                boole, pos1 = self.player.videoplayer.query_position(Gst.Format.TIME)
 
        
            #send
            elif bm == 2 and bp == 2:
                self.cstate = "send"
                if self.player.pre_entanglement and not self.player.in_entanglement:
                    # send message 
                    self.tempsender.send_temp(entanglement=True)
                else:
                    self.tempsender.send_temp(cancel_entanglement=True)


                #self.log.warning("send  ")
                boole, pos2 = self.player.videoplayer.query_position(Gst.Format.TIME)
 


            #receive
            elif bm == 3 and bp == 3:

                self.cstate = "receive"
                value = self.tempsender.get_stats(self.playlist.get_other_node(), "entanglement", "last")
                rxtime = self.tempsender.get_stats(self.playlist.get_other_node(), "entanglement", "last_seconds")
                print('b: ' + str(beatno)  +'checktime: ' + str(entseconds) + 'rxtime other: ' + str(rxtime) + ' value: ' + str(value) + 'phase: ' + str(bp), 'pre: ' + str(self.player.pre_entanglement) +  'ent: ' + str(self.player.in_entanglement))
                if (value == 127 and rxtime == entseconds)  and not self.player.in_entanglement and self.player.pre_entanglement:
                    self.log.critical('ENTANG, exact time match')

                if ( value == 127 and rxtime < entseconds + 2 and rxtime > entseconds - 3 )  and not self.player.in_entanglement and self.player.pre_entanglement:
                    self.log.critical('ENTANG, plusminus time match')
 
                #if ( value == 127 and rxtime < entseconds + 2 and rxtime > entseconds - 2 )  and not self.player.in_entanglement and self.player.pre_entanglement:
                if (value == 127 and rxtime == entseconds)  and not self.player.in_entanglement and self.player.pre_entanglement:
                    self.log.critical("ENTANGLEMENT")
                    self.player.playlist.send_specific_midi(19) 
                    #self.tempsender.send_temp(cancel_entanglement=True)

                    self.player.mt_interrupt_next(entanglement=True)
                    self.player.in_entanglement = True
                    self.player.pre_entanglement = False
                    
                ###
                #self.log.warning("receive ")
                await asyncio.sleep(0)
                boole, pos3 = self.player.videoplayer.query_position(Gst.Format.TIME)
                await asyncio.sleep(0)
                self.log.critical( str(pos1) + ' ' + str(pos2) + ' ' + str(pos3))
                if pos1 == pos2 and pos2 == pos3:
                    self.log.critical("the player is stuck")
                    self.player.videoplayer.set_state(Gst.State.NULL)
                    await asyncio.sleep(0)
                    self.player.videoplayer.set_state(Gst.State.PLAYING)
 


            #play
            elif bm == 4 and bp == 4:
                self.cstate = "interrupt"
                #self.log.warning("interrupting.............")

                if eval(self.config.playlist.interrupting + ' == True'):
                    self.log.critical("interrupting!")

                    self.player.interrupt_next()
                else:
                    self.log.critical("playlist interruption disabled")
            elif bm == 5 and bp == 5:
                self.cstate = "sleep"

            #elif bm == 6 and bp == 6:
                #self.player.toggle_overlay()
            await asyncio.sleep(0)


            if self.dw:
                GLib.idle_add(lambda: self.text_cstate.set_label('cstate: ' + self.cstate + str(self.player.pre_entanglement) + str(self.player.in_entanglement)))

            #self.log.critical('bang! ' + str(beatno))



    def th_test(self):
        #time.sleep(random.randint(3,9))
        #self.log.critical("hello from th_test")
        asyncio.run(self.beat_test())
        #Glib.idle_add(lambda: self.th_test())
        #Glib.timeout_add(300, lambda: self.th_test())
 
      
    #def update(self):
    #    #print('called: update()')

     #   #print('testing')
     #   appmsg = Gst.Structure.new_empty('user_text')
     #   appmsg.set_value('text', 'testing')

      #  bus = self.pipeline.get_bus()
      #  bus.post(Gst.Message.new_application(self.pipeline, appmsg))
      #  GLib.timeout_add(1000, self.update)

    def onnetmessage(self):
        self.log.debug("net message")
        atemp = self.tempsender.get_stats(self.config.playlist.tempa_node , "temperature", "last")
        btemp = self.tempsender.get_stats(self.config.playlist.tempb_node , "temperature", "last")
        atime = self.tempsender.get_stats(self.config.playlist.tempa_node , "temperature", "last_seconds")
        adt = datetime.utcfromtimestamp(atime).strftime('%Y-%m-%d %H:%M:%S')
        btime = self.tempsender.get_stats(self.config.playlist.tempb_node , "temperature", "last_seconds")
        bdt = datetime.utcfromtimestamp(btime).strftime('%Y-%m-%d %H:%M:%S')
        nowt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.dw:
            GLib.idle_add(lambda: self.text_clocknet.set_label('nclock: ' + nowt))
            GLib.idle_add(lambda: self.text_tempa.set_label(self.config.playlist.tempa_node + ' temp: ' + str(atemp) + ' : ' + str(adt)))
            GLib.idle_add(lambda: self.text_tempb.set_label(self.config.playlist.tempb_node + ' temp: ' + str(btemp) + ' : ' + str(bdt)))
        #self.text_clocknet.set_label(' net msg last:' + str(now))


        #while (msg := self.tempsender.retrieve_one()) is not None: 
        #    print('got message from net: ' + msg)
        #    self.text_tempa.set_label(msg)


    def quit(self, window):
        self.player.quit()
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

