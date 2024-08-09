

GST_DEBUG_DUMP_DOT_DIR=. GST_DEBUG=4 DISPLAY=:0 gst-launch-1.0 uridecodebin uri=file:///home/user/src/More-Heat-Than-Light/videos/entanglement.mp4 ! videoconvert ! kmssink

gst-launch-1.0 -v filesrc location='/path/to/file.mp4' ! qtdemux name=demux demux.video_0 ! queue2 ! h265parse ! v4l2slh265dec ! autovideosink demux.audio_0 ! queue2 ! decodebin ! audioconvert ! audioresample ! autoaudiosink
