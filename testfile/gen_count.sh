

for i in $(seq 1 5)
do 
  
  ffmpeg  -r 30 -t 5\
    -f lavfi -i "

  color=white:1920x1080:d=5,
format=rgb24,
trim=end=30,
drawtext=
  fontcolor=black:
  fontsize=60:
  text='testje $i %{eif\:t\:d}':
  x=(w-text_w)/2:
  y=(h-text_h)/2
" "test$i.mp4"

done


