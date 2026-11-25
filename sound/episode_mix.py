"""Episode sound mixer: Thomas's voice + the heist underscore (layered) + bass hits.

Implements the music plan proprietarul approved (20 nov 2026), revised the same evening:
music only in the teaser and at key moments, NOT as a constant background. The script carries
[MUSIC: ...] tags; each state turns layers of the same tempo-locked piece on/off:

  full   = clock + bass + drums + arpeggio   (teaser, the heist itself, close)
  drums  = clock + bass + drums              (tension rising)
  pulse  = clock + bass                      (story in motion)
  clock  = clock only                        (Thomas on camera)
  out    = silence                           (before key lines, sombre parts)
  fade   = whatever plays fades out over 5 s

The piece keeps running underneath even when muted, so it always comes back in time.

Usage: python3 sound/episode_mix.py <voice_dir> <out.wav> [demo|full]
The demo plan below covers ep. 001 from the teaser to the end of Act 1.
"""
import os
import sys
import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(__file__))
from sting_design import SR, place, note_hz, sub_boom, sub_drop  # noqa: E402
import heist_design  # noqa: E402
from teaser_mix import load_voice  # noqa: E402

STATES = {
    "full": {"hats": 1, "bass": 1, "drums": 1, "arp": 1},
    "drums": {"hats": 1, "bass": 1, "drums": 1, "arp": 0},
    "pulse": {"hats": 1, "bass": 1, "drums": 0, "arp": 0},
    "clock": {"hats": 1, "bass": 0, "drums": 0, "arp": 0},
    "out": {"hats": 0, "bass": 0, "drums": 0, "arp": 0},
}
LAYERS = ("hats", "bass", "drums", "arp")
MUSIC_DB = {"teaser": -13, "narration": -12, "key": -10, "feature": -10}   # music level under the voice
# 22 nov 2026 (Proprietarul: "I didn't hear the new music"): narration -18 -> -12, key -15 -> -10, memory_piano -10
RAMP = 0.35        # seconds for a layer to come in / go out
END_FADE = 5.0     # proprietarul: slow fade, never an abrupt stop

# proprietarul (21 nov 2026, late): "more music" -> 6 extra spots under the narration (never under
# Thomas on camera; every stop is a smooth ~2.9 s fade that ends before the key line).
# MORE_MUSIC=0 reproduces the previous mix exactly.
def MORE_MUSIC(*steps):
    return steps if os.environ.get("MORE_MUSIC", "1") == "1" else ()


# pause between two lines of the same re-synced Thomas shot (a7|a8, b3|b4, b7|b8, g7|g8): the shot jumps
# straight to the next line on the camera cut, so he never seems to mouth words in a silence
TIGHT = 0.12

# ep. 001 demo plan (v2, proprietarul 20 nov 2026): music ONLY in the teaser and at key
# moments; the narration runs dry, with bass hits on cards and reveals.
PLAN = [
    ("level", "teaser"), ("music", "full"),
    ("pause", 1.2),
    ("voice", "t1"), ("hit",), ("pause", 0.9), ("card", 3.0),
    ("voice", "t2"), ("hit",), ("pause", 0.9), ("card", 3.0),
    ("voice", "t3"), ("pause", 0.25), ("hit",), ("music", "fade"),
    ("pause", 1.4), ("drop",), ("card", 4.0),          # black + ringing bass ~1.4 s, then the title on the sub drop
    ("voice", "i1"), ("pause", 0.5), ("voice", "i2"), ("pause", 0.9),
    ("hit",), ("card", 2.0),                           # T-MINUS 6 MONTHS
    *MORE_MUSIC(("level", "narration"), ("music", "pulse@3")),
    ("voice", "a1"), ("pause", 0.5), ("voice", "a2"), ("pause", 0.5),
    ("voice", "a3"), ("pause", 0.7), ("voice", "a4"), ("pause", 0.5),
    ("voice", "a5"), ("pause", 0.9),
    ("hit",), ("card", 2.0),                           # T-MINUS 3 MONTHS
    ("voice", "a6"), *MORE_MUSIC(("music", "fade:4.0", -2.8)),
    ("hit",), ("card", 1.6),                           # big number $1,000,000+
    ("voice", "a7"), ("pause", TIGHT),   # proprietarul 22 nov: no silent mouthing between the two on-camera lines
    ("voice", "a8"), ("hit",), ("pause", 2.0),
]

