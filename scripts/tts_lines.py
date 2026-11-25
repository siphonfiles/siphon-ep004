"""Generate Thomas's voice (Siphon Narrator v1, ZONOS3-Mini, CPU) for a list of lines.

Usage: python scripts/tts_lines.py <lines.json> <out_dir>
lines.json: [{"id": "t1", "text": "..."}, ...]  -> <out_dir>/<id>.wav (one file per line)
"""
import json, os, sys, time
import soundfile as sf
import torch
from transformers import AutoModel

lines_path, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
torch.set_num_threads(os.cpu_count() or 2)
model = AutoModel.from_pretrained("Zyphra/ZONOS3-Mini-hf", trust_remote_code=True, dtype=torch.float32).to("cpu")
emb = torch.load("presenter/siphon_narrator_v1_embedding.pt")

report = []
for line in json.load(open(lines_path)):
    t = time.time()
    out = model.generate(line["text"], speaker_embedding=emb, language="en_us", seed=line.get("seed", 1))
    audio = out.waveform.squeeze().numpy()
    sf.write(f"{out_dir}/{line['id']}.wav", audio, out.sampling_rate)
    report.append({"id": line["id"], "audio_s": round(len(audio) / out.sampling_rate, 1),
                   "gen_s": round(time.time() - t, 1)})
    print(report[-1], flush=True)
json.dump(report, open(f"{out_dir}/report.json", "w"), indent=2)
