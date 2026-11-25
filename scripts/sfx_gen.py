"""Generate SFX candidates with Stable Audio Open Small on CPU. Usage: python scripts/sfx_gen.py jobs.json out_dir"""
import json, os, sys, time, torch, torchaudio
from einops import rearrange
from stable_audio_tools import get_pretrained_model
from stable_audio_tools.inference.generation import generate_diffusion_cond
jobs = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
model, cfg = get_pretrained_model("stabilityai/stable-audio-open-small")
sr, n = cfg["sample_rate"], cfg["sample_size"]
log = []
for name, secs, prompt in jobs["items"]:
    for seed in (11, 22, 33):
        t = time.time()
        a = generate_diffusion_cond(model, steps=8, cfg_scale=1.0, sampler_type="pingpong", device="cpu", seed=seed,
                                    conditioning=[{"prompt": prompt, "seconds_total": secs}], sample_size=n)
        a = rearrange(a, "b d n -> d (b n)").to(torch.float32)
        a = a[:, : int(secs * sr)]
        a = (a / a.abs().max().clamp(min=1e-6) * 0.89).clamp(-1, 1)
        torchaudio.save(f"{out}/{name}_s{seed}.wav", a, sr)
        log.append({"name": name, "seed": seed, "seconds": round(time.time() - t, 1)}); print(log[-1], flush=True)
json.dump(log, open(f"{out}/log.json", "w"), indent=1)
