#!/usr/bin/env bash

#  Stream #0:0[0x1](eng): Video: prores (4444) (ap4h / 0x68347061), yuva444p12le(tv, bt709, progressive), 3840x2160, 365922 kb/s, SAR 1:1 DAR 16:9, 24 fps, 24 tbr, 24 tbn (default)

ffmpeg -i Alice_3840x2160_v1.mov \
  -c:v libvpx -pix_fmt yuva420p \
  -qmin 0 -qmax 20 -crf 5 -b:v 10M \
  -metadata:s:v:0 alpha_mode="1" \
  -s 1920x1080 \
  -auto-alt-ref 0 \
  alice_high.webm

exit 1

ffmpeg -y -i Alice_3840x2160_v1.mov \
  -codec prores_ks \
  -pix_fmt yuva444p12le \
  -alpha_bits 16 \
  -profile:v 4444 \
  -s 1920x1080 \
  -f mov \
  alice_hd.mov

exit 1
ffmpeg -y -i filename.mov \
  -r 29.97 -codec prores_ks \
  -pix_fmt yuva444p10le \
  -alpha_bits 16 \
  -profile:v 4444 \
  -f mov \
  filenameb.mov
