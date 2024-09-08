#!/usr/bin/env bash
cd ~/media/moreheat
set -eu
TYPE='mov'
EXT='mov'
RATE=24
DURATION=15
RES="1920x1080"
GEN=0
#validate_colorimetry: Need to specify a color matrix when using YUV format (A444_10LE)
##
#    -pix_fmt rgba \
#
function generate () {
  ffmpeg -y -r ${RATE} \
    -f lavfi -i "testsrc=duration=${DURATION}:size=${RES}:rate=${RATE}" \
    -vf drawtext="fontcolor=black:fontsize=100 \
    :text=\'s: ${1} %{eif\:t\:d} f: %{frame_num}\'\
    :x=2:y=(h-text_h)/4" \
    -codec prores_ks \
    -qscale:v 32 \
    -profile:v 4444 \
    -s 1920x1080 \
    -f ${TYPE} ${1}.${EXT}
}

if [ $GEN == 0 ]
then
  echo "generating files"
  cd /home/user/media/moreheat/
  generate VIDEO_MISSING
  generate ENTANGLEMENT
  generate BROKENCHANNEL_A
  generate BROKENCHANNEL_B


else
  echo "listing files"
fi

exit 0

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

