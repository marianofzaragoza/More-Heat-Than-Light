#export GST_DEBUG_DUMP_DOT_DIR=./debug/ 
#export GST_DEBUG=4 
export DISPLAY=:0 
#gst-launch-1.0 uridecodebin uri=file:///home/user/src/More-Heat-Than-Light/videos/entanglement.mp4 ! videoconvert ! kmssink


DIR=`pwd`
#SRC="$DIR/testfile/quality/4k-h265.mp4"
SRC="$DIR/video/quality/movie1.mp4"
SRC2="$DIR/video/animation/alice_hd.mov" 
#SRC2="$DIR/video/animation/Alice_3840x2160_v1.mov"
#SRC2="$DIR/video/quality/movie2.mp4"
SRC="$DIR/video/quality/HD PRORESS.mov"
#SRC2="$DIR/testfile/quality/4k-prores.mov"
#SRC2="$DIR/testfile/bbb_sunflower_2160p_30fps_stereo_abl.mp4"

lala () {
gst-launch-1.0 \
    uridecodebin3 uri="file://${SRC2}" !\
    videoconvert ! videorate ! glupload ! glcolorconvert ! glimagesink\

    exit 0
gst-launch-1.0 \
    uridecodebin3 uri="file://${SRC2}" name=demux2 ! \
    queue2 ! queue ! videorate ! queue ! glupload ! glcolorconvert ! glcolorscale ! \
    glimagesink

exit 0
}

#! video/x-raw-yuv,width=1280,height=720,framerate=30/1 !
gst-launch-1.0 \
    glvideomixer name=videomix latency=1000 sink_1::alpha=0.5 message-forward=false start-time-selection=2  ! glimagesink sync=false\
    uridecodebin uri="file://${SRC}" name=demux1 ! queue leaky=0 ! videoconvert ! videorate ! queue ! glupload !glcolorconvert ! glcolorscale ! videomix. \
    uridecodebin uri="file://${SRC2}" name=demux2 ! \
    queue leaky=0 ! decodebin ! queue  ! videoconvert ! queue ! videorate ! glupload ! glcolorconvert  ! glcolorscale ! videomix.
# ! video/x-raw,width=640,height=360!


exit 0


gst-launch-1.0 \
    glvideomixer name=videomix sink_1::xpos=290 sink_1::ypos=300 ! glimagesink sync=true\
    uridecodebin uri=file://$SRC name=demux1 ! queue2 ! decodebin ! queue! glupload !glcolorconvert ! glcolorscale ! videomix. \
    uridecodebin uri=file://$SRC2 name=demux2 ! \
    queue2 ! decodebin ! queue  ! videorate ! glupload ! glcolorconvert  ! glcolorscale ! videomix.
# ! video/x-raw,width=640,height=360!


exit 0
queue2 ! audioconvert ! audioresample ! audiomix. \
    audiomixer name=audiomix !  audioconvert ! autoaudiosink sync=false \
    queue2 ! audioconvert ! audioresample ! audiomix. \

 gst-launch-1.0  glvideomixer name=m ! glimagesink \
     videotestsrc ! video/x-raw, format=YUY2 ! glupload ! glcolorconvert ! m. \
     videotestsrc pattern=12 ! video/x-raw, format=I420, framerate=5/1, width=100, height=200 ! queue ! \
     glupload ! glcolorconvert ! m. \
     videotestsrc ! glupload ! gleffects effect=2 ! queue ! m.  \
     videotestsrc ! glupload ! glfiltercube ! queue ! m. \
     videotestsrc ! glupload ! gleffects effect=6 ! queue ! m.


gst-launch-1.0 \
    glvideomixer name=videomix ! glimagesink sync=true\
    audiomixer name=audiomix !  audioconvert ! autoaudiosink sync=false \
    uridecodebin uri=file://$SRC name=demux1 ! \
    queue2 ! audioconvert ! audioresample ! audiomix. \
    demux1. ! queue2 ! decodebin ! glupload ! glcolorconvert ! videoscale ! video/x-raw,width=640,height=360 ! videomix. \
    uridecodebin uri=file://$SRC2 name=demux2 ! \
    queue2 ! audioconvert ! audioresample ! audiomix. \
    demux2. ! queue2 ! decodebin ! glupload ! glcolorconvert ! videoscale ! video/x-raw,width=320,height=180 ! videomix.


