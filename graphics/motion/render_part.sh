#!/bin/bash
# Render part N (20 s each) of a full episode in 4K, then concat (see CLAUDE.md, section 8).
# usage: render_part.sh N [timeline.json]
cd "$(dirname "$0")"
N=$1; TL=${2:-../../render/ep001_full.timeline.json}; A=$((N*20)); B=$((A+20))
mkdir -p ../../render/full_parts
python3 ep001.py "$TL" none ../../render/full_parts/p$(printf %02d $N).mp4 --from $A --to $B
