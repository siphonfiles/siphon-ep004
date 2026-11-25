"""Mix the episode teaser in the cold-open style proprietarul asked for (20 nov 2026):
Thomas's cut-off sentences, the music bed underneath, and a deep bass hit the
moment each sentence is cut (in the pauses between lines), then hard cut to black.

Usage: python3 sound/teaser_mix.py <voice_dir> <out.wav> [heist|ambient]
voice_dir holds t1.wav, t2.wav, t3.wav from the tts-lines workflow.
"""
import os
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly

sys.path.insert(0, os.path.dirname(__file__))
from sting_design import SR, place, note_hz, sub_boom, sub_drop  # noqa: E402
import underscore_design  # noqa: E402
import heist_design  # noqa: E402

CARD_SECONDS = 3.0      # on-screen quote cards between the lines (music + silence of voice)
GAP_AFTER_HIT = 0.9     # breath between the hit and the next element
END_FADE = 5.0          # proprietarul: the music fades out slowly at the end (~5 s), no abrupt stop


def load_voice(path):
    sr, v = wavfile.read(path)
    v = v.astype(float)
    v /= np.max(np.abs(v)) + 1e-9
    if v.ndim > 1:
        v = v.mean(1)
    if sr != SR:
        v = resample_poly(v, SR, sr)
    # trim leading/trailing silence so the cut lands right on the last syllable
    env = np.convolve(np.abs(v), np.ones(441) / 441, mode="same")
    idx = np.where(env > 0.004)[0]          # low threshold: never eat the tail of the last word
    v = v[max(0, idx[0] - 441): min(len(v), idx[-1] + int(0.08 * SR))]
    f = int(0.04 * SR)  # 40 ms fade: the cut stays crisp but the word finishes
    v[-f:] *= np.linspace(1, 0, f)
    return v


def main(voice_dir, out_path, bed_name="heist"):
    lines = [load_voice(os.path.join(voice_dir, f"t{i}.wav")) for i in (1, 2, 3)]

    plan, t = [], 1.2  # (kind, start, length)
    for i, v in enumerate(lines):
        plan.append(("voice", t, v))
        t += len(v) / SR
        plan.append(("hit", t, None))
        t += GAP_AFTER_HIT
        if i < 2:
            plan.append(("card", t, None))
            t += CARD_SECONDS
    cut_to_black = t - GAP_AFTER_HIT + 0.35    # last hit rings briefly, then everything stops
    title_at = cut_to_black + 0.6              # half a second of true silence, then the title
    total = max(title_at + 3.2, cut_to_black + END_FADE + 0.3)

    n = int(total * SR)
    voice = np.zeros(n)
    hits = np.zeros(n)
    for kind, start, v in plan:
        if kind == "voice":
            place(voice, 0.9 * v, start)
        elif kind == "hit":
            place(hits, 0.5 * sub_boom(note_hz("D1"), dur=1.8, hold=0.9), start)
    place(hits, 0.6 * sub_drop(), title_at)

    if bed_name == "heist":
        bed = heist_design.build(bars=int(total / heist_design.BAR) + 2)
    else:
        bed = underscore_design.build(with_low=False)[:, 0]
    music = np.zeros(n)
    end = int((cut_to_black + END_FADE) * SR)
    m = bed[:end] * 10 ** (-13 / 20)
    music[: len(m)] = m
    fi = int(1.0 * SR)
    music[:fi] *= np.linspace(0, 1, fi)
    c = int(cut_to_black * SR)                 # slow fade (cosine) after the last line
    fo = len(m) - c
    music[c:len(m)] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, fo)))

    mix = voice + music + hits
    mix /= np.max(np.abs(mix))
    mix *= 10 ** (-1 / 20)
    st = np.stack([mix, mix], axis=1)
    wavfile.write(out_path, SR, (st * 32767).astype(np.int16))
    print("wrote", out_path, f"{total:.1f}s", "hits at",
          [round(s, 2) for k, s, _ in plan if k == "hit"], "title", round(title_at, 2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "heist")
