 gst-launch-1.0  glvideomixer name=m ! glimagesink \
     videotestsrc ! video/x-raw, format=YUY2 ! glupload ! glcolorconvert ! m. \
     videotestsrc pattern=12 ! video/x-raw, format=I420, framerate=5/1, width=100, height=200 ! queue ! \
     glupload ! glcolorconvert ! m. \
     videotestsrc pattern=1 ! glupload ! gleffects effect=2 ! queue ! m.  \
     videotestsrc pattern=15 ! glupload ! glfiltercube ! queue ! m. \
     videotestsrc ! glupload ! gleffects effect=6 ! queue ! m.
