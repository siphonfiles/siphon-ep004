"""Ep. 004 (Ledger, the CryptoBilis implant) sound plan, same engine and pattern as ep. 001-003 (sound/episode_mix.py).

  - teaser: heist piece in full, ~13 dB under the voice, a bass hit on every cut, black + sub drop + title
  - narration: music only in places, every stop a smooth fade that ends before the next line (never under Thomas)
  - Thomas on camera: dry, except the sign-off (k5, k6) under the closing theme
  - act 3: memory_piano; act 4: drums build -> out + hit on the T-minus cards -> T-0 'vault_run' at 'key' -> fade before d15
  - finale: the heist piece returns soft, fades on the end card

Usage: python3 sound/ep004/ep004_mix.py <voice_dir> <out.wav>   (writes <out>.timeline.json too)
"""
import json
import os
import sys

import numpy as np
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import episode_mix as EM  # noqa: E402
from sting_design import SR  # noqa: E402

V = lambda i, p=0.5: [("voice", i), ("pause", p)]
SECTION = 1.2
FADE = ("music", "fade:4.0", -2.8)   # starts 2.8 s before the end of the line, ends before the next one

P = []
# ---------------- TEASER ----------------
P += [("level", "teaser"), ("music", "full"), ("pause", 1.2)]
P += [("voice", "t1"), ("hit",), ("pause", 0.9), ("card", 2.0)]          # the sealed box
P += [("voice", "t2"), ("hit",), ("pause", 0.9)]
P += [("voice", "t3"), ("hit",), ("pause", 0.9)]
P += [("voice", "t4"), ("hit",), ("pause", 0.9), ("card", 1.6)]          # 335 WALLETS
P += [("voice", "t5"), ("hit",), ("pause", 0.9)]
P += [("voice", "t6"), ("hit",), ("pause", 0.9)]
P += [("voice", "t7"), ("pause", 0.25), ("hit",), ("music", "fade")]
P += [("pause", 1.4), ("drop",), ("card", 4.0)]                          # title
# ---------------- THOMAS (intro, dry) ----------------
P += V("i1", .5) + V("i2", .6) + [("voice", "i3"), ("hit",), ("pause", SECTION + .4)]
# ---------------- ACT 1: THE MAN WHO DID EVERYTHING RIGHT ----------------
P += [("card", 1.5), ("level", "narration"), ("music", "pulse@3")] \
    + V("a1", .7) + V("a2", .7) + V("a3", .6) + V("a4", .6) + V("a5", .8) \
    + [("voice", "a6"), ("hit",), ("pause", .8)] + V("a7", .6) + [("voice", "a8")] + [FADE] + [("pause", .9)] \
    + V("a9", .6) + [("voice", "a10"), ("hit",), ("pause", SECTION)]
# ---------------- ACT 2: THE BOX (dry, the explainer) ----------------
P += [("hit",), ("card", 2.0)] + V("b1", .6) + V("b2", .6) + V("b3", .6) + [("voice", "b4"), ("pause", .3), ("card", 2.4)] \
    + V("b5", .7) + V("b6", .6) + V("b7", .8) + V("b8", .6) + [("voice", "b9"), ("pause", .3), ("card", 2.0)] \
    + V("b10", .6) + V("b11", .5) + V("b12", .7) + V("b13", .6) + V("b14", .7) + [("voice", "b15"), ("hit",), ("pause", .9)] \
    + V("b16", SECTION)
# ---------------- ACT 3: THE WARNING (memory_piano) ----------------
P += [("hit",), ("card", 2.0), ("track", "memory_piano"), ("level", "feature"), ("music", "full@3")] \
    + V("c1", .6) + V("c2", .6) + V("c3", .6) + V("c4", .6) + V("c5", .6) + [("voice", "c6")] + [FADE] + [("pause", .8)] \
    + V("c7", .8) + V("c8", .6) + V("c9", .8) + [("voice", "c10"), ("hit",), ("pause", SECTION)]
# ---------------- ACT 4: T-MINUS ----------------
P += [("hit",), ("card", 2.0), ("track", "heist"), ("level", "narration"), ("music", "drums@3")] \
    + V("d1", .6) + V("d2", .6) + V("d3", .6) + [("voice", "d4"), ("pause", .3), ("card", 1.6)] \
    + [("voice", "d5"), ("pause", .3), ("card", 2.4)] + V("d6", .6) + [("voice", "d7")] + [FADE] + [("pause", .6)] \
    + [("hit",), ("card", 2.6)] \
    + [("hit",), ("card", 2.6)] \
    + V("d8", .8) + [("voice", "d9"), ("pause", 1.0)] \
    + [("hit",), ("card", 2.2), ("track", "vault_run"), ("level", "key"), ("music", "full")] \
    + V("d10", .6) + V("d11", .7) + V("d12", .6) + V("d13", .7) + V("d13b", .6) + V("d13c", .6) \
    + [("voice", "d14"), ("music", "fade:4.0", -2.8), ("pause", 1.0)] \
    + [("voice", "d15"), ("hit",), ("pause", SECTION + .4)]
# ---------------- ACT 5: THE CHASE ----------------
P += [("card", 1.5)] + V("e1", .6) + [("voice", "e1b"), ("pause", .3), ("card", 1.8)] + [("voice", "e2"), ("pause", .3), ("card", 1.6)] + V("e3", .7) + V("e4", .8) \
    + V("e4b", .6) + V("e4c", .9) \
    + [("track", "heist"), ("level", "narration"), ("music", "pulse@3")] \
    + V("e5", .6) + V("e6", .6) + V("e7", .6) + [("voice", "e7b")] + [FADE] + [("pause", .8)] \
    + [("voice", "e8"), ("hit",), ("pause", SECTION)]
# ---------------- ACT 6: THE RETURN ----------------
P += [("hit",), ("card", 2.0), ("music", "drums@3")] \
    + V("f1", .6) + V("f2", .6) + V("f3", .6) + [("voice", "f4"), ("pause", .3), ("card", 1.6)] + [("voice", "f5")] + [FADE] \
    + [("pause", .8)] + [("voice", "f6"), ("hit",), ("pause", .9)] + V("f7", .7) + V("f8", SECTION)
# ---------------- IF YOU OWN ONE (dry, police advice) ----------------
P += [("card", 2.2)] + V("h1", .6) + V("h2", .7) + V("h3", .7) + V("h4", SECTION)
# ---------------- WHO? (dry) ----------------
P += [("card", 2.4)] + V("g1", .7) + V("g2", .7) + V("g3", .7) + V("g4", .8) + [("voice", "g5"), ("hit",), ("pause", SECTION)]
# ---------------- FINALE ----------------
P += [("card", 1.5), ("track", "heist"), ("level", "key"), ("music", "full@3")] \
    + V("k1", .7) + V("k2", .8) + V("k3", .6) + V("k4", 1.0) + V("k5", 1.0) + V("k6", 1.2) \
    + [("music", "fade"), ("pause", EM.END_FADE + 0.5)]

PLAN = P

if __name__ == "__main__":
    mix, total = EM.render(sys.argv[1], PLAN)
    wavfile.write(sys.argv[2], SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
    json.dump(EM.LAST_TIMELINE, open(os.path.splitext(sys.argv[2])[0] + ".timeline.json", "w"), indent=1)
    print("wrote", sys.argv[2], f"{total:.1f}s")
