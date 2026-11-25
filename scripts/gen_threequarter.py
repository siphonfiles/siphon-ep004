"""Thomas Archer, second camera angle (three-quarter view) at the same desk — ONE image with Qwen-Image-Edit-2511.
Image 1 = the approved desk reference (scene, clothes, lighting); image 2 = the approved portrait (face identity)."""
import json, os, shutil, time
from gradio_client import Client, handle_file

OUT = "out"; os.makedirs(OUT, exist_ok=True)
REF = "presenter/reference/thomas_ref_v1_source_1344x768.png"
PORTRAIT = "presenter/portrait_v1_896x1152.png"
PROMPT = (
    "Show the exact same scene as image 1, filmed by a second camera placed to the left of the desk, about forty degrees off axis, "
    "so we see the same man in a three-quarter view. He sits in the same chair at the same dark wooden desk, upper body from the waist up, "
    "his head turned slightly down toward the open manila case folder on the desk, reading it attentively, calm and focused. "
    "Both forearms rest on the desk, one hand holding the edge of the folder, fingers natural. "
    "Keep his face, short dark brown hair, light stubble and plain dark charcoal crew-neck sweater exactly as in image 2. "
    "Same warm brass desk lamp now on the far side of the desk, same out-of-focus evidence board with pinned documents and amber threads behind him, "
    "same dark charcoal and deep navy tones with amber accent light, soft light on his face, photorealistic, 16:9."
)
t = time.time()
q = Client("Qwen/Qwen-Image-Edit-2511", token=os.environ["HF_TOKEN"])
g, _ = q.predict(images=[{"image": handle_file(p), "caption": None} for p in (REF, PORTRAIT)], prompt=PROMPT, seed=55,
                 randomize_seed=False, true_guidance_scale=4.0, num_inference_steps=40, height=768, width=1344,
                 rewrite_prompt=False, api_name="/infer")
item = g[0]; img = item.get("image") if isinstance(item, dict) else item
shutil.copy(img["path"] if isinstance(img, dict) else img, f"{OUT}/thomas_ref_threequarter_s55.png")
json.dump({"seed": 55, "seconds": round(time.time() - t, 1), "prompt": PROMPT}, open(f"{OUT}/log.json", "w"), indent=2)
print("done", round(time.time() - t, 1), "s")
