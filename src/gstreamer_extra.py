class MhGstPlayerExtra():
    def __init__(self):
 
        """ TODO gst debug in config file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.environ["GST_DEBUG_DUMP_DOT_DIR"] = current_dir
        os.putenv('GST_DEBUG_DUMP_DIR_DIR', current_dir)
        os.putenv('GST_DEBUG_NO_COLOR', "1")
        os.putenv('GST_DEBUG_FILE', current_dir + '/debug.log')
        print('debug: ' + current_dir)
        Gst.debug_set_active(True)
        Gst.debug_set_default_threshold(4)
        """

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

    def on_eos(self, bus, msg):
        self.log.critical("EOS")
        #self.interrupt_next()

    def next(self):
        print('called: next()')
        self.interrupt_next(almostfinished=True)
 
    def on_about_to_finish(self,*args):
        self.next()

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())
 
