"""Ep. 003 (Coldcard) sound plan: same engine and same pattern as ep. 001 and ep. 002 (sound/episode_mix.py).

Pattern (approved by proprietarul for ep. 001/002, reused as asked on 23 Nov 2026):
  - teaser: heist piece in full, ~13 dB under the voice, a bass hit on every cut, black + sub drop + title
  - narration: music only in places (pulse/drums), every stop a smooth fade that ends before the key line
  - Thomas on camera: dry (no music under him), except the sign-off
  - T-minus cards: bass hit + card
  - the sweep (01:10): 'vault_run' at the 'key' level, faded before "Then it reaches Goodman"
  - the discovery ("I'll just check"): 'memory_piano' under the narration
  - the close: the heist piece returns and fades on the end card

Usage: python3 sound/ep003/ep003_mix.py <voice_dir> <out.wav>   (writes <out>.timeline.json too)
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
M = lambda *s: list(s)
SECTION = 1.2
FADE = ("music", "fade:4.0", -2.8)    # starts 2.8 s before the end of the previous line, ends before the next

P = []
# ---------------- TEASER ----------------
P += [("level", "teaser"), ("music", "full"), ("pause", 1.2)]
P += [("voice", "t1"), ("hit",), ("pause", 0.9), ("card", 2.2)]          # the vault
P += [("voice", "t2"), ("hit",), ("pause", 0.9)]
P += [("voice", "t3"), ("hit",), ("pause", 0.9), ("card", 2.0)]
P += [("voice", "t4"), ("hit",), ("pause", 0.9)]
P += [("voice", "t5"), ("hit",), ("pause", 0.9)]
P += [("voice", "t6"), ("pause", 0.25), ("hit",), ("music", "fade")]
P += [("pause", 1.4), ("drop",), ("card", 4.0)]                          # title
# ---------------- THOMAS (intro, dry) ----------------
P += V("i1", .5) + V("i2", .6) + V("i3", .5) + [("voice", "i4"), ("hit",), ("pause", SECTION + .4)]
# ---------------- THE MAN WHO DID EVERYTHING RIGHT ----------------
P += [("card", 1.5), ("level", "narration"), ("music", "pulse@3")] + V("a1", .7) + V("a2", .6) + V("a3", .8) \
    + [("voice", "a4")] + M(FADE) + [("pause", .9)] + [("voice", "a5"), ("hit",), ("pause", SECTION)]
# ---------------- THE COMBINATION ----------------
P += [("card", 1.5)] + M(("music", "pulse@3")) + V("b1", .6) + V("b2", .6) + [("hit",), ("card", 2.0)] \
    + V("b3", .5) + [("card", 3.0)] + V("b4", .7) + V("b5", .7) \
    + [("voice", "b6")] + M(FADE) + [("pause", .3), ("card", 2.4)] + [("voice", "b7"), ("hit",), ("pause", 1.0)] \
    + V("b8", .5) + V("b9", .5) + V("b10", SECTION)
# ---------------- FIVE YEARS ----------------
P += [("card", 1.5)] + M(("music", "pulse@3")) + V("c1", .6) + [("voice", "c2")] + M(FADE) + [("pause", .8)] \
    + V("c3", .5) + V("c4", .8) \
    + M(("music", "pulse@3")) + V("c5", .6) + [("voice", "c6"), ("pause", .3), ("card", 2.6)] + V("c7", .6) \
    + [("voice", "c8")] + M(FADE) + [("pause", .7)] + V("c9", .6) + [("hit",), ("card", 2.0)] \
    + V("c10", .4) + [("card", 2.4)] + [("voice", "c11"), ("hit",), ("pause", .8)] \
    + V("c12", .5) + V("c13", .6) + V("c14", .5) + V("c15", .6) + V("c16", SECTION)
# ---------------- 01:10 (the sweep, vault_run) ----------------
P += [("hit",), ("card", 2.2), ("track", "vault_run"), ("level", "key"), ("music", "full")]
P += V("d1", .6) + V("d2", .6) + V("d3", .6) + V("d4", .6) \
    + [("voice", "d5"), ("music", "fade:2.9", -1.7), ("pause", 1.0)] \
    + V("d6", .6) + [("voice", "d7"), ("hit",), ("pause", .9)] + V("d8", .8) + [("voice", "d9"), ("hit",), ("pause", SECTION + .4)]
# ---------------- "I'LL JUST CHECK" (memory_piano) ----------------
P += [("card", 1.5)] + M(("track", "memory_piano"), ("level", "narration"), ("music", "full@3")) + V("e1", .6) + V("e2", .7) \
    + [("voice", "e3"), ("pause", .3), ("card", 2.6)] + [("voice", "e4"), ("pause", .3), ("card", 2.4)] \
    + V("e5", .6) + V("e6", .7) + [("voice", "e7")] + M(FADE) + [("pause", .3), ("card", 2.6)] \
    + V("e8", .5) + [("voice", "e9"), ("hit",), ("pause", SECTION)]
# ---------------- THE RACE ----------------
P += [("card", 1.5)] + M(("track", "heist"), ("level", "narration"), ("music", "drums@3")) \
    + V("f1", .6) + V("f2", .6) + V("f3", .6) + V("f4", .7) + V("f5", .6) + V("f6", .6) \
    + [("voice", "f7")] + M(FADE) + [("pause", .8)] + [("voice", "f8"), ("hit",), ("pause", SECTION)]
# ---------------- THE MISTAKE ----------------
P += V("g1", .5) + V("g2", .5) + V("g3", .5) + V("g4", .7) \
    + M(("music", "pulse@3")) + V("g5", .6) + V("g6", .6) + [("voice", "g7")] + M(FADE) + [("pause", .6)] \
    + V("g8", .5) + V("g9", .8) + V("g10", .6) + [("voice", "g11"), ("hit",), ("pause", SECTION)]
# ---------------- WHO? ----------------
P += [("card", 2.4)] + V("h1", .7) + V("h2", .7) + V("h3", .7) + [("voice", "h4"), ("pause", .3), ("card", 2.4)] \
    + V("h5", SECTION)
# ---------------- THE BOX, AGAIN ----------------
P += [("card", 1.5)] + V("k1", .5) + V("k2", .9) \
    + V("k3", .5) + V("k4", .5) + V("k5", .6) + V("k6", .5) + V("k7", .8) \
    + [("track", "heist"), ("level", "key"), ("music", "full@2"), ("pause", .3)] \
    + V("k8", .8) + V("k9", 1.2) + V("k10", 1.2) + [("music", "fade"), ("pause", EM.END_FADE + 0.5)]

PLAN = P

if __name__ == "__main__":
    mix, total = EM.render(sys.argv[1], PLAN)
    wavfile.write(sys.argv[2], SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
    json.dump(EM.LAST_TIMELINE, open(os.path.splitext(sys.argv[2])[0] + ".timeline.json", "w"), indent=1)
    print("wrote", sys.argv[2], f"{total:.1f}s")
