#!/usr/bin/env bash
#
#
GST_DEBUG_DUMP_DIR_DIR=debug/

XDG_RUNTIME_DIR="/run/user/1000" 
GST_DEBUG=0 
GDK_BACKEND=x11
DISPLAY=:0 ./venv/bin/python3 $@
