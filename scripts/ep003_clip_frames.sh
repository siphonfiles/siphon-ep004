#!/usr/bin/env bash
# Extract every ep. 002 Thomas clip (presenter/clips/ep003/*.mp4) to PNG frames at 30 fps for ep003.py.
set -e
mkdir -p presenter/clips/frames
for f in presenter/clips/ep003/*.mp4; do
  [ -e "$f" ] || continue
  n=$(basename "$f" .mp4)
  mkdir -p "presenter/clips/frames/$n"
  ffmpeg -v error -y -i "$f" -vf fps=30 "presenter/clips/frames/$n/%05d.png"
  echo "$n: $(ls presenter/clips/frames/$n | wc -l) frames"
done
