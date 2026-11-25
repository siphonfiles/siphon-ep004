"""Cut the main object out of illustrations with BiRefNet (MIT, ZhengPeng7/BiRefNet) on CPU.
Usage: python scripts/birefnet_cut.py out_dir img1.jpg img2.jpg ...  -> <name>_cut.png (RGBA) + <name>_mask.png"""
import os, sys, time, torch
from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
torch.set_float32_matmul_precision("high")
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
m = AutoModelForImageSegmentation.from_pretrained("ZhengPeng7/BiRefNet", trust_remote_code=True).eval()
tf = transforms.Compose([transforms.Resize((1024, 1024)), transforms.ToTensor(),
                         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
for p in sys.argv[2:]:
    t = time.time(); im = Image.open(p).convert("RGB")
    with torch.no_grad():
        pred = m(tf(im).unsqueeze(0))[-1].sigmoid()[0, 0]
    mask = transforms.ToPILImage()(pred).resize(im.size, Image.BILINEAR)
    name = os.path.basename(p).rsplit(".", 1)[0]
    rgba = im.copy(); rgba.putalpha(mask)
    rgba.save(f"{out}/{name}_cut.png"); mask.save(f"{out}/{name}_mask.png")
    print(name, round(time.time() - t, 1), "s", flush=True)
