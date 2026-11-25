"""Frames for every Thomas shot of ep. 001, ready for the montage (graphics/motion/ep001.py).

480p clips (LongCat chained clips + LatentSync re-synced ones) -> 1872x1080 PNG frames at 30 fps,
60% Real-ESRGAN x4v3 (<name>_sr2.mp4 from Kaggle) + 40% Lanczos from the 480p original: sharper eyes and
contours, while the skin, stubble and sweater keep their texture (decided 22 nov 2026). If an *_sr2.mp4 is
missing, the clip falls back to Lanczos only (printed as a warning). The 720p outro is extracted as before.

Usage: python3 scripts/thomas_frames.py <sr_dir> [--from A --to B]
Only clips whose shots overlap [A, B) (episode seconds) are extracted, so each render job stays small.
"""
import json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "graphics", "motion"))
import ep001  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mouth_hold  # noqa: E402

args = sys.argv[1:]
sr_dir = args[0]
A = float(args[args.index("--from") + 1]) if "--from" in args else -1e9
B = float(args[args.index("--to") + 1]) if "--to" in args else 1e9
tl = json.load(open(os.path.join(ROOT, "graphics", "motion", "ep001_full.timeline.json")))
PLAN = ep001.thomas_plan(tl)
need = sorted({n for a, b, n, *_ in PLAN if a < B and b > A})
# re-synced clips: episode window, for the "mouth closed in the pauses" fix (mouth_hold.py)
RS_WIN = {}
for a, b, n, t0, _ in PLAN:
    if n.startswith("thomas_resync_"):
        w = RS_WIN.get(n, (t0, b))
        RS_WIN[n] = (t0, max(w[1], b))
PAUSES = mouth_hold.resync_pauses(tl, RS_WIN)
CL = os.path.join(ROOT, "presenter", "clips")
for n in need:
    src = os.path.join(CL, n + ".mp4")
    if not os.path.exists(src):
        src = os.path.join(CL, "resync", n + ".mp4")
    out = os.path.join(CL, "frames", n)
    os.makedirs(out, exist_ok=True)
    sr = os.path.join(sr_dir, n + "_sr2.mp4")
    if os.path.exists(sr):
        fc = ("[0:v]fps=30,scale=1872:1080:flags=lanczos,format=gbrp[a];"
              "[1:v]fps=30,scale=1872:1080:flags=lanczos,format=gbrp[b];"
              "[a][b]blend=all_expr='A*0.4+B*0.6',format=rgb24")
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-i", sr, "-filter_complex", fc, os.path.join(out, "f%04d.png")]
    else:
        print("WARNING: no Real-ESRGAN version for", n, "- Lanczos only", flush=True)
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "fps=30,scale=1872:1080:flags=lanczos",
               os.path.join(out, "f%04d.png")]
    subprocess.run(cmd, check=True)
    print(n, len(os.listdir(out)), "frames", flush=True)
    if PAUSES.get(n):
        mouth_hold.hold(out, PAUSES[n], mouth_hold.REF.get(n))
o = os.path.join(CL, "frames", "thomas_outro_720p")
os.makedirs(o, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(CL, "thomas_outro_720p.mp4"), "-vf", "fps=30",
                os.path.join(o, "f%04d.png")], check=True)
