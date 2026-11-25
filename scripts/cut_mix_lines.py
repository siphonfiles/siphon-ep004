"""Cut every voice line out of the final episode audio (what viewers hear) for an ASR check.
Usage: python3 scripts/cut_mix_lines.py <audio.m4a> <timeline.json> <lines.json> <out_dir>
Writes <id>.flac (16 kHz mono, 0.15 s padding) + texts.json."""
import json, os, subprocess, sys
audio, tl, lines, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
T = json.load(open(tl)); texts = {x["id"]: x["text"] for x in json.load(open(lines))}
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]))
print(f"audio {dur:.2f} s, timeline {T['total']:.2f} s")
assert abs(dur - T["total"]) < 0.5, "audio and timeline do not match"
used = {}
for e in T["events"]:
    if e.get("kind") != "voice": continue
    k = e["id"]; s = max(0, e["t"] - 0.15); d = e["dur"] + 0.3
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", audio,
                    "-ac", "1", "-ar", "16000", os.path.join(out, k + ".flac")], check=True)
    used[k] = texts[k]
missing = sorted(set(texts) - set(used))
print(len(used), "lines cut; in script but not in the mix:", missing or "none")
json.dump(used, open(os.path.join(out, "texts.json"), "w"), indent=1)
