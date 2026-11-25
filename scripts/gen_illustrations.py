"""Generate Siphon Files illustrations with Z-Image-Turbo (ZeroGPU, HF_TOKEN). One call per image, fixed seeds.
Usage: python scripts/gen_illustrations.py <jobs.json>   -> out/<id>.png + out/log.json
Style rules: research/visual-style.md"""
import json, os, shutil, sys, time
from gradio_client import Client

STYLE = (
    " Cinematic 3D render for a premium investigative documentary, stylized realism with clean matte materials, "
    "low-key lighting with deep navy and charcoal shadows, one warm amber key light as the only strong accent, "
    "a subtle cool teal rim light, soft volumetric haze, shallow depth of field, 35mm lens, "
    "clearly separated foreground, midground and background layers, calm restrained mood, fine film grain."
)

jobs = json.load(open(sys.argv[1]))
OUT = "out"; os.makedirs(OUT, exist_ok=True)
z = Client("Tongyi-MAI/Z-Image-Turbo", token=os.environ["HF_TOKEN"])
log = []
for j in jobs["images"]:
    prompt = j["prompt"].strip() + jobs.get("style", STYLE)
    t = time.time()
    try:
        g, used, _ = z.predict(prompt=prompt, resolution=jobs.get("resolution", "2048x1152 ( 16:9 )"), seed=j["seed"],
                               steps=jobs.get("steps", 8), shift=jobs.get("shift", 3.0), random_seed=False,
                               gallery_images=[], api_name="/generate")
        item = g[0]; img = item.get("image") if isinstance(item, dict) else item
        src = img["path"] if isinstance(img, dict) else img
        dst = f"{OUT}/{j['id']}.png"; shutil.copy(src, dst)
        log.append({"id": j["id"], "seed": j["seed"], "seconds": round(time.time() - t, 1), "prompt": prompt})
    except Exception as e:
        log.append({"id": j["id"], "seed": j["seed"], "error": f"{type(e).__name__}: {e}"})
    print(log[-1]["id"], log[-1].get("seconds", log[-1].get("error")), flush=True)
json.dump(log, open(f"{OUT}/log.json", "w"), indent=2, ensure_ascii=False)
