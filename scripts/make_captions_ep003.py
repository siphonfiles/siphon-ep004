"""English captions (SRT) for ep. 003, from the exact voice timeline + the written script lines.

Text comes from sound/ep003/ep003_script_lines.json (written form: digits, names), timing from
graphics/motion/ep003_full.timeline.json (voice events: start + duration). Long lines are split at
sentence/clause breaks into cues of at most ~84 characters, timed in proportion to their length.
Usage: python3 scripts/make_captions_ep003.py  ->  episodes/publish/003-captions-en.srt
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TEXT = {d["id"]: d["text"] for d in json.load(open(os.path.join(ROOT, "sound/ep003/ep003_script_lines.json")))}
TL = json.load(open(os.path.join(ROOT, "graphics/motion/ep003_full.timeline.json")))
OUT = os.path.join(ROOT, "episodes/publish/003-captions-en.srt")
MAX = 84


def chunks(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    out = []
    for p in parts:
        while len(p) > MAX:
            cut = max(p.rfind(", ", 0, MAX), p.rfind(": ", 0, MAX), p.rfind("; ", 0, MAX))
            if cut < 20:
                cut = p.rfind(" ", 0, MAX)
            out.append(p[:cut + 1].strip())
            p = p[cut + 1:].strip()
        if p:
            out.append(p)
    # merge very short neighbours when they fit on one cue
    merged = []
    for c in out:
        if merged and len(merged[-1]) + 1 + len(c) <= MAX and (len(c) < 30 or len(merged[-1]) < 30):
            merged[-1] = merged[-1] + " " + c
        else:
            merged.append(c)
    return merged


def ts(t):
    t = max(0.0, t)
    h, r = divmod(int(round(t * 1000)), 3600000)
    m, r = divmod(r, 60000)
    s, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    voices = [e for e in TL["events"] if e["kind"] == "voice"]
    cues = []
    for e in voices:
        text = TEXT[e["id"]]
        cs = chunks(text)
        total = sum(len(c) for c in cs)
        t = e["t"]
        for c in cs:
            d = e["dur"] * len(c) / total
            cues.append((t, t + d, c))
            t += d
    # no overlaps, small gap
    fixed = []
    for i, (a, b, c) in enumerate(cues):
        if i + 1 < len(cues):
            b = min(b, cues[i + 1][0] - 0.04)
        fixed.append((a, max(b, a + 0.6), c))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        for i, (a, b, c) in enumerate(fixed, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{c}\n\n")
    print(len(fixed), "cues ->", OUT)


if __name__ == "__main__":
    main()
