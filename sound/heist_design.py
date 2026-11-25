"""Siphon Files: "heist" underscore v1 (synthesized, 100% original).

Proprietarul (20 nov 2026): the ambient bed sounded like a funeral; he wants
something rhythmic, like the music in a bank-robbery film.
Recipe (genre conventions, not any specific track): 112 BPM, D minor,
driving 8th-note bass ostinato, 16th-note muted synth arpeggio, ticking
16th hi-hats (the "clock"), finger-snap backbeat, soft kick, chord loop
Dm | Bb | Gm | A (the A major chord keeps it tense and pulling back to Dm).
Intro builds: hats -> + bass -> + kick/snaps -> + arpeggio.

Run:  python3 sound/heist_design.py  ->  sound/stings/underscore_heist_v1.wav
"""
import os
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve

sys.path.insert(0, os.path.dirname(__file__))
from sting_design import SR, OUT, t_axis, lowpass, highpass, place, note_hz  # noqa: E402

BPM = 112
S16 = 60 / BPM / 4            # one 16th note in seconds
BAR = 16 * S16
rng = np.random.default_rng(5)

CHORDS = [("D", [0, 3, 7]), ("Bb", [0, 4, 7]), ("G", [0, 3, 7]), ("A", [0, 4, 7])]  # 2 bars each
ROOT_MIDI = {"D": 38, "Bb": 34, "G": 31, "A": 33}   # bass octave (D2, Bb1, G1, A1)


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(dur, decay, attack=0.002):
    t = t_axis(dur)
    return np.clip(t / attack, 0, 1) * np.exp(-t / decay)


def bass(m, dur=S16 * 2 * 0.9):
    t = t_axis(dur)
    f = midi_hz(m)
    ph = 2 * np.pi * f * t
    saw = 2 * ((f * t) % 1) - 1
    sig = lowpass(0.6 * saw, 700) + 0.7 * np.sin(ph)
    return sig * env(dur, 0.16, 0.003)


def pluck_arp(m, dur=S16 * 1.6):
    t = t_axis(dur)
    f = midi_hz(m)
    sq = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + 0.5 * np.sin(2 * np.pi * f * t)
    return lowpass(sq, 2600) * env(dur, 0.07, 0.001)


def kick(dur=0.32):
    t = t_axis(dur)
    f = 45 + 75 * np.exp(-t / 0.035)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(dur, 0.14, 0.001)


def hat(dur=0.05, accent=1.0):
    n = rng.normal(0, 1, int(dur * SR))
    return highpass(n, 7000, order=4) * env(dur, 0.012 * accent, 0.0005) * accent


def snap(dur=0.18):
    n = rng.normal(0, 1, int(dur * SR))
    body = highpass(lowpass(n, 4500), 1200)
    return body * env(dur, 0.045, 0.0008)


def low_pad(m_list, dur):
    t = t_axis(dur)
    sig = sum(np.sin(2 * np.pi * midi_hz(m) * t) + 0.3 * np.sin(4 * np.pi * midi_hz(m) * t) for m in m_list)
    fade = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
    return lowpass(sig / len(m_list), 1200) * fade


def room(x, seconds=1.2, mix=0.22, seed=3):
    n = int(seconds * SR)
    tt = np.arange(n) / SR
    ir = np.random.default_rng(seed).normal(0, 1, n) * np.exp(-tt / (seconds / 6.5))
    ir = lowpass(ir, 6000)
    ir /= np.sqrt(np.sum(ir ** 2))
    return (1 - mix) * x + mix * fftconvolve(x, ir)[: len(x)]


BASS_PATTERN = [0, 0, 12, 0, 0, 0, 7, 10]                  # 8ths, semitones over the root
ARP_PATTERN = [0, 1, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 1, 2, 3]  # index into chord tones (+octave)
HAT_ACCENT = [0.5, 0.35, 1.0, 0.35] * 4


def build_stems(bars=20, full_from_start=False):
    """Separate, tempo-locked layers: hats ("clock"), bass, drums, arp (+ its pad).
    With full_from_start every layer plays from bar 0 (the episode mixer turns them
    on and off); otherwise the intro builds hats -> bass -> drums -> arpeggio."""
    n = int(bars * BAR * SR) + SR
    hats, bass_tr, drums, arp_tr, pad_tr = (np.zeros(n) for _ in range(5))
    start = {"bass": 0, "drums": 0, "arp": 0} if full_from_start else {"bass": 2, "drums": 4, "arp": 6}
    for b in range(bars):
        name, ivs = CHORDS[(b // 2) % 4]
        root = ROOT_MIDI[name]
        t0 = b * BAR
        for i in range(16):  # the ticking clock
            place(hats, 0.22 * hat(accent=HAT_ACCENT[i]), t0 + i * S16)
        if b >= start["bass"]:
            for i, off in enumerate(BASS_PATTERN):
                place(bass_tr, 0.55 * bass(root + off), t0 + i * 2 * S16)
        if b >= start["drums"]:
            for i in (0, 8) + ((14,) if b % 2 else ()):
                place(drums, 0.8 * kick(), t0 + i * S16)
            for i in (4, 12):
                place(drums, 0.35 * snap(), t0 + i * S16)
        if b >= start["arp"]:
            tones = [root + 24 + iv for iv in ivs] + [root + 36]
            for i, k in enumerate(ARP_PATTERN):
                place(arp_tr, 0.16 * pluck_arp(tones[k]), t0 + i * S16)
            if b % 2 == 0:
                place(pad_tr, 0.12 * low_pad([root + 12 + iv for iv in ivs], 2 * BAR), t0)
    L = int(bars * BAR * SR)
    return {"hats": hats[:L], "bass": bass_tr[:L], "drums": drums[:L],
            "arp": (room(arp_tr, mix=0.3) + room(pad_tr, mix=0.35))[:L]}


def build(bars=20):
    music = sum(build_stems(bars).values())
    f = int(5.0 * SR)  # proprietarul: slow 5 s fade-out instead of an abrupt end
    music[-f:] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, f)))
    music /= np.max(np.abs(music))
    return music * 10 ** (-1 / 20)


if __name__ == "__main__":
    x = build()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "underscore_heist_v1.wav")
    wavfile.write(path, SR, (np.stack([x, x], 1) * 32767).astype(np.int16))
    print("wrote", path, f"{len(x) / SR:.1f}s")
