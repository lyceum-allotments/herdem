#! /usr/bin/env bash

convert dog/0.png -rotate 90 -resize 104x68 ../dog/0.png
convert brown_dog/0.png -rotate 90 -resize 104x68 ../brown_dog/0.png

for i in 0 1 2 3
do
convert sheep/anim3/${i}.png -rotate 90 -resize 102x67 ../sheep/${i}.png
convert black_sheep/anim3/${i}.png -rotate 90 -resize 102x67 ../black_sheep/${i}.png
done

cp ../sheep/2.png ../sheep/4.png
cp ../black_sheep/2.png ../black_sheep/4.png
