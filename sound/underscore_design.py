"""Siphon Files: cold-open underscore, draft v1 (synthesized, 100% original).

Style target (Proprietarul, 20 nov 2026): the *style* of the DOAC cold-open music, not a copy.
What we measured in a 1:41 reference recording (analysis only):
  - a dark, sustained ambient pad under the speech, almost no rhythm;
  - tonal centre D minor with A held on top; around the middle it moves to
    C / Bb, then returns to D minor (a chord change every ~15-30 s);
  - deep sub "booms" around 32-34 Hz on the cuts, about one every 6-8 s;
  - an opening sub drop from about 86 to 30 Hz.
Our version: own progression and voicing (Dm -> Bb -> Csus -> Dm), own sparse
piano motif, felt pulse, booms on our own cut points.

Run:  python3 sound/underscore_design.py
"""
import os
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve

sys.path.insert(0, os.path.dirname(__file__))
from sting_design import (SR, OUT, t_axis, lowpass, highpass, place, note_hz,  # noqa: E402
                          pluck, thump, sub_boom, sub_drop, env_exp)

DUR = 62.0
rng = np.random.default_rng(11)


def saw(f, n, det):
    ph = 2 * np.pi * np.cumsum(np.full(n, f * (1 + det))) / SR + rng.uniform(0, 6.28)
    return 2 * ((ph / (2 * np.pi)) % 1) - 1


def pad_chord(notes, dur, cutoff=700):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for nm in notes:
        f = note_hz(nm)
        for det in (-0.004, 0.0, 0.005):
            sig += saw(f, n, det)
    sig /= 3 * len(notes)
    # slow breathing filter
    lfo = 0.5 * (1 + np.sin(2 * np.pi * 0.07 * t))
    lo = lowpass(sig, cutoff * 0.6)
    hi = lowpass(sig, cutoff * 1.4)
    sig = lo * (1 - lfo) + hi * lfo
    fade = np.minimum(1, t / 3.0) * np.minimum(1, (dur - t) / 3.0)  # 3 s crossfades
    return sig * fade


def shimmer(dur):
    """Very quiet high air: filtered noise + faint high D/A partials."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    air = highpass(lowpass(rng.normal(0, 1, n), 9000), 3000) * 0.02
    tones = sum(np.sin(2 * np.pi * note_hz(nm) * t) for nm in ("A6", "D7")) * 0.004
    return (air + tones) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t))


def reverb_st(x, seconds=4.5, mix=0.45):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    outs = []
    for seed in (21, 22):
        ir = np.random.default_rng(seed).normal(0, 1, n) * np.exp(-t / (seconds / 6.0))
        ir = lowpass(ir, 5000)
        ir /= np.sqrt(np.sum(ir ** 2))
        outs.append((1 - mix) * x + mix * fftconvolve(x, ir)[: len(x)])
    return np.stack(outs, axis=1)


def build(with_low=True):
    n = int(DUR * SR)
    pads = np.zeros(n)
    sections = [  # (start, length, voicing)
        (0.0, 17.0, ["D2", "A2", "D3", "F3", "A3"]),
        (14.0, 17.0, ["Bb1", "F2", "Bb2", "D3", "F3"]),
        (28.0, 17.0, ["C2", "G2", "C3", "D3", "G3"]),     # Csus2: unresolved
        (42.0, 20.0, ["D2", "A2", "D3", "F3", "A3"]),
    ]
    for start, length, notes in sections:
        place(pads, 0.55 * pad_chord(notes, length), start)

    keys = np.zeros(n)  # sparse, high, lonely piano: one note every few seconds
    motif = [(2.0, "A4"), (6.5, "F4"), (11.0, "D4"),
             (16.5, "F4"), (21.0, "D4"), (25.5, "Bb3"),
             (30.5, "G4"), (35.0, "D4"), (39.5, "C4"),
             (44.5, "A4"), (49.0, "F4"), (53.5, "E4"), (57.5, "D4")]
    for start, nm in motif:
        place(keys, 0.28 * lowpass(pluck(note_hz(nm), 4.0, damp=0.998), 2500), start)

    pulse = np.zeros(n)  # felt heartbeat in the last section: tension before the title
    for k, start in enumerate(np.arange(44.0, 60.0, 1.0)):
        place(pulse, (0.12 + 0.18 * k / 16) * thump(50, 0.35), start)

    music = pads + keys + pulse + shimmer(DUR)
    wet = reverb_st(music)

    low = np.zeros(n)  # sub accents on cuts (kept dry: they would smear in the reverb)
    place(low, 0.6 * sub_drop(), 0.3)
    for start in (8.0, 14.5, 21.5, 28.0, 35.5, 42.0, 49.0, 55.5):
        place(low, 0.42 * sub_boom(note_hz("D1")), start)
    mix = wet + low[:, None] if with_low else wet

    t = np.arange(n) / SR
    mix *= np.minimum(1, (DUR - t) / 2.5)[:, None]
    mix /= np.max(np.abs(mix))
    return mix * 10 ** (-1 / 20)


def save(x, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    wavfile.write(path, SR, (x * 32767).astype(np.int16))
    print("wrote", path)


if __name__ == "__main__":
    bed = build()
    save(bed, "underscore_cold_open_v1.wav")

    # mix under Thomas's reference voice, the way it would sit in an episode
    vp = os.path.join(os.path.dirname(__file__), "..", "presenter", "voice_ref_v1.wav")
    sr_v, v = wavfile.read(vp)
    v = v.astype(float) / 32768
    if v.ndim > 1:
        v = v.mean(1)
    v /= np.max(np.abs(v))
    demo = bed[: int(24 * SR)].copy() * 10 ** (-17 / 20)   # music ~17 dB under the voice peak
    place_at = int(3.0 * SR)
    demo[place_at:place_at + len(v)] += 0.85 * v[: len(demo) - place_at, None]
    demo *= np.minimum(1, (24 - np.arange(len(demo)) / SR) / 2.0)[:, None]
    demo /= np.max(np.abs(demo))
    save(demo * 10 ** (-1 / 20), "demo_underscore_with_thomas.wav")