# 22 nov 2026: b2 and k9 re-voiced (ASR: "Drift Zone", "wallet's link"); the pause after each grows by
# exactly what the new take is shorter, so every later event stays where it was (no re-render).
# Whole ep. 001 (same rules): music only in the teaser, the Act 5 drain and the close.
V = lambda i, p=0.5: [("voice", i), ("pause", p)]
M = lambda *steps: list(MORE_MUSIC(*steps))
SECTION = 1.2   # breath between sections
PLAN_FULL = PLAN[:-1] + [("pause", SECTION)]          # teaser .. end of Act 1
# Act 2: THE FACES
PLAN_FULL += [("card", 1.5)] + V("b1", .6) + V("b2", .6 + 0.121088) + V("b3", TIGHT) + V("b4") + V("b5", .6) + V("b5b", .9) + V("b6", .8) \
    + V("b7", TIGHT) + V("b8", 1.0) + M(("level", "narration"), ("music", "pulse@3")) + V("b9") + V("b10") \
    + M(("music", "drums@2")) + V("b11", 1.2) + [("voice", "b12")] + M(("music", "fade:4.0", -2.8)) + [("pause", .7)] \
    + [("voice", "b13"), ("hit",), ("pause", SECTION + .6)]
# Act 3: THE CHEQUE WITH NO DATE
PLAN_FULL += [("hit",), ("card", 2.0)] + M(("music", "pulse@3")) + V("c1", .6) + V("c2", .7) + V("c3", .6) + V("c4", 1.0) \
    + V("c5", 1.0) + V("c6", .6) + V("c7", .8) + V("c8", .6) + V("c9", .7) + V("c10", .6) + [("voice", "c11")] + M(("music", "fade:4.0", -2.8)) + [("pause", .8)] \
    + [("voice", "c12"), ("hit",), ("pause", SECTION + .6)]
# Bridge: Thomas on camera, dry
PLAN_FULL += V("d1", .7) + V("d2", .7) + V("d3", SECTION)
# Act 4: THE FAKE DOLLAR
PLAN_FULL += [("hit",), ("card", 2.0)] + M(("music", "drums@3")) + V("e1", .7) + V("e2", .6) + V("e3", 1.0) \
    + [("voice", "e4")] + M(("music", "fade:4.0", -2.8)) + [("pause", .8)] \
    + V("e5", .9) + V("e6", .8) + [("voice", "e7"), ("hit",), ("pause", SECTION + .6)]
# Act 5: APRIL FIRST, the key moment: music in for the drain, out for the key line
ACT5_TRACK = os.environ.get("ACT5_TRACK", "vault_run")   # proprietarul: a different heist piece at ~5:40
PLAN_FULL += [("track", ACT5_TRACK), ("level", "key"), ("music", "full"), ("hit",), ("card", 2.5)] \
    + V("f1", .6) + V("f2", .7) + V("f3", .6) \
    + [("voice", "f4"), ("music", "fade:2.9", -1.7), ("pause", 1.3)] \
    + [("voice", "f5"), ("hit",), ("card", 2.0)] \
    + V("f6", .6) + V("f7", .8) + V("f8", .7) + V("f9", .6) + V("f10", .8) + V("f11", .5) \
    + V("f12", SECTION + .4)
