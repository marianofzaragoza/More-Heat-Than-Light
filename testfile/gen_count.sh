#!/usr/bin/env bash
set -eux
TYPE='mov'
EXT='mov'
RATE=24
DURATION=1
RES="1920x1080"

function generate () {

#ffmpeg -f lavfi -i testsrc=duration=5:size=800x600:rate=30 -vf drawtext=
#"fontfile=C\\:/Windows/Fonts/arial.ttf:text="%"{pts}:x=(w-tw)/2:y=h-(2*lh):
#fontcolor=white:box=1:boxcolor=0x00000000@1" -preset ultrafast output.mp4
#-vf setpts=N/10/TB \
#ffmpeg -i /path/to/video.mov -qscale:v 3 -vf "drawtext=fontsize=100:fontfile=/Library/Fonts/Arial.ttf: text='%{frame_num}': start_number=1: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000099" /path/to/frames/%d.jpg

  ffmpeg -y -r ${RATE} \
    -f lavfi -i "testsrc=duration=${DURATION}:size=${RES}:rate=${RATE}" \
    -vf drawtext="fontcolor=black:fontsize=100 \
    :text=\'${1}\'\
    :x=(w-text_w)/2:y=(h-text_h)/2" \
    -vf drawtext="fontcolor=black:fontsize=160 \
    :text=\'s: %{eif\:t\:d} f: %{frame_num}\'\
    :x=2:y=(h-text_h)/4" \
    -codec prores_ks \
    -pix_fmt yuva444p10le \
    -alpha_bits 16 \
    -profile:v 4444 \
    -s 1920x1080 \
    -f ${TYPE} ${1}.${EXT}

}

generate entanglement
generate broken_channel



for node in a b
do
  for ca in $(seq 0 11)
  do
  dirn="${node}_${ca}"
  mkdir -p $dirn
  cd $dirn

    for i in $(seq 1 2)
    do 
    generate "testfile_${node}_${ca}_${i}"   

    done
  done
done

