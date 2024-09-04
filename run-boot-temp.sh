#!/usr/bin/env bash

cd /home/user/src/More-Heat-Than-Light/


#./run.sh src/gstinter_overlay_experiment.py



case `hostname` in

  debian)
    ./run.sh src/test_midi.py
    ;;
  alice-vid)
    ./run.sh src/test_midi.py
    ;;
  alice)
    ./run.sh src/tempsender.py
    ;;

  bob)
    ./run.sh src/tempsender.py
    ;;
  carol)
    ./run.sh src/printerreceiver.py
    ;;

  *)
    echo -n "unknown"
    sleep 360

    ;;
esac
