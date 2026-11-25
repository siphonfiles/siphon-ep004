"""Alternative "bank heist" tracks for the key moment of an episode (ep. 001: Act 5, ~5:40).

Proprietarul (21 nov 2026): at 5:40 he wants a different piece than the opening heist bed,
still in the bank-robbery-film register. Three original candidates, synthesized in code:

  vault_run   124 BPM, E minor. Driving 16th-note bass, staccato string-like stabs, toms.
              The "they're inside, the clock is running" feel.
  spy_wire    118 BPM, A minor. Twangy tremolo lead over a walking bass, brushed snare,
              finger snaps: cool, sly, the caper.
  clockwork   96 BPM half-time, D minor. Big slow drums, pulsing low synth 8ths, a rising
              string ostinato and a ticking clock: heavy, inevitable.

Each track is built as one continuous piece; it starts at the first bar so it can be dropped
on a cut, and ends with a 5 s fade (house rule: never stop abruptly).

Run:  python3 sound/heist_tracks.py  ->  sound/stings/track_<name>.wav (30 s each)
"""
import os
import sys
import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(__file__))
from sting_design import SR, OUT, t_axis, lowpass, highpass, place  # noqa: E402
from heist_design import midi_hz, env, kick, hat, snap, room  # noqa: E402

rng = np.random.default_rng(21)


def saw(f, dur, det=(-0.006, 0.0, 0.007)):
    t = t_axis(dur)
    return sum(2 * ((f * (1 + d) * t) % 1) - 1 for d in det) / len(det)


def bass_note(m, dur, cutoff=650, decay=0.18):
    t = t_axis(dur)
    f = midi_hz(m)
    return (lowpass(0.6 * saw(f, dur, (0.0,)), cutoff) + 0.7 * np.sin(2 * np.pi * f * t)) * env(dur, decay, 0.003)


def stab(ms, dur, cutoff=2400):
    """Staccato string-section-like stab (detuned saws, bright then closing)."""
    s = sum(saw(midi_hz(m), dur) for m in ms) / len(ms)
    return lowpass(s, cutoff) * env(dur, 0.09, 0.004)


def tom(f0=110, dur=0.5):
    t = t_axis(dur)
    f = f0 * (1 + 0.5 * np.exp(-t / 0.04))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(dur, 0.22, 0.002)


def tremolo_lead(m, dur, rate=12.0):
    """Surf/spy style twang: plucked bright tone with fast tremolo and a little spring."""
    t = t_axis(dur)
    f = midi_hz(m)
    sig = (np.sign(np.sin(2 * np.pi * f * t)) * 0.4 + np.sin(2 * np.pi * f * t) * 0.6
           + 0.3 * np.sin(4 * np.pi * f * t))
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * rate * t)
    return lowpass(sig, 3200) * trem * env(dur, 0.5, 0.003)


def brush(dur=0.25):
    n = rng.normal(0, 1, int(dur * SR))
    return highpass(lowpass(n, 6000), 1500) * env(dur, 0.07, 0.01)


def string_note(m, dur):
    t = t_axis(dur)
    s = saw(midi_hz(m), dur) + 0.5 * saw(midi_hz(m + 12), dur)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)
    a = np.minimum(1, t / 0.08) * np.minimum(1, (dur - t) / 0.06)
    return lowpass(s * vib, 2000) * a


def finish(x, seconds, fade=5.0):
    n = int(seconds * SR)
    x = x[:n]
    f = int(fade * SR)
    x[-f:] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, f)))
    x /= np.max(np.abs(x)) + 1e-9
    return x * 10 ** (-1 / 20)


