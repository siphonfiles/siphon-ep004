"""Sound effects layer for ep. 001 (A4 in DaVinci Resolve), synthesized in code (100% original, no licences).
Usage: python3 sound/sfx_layer.py <timeline.json> <out.wav>
- whoosh on chapter cards that have no bass hit
- soft pop for each chat bubble, a reverse 'swallow' when the chats are deleted
- keyboard + a small blip when the hidden process starts (code editor)
- phone notification on the Radiant message
- quiet room tone under every Thomas shot
"""
import json, os, sys, types
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(7)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.modules.setdefault("cairo", types.ModuleType("cairo"))
sys.path.insert(0, os.path.join(ROOT, "graphics", "motion"))


def db(x):
    return 10 ** (x / 20)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def env(n, a, r):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / r)


def whoosh(dur=0.7, rev=False):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    # sweep a band-pass up (or down) through the noise, in short blocks
    B = 512
    for i in range(0, n, B):
        p = i / n
        f = 300 + 3200 * (p if not rev else 1 - p) ** 1.5
        seg = noise[max(0, i - 2048):i + B]
        out[i:i + B] = bp(seg, f * 0.7, min(f * 1.4, 20000))[-len(out[i:i + B]):]
    shape = np.sin(np.pi * np.clip(np.arange(n) / n, 0, 1)) ** 2
    return out * shape / (np.abs(out).max() + 1e-9)


def pop():
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 18) + 600
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.025)
    return s / np.abs(s).max()


def ping():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 1975.5 * t)) * env(n, 0.004, 0.18)
    s2 = np.zeros(n); k = int(0.12 * SR)
    s2[k:] = (np.sin(2 * np.pi * 1760 * t[:n - k]) + 0.4 * np.sin(2 * np.pi * 2637 * t[:n - k])) * env(n - k, 0.004, 0.25)
    s = s + s2
    return s / np.abs(s).max()


def key_click():
    n = int(0.035 * SR)
    s = bp(rng.standard_normal(n), 1500, 6000) * env(n, 0.001, 0.008)
    thump = np.sin(2 * np.pi * 180 * np.arange(n) / SR) * env(n, 0.001, 0.01) * 0.5
    s = s + thump
    return s / np.abs(s).max()


def blip():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * 523.25 * t) * env(n, 0.005, 0.07) + 0.6 * np.sin(2 * np.pi * 784 * t) * env(n, 0.005, 0.05)
    return s / np.abs(s).max()


def place(buf, x, t, gain_db):
    i = int(t * SR)
    if i < 0 or i >= len(buf):
        return
    j = min(len(buf), i + len(x))
    buf[i:j] += x[:j - i] * db(gain_db)


def main(tl_path, out):
    import ep001
    import scenes as S
    tl = json.load(open(tl_path))
    ev = tl["events"]
    v = {e["id"]: (e["t"], e["t"] + e["dur"]) for e in ev if e["kind"] == "voice"}
    hits = [e["t"] for e in ev if e["kind"] == "hit"]
    cards = [e["t"] for e in ev if e["kind"] == "card"]
    buf = np.zeros(int((tl["total"] + 2) * SR))
    T, _ = ep001.build(tl)
    # 1) whoosh into chapter cards without a bass hit (the hit already marks the others)
    for c in cards:
        if min(abs(c - h) for h in hits) > 0.5:
            place(buf, whoosh(0.7), c - 0.45, -27)
    # 2) chat bubbles / deleted chats / code editor, from the scenes' own timing
    for a, b, fn, p in T:
        if fn is S.chat:
            for at, _, _ in p.get("messages", []):
                place(buf, pop(), a + at + 0.05, -26)
        elif fn is S.chat_deleted:
            place(buf, whoosh(0.9, rev=True), a + (b - a) * 0.45, -28)
        elif fn is S.code_editor:
            d = b - a
            t0 = a + d * 0.10
            k = t0
            while k < a + d * 0.45:
                place(buf, key_click(), k, -34 + rng.uniform(-3, 2))
                k += rng.uniform(0.07, 0.16)
            place(buf, blip(), a + d * 0.55, -28)
        elif fn is S.illus and p.get("name") == "a6_radiant_message":
            place(buf, ping(), a + 0.6, -24)
    # 3) room tone under Thomas (very quiet: you feel it, you don't hear it)
    room = lp(np.cumsum(rng.standard_normal(len(buf))) * 0.02, 400)
    room = room - lp(room, 40)
    room /= np.sqrt(np.mean(room ** 2)) + 1e-12
    mask = np.zeros(len(buf))
    for a, b, *_ in ep001.thomas_plan(tl):
        i, j = int(a * SR), int(b * SR)
        mask[i:j] = 1
    mask = np.convolve(mask, np.ones(int(0.15 * SR)) / int(0.15 * SR), mode="same")
    buf += room * mask * db(-54)
    wavfile.write(out, SR, buf.astype(np.float32))
    print("sfx peak dBFS", round(20 * np.log10(np.abs(buf).max() + 1e-12), 1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
