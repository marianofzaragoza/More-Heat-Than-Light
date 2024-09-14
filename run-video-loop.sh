#!/usr/bin/env bash
cd /home/user/src/More-Heat-Than-Light/

DISPLAY=:0 xrandr --output HDMI-0 --mode 1920x1200

while true
do
    ./run.sh src/gst-player.py 
done

