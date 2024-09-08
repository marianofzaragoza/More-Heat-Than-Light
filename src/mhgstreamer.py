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
    def __init__(self, xid=None, playlist=None, osc=None):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        #FIXME 
        #os.putenv('GST_DEBUG_DUMP_DIR_DIR', current_dir + '/../debug/')
        self.ot = False
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("GstPlayer", self)
        self.log.setLevel(logging.WARN)
       
        self.playlist = playlist
        self.xid = xid
        self.osc = osc
        
        self.overlay_enabled = True
        self.overlaytest = True
        self.overlay_active = False
        #self.tfile = "video/random/305_24p.mp4"

        self.cst = "TRANSMISSION"
        self.lst = "ENTANGLEMENT" 
        self.in_entanglement = False
        self.pre_entanglement = False
        #self.hdfile = "video/quality/HD PRORESS.mov"
        #self.overlayfile = "video/animation/alice_hd.mov"
        #self.hdfile = "/home/user/media/moreheat/VIDEO_MISSING.mov"
        self.overlayfile = "/home/user/media/moreheat/BROKENCHANNEL_A.mov"
        
        self.tfile = "/home/user/media/moreheat/VIDEO_MISSING.mov"

        Gst.debug_set_active(True)
        Gst.debug_set_default_threshold(1)

        #GST
        Gst.init(None)

        self.videomixer = self.create_mixerpipeline() 
        # This is needed to make the video output in gtk DrawingArea:
        self.bus = self.videomixer.get_bus()

        if self.xid:
            self.bus.enable_sync_message_emission()
            self.bus.connect('sync-message::element', self.on_sync_message)


        self.videomixer.set_state(Gst.State.PLAYING)


        self.videoplayer = self.create_pb('_video', self.tfile)
        
        self.videomixer.get_bus().connect('message', self.on_message)


        self.videoplayer.set_state(Gst.State.PLAYING)

        if self.overlay_enabled:
            self.overlayplayer = self.create_pb('_overlay', self.overlayfile)
            self.overlayplayer.set_state(Gst.State.PLAYING)
        self.log_stuff()
        #self.interrupt_next(start=True)

    def on_state_changed(self, bus, msg):
        old, new, pending = msg.parse_state_changed()
        if not msg.src == self.videoplayer:
            # not from the playbin, ignore
            return

        self.state = new
        print("State changed from {0} to {1}".format(
            Gst.Element.state_get_name(old), Gst.Element.state_get_name(new)))

        #if old == Gst.State.PAUSED and new == Gst.State.PAUSED:
        #    self.videoplayer.set_state(Gst.State.NULL)
        #    self.videoplayer.set_state(Gst.State.PLAYING)



    def statemachine(self, onvideochange=False):

        # get temp from  playlist
        self.playlist.a_temp 
        # get state from videochooser
        nst = self.playlist.vc.state_from_temp(self.playlist.a_temp, self.playlist.b_temp)
        # check 
        cst = self.cst
        if nst == self.cst:
            #self.overlay(True)

            return (cst, nst)

        elif cst == "TRANSMISSION" and nst == "ENTANGLEMENT":
            self.pre_entanglement = True
            self.cst = "ENTANGLEMENT"

        elif cst == "TRANSMISSION" and nst == "BROKENCHANNEL":
            self.overlay(True)
            # enable overlay  (go to start of overlay video)
            self.cst = "BROKENCHANNEL"

        elif cst == "ENTANGLEMENT" and nst == "TRANSMISSION":
            self.pre_entanglement = False
            self.in_entanglement = False
            self.cst = "TRANSMISSION"

        elif cst == "ENTANGLEMENT" and nst == "BROKENCHANNEL":
            self.pre_entanglement = False
            self.in_entanglement = False
            self.overlay(True)
            self.cst = "BROKENCHANNEL"

        elif cst == "BROKENCHANNEL" and nst == "TRANSMISSION":
            self.overlay(False)
            #note = self.playlist.vc.get_midi_note()
            note = self.playlist.vc.get_midi_note(self.playlist.channel, self.playlist.a_temp, self.playlist.b_temp)

            self.log.critical('note exiting brokenchannel ' + str(note))
            self.playlist.send_specific_midi(note) 
            self.cst = "TRANSMISSION"
            
        elif cst == "BROKENCHANNEL" and nst == "ENTANGLEMENT":
            self.pre_entanglement = True
            self.overlay(False)
            self.cst = "ENTANGLEMENT"
        self.log.critical("went from: " + cst + " to " + nst) 
        return (cst, nst)

    
    def format_ns(self, ns):
        s, ns = divmod(ns, 1000000000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)

        #return "%u:%02u:%02u.%09u" % (h, m, s, ns)
        return "%u:%02u:%02u" % (h, m, s)

    def get_pos(self):
        booledur, duration = self.videoplayer.query_duration(Gst.Format.TIME)
        boole, current = self.videoplayer.query_position(Gst.Format.TIME)
        if boole == False:
            #self.log.critical("video stuck")
            vidpos = "P (STUCK): {0} / {1}".format(self.format_ns(current), self.format_ns(duration))
            #self.interrupt_next(start=True)
        else:
            #self.log.critical("video not stuck yet")
            vidpos = "P: {0} / {1}".format(self.format_ns(current), self.format_ns(duration))

        self.log.info( 'video, dur: ' + str(self.videoplayer.query_duration(Gst.Format.TIME)) + ' pos: '+ str(self.videoplayer.query_position(Gst.Format.TIME)) )
        
        #print(vidpos)
        return vidpos

    def get_olpos(self):
        booledur, duration = self.overlayplayer.query_duration(Gst.Format.TIME)
        boole, current = self.overlayplayer.query_position(Gst.Format.TIME)
        if boole == False:
            #self.log.critical("video stuck")
            vidpos = "P (STUCK): {0} / {1}".format(self.format_ns(current), self.format_ns(duration))
            #self.interrupt_next(start=True)
        else:
            #self.log.critical("video not stuck yet")
            vidpos = "P: {0} / {1}".format(self.format_ns(current), self.format_ns(duration))

        #self.log.info( 'video, dur: ' + str(self.videoplayer.query_duration(Gst.Format.TIME)) + ' pos: '+ str(self.videoplayer.query_position(Gst.Format.TIME)) )
        
        #print(vidpos)
        return vidpos


    def log_stuff(self):

        ps = self.playlist.get_playlist_state()
        self.osc.send_video_msg(ps)

        '''
        video_state = self.videoplayer.get_state(Gst.CLOCK_TIME_NONE)

        if self.overlay_enabled:
            overlay_state = self.overlayplayer.get_state(Gst.CLOCK_TIME_NONE)

            print('video state: ' + str(video_state.state) + 'overlay state ' + str(overlay_state.state))
        '''

        Gst.debug_bin_to_dot_file(self.videoplayer, Gst.DebugGraphDetails.ALL, 'gstdebug_videoplayer_' )
        Gst.debug_bin_to_dot_file(self.videomixer, Gst.DebugGraphDetails.ALL, 'gstdebug_videomixer_' + '3' )
        #self.toggle_overlay()
        #print(self.get_pos())
        if self.overlay_enabled:

            Gst.debug_bin_to_dot_file(self.overlayplayer, Gst.DebugGraphDetails.ALL, 'gstdebug_overlayplayer_' + '2' )
            self.log.info( 'overlay, dur: ' + str(self.overlayplayer.query_duration(Gst.Format.TIME)) + ' pos: '+ str(self.overlayplayer.query_position(Gst.Format.TIME)) )
     

    def quit(self):
        self.videomixer.set_state(Gst.State.NULL)
        self.videoplayer.set_state(Gst.State.NULL)
        if self.overlay_enabled:
            self.overlayplayer.set_state(Gst.State.NULL)

    def get_overlay_pad(self):
        pads = self.videomixer.get_by_name('videomix').pads
        for p in pads:
            if p.get_peer().get_parent_element().name == "overlayplayer":
                return p


    def toggle_overlay(self):
        if self.ot == True:
            self.overlay(True)
            self.ot = False
        else:
            self.ot = True
            self.overlay(False)
            
        """
        pads = self.videomixer.get_by_name('videomix').pads
        for p in pads:
            if p.get_peer().get_parent_element().name == "overlayplayer":
                active = p.get_property("alpha") 

        print("toggle " + str(active))

        if active == 1:
            ns = 0
            self.overlay_active = False
        else:
            ns = 1
            self.overlay_active = True

        pads = self.videomixer.get_by_name('videomix').pads
        for p in pads:
            if p.get_peer().get_parent_element().name == "overlayplayer":
                p.set_property("alpha", ns) 
        """

    def overlay(self, onoff):
        print('overlay ' + str(onoff) + ' a: ' + str(self.overlay_active)) 
        p = self.get_overlay_pad()
        active = p.get_property("alpha") 
        if onoff == True and active == 0:
            self.playlist.send_specific_midi(20) 
        #and self.overlay_active == False:
            # should be enabled, but is not enabled
            self.overlayplayer.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0 * Gst.SECOND)
            p.set_property("alpha", 1) 
            self.overlay_active = True
        elif onoff == False and active == 1:
            p.set_property("alpha", 0)
            self.overlay_active == False




    def create_mixerpipeline(self):
        #  intervideosrc gstintervideosrc.c:411:gst_inter_video_src_create:<video_src_1> Failed to negotiate caps video/x-raw, format=(string)I420, width=(int)1280, height=(int)720, interlace-mode=(string)progressive, pixel-aspect-ratio=(fraction)1/1, chroma-site=(string)mpeg2, colorimetry=(string)bt709, framerate=(fraction)24/1

        videomixer = Gst.parse_launch(
           "intervideosrc name=video_src_1 channel=channel_video ! queue  !  clocksync sync-to-first=true sync=true !  videoconvert ! queue ! videoscale !  video/x-raw,width=1920,height=1080,framerate=24/1 ! queue name=videoplayer ! videomix. " +
            "intervideosrc name=video_src_2 channel=channel_overlay ! queue ! clocksync sync-to-first=true sync=true ! videoconvert ! queue ! videoscale ! video/x-raw,width=1920,height=1080,framerate=24/1 ! queue name=overlayplayer ! videomix. " +
            "glvideomixer " + 
            "sink_0::alpha=1 "+
            "sink_0::blend-constant-color-alpha=0 "+
            "sink_0::blend-function-src-alpha=14 "+
            #"sink_0::blend-function-dst-alpha=0"+
            "sink_0::blend-function-src-rgb=6 "+ 
            "sink_0::blend-function-dst-rgb=7 "+

            "sink_1::alpha=0 " +
            "sink_1::blend-constant-color-alpha=0 "+
            "sink_1::blend-function-src-alpha=14 "+
            #"sink_1::blend-function-dst-alpha=0 "+
            "sink_1::blend-function-src-rgb=6 "+
            "sink_1::blend-function-dst-rgb=7 "+
                        "name=videomix ! glcolorconvert ! glimagesink sync=true"
            )

        return videomixer

    def on_eos(self, bus, msg):
        # gstreamer stuff needs to be called from main thread, but this function can be called from any
        GLib.idle_add(lambda: self.mt_on_eos(bus, msg))


    # this should not be called normally, maybe could be used when the interrupt video is played in separate playbin (so it can be preloaded and mixed in)
    def mt_on_eos(self, bus, msg):
        self.log.critical("EOS received from " + str(msg.src))
        pb = msg.src
        name = pb.get_property("name")
        name = pb.get_property("uri")

        if name == "playbin_overlay":
            self.log.critical("playbinoverlay eos")
            msg.src.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0 * Gst.SECOND)
            #uri = Gst.filename_to_uri(self.playlist.get_overlay())
        elif name == "playbin_video":
            self.log.critial("playbinvideo ,  playlist: " + str(uri))
        else:
            self.log.critical("unknown eos")
            #uri = Gst.filename_to_uri(self.hdfile)



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
        self.log.critical(str(name) + " about to finish " + str(uri))
        #print(str(name)+ ' ' + str(state) + ' '  + str(uri))
        #self.log_stuff()
        if name == "playbin_overlay":
            self.log.critical("playbinoverlay about to finish, not doing anytyhing")
            #uri = Gst.filename_to_uri(self.playlist.get_overlay())
            #self.videoplayer.set_state(Gst.State.NULL) 
            #self.videoplayer.set_state(Gst.State.PLAYING) 
 
        elif name == "playbin_video":
            #GLib.idle_add(lambda: self.playlist.send_midi())

            #self.videoplayer.set_state(Gst.State.NULL) 
            uri = Gst.filename_to_uri(self.playlist.next())
            #self.videoplayer.set_state(Gst.State.PLAYING) 
 
            self.log.critical("playbinvideo about to finish,  playlist: " + str(uri))
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

    def on_message(self, bus, msg):
        #print(msg)
        t = msg.type
    
        #print(t)
        if t == Gst.MessageType.ERROR:
            err, dbg = msg.parse_error()
            print("ERROR:", msg.src.get_name(), ":", err)
            #if dbg:
            print("Debug info:", dbg)
            self.terminate = True
        elif t == Gst.MessageType.TAG:
            return 
        elif t == Gst.MessageType.TAG:
            return  
        elif t == Gst.MessageType.EOS:
            print("End-Of-Stream reached")
            self.terminate = True
        elif t == Gst.MessageType.DURATION_CHANGED:
            # the duration has changed, invalidate the current one
            self.duration = Gst.CLOCK_TIME_NONE
        '''
        elif t == Gst.MessageType.STATE_CHANGED:
            old_state, new_state, pending_state = msg.parse_state_changed()
            if msg.src == self.playbin:
                print("Pipeline state changed from '{0:s}' to '{1:s}'".format(
                    Gst.Element.state_get_name(old_state),
                    Gst.Element.state_get_name(new_state)))
                # remember whether we are in the playing state or not
                self.playing = new_state == Gst.State.PLAYING

                if self.playing:
                    # we just moved to the playing state
                    query = Gst.Query.new_seeking(Gst.Format.TIME)
                    if self.playbin.query(query):
                        fmt, self.seek_enabled, start, end = query.parse_seeking()

                        if self.seek_enabled:
                            print(
                                "Seeking is ENABLED (from {0} to {1})".format(
                                    format_ns(start), format_ns(end)))
                        else:
                            print("Seeking is DISABLED for this stream")
                    else:
                        print("ERROR: Seeking query failed")
        '''

    def create_pb(self, name, file):
        uri = Gst.filename_to_uri(file)

        #create playbin
        pb = Gst.parse_launch('playbin3 name=playbin' + name)
        pb.set_property('instant-uri', True)
        pb.set_property("uri", uri) 

        bus = pb.get_bus()
        bus.add_signal_watch()
        #bus.connect("message::error", self.on_error)
        bus.connect("message::eos", self.on_eos)
        bus.connect("message::state-changed", self.on_state_changed)
        #bus.connect("message::application", self.on_application_message)
        bus.connect('message', self.on_message)

        obsink = self.create_ob(name)
        pb.set_property('video-sink', obsink)

        asink = Gst.ElementFactory.make("fakesink", "audiosink")
        pb.set_property('audio-sink', asink)

        #signals
        pb.connect('about-to-finish', self.on_about_to_finish) 


        #playsink = pb.get_by_name('playsink')
        #pb.set_state(Gst.State.PAUSED)
        return pb


    # loads next file in main thread, almostfinished=True will not reset playback
    def interrupt_next(self, start=False, almostfinished=False):
        # gstreamer stuff needs to be called from main thread, but this function can be called from any
        GLib.idle_add(lambda: self.mt_interrupt_next(start=start))


    # this function needs to be called from main thread, do not use directly, use interrupt_next
    def mt_interrupt_next(self, start=False, entanglement=False):
        #print('called: MT_interrupt_next()')
        self.videoplayer.set_state(Gst.State.NULL)
        
        if start:
            nextfile = self.playlist.next(interrupt=False)
        elif entanglement:
            nextfile = self.playlist.next(interrupt=True, entanglement=True)
        else: 
            nextfile = self.playlist.next(interrupt=True)
        
        self.videoplayer.set_property("uri", "file://" + nextfile) 
        self.videoplayer.set_state(Gst.State.PLAYING)

        # returning False  removes it from the glib event loop
        return False

    # for playing in a gtk window
    def on_sync_message(self, bus, msg):
        #self.log.critical("sync message")
        if msg.get_structure().get_name() == 'prepare-window-handle':
            #print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)

   

if __name__ == '__main__':

    playlist = Playlist()
    GObject.threads_init()
    mainloop = GObject.MainLoop()

    p = MhGstPlayer(playlist=playlist)

    mainloop.run()

