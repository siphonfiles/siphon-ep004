"""Depth maps for the illustrations (Depth Anything V2 Small, Apache-2.0, CPU).
Usage: python scripts/depth_maps.py <list.json> <renders_dir> <out_dir>  -> <out>/<id>_depth.png (16-bit, near = bright)"""
import json, os, sys, time
import numpy as np
from PIL import Image
from transformers import pipeline

items, src, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
pipe = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=-1)
for it in items:
    t = time.time()
    img = Image.open(os.path.join(src, it + ".png")).convert("RGB")
    d = pipe(img)["predicted_depth"].squeeze().numpy().astype(np.float32)
    d = (d - d.min()) / max(1e-6, d.max() - d.min())
    dm = Image.fromarray((d * 65535).astype(np.uint16)).resize(img.size, Image.BICUBIC)
    dm.save(os.path.join(out, it.split("/")[-1] + "_depth.png"))
    print(it, round(time.time() - t, 1), flush=True)
