"""Siphon Files — sonic signature drafts (v1).

Everything is synthesized from scratch (numpy), so the stings are 100% original:
no samples, no models, no licences to worry about.

Run:  python3 sound/sting_design.py   ->  sound/stings/*.wav
"""
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
OUT = os.path.join(os.path.dirname(__file__), "stings")
rng = np.random.default_rng(7)


# ---------- building blocks ----------
def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def env_exp(dur, decay, attack=0.004):
    t = t_axis(dur)
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-t / decay)


def lowpass(x, fc, order=4):
    return sosfilt(butter(order, fc, btype="low", fs=SR, output="sos"), x)


def highpass(x, fc, order=2):
    return sosfilt(butter(order, fc, btype="high", fs=SR, output="sos"), x)


def place(buf, sig, start):
    sig = sig.copy()
    f = min(len(sig) // 4, int(0.04 * SR))  # fade every element out: no truncation clicks
    sig[-f:] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, f)))
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


def note_hz(name):
    names = {"C": -9, "C#": -8, "D": -7, "Eb": -6, "E": -5, "F": -4, "F#": -3,
             "G": -2, "Ab": -1, "A": 0, "Bb": 1, "B": 2}
    n, octv = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (octv - 4)) / 12)


def glass_bell(f, dur=3.0, bright=1.0):
    """FM bell: inharmonic ratio gives a cold, glassy 'evidence' tone."""
    t = t_axis(dur)
    idx = 2.2 * bright * np.exp(-t / 0.35)
    mod = np.sin(2 * np.pi * f * 3.5 * t)
    car = np.sin(2 * np.pi * f * t + idx * mod)
    body = 0.35 * np.sin(2 * np.pi * f * 0.5 * t)  # warm sub-octave
    return (car + body) * env_exp(dur, 0.9)


def pluck(f, dur=2.5, damp=0.996):
    """Karplus-Strong: muted, felt-piano-like pluck."""
    n = int(dur * SR)
    p = int(SR / f)
    buf = rng.uniform(-1, 1, p)
    buf = lowpass(buf, 2500)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = damp * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return lowpass(out, 3000) * env_exp(dur, 1.1, attack=0.002)


def drip(f0=700, f1=2100, dur=0.25, level=1.0):
    """Water droplet: fast rising chirp with a short decay (the logo's drop)."""
    t = t_axis(dur)
    sweep = f0 + (f1 - f0) * (1 - np.exp(-t / 0.012))
    ph = 2 * np.pi * np.cumsum(sweep) / SR
    return level * np.sin(ph) * env_exp(dur, 0.045, attack=0.001)


def sub_hit(dur=2.2, f_start=62, f_end=38):
    t = t_axis(dur)
    f = f_end + (f_start - f_end) * np.exp(-t / 0.08)
    ph = 2 * np.pi * np.cumsum(f) / SR
    click = highpass(rng.normal(0, 1, len(t)), 2000) * env_exp(dur, 0.006)
    return (np.sin(ph) * env_exp(dur, 0.7) + 0.15 * click)


def tick(dur=0.06):
    t = t_axis(dur)
    n = highpass(rng.normal(0, 1, len(t)), 3500) * env_exp(dur, 0.008, attack=0.0005)
    tone = np.sin(2 * np.pi * 2600 * t) * env_exp(dur, 0.01, attack=0.0005)
    return 0.6 * n + 0.5 * tone


def riser(dur=1.2):
    """Noise swell whose brightness rises smoothly (crossfaded filter bank, no seams)."""
    t = t_axis(dur)
    noise = rng.normal(0, 1, len(t))
    cutoffs = [300, 800, 2000, 5000, 11000]
    bank = [lowpass(noise, fc) for fc in cutoffs]
    pos = (t / dur) * (len(cutoffs) - 1)
    out = np.zeros_like(noise)
    for k, band in enumerate(bank):
        w = np.clip(1 - np.abs(pos - k), 0, 1)
        out += w * band
    return out * (t / dur) ** 2


def glide_synth(f_start, f_end, dur=1.6):
    """Detuned saw that slides downward: the money 'draining'."""
    t = t_axis(dur)
    f = f_end * (f_start / f_end) ** (1 - (t / dur) ** 0.7)
    sig = np.zeros_like(t)
    for det in (-0.006, 0.0, 0.007):
        ph = 2 * np.pi * np.cumsum(f * (1 + det)) / SR
        sig += 2 * ((ph / (2 * np.pi)) % 1) - 1
    sig = lowpass(sig / 3, 1400)
    return sig * env_exp(dur, 0.8, attack=0.03)