# Act 6: WHO
PLAN_FULL += [("card", 1.5)] + V("g1", .7) + V("g2", .7) + V("g3", 1.0) + [("card", 1.5)] \
    + M(("track", "memory_piano"), ("level", "feature"), ("music", "full@3")) + V("g4", .6) + V("g5", .5) \
    + [("voice", "g6")] + M(("music", "fade:4.0", -2.8)) + [("pause", 1.0)] + V("g7", TIGHT) + [("voice", "g8"), ("hit",), ("pause", 1.0)] \
    + V("g9", .8) + V("g10", .6) + [("card", 1.5), ("pause", SECTION)]
# Act 7: AFTER
PLAN_FULL += [("card", 1.5)] + V("h1", .6) + V("h2", .6) + V("h3", 1.0) + [("card", 1.0)] \
    + V("h4", .6) + V("h5", .6) + V("h6", .9) + V("h7", 1.2) \
    + [("hit",), ("card", 1.2), ("voice", "h8"), ("pause", 2.0)] \
    + V("h9", 1.0) + [("card", 1.0)] + M(("track", "heist"), ("level", "narration"), ("music", "pulse@3")) \
    + V("h10", .5) + V("h11", .6) + [("voice", "h12")] + M(("music", "fade:4.0", -2.8)) + [("pause", SECTION)]
# Close: Binance, then Thomas; music returns for the last ~20 s and fades on the end card
PLAN_FULL += [("card", 1.5)] + V("k1", .6) + V("k2", .8) + V("k3", .6) + V("k4", .6) + V("k5", .8) \
    + [("voice", "k6"), ("hit",), ("pause", SECTION + .4)] \
    + V("k7", .8) + V("k8", .9) \
    + [("track", "heist"), ("level", "key"), ("music", "full"), ("pause", 1.0)] + V("k9", .6 + 0.125692) + V("k10", .9) \
    + V("k11", 1.2) + [("music", "fade"), ("pause", END_FADE + 0.5)]


