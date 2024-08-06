#!/usr/bin/env bash
#

SRC_DIR='./src/'
protoc -I=$SRC_DIR --python_out=$SRC_DIR $SRC_DIR/moreheat.proto