def drone(f, dur):
    t = t_axis(dur)
    sig = sum(np.sin(2 * np.pi * f * m * (1 + d) * t) / m
              for m, d in ((1, 0), (2, 0.003), (3, -0.002)))
    fade = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 1.5)
    return lowpass(sig, 900) * fade


def reverb(x, seconds=2.6, mix=0.35):
    """Stereo reverb from decaying filtered noise impulse responses."""
    n = int(seconds * SR)
    t = np.arange(n) / SR
    outs = []
    for seed in (1, 2):
        ir = np.random.default_rng(seed).normal(0, 1, n) * np.exp(-t / (seconds / 6.5))
        ir = lowpass(ir, 6000)
        ir /= np.sqrt(np.sum(ir ** 2))
        wet = fftconvolve(x, ir)[: len(x)]
        outs.append((1 - mix) * x + mix * wet)
    return np.stack(outs, axis=1)


def finish(stereo, name):
    fade = int(0.05 * SR)
    stereo[-fade:] *= np.linspace(1, 0, fade)[:, None]
    peak = np.max(np.abs(stereo))
    stereo = stereo / peak * 10 ** (-1 / 20)  # -1 dBFS
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    wavfile.write(path, SR, (stereo * 32767).astype(np.int16))
    print("wrote", path, f"{len(stereo) / SR:.2f}s")


# ---------- variant A: "The Drain" (glass bells + drop) ----------
def variant_a():
    dur = 5.0
    b = np.zeros(int(dur * SR))
    notes = ["E5", "C5", "A4"]  # descending A-minor arpeggio: something slipping away
    for k, n in enumerate(notes):
        place(b, 0.5 * glass_bell(note_hz(n), bright=1.0 - 0.2 * k), 0.10 + 0.34 * k)
    place(b, 0.55 * sub_hit(), 0.78)
    place(b, 0.35 * drone(note_hz("A2"), 4.0), 0.78)
    place(b, 0.55 * drip(), 1.75)
    place(b, 0.22 * drip(650, 1900), 2.15)  # echo of the drop
    finish(reverb(b, 2.8, 0.38), "A_the_drain.wav")


# ---------- variant B: "Outflow" (riser + draining glide + triple drip) ----------
def variant_b():
    dur = 4.6
    b = np.zeros(int(dur * SR))
    place(b, 0.25 * riser(1.1), 0.0)
    place(b, 0.7 * sub_hit(f_start=70, f_end=36), 1.1)
    place(b, 0.45 * glide_synth(note_hz("A3"), note_hz("E2"), 1.8), 1.1)
    place(b, 0.35 * glass_bell(note_hz("A4"), 2.5, bright=0.6), 1.1)
    for k, lvl in enumerate((0.6, 0.32, 0.16)):  # drop + two echoes
        place(b, drip(level=lvl), 2.55 + 0.27 * k)
    finish(reverb(b, 2.4, 0.33), "B_outflow.wav")


# ---------- variant C: "Case File" (clock ticks + muted piano + drop) ----------
def variant_c():
    dur = 5.2
    b = np.zeros(int(dur * SR))
    for k in range(3):  # ties into the T-minus countdown cards
        place(b, 0.35 * tick(), 0.05 + 0.42 * k)
    notes = ["D4", "Bb3", "G3"]  # descending G-minor: grave, investigative
    for k, n in enumerate(notes):
        place(b, 0.6 * pluck(note_hz(n), 3.0), 1.30 + 0.30 * k)
    place(b, 0.3 * drone(note_hz("G2"), 3.6), 1.30)
    place(b, 0.45 * sub_hit(f_start=55, f_end=36), 1.90)
    place(b, 0.5 * drip(600, 1800), 2.85)
    finish(reverb(b, 2.6, 0.30), "C_case_file.wav")


# ---------- v2: discreet variants (owner: "mult mai discret") ----------
def soft_tone(f, dur=2.5):
    """Pure sine + faint octave, slow attack: a felt-muted, almost whispered note."""
    t = t_axis(dur)
    sig = np.sin(2 * np.pi * f * t) + 0.12 * np.sin(2 * np.pi * 2 * f * t)
    return lowpass(sig, 1800) * env_exp(dur, 0.9, attack=0.02)


def variant_d():  # two soft notes falling + tiny drop
    dur = 3.2
    b = np.zeros(int(dur * SR))
    place(b, 0.5 * soft_tone(note_hz("E4")), 0.05)
    place(b, 0.5 * soft_tone(note_hz("A3"), 2.8), 0.42)
    place(b, 0.18 * drip(650, 1700), 1.15)
    finish(reverb(b, 1.8, 0.25), "D_two_notes.wav")


