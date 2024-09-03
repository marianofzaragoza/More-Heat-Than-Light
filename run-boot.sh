#!/usr/bin/env bash

cd /home/user/src/More-Heat-Than-Light/


#./run.sh src/gstinter_overlay_experiment.py



case `hostname` in

  debian)
    ./run.sh src/gst-player.py
    ;;
  alice-vid)
    ./run.sh src/gst-player.py
    ;;
  bob-vid)
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