def render(voice_dir, plan=PLAN):
    voices, t, events = {}, 0.0, []
    for step in plan:
        kind = step[0]
        if kind == "voice":
            v = voices.setdefault(step[1], load_voice(os.path.join(voice_dir, step[1] + ".wav")))
            events.append(("voice", t, v))
            t += len(v) / SR
        elif kind in ("pause", "card"):
            if kind == "card":
                events.append(("card", t, None))
            t += step[1]
        else:   # optional 3rd item = offset in seconds (e.g. start a fade before a line ends)
            off = step[2] if len(step) > 2 else 0.0
            events.append((kind, t + off, step[1] if len(step) > 1 else None))
    total = t + 0.5
    n = int(total * SR)
    global LAST_TIMELINE
    LAST_TIMELINE = {"total": round(total, 3), "events": [
        {"kind": k, "t": round(at, 3), **({"id": next(i for i, w in voices.items() if w is v),
                                         "dur": round(len(v) / SR, 3)} if k == "voice" else
                                        ({"value": v} if isinstance(v, str) else {}))}
        for k, at, v in events]}

    # layer gains over time
    gains = {k: np.zeros(n) for k in LAYERS}
    level = np.zeros(n)
    cur = dict(STATES["out"])
    cur_lvl = MUSIC_DB["teaser"]
    marks = sorted([e for e in events if e[0] in ("music", "level")], key=lambda e: e[1])
    tt = np.arange(n) / SR
    for k in LAYERS:
        gains[k][:] = 0
    timeline = [(0.0, dict(cur), cur_lvl, "set")]
    for kind, at, val in marks:
        if kind == "level":
            cur_lvl = MUSIC_DB[val]
            timeline.append((at, dict(cur), cur_lvl, "set"))
        elif val.startswith("fade"):
            fd = float(val.split(":")[1]) if ":" in val else END_FADE   # "fade:2.5" = custom length
            timeline.append((at, dict(cur), cur_lvl, "fade", fd))
            cur = dict(STATES["out"])
            timeline.append((at + fd, dict(cur), cur_lvl, "set"))
        else:
            name, _, rmp = val.partition("@")          # "pulse@3" = come in over 3 s (Proprietarul: slow in)
            cur = dict(STATES[name])
            timeline.append((at, dict(cur), cur_lvl, "set", float(rmp) if rmp else RAMP))
    timeline.sort(key=lambda e: e[0])
    prev = {k: 0.0 for k in LAYERS}
    for idx, entry in enumerate(timeline):
        at, st, lvl, mode = entry[:4]
        fd = entry[4] if len(entry) > 4 and mode == "fade" else END_FADE
        rp = entry[4] if len(entry) > 4 and mode == "set" else RAMP
        end = timeline[idx + 1][0] if idx + 1 < len(timeline) else total
        i0, i1 = int(at * SR), int(end * SR)
        seg = tt[i0:i1] - at
        level[i0:i1] = 10 ** (lvl / 20)
        for k in LAYERS:
            if mode == "fade":
                g = prev[k] * 0.5 * (1 + np.cos(np.pi * np.clip(seg / fd, 0, 1)))
                gains[k][i0:i1] = g
                prev[k] = 0.0
            else:
                r = np.clip(seg / rp, 0, 1)
                r = 0.5 * (1 - np.cos(np.pi * r)) if rp > RAMP else r   # smooth S-curve for slow entries
                gains[k][i0:i1] = prev[k] + (st[k] - prev[k]) * r
                prev[k] = st[k]

    stems = heist_design.build_stems(bars=int(total / heist_design.BAR) + 2, full_from_start=True)
    peak = max(np.max(np.abs(sum(stems.values()))), 1e-9)
    # ("track", name) switches the bed: "heist" = the layered opening piece; any name from
    # heist_tracks.TRACKS = an alternative piece that starts from its first bar at that moment.
    # The layer gains still drive it (their max), so "out"/"fade" work the same on any track.
    use_heist = np.ones(n)
    alt = np.zeros(n)
    tr_events = sorted([(at, v) for k, at, v in events if k == "track"])
    for idx, (at, name) in enumerate(tr_events):
        end = tr_events[idx + 1][0] if idx + 1 < len(tr_events) else total
        i0, i1 = int(at * SR), int(end * SR)
        if name == "heist":
            continue
        import heist_tracks
        tr = heist_tracks.TRACKS[name](seconds=max(end - at, 6.0) + 6.0)
        seg = tr[: i1 - i0]
        alt[i0:i0 + len(seg)] = seg * 0.85
        use_heist[i0:i1] = 0
    g_all = np.maximum.reduce([gains[k] for k in LAYERS])
    music = (sum(stems[k][:n] * gains[k] for k in LAYERS) / peak * use_heist + alt * g_all) * level

    voice, hits = np.zeros(n), np.zeros(n)
    for kind, at, v in events:
        if kind == "voice":
            place(voice, 0.9 * v, at)
        elif kind == "hit":
            place(hits, 0.5 * sub_boom(note_hz("D1"), dur=1.8, hold=0.9), at)
        elif kind == "drop":
            place(hits, 0.6 * sub_drop(), at)
    mix = voice + music + hits
    k = 10 ** (-1 / 20) / np.max(np.abs(mix))
    global LAST_STEMS   # the same three layers, scaled exactly like the mix (for the DaVinci Resolve package)
    LAST_STEMS = {"voice": voice * k, "music": music * k, "bass": hits * k}
    return mix * k, total


if __name__ == "__main__":
    which = sys.argv[3] if len(sys.argv) > 3 else "demo"
    mix, total = render(sys.argv[1], PLAN_FULL if which == "full" else PLAN)
    wavfile.write(sys.argv[2], SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
    import json
    json.dump(LAST_TIMELINE, open(os.path.splitext(sys.argv[2])[0] + ".timeline.json", "w"), indent=1)
    print("wrote", sys.argv[2], f"{total:.1f}s")
    if os.environ.get("STEMS_DIR"):
        d = os.environ["STEMS_DIR"]
        os.makedirs(d, exist_ok=True)
        for name, x in LAST_STEMS.items():
            wavfile.write(os.path.join(d, f"{name}.wav"), SR, x.astype(np.float32))
        print("stems in", d)