def vault_run(seconds=30):
    bpm = 124
    s16 = 60 / bpm / 4
    bar = 16 * s16
    n = int((seconds + 2) * SR)
    drums, low, mid = np.zeros(n), np.zeros(n), np.zeros(n)
    prog = [(40, [64, 67, 71]), (36, [60, 64, 67]), (38, [62, 66, 69]), (35, [59, 63, 66])]  # Em C D B
    bars = int(seconds / bar) + 1
    for b in range(bars):
        root, ch = prog[(b // 2) % 4]
        t0 = b * bar
        for i in range(16):
            place(drums, 0.18 * hat(accent=(1.0 if i % 4 == 2 else 0.4)), t0 + i * s16)
            place(low, 0.5 * bass_note(root + (12 if i % 8 == 6 else 0), s16 * 0.9, decay=0.09), t0 + i * s16)
        for i in (0, 6, 8, 11):
            place(drums, 0.85 * kick(), t0 + i * s16)
        for i in (4, 12):
            place(drums, 0.45 * snap(), t0 + i * s16)
        if b % 2 == 1:
            for k, i in enumerate((12, 13, 14, 15)):
                place(drums, 0.5 * tom(140 - 18 * k), t0 + i * s16)
        for i in (0, 3, 6, 10, 13):
            place(mid, 0.22 * stab(ch, s16 * 1.6), t0 + i * s16)
    x = drums + low + room(mid, mix=0.28)
    return finish(x, seconds)


def spy_wire(seconds=30):
    bpm = 118
    beat = 60 / bpm
    bar = 4 * beat
    n = int((seconds + 2) * SR)
    drums, low, lead = np.zeros(n), np.zeros(n), np.zeros(n)
    walk = [45, 48, 52, 55, 57, 55, 52, 48]          # A minor walking line (A C E G A G E C)
    melody = [(0.0, 69, 1.5), (1.5, 72, 0.5), (2.0, 71, 1.0), (3.0, 67, 1.0),
              (4.0, 69, 2.0), (6.5, 64, 0.5), (7.0, 65, 1.0),
              (8.0, 69, 1.5), (9.5, 72, 0.5), (10.0, 76, 1.0), (11.0, 74, 1.0),
              (12.0, 72, 2.0), (14.0, 71, 1.0), (15.0, 68, 1.0)]   # 4-bar original motif
    bars = int(seconds / bar) + 1
    for b in range(bars):
        t0 = b * bar
        for i in range(8):
            place(low, 0.6 * bass_note(walk[(b * 8 + i) % 8] - (2 if b % 4 == 3 else 0), beat * 0.48,
                                       cutoff=900, decay=0.2), t0 + i * beat / 2)
        for i in range(4):
            place(drums, 0.25 * brush(), t0 + i * beat)
            place(drums, 0.15 * hat(accent=0.5), t0 + i * beat + beat / 2)
        for i in (1, 3):
            place(drums, 0.4 * snap(), t0 + i * beat)
        place(drums, 0.6 * kick(), t0)
        place(drums, 0.45 * kick(), t0 + 2.5 * beat)
    for rep in range(int(seconds / (4 * bar)) + 1):
        if rep == 0:
            continue                                  # let the groove set in for 4 bars first
        for at, m, ln in melody:
            place(lead, 0.3 * tremolo_lead(m, ln * beat * 0.95), rep * 4 * bar + at * beat)
    x = drums + low + room(lead, seconds=1.8, mix=0.35)
    return finish(x, seconds)


def clockwork(seconds=30):
    bpm = 96
    s8 = 60 / bpm / 2
    bar = 8 * s8
    n = int((seconds + 2) * SR)
    drums, low, strings, clock = (np.zeros(n) for _ in range(4))
    roots = [38, 38, 34, 36]                          # D D Bb C (two bars each)
    bars = int(seconds / bar) + 1
    for b in range(bars):
        t0 = b * bar
        root = roots[(b // 2) % 4]
        for i in range(8):
            place(low, 0.55 * bass_note(root, s8 * 0.85, cutoff=500, decay=0.25), t0 + i * s8)
            place(clock, 0.16 * hat(accent=0.6), t0 + i * s8)
        place(drums, 1.0 * kick(0.45), t0)
        place(drums, 0.6 * kick(0.45), t0 + 3.5 * s8)
        place(drums, 0.7 * snap(0.3) + 0.0, t0 + 4 * s8)
        place(drums, 0.45 * tom(90, 0.7), t0 + 4 * s8)
        # rising ostinato: climbs a step every 2 bars, the tension builds
        step = min(b // 2, 6)
        for i in range(4):
            place(strings, 0.16 * string_note(root + 24 + [0, 3, 7, 10][i] + step, s8 * 1.9), t0 + i * 2 * s8)
    x = drums + low + room(strings, seconds=2.0, mix=0.4) + clock
    return finish(x, seconds)


def piano_note(m, dur=3.5, vel=1.0):
    """Struck, decaying piano-like tone (a few slightly inharmonic partials + a soft hammer)."""
    t = t_axis(dur)
    f = midi_hz(m)
    x = np.zeros_like(t)
    for k, a in ((1, 1.0), (2, 0.45), (3, 0.22), (4, 0.12), (5, 0.06)):
        fk = f * k * (1 + 0.0004 * k * k)
        x += a * np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.1 + 0.9 * k))
    hammer = highpass(rng.normal(0, 1, len(t)), 1800) * np.exp(-t * 90) * 0.05
    a = np.minimum(1, t / 0.004)
    return lowpass((x + hammer) * a, 4500) * vel


def memory_piano(seconds=30):
    """The heist piece's chord loop (Dm | Bb | Gm | A) slowed down and played on a sparse piano:
    a flashback / "it already happened before" colour for Act 6 (Radiant 2024). Dark but moving,
    a soft clock keeps the heist feel; deliberately not an ambient pad (that one was rejected)."""
    bpm = 72
    beat = 60 / bpm
    bar = 4 * beat
    n = int((seconds + 6) * SR)
    keys, low, clock = np.zeros(n), np.zeros(n), np.zeros(n)
    prog = [(38, [62, 65, 69, 74]), (34, [58, 62, 65, 70]), (31, [55, 58, 62, 67]), (33, [57, 61, 64, 69])]
    figure = [(0.0, 3, 0.85), (1.0, 2, 0.6), (2.0, 1, 0.65), (3.5, 0, 0.55),
              (4.5, 2, 0.5), (6.0, 1, 0.45)]               # descending 2-bar figure, beats from chord start
    chords = int(seconds / (2 * bar)) + 2
    for c in range(chords):
        root, tones = prog[c % 4]
        t0 = c * 2 * bar
        place(low, 0.55 * piano_note(root + 12, dur=7.5, vel=0.8), t0)
        place(low, 0.35 * piano_note(root, dur=7.5, vel=0.8), t0)
        for at, k, v in figure:
            m = tones[k] + (12 if c % 8 >= 4 and k == 3 else 0)   # the top note lifts on the 2nd round
            place(keys, 0.42 * piano_note(m, dur=4.0, vel=v), t0 + at * beat)
        for i in range(8):
            place(clock, 0.05 * hat(accent=0.6 if i % 2 == 0 else 0.35), t0 + i * beat)
    x = room(keys + low, seconds=2.6, mix=0.38) + clock
    return finish(x, seconds, fade=3.0)


TRACKS = {"vault_run": vault_run, "spy_wire": spy_wire, "clockwork": clockwork, "memory_piano": memory_piano}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in TRACKS.items():
        x = fn(30)
        path = os.path.join(OUT, f"track_{name}.wav")
        wavfile.write(path, SR, (np.stack([x, x], 1) * 32767).astype(np.int16))
        print("wrote", path)
