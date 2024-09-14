#!/usr/bin/env bash
cd /home/user/src/More-Heat-Than-Light/
mkdir -p debug
DISPLAY=:0 xrandr --output HDMI-0 --mode 1920x1200

while true
do
    #./run.sh src/gst-player.py > >(tee -a debug/`date +%s`_stdout.log) 2> >(tee -a debug/`date +%s`_stderr.log >&2)
    #./run.sh src/gst-player.py |& tee -a debug/`date +%s`_combined_videoloop.log

  ./run.sh src/gst-player.py



  # Create a new file descriptor 4, pointed at the file
  # which will receive standard error.
  #exec 4<>debug/ccc.out
  # Also print the contents of this file to screen.
  #tail -f debug/ccc.out &
  # Run the command; tee standard output as normal, and send standard error
  # to our file descriptor 4.
  #./run.sh src/gst-player.py 2>&4 | tee debug/bbb.out
  # Clean up: Close file descriptor 4 and kill tail -f.
  #exec 4>&-
  #kill %1
done

