#!/usr/bin/env bash

cd /home/user/src/More-Heat-Than-Light/


#./run.sh src/gstinter_overlay_experiment.py



case `hostname` in

  debian)
    ./run.sh src/gst-player.py
    ;;
  alice-vid)
    DISPLAY=:0 xrandr --output HDMI-0 --mode 1920x1200
    ./run.sh src/gst-player.py
    ;;
  bob-vid)
    DISPLAY=:0 xrandr --output HDMI-0 --mode 1920x1200
    ./run.sh src/gst-player.py
    ;;
  rivest)
    DISPLAY=:0 xrandr --output HDMI-0 --mode 1920x1200
    ./run.sh src/gst-player.py
    ;;
  alice)
    ./run.sh src/tempsender.py
    ;;

  bob)
    ./run.sh src/tempsender.py
    ;;
  carol)
    ./run.sh src/printer.py
    ;;

  *)
    echo -n "unknown"
    ./run.sh src/gst-player.py

    ;;
esac
