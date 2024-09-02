#!/usr/bin/env bash
#
##ffmpeg -f lavfi -i testsrc=duration=5:size=800x600:rate=30 -vf drawtext=
#"fontfile=C\\:/Windows/Fonts/arial.ttf:text="%"{pts}:x=(w-tw)/2:y=h-(2*lh):
#fontcolor=white:box=1:boxcolor=0x00000000@1" -preset ultrafast output.mp4
#-vf setpts=N/10/TB \
#ffmpeg -i /path/to/video.mov -qscale:v 3 -vf "drawtext=fontsize=100:fontfile=/Library/Fonts/Arial.ttf: text='%{frame_num}': start_number=1: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000099" /path/to/frames/%d.jpg
#    -vf drawtext="fontcolor=black:fontsize=100 \
#    :text=\'${1}\'\
#    :x=(w-text_w)/2:y=(h-text_h)/2" \
    #-pix_fmt yuva444p10le \
    #-pix_fmt rgba
    #-alpha_bits 10 \
#Incompatible pixel format 'x2rgb10le' for codec 'prores_ks', auto-selecting format 'yuv444p10le'
#Incompatible pixel format 'rgba' for codec 'prores_ks', auto-selecting format 'yuva444p10le'


set -eu
TYPE='mov'
EXT='mov'
RATE=24
DURATION=15
RES="1920x1080"
GEN=0
function ffv1 () {
  ffmpeg -y -r ${RATE} \
    -f lavfi -i "testsrc=duration=${DURATION}:size=${RES}:rate=${RATE}" \
    -vf drawtext="fontcolor=black:fontsize=100 \
    :text=\'s: ${1} %{eif\:t\:d} f: %{frame_num}\'\
    :x=2:y=(h-text_h)/4" \
    -codec ffv1 \
    -pix_fmt rgba \
    -s 1920x1080 \
    -f ${TYPE} ${1}.${EXT}
}

ffv1 testvideo

function generate () {
  ffmpeg -y -r ${RATE} \
    -f lavfi -i "testsrc=duration=${DURATION}:size=${RES}:rate=${RATE}" \
    -vf drawtext="fontcolor=black:fontsize=100 \
    :text=\'s: ${1} %{eif\:t\:d} f: %{frame_num}\'\
    :x=2:y=(h-text_h)/4" \
    -codec prores_ks \
    -pix_fmt rgba \
    -profile:v 4444 \
    -s 1920x1080 \
    -f ${TYPE} ${1}.${EXT}
}

exit 0
if [ $GEN == 0 ]
then
  echo "generating files"
  generate entanglement
  generate broken_channel


else
  echo "listing files"
fi


for node in a b
do
  # 11 categories
  for ca in $(seq 0 11)
  do
    dirn="${node}_${ca}"
    mkdir -p $dirn
    cd $dirn
    pwd

    # 2 testfiles per cat
    for i in $(seq 1 2)
    do 
      echo "$dirn/testfile_${node}_${ca}_${i}" 
      if [ $GEN == 0 ]
      then
        generate "testfile_${node}_${ca}_${i}"   
      fi
    done


    cd ..
  done
done