def variant_e():  # one muted piano note + drop
    dur = 2.8
    b = np.zeros(int(dur * SR))
    place(b, 0.5 * lowpass(pluck(note_hz("A3"), 2.6), 1500), 0.05)
    place(b, 0.15 * drip(600, 1600), 0.75)
    finish(reverb(b, 1.6, 0.22), "E_single_note.wav")


def variant_f():  # just the drop over a faint low swell
    dur = 2.6
    b = np.zeros(int(dur * SR))
    place(b, 0.25 * drone(note_hz("A2"), 2.5), 0.0)
    place(b, 0.3 * drip(600, 1700), 0.9)
    place(b, 0.08 * drip(580, 1600), 1.2)
    finish(reverb(b, 1.6, 0.25), "F_drop_only.wav")


# ---------- v3: low and discreet (owner: "mai pe bas, dar discret") ----------
def soft_sub(f=55, dur=2.6):
    """Sub-bass swell: slow in, slow out, no transient."""
    t = t_axis(dur)
    sig = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    shape = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return sig * shape


def variant_g():  # two low notes + sub
    dur = 3.4
    b = np.zeros(int(dur * SR))
    place(b, 0.5 * soft_tone(note_hz("E3"), 2.6), 0.05)
    place(b, 0.55 * soft_tone(note_hz("A2"), 3.0), 0.45)
    place(b, 0.35 * soft_sub(note_hz("A1"), 2.8), 0.35)
    place(b, 0.14 * drip(380, 1000, 0.3), 1.25)
    finish(reverb(b, 1.8, 0.22), "G_low_two_notes.wav")


def variant_h():  # one low muted piano note + sub
    dur = 3.0
    b = np.zeros(int(dur * SR))
    place(b, 0.6 * lowpass(pluck(note_hz("A2"), 2.8, damp=0.997), 900), 0.05)
    place(b, 0.35 * soft_sub(note_hz("A1"), 2.6), 0.0)
    place(b, 0.13 * drip(380, 1000, 0.3), 0.9)
    finish(reverb(b, 1.6, 0.2), "H_low_single_note.wav")


def variant_i():  # deep swell + low drop
    dur = 2.8
    b = np.zeros(int(dur * SR))
    place(b, 0.45 * soft_sub(note_hz("A1"), 2.7), 0.0)
    place(b, 0.2 * drone(note_hz("A2"), 2.6), 0.0)
    place(b, 0.25 * drip(320, 850, 0.35), 1.0)
    place(b, 0.07 * drip(300, 800, 0.35), 1.3)
    finish(reverb(b, 1.6, 0.22), "I_low_drop.wav")


# ---------- v4: low, discreet, suspense (owner: "ceva mai de suspans") ----------
def thump(f=50, dur=0.35):
    """Soft heartbeat-like low thump, no click."""
    t = t_axis(dur)
    fr = f * (1 + 0.6 * np.exp(-t / 0.03))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    return lowpass(np.sin(ph) * env_exp(dur, 0.09, attack=0.008), 200)


def tremolo_drone(f, dur, rate=5.0, depth=0.5):
    t = t_axis(dur)
    return drone(f, dur) * (1 - depth * 0.5 * (1 + np.sin(2 * np.pi * rate * t)))


def variant_j():  # heartbeat + unresolved minor-second cluster
    dur = 3.6
    b = np.zeros(int(dur * SR))
    for k, start in enumerate((0.05, 0.30, 1.05, 1.30)):  # lub-dub, lub-dub
        place(b, (0.8 if k % 2 == 0 else 0.55) * thump(), start)
    place(b, 0.35 * soft_tone(note_hz("A2"), 2.6), 1.05)
    place(b, 0.25 * soft_tone(note_hz("Bb2"), 2.6), 1.10)  # semitone rub = unease
    place(b, 0.12 * drip(360, 950, 0.3), 2.0)
    finish(reverb(b, 2.0, 0.25), "J_heartbeat.wav")


def variant_k():  # tritone, never resolves, trembling drone under it
    dur = 3.6
    b = np.zeros(int(dur * SR))
    place(b, 0.3 * tremolo_drone(note_hz("A1"), 3.5, rate=4.0), 0.0)
    place(b, 0.5 * soft_tone(note_hz("A2"), 2.8), 0.15)
    place(b, 0.45 * soft_tone(note_hz("Eb3"), 2.8), 0.75)  # tritone above: the "devil's interval"
    place(b, 0.12 * drip(360, 950, 0.3), 1.9)
    finish(reverb(b, 2.2, 0.28), "K_tritone.wav")


