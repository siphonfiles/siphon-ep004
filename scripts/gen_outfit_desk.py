"""Thomas at the desk in the new outfit (Qwen-Image-Edit-2511): the chosen portrait + the SAME empty set plate as the
ep. 001 reference (plate_20251120, seed 11, 40 steps, 1344x768), then brought to 1920x1080 on CPU exactly like the
ep. 001 reference (Lanczos to 1920x1097, crop 12 px from the top).
Usage: python scripts/gen_outfit_desk.py <portrait.png> <outfit sentence> <out_dir>"""
import json, os, shutil, sys, time
from gradio_client import Client, handle_file
from PIL import Image

portrait, outfit, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
PLATE = "presenter/set_candidates/plate_20251120.png"
PROMPT = ("Place the man from image 1 into the office from image 2. He sits in the chair behind the desk, upper body visible from the waist up, "
          "positioned slightly left of centre, facing the camera and looking straight into the lens with a calm, composed expression. "
          "Both forearms rest on the desk and his hands lie still and relaxed on the desk surface, near the case folder, fingers natural. "
          "On the desk, objects from this case (Coldcard: bitcoin hardware wallets whose secret words were guessable): a closed manila case folder "
          "under his hands, three small identical matte black pocket-sized hardware wallet devices in a neat row to his left, "
          "a small loose pile of white six-sided dice beside them, a small brushed steel plate with rows of tiny blurred stamped marks, "
          "and a small brass safe-deposit box key on a ring. "
          "All surfaces are plain and unbranded, every printed character too small and blurred to read. "
          "Keep the warm brass desk lamp on the right exactly where it is. "
          f"Keep his face, hair, short stubble and his clothing exactly as in image 1: {outfit} "
          "Soft even frontal light on his face, warm amber lamp light on the desk, background softly out of focus. Photorealistic, 16:9.")
q = Client("Qwen/Qwen-Image-Edit-2511", token=os.environ["HF_TOKEN"])
t = time.time()
g, _ = q.predict(images=[{"image": handle_file(p), "caption": None} for p in (portrait, PLATE)], prompt=PROMPT, seed=11,
                 randomize_seed=False, true_guidance_scale=4.0, num_inference_steps=40, height=768, width=1344,
                 rewrite_prompt=False, api_name="/infer")
item = g[0]; img = item.get("image") if isinstance(item, dict) else item
path = img["path"] if isinstance(img, dict) else img
src = os.path.join(OUT, "thomas_ref_ep003_source_1344x768.png"); shutil.copy(path, src)
im = Image.open(src).convert("RGB").resize((1920, 1097), Image.LANCZOS).crop((0, 12, 1920, 1092))
im.save(os.path.join(OUT, "thomas_ref_ep003_1920x1080.png"))
json.dump(dict(portrait=portrait, plate=PLATE, seed=11, steps=40, prompt=PROMPT, seconds=round(time.time() - t, 1)),
          open(os.path.join(OUT, "desk_log.json"), "w"), indent=2)
print("done", round(time.time() - t, 1), "s")
