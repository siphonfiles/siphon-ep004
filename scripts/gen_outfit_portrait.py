"""Thomas in a new outfit (ep. 004): the ep. 001 portrait recipe (Z-Image-Turbo, seed 596067, 896x1152,
8 steps, time shift 3), same prompt word for word except the clothing sentence. One image per outfit.
Usage: python scripts/gen_outfit_portrait.py <out_dir>"""
import json, os, shutil, sys, time
from gradio_client import Client

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
BASE = ("Photorealistic studio portrait photograph of a man in his late thirties. Short dark brown hair, neatly cut, clean-shaven face "
        "with no beard or stubble, no glasses. Composed, calm expression at rest, with the faintest upward set at the corners of the mouth, "
        "mouth closed, relaxed brows, open and clearly defined eyes, looking straight into the camera. Defined but not heavy jawline, "
        "no aggressive features. {OUTFIT} Medium shot from the chest up, centred in frame, facing the camera square on. Even soft frontal "
        "key light with gentle fill, no harsh shadows and no side lighting across the face. Plain empty seamless dark grey studio background, "
        "slightly darker toward the edges, nothing else in frame. Shot on an 85mm lens, shallow depth of field, natural skin texture and pores, "
        "neutral colour grade, documentary news presenter portrait.")
ORIGINAL = "He wears a plain dark charcoal crew-neck sweater, no pattern, no logo."
# Proprietarul (01:01): no accessories, no labels on the clothes. Described positively (Z-Image: negations
# activate the negated concept): bare plain fabric, nothing worn but the garment.
OUTFITS = {  # ep. 004 (Ledger implant): dark burgundy crew-neck (CLAUDE.md section 0), three shades/knits
    "burgundy_crewneck": "He wears only a plain dark burgundy crew-neck sweater in fine knit wool, completely unadorned smooth fabric.",
    "wine_merino": "He wears only a plain deep wine-red merino crew-neck sweater, fine smooth knit, completely unadorned fabric.",
    "oxblood_cotton": "He wears only a plain oxblood-red cotton crew-neck sweater with a soft ribbed collar, completely unadorned fabric.",
}
assert ORIGINAL in BASE.replace("{OUTFIT}", ORIGINAL)
z = Client("Tongyi-MAI/Z-Image-Turbo", token=os.environ["HF_TOKEN"])
api = json.dumps(z.view_api(print_info=False, return_format="dict"))
res = next((r for r in ["896x1152 ( 7:9 )", "896x1152"] if r in api), None)
if res is None:
    import re
    res = next(iter(re.findall(r'896x1152[^"]*', api)), "896x1152 ( 7:9 )")
print("resolution option:", res, flush=True)
log = []
for name, outfit in OUTFITS.items():
    t = time.time()
    try:
        g, used, _ = z.predict(prompt=BASE.replace("{OUTFIT}", outfit), resolution=res, seed=596067, steps=8, shift=3.0,
                               random_seed=False, gallery_images=[], api_name="/generate")
        item = g[0]; img = item.get("image") if isinstance(item, dict) else item
        path = img["path"] if isinstance(img, dict) else img
        dst = os.path.join(OUT, f"portrait_{name}_896x1152.png"); shutil.copy(path, dst)
        log.append(dict(outfit=name, prompt_sentence=outfit, seed=596067, seconds=round(time.time() - t, 1), file=dst))
    except Exception as e:
        log.append(dict(outfit=name, error=f"{type(e).__name__}: {e}"))
    print(log[-1], flush=True)
json.dump(log, open(os.path.join(OUT, "portrait_log.json"), "w"), indent=2)