def variant_l():  # reversed swell sucked in, hard stop, drop in the silence
    dur = 3.0
    b = np.zeros(int(dur * SR))
    sw = np.zeros(int(2.0 * SR))
    place(sw, 0.5 * soft_tone(note_hz("A2"), 2.0), 0.0)
    place(sw, 0.3 * soft_tone(note_hz("Bb2"), 2.0), 0.0)
    sw = reverb(sw, 1.8, 0.5)[:, 0][::-1]  # reversed reverb tail: the "siphon" inhale
    sw *= np.linspace(0.2, 1, len(sw)) ** 2
    place(b, sw, 0.0)
    place(b, 0.6 * thump(45, 0.4), 2.0)
    place(b, 0.16 * drip(340, 900, 0.35), 2.25)
    finish(reverb(b, 1.4, 0.18), "L_inhale.wav")


# ---------- v5: bass only (owner: "ceva doar din bas, atat") ----------
# Everything low-passed at 220 Hz; a soft 2nd harmonic keeps it audible on laptops.
def bass_only(x):
    return lowpass(x, 220, order=6)


def variant_m():  # two deep heartbeats, nothing else
    dur = 2.4
    b = np.zeros(int(dur * SR))
    place(b, 0.9 * thump(48, 0.6), 0.05)
    place(b, 0.6 * thump(44, 0.7), 0.33)
    finish(reverb(bass_only(b), 1.2, 0.15), "M_bass_heartbeat.wav")


def variant_n():  # slow sub swell, two notes a semitone apart beating against each other
    dur = 3.4
    b = np.zeros(int(dur * SR))
    place(b, 0.5 * soft_sub(note_hz("A1"), 3.3), 0.0)
    place(b, 0.35 * soft_sub(note_hz("Bb1"), 3.0), 0.3)
    finish(reverb(bass_only(b), 1.4, 0.15), "N_bass_swell.wav")


def variant_o():  # sub inhale that stops on one deep thump
    dur = 2.8
    b = np.zeros(int(dur * SR))
    t = t_axis(1.8)
    f = 38 + 22 * (t / 1.8)  # pitch rises slowly: pressure building
    ph = 2 * np.pi * np.cumsum(f) / SR
    sw = (np.sin(ph) + 0.25 * np.sin(2 * ph)) * (t / 1.8) ** 2.5
    place(b, 0.5 * sw, 0.0)
    place(b, 1.0 * thump(42, 0.9), 1.8)
    finish(reverb(bass_only(b), 1.2, 0.15), "O_bass_inhale.wav")


# ---------- v6: cinematic sub accents (reference analysed 20 nov 2026) ----------
# Measured on a DOAC cold open (1:41 screen recording, analysis only, nothing copied):
# about 15 low accents in 100 s, mostly a sub "boom" around 34 Hz that comes in fast
# (+20 dB in about 0.15 s), holds about 1.2-1.5 s and fades, placed on cuts between
# clips; the opening one is a pitch drop from about 86 to 30 Hz over about 1.2 s.
# Ours: our own tuning (A0/A1), our own envelope, plus a soft 2nd/3rd harmonic so
# phone speakers still hint at it.
def sub_boom(f=34.0, dur=2.2, hold=1.2):
    t = t_axis(dur)
    ph = 2 * np.pi * f * t
    sig = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    att = np.clip(t / 0.12, 0, 1) ** 2
    rel = np.where(t < hold, 1.0, np.exp(-(t - hold) / 0.35))
    return lowpass(sig * att * rel, 200, order=4)


def sub_drop(f0=86.0, f1=31.0, dur=2.6, glide=1.2):
    t = t_axis(dur)
    f = f1 + (f0 - f1) * np.exp(-t / (glide / 3))
    ph = 2 * np.pi * np.cumsum(f) / SR
    sig = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    att = np.clip(t / 0.03, 0, 1)
    rel = np.where(t < 1.4, 1.0, np.exp(-(t - 1.4) / 0.4))
    return lowpass(sig * att * rel, 250, order=4)


def variant_p():
    finish(reverb(sub_drop(), 1.0, 0.1), "P_sub_drop.wav")


def variant_q():
    # tuned to our key area: C#1 = 34.6 Hz, right where the reference sits
    finish(reverb(sub_boom(note_hz("C#1")), 1.0, 0.1), "Q_sub_boom.wav")


def demo_rhythm():
    """30 s silence-bed demo: drop at 0, booms on imagined cuts, like an episode cold open."""
    dur = 30.0
    b = np.zeros(int(dur * SR))
    place(b, 0.9 * sub_drop(), 0.5)
    for start in (6.8, 12.4, 17.0, 21.9, 26.5):
        place(b, 0.75 * sub_boom(note_hz("C#1")), start)
    finish(reverb(b, 1.0, 0.1), "demo_cold_open_rhythm.wav")


if __name__ == "__main__":
    variant_p()
    variant_q()
    demo_rhythm()
