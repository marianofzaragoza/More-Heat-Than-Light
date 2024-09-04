#!/usr/bin/env bash

cd /home/user/src/More-Heat-Than-Light/


#./run.sh src/gstinter_overlay_experiment.py



case `hostname` in

  alice-vid)
    # connect midi
    #./run.sh src/test_midi.py
    sleep 5
    ;;

  *)
    echo -n "unknown"
    sleep 360

    ;;
esac
