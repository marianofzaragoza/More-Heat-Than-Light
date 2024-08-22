#!/usr/bin/env bash
set -eux
TYPE='mpegts'
EXT='ts'

ffmpeg -y -r 30 -t 5 \
      -f lavfi -i "
    color=white:1920x1080:d=5,
  format=rgb24,
  trim=end=30,
  drawtext=fontcolor=black:fontsize=60:text=\'entanglement seconds: %{eif\:t\:d}\':x=(w-text_w)/2:y=(h-text_h)/2" -f $TYPE entanglement.$EXT

ffmpeg -y -r 30 -t 5\
      -f lavfi -i "
    color=white:1920x1080:d=5,
  format=rgb24,
  trim=end=30,
  drawtext=
    fontcolor=black:
    fontsize=60:
    text=\'broken_channel seconds: %{eif\:t\:d}\':
    x=(w-text_w)/2:
    y=(h-text_h)/2
  " -f $TYPE broken_channel.$EXT




for node in a b
do
  for ca in $(seq 0 11)
  do
  dirn="${node}_${ca}"
  mkdir -p $dirn

    for i in $(seq 1 2)
    do 
 
    fname="testfile_${node}_${ca}_${i}.mp4"     
    echo $fname
      ffmpeg -y  -r 30 -t 5\
        -f lavfi -i "

      color=white:1920x1080:d=5,
    format=rgb24,
    trim=end=30,
    drawtext=
      fontcolor=black:
      fontsize=60:
      text=\'node: $node category: $ca count: $i seconds: %{eif\:t\:d}\':
      x=(w-text_w)/2:
      y=(h-text_h)/2
    " "${dirn}/${fname}"

    done
  done
done

