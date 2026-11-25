"""Build the LongCat 720p job inputs for the ep. 003 Thomas clips (olive shirt reference).

Usage: python3 scripts/make_ep003_clip_inputs.py <voice_dir>
Each clip = 0.3 s of silence + the line(s) exactly as in the mix (same trim, same pause) + silence to 5.0 s.
Writes presenter/clips/inputs/ep003/thomas_e3_<id>.wav + .json and presenter/clips/inputs/ep003_clip_plan.json.
"""
import json
import os
import sys

import numpy as np
from scipy.io import wavfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "sound"))
from teaser_mix import load_voice  # noqa: E402
from sting_design import SR  # noqa: E402

LEAD, LEN = 0.3, 5.0
# (clip id, [line ids], pause between lines as in sound/ep003/ep003_mix.py)
CLIPS = [("i1", ["i1"], 0), ("i2", ["i2"], 0), ("i3", ["i3"], 0), ("i4", ["i4"], 0),
         ("b8", ["b8", "b9"], 0.5), ("b10", ["b10"], 0), ("c12", ["c12"], 0), ("e8", ["e8"], 0),
         ("g8", ["g8"], 0), ("g9", ["g9"], 0), ("k3", ["k3"], 0), ("k6", ["k6"], 0),
         # second set (owner, 23 Nov: every Thomas line gets its own HF 720p clip, no Kaggle resync)
         ("c3", ["c3"], 0), ("c4", ["c4"], 0), ("c13", ["c13"], 0), ("c14", ["c14"], 0), ("c15", ["c15"], 0),
         ("c16", ["c16"], 0), ("e9", ["e9"], 0), ("g1", ["g1"], 0), ("g2", ["g2"], 0), ("g3", ["g3"], 0),
         ("g4", ["g4"], 0), ("k4", ["k4"], 0), ("k5", ["k5"], 0), ("k7", ["k7"], 0), ("k10", ["k10"], 0)]
# second camera, alternating inside each run of Thomas lines
CAMERA = {"i2": "C", "i4": "C", "b10": "C", "c4": "C", "c13": "C", "c15": "C", "e8": "C",
          "g2": "C", "g4": "C", "g9": "C", "k4": "C", "k6": "C"}

PROMPT = ("A British man in his early forties with short dark brown hair and light stubble, wearing a plain "
          "dark olive green cotton shirt with a soft open collar, sits at a wooden desk in a dim investigation "
          "office and speaks calmly and clearly to the camera. His hands rest still and relaxed on the manila "
          "folder on the desk. Subtle natural head movements, steady eye contact, occasional natural blinks. "
          "Static locked-off camera, soft frontal light, realistic skin texture.")


def main(vdir):
    lines = {x["id"]: x["text"] for x in json.load(open(os.path.join(ROOT, "sound", "ep003", "ep003_lines.json")))}
    out = os.path.join(ROOT, "presenter", "clips", "inputs", "ep003")
    os.makedirs(out, exist_ok=True)
    plan = []
    for cid, ids, pause in CLIPS:
        parts = [np.zeros(int(LEAD * SR))]
        for k, i in enumerate(ids):
            if k:
                parts.append(np.zeros(int(pause * SR)))
            parts.append(load_voice(os.path.join(vdir, i + ".wav")))
        a = np.concatenate(parts)
        if len(a) > LEN * SR:
            raise SystemExit(f"{cid}: {len(a) / SR:.2f} s > {LEN} s")
        a = np.concatenate([a, np.zeros(int(LEN * SR) - len(a))]) * 0.89
        name = f"thomas_e3_{cid}"
        wav = os.path.join(out, name + ".wav")
        wavfile.write(wav, SR, (a * 32767).astype(np.int16))
        job = dict(name=name + "_720p", image="presenter/reference/thomas_ref_ep003_1920x1080.png",
                   audio=os.path.relpath(wav, ROOT), line=" ".join(lines[i] for i in ids), prompt=PROMPT,
                   resolution="720p", seed=42, vocal_mode="Clean speech (fast)", acceleration="DBCache faster",
                   note="ep. 003, olive shirt; 720p only (rule 18d)")
        json.dump(job, open(os.path.join(out, name + ".json"), "w"), indent=1)
        plan.append(dict(name=name + "_720p", first=ids[0], last=ids[-1], lead=LEAD,
                         camera=CAMERA.get(cid, "M"), tail=0.35))
        print(name, f"{sum(len(p) for p in parts) / SR:.2f} s")
    json.dump(dict(clips=plan), open(os.path.join(ROOT, "presenter", "clips", "inputs", "ep003_clip_plan.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
