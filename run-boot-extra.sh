#!/usr/bin/env bash

cd /home/user/src/More-Heat-Than-Light/


#./run.sh src/gstinter_overlay_experiment.py



case `hostname` in

  alice-vid)
    # connect midi
    #./run.sh src/test_midi.py
    #
    while true
    do
      aconnect -l
      aconnect 'MIDI Mix':'MIDI Mix MIDI 1' 'mhtemp':'output'
      aconnect -l
      sleep 3
    done
    ;;

  *)
    echo -n "unknown"
    sleep 360

    ;;
esac
