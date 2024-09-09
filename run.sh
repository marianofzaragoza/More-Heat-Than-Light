#!/usr/bin/env bash
#
#
export GST_DEBUG_DUMP_DIR_DIR=/home/user/media/moreheat/debug

#XDG_RUNTIME_DIR="/run/user/1000" 
#GST_DEBUG=0 
export GDK_BACKEND=x11
DISPLAY=:0 ./venv/bin/python3 $@
