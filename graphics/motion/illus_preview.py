"""All ep. 001 illustration shots back to back (with their real durations, text, fog and lights), 1080p.
For checking the animation before rendering the whole episode. Usage: SIPHON_SCALE=1 python3 illus_preview.py out.mp4"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
import ep001  # noqa: E402
import scenes as S  # noqa: E402

T, _ = ep001.build(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep001_full.timeline.json"))))
out, t = [], 0.0
for a, b, fn, p in sorted(T, key=lambda x: x[0]):
    if fn is S.illus:
        d = b - a
        out.append((t, t + d, fn, dict(p, fi=0.15, fo=0.15)))
        t += d
print(len(out), "shots,", round(t, 1), "s")
engine.render(out, t, sys.argv[1], seg_seconds=10)
