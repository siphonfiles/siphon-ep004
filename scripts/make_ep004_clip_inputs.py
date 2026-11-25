"""Build the LongCat 720p job inputs for the ep. 004 Thomas clips (burgundy sweater reference).

Usage: python3 scripts/make_ep004_clip_inputs.py <voice_dir>
Each clip = 0.3 s of silence + the line(s) exactly as in the mix (same trim, same pause) + silence to 5.0 s.
Writes presenter/clips/inputs/ep004/thomas_e4_<id>.wav + .json and presenter/clips/inputs/ep004_clip_plan.json.
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
# (clip id, [line ids], pause between lines as in sound/ep004/ep004_mix.py)
# (clip id, [line ids], pause) — the 16 THOMAS lines of script v1.2, one 5 s clip each
CLIPS = [("i1", ["i1"], 0), ("i2", ["i2"], 0), ("i3", ["i3"], 0), ("a9", ["a9"], 0), ("a10", ["a10"], 0), ("b7", ["b7"], 0), ("b15", ["b15"], 0), ("c7", ["c7"], 0), ("c10", ["c10"], 0), ("d9", ["d9"], 0), ("d15", ["d15"], 0), ("e8", ["e8"], 0), ("f6", ["f6"], 0), ("g5", ["g5"], 0), ("k5", ["k5"], 0), ("k6", ["k6"], 0)]
# second camera inside runs of consecutive Thomas lines (i1-i3, a9-a10, c7/c10 apart, k5-k6)
CAMERA = {'i2': 'C', 'a10': 'C', 'c10': 'C', 'k6': 'C'}

PROMPT = ("A British man in his early forties with short dark brown hair and light stubble, wearing a plain "
          "dark burgundy crew-neck sweater, sits at a wooden desk in a dim investigation "
          "office and speaks calmly and clearly to the camera. His hands rest still and relaxed on the manila "
          "folder on the desk. Subtle natural head movements, steady eye contact, occasional natural blinks. "
          "Static locked-off camera, soft frontal light, realistic skin texture.")


def main(vdir):
    lines = {x["id"]: x["text"] for x in json.load(open(os.path.join(ROOT, "sound", "ep004", "ep004_lines.json")))}
    out = os.path.join(ROOT, "presenter", "clips", "inputs", "ep004")
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
        name = f"thomas_e4_{cid}"
        wav = os.path.join(out, name + ".wav")
        wavfile.write(wav, SR, (a * 32767).astype(np.int16))
        job = dict(name=name + "_720p", image="presenter/reference/thomas_ref_ep004_1920x1080.png",
                   audio=os.path.relpath(wav, ROOT), line=" ".join(lines[i] for i in ids), prompt=PROMPT,
                   resolution="720p", seed=42, vocal_mode="Clean speech (fast)", acceleration="DBCache faster",
                   note="ep. 004, burgundy sweater; 720p only (rule 18d)")
        json.dump(job, open(os.path.join(out, name + ".json"), "w"), indent=1)
        plan.append(dict(name=name + "_720p", first=ids[0], last=ids[-1], lead=LEAD,
                         camera=CAMERA.get(cid, "M"), tail=0.35))
        print(name, f"{sum(len(p) for p in parts) / SR:.2f} s")
    json.dump(dict(clips=plan), open(os.path.join(ROOT, "presenter", "clips", "inputs", "ep004_clip_plan.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
