"""Test of the light/fog effects on 3 illustrations (1080p). Usage: SIPHON_SCALE=1 python3 fx_test.py out.mp4"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
import scenes as S  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
S.ILL_DIR = os.path.join(ROOT, "illustrations", "ep001", "img")
D = 6.0
T = [
    (0, D, S.illus, dict(name="a1_conference_hall", move="in", kicker="FALL 2025", line="A major crypto conference.",
                         fog=dict(density=0.30, color=(0.62, 0.52, 0.40), speed=12, far=0.45))),
    (D, 2 * D, S.illus, dict(name="a5_drawer_open", move="in",
                             glows=[dict(kind="pulse", x=330, y=255, r=220, color=(1.0, 0.12, 0.10), min=0.05, max=0.45, hz=1.2),
                                    dict(kind="flicker", x=626, y=50, r=200, color=(1.0, 0.72, 0.35), base=0.22)])),
    (2 * D, 3 * D, S.illus, dict(name="a7_dusty_safe", move="in", kicker="LATE OCTOBER 2026",
                                 line="Still in Drift-linked wallets: ~$138M",
                                 glows=[dict(kind="beam", poly=[(560, 190), (1040, 190), (1330, 400), (600, 400)],
                                             color=(1.0, 0.85, 0.6), base=0.14)])),
]
engine.render(T, 3 * D, sys.argv[1], seg_seconds=6)
print("wrote", sys.argv[1])
