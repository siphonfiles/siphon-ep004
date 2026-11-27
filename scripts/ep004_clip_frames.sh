#!/usr/bin/env bash
# Extract every ep. 004 Thomas clip (presenter/clips/thomas_e4_*.mp4) to PNG frames at 30 fps for ep004.py.
set -e
mkdir -p presenter/clips/frames
for f in presenter/clips/thomas_e4_*.mp4; do
  [ -e "$f" ] || continue
  n=$(basename "$f" .mp4)
  mkdir -p "presenter/clips/frames/$n"
  ffmpeg -v error -y -i "$f" -vf fps=30 "presenter/clips/frames/$n/%05d.png"
  echo "$n: $(ls presenter/clips/frames/$n | wc -l) frames"
done
