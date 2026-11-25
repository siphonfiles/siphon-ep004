from PIL import Image, ImageDraw, ImageFont, ImageFilter
import glob, os

PLATE = "/home/claude/siphon-files/brand/banner_plate_moss.jpg"
OUT = "/home/claude/siphon-files/brand/banner_2560x1440.png"
MARK = "/home/claude/siphon-files/brand/mark_white.svg"

W, H = 2560, 1440   # YouTube's recommended size; the safe area for every device is the centre 1546x423
AMBER = (255, 176, 32)

# --- 1. plate: crop to 16:9, upscale ---
plate = Image.open(PLATE).convert("RGB")
pw, ph = plate.size
target_ar = W / H
crop_w = int(ph * target_ar)
if crop_w <= pw:
    x0 = (pw - crop_w) // 2
    plate = plate.crop((x0, 0, x0 + crop_w, ph))
else:
    crop_h = int(pw / target_ar)
    y0 = (ph - crop_h) // 2
    plate = plate.crop((0, y0, pw, y0 + crop_h))
plate = plate.resize((W, H), Image.LANCZOS)

# --- 2. darken the centre so the lockup reads ---
vig = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(vig)
d.ellipse([W * 0.14, H * 0.02, W * 0.86, H * 1.02], fill=165)
vig = vig.filter(ImageFilter.GaussianBlur(170))
plate = Image.composite(Image.new("RGB", (W, H), (6, 7, 9)), plate, vig)

# gentle overall grade toward the brand charcoal
grade = Image.new("RGB", (W, H), (13, 15, 18))
plate = Image.blend(plate, grade, 0.18)

canvas = plate.convert("RGBA")

# --- 3. mark ---
tmp_mark = "/tmp/mark_banner.png"
os.system(f"rsvg-convert -w 240 -h 240 -b none {MARK} -o {tmp_mark}")
mark = Image.open(tmp_mark).convert("RGBA")
mark = mark.crop(mark.getbbox())
mh = 150
mark = mark.resize((int(mark.width * mh / mark.height), mh), Image.LANCZOS)

# --- 4. type ---
SAFE_W, SAFE_H = 1546, 423
PAD = 190          # empty margin left and right inside the safe area, so phones never clip the S
ARCHIVO = "/usr/share/fonts/truetype/google-fonts/ofl/archivoblack/ArchivoBlack-Regular.ttf"
_probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
size = 200
while True:   # largest title that fits in the safe area minus the padding
    f_title = ImageFont.truetype(ARCHIVO, size)
    w = sum(_probe.textlength(c, font=f_title) for c in "SIPHON FILES") + 10 * 11
    if w <= SAFE_W - 2 * PAD:
        break
    size -= 2
f_tag = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/ofl/firasans/FiraSans-Bold.ttf", int(size * 0.25))
print("title size", size, "width", w)

def tracked(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x - tracking

def tracked_width(draw, text, font, tracking):
    return sum(draw.textlength(c, font=font) for c in text) + tracking * (len(text) - 1)

layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dr = ImageDraw.Draw(layer)

title = "SIPHON FILES"
tag = "WHERE THE MONEY WENT"
tr_title, tr_tag = 10, 13

tw = tracked_width(dr, title, f_title, tr_title)
gw = tracked_width(dr, tag, f_tag, tr_tag)

tb = f_title.getbbox(title)
gb = f_tag.getbbox(tag)
title_h = tb[3] - tb[1]
tag_h = gb[3] - gb[1]

GAP2, GAP3, RULE_H = 30, 26, 4
block_h = title_h + GAP2 + RULE_H + GAP3 + tag_h
top = (H - block_h) / 2

ty = top - tb[1]
tracked(dr, ((W - tw) / 2, ty), title, f_title, (255, 255, 255, 255), tr_title)

rule_y = top + title_h + GAP2
dr.rectangle([W / 2 - 190, rule_y, W / 2 + 190, rule_y + RULE_H], fill=AMBER + (255,))

gy = rule_y + RULE_H + GAP3 - gb[1]
tracked(dr, ((W - gw) / 2, gy), tag, f_tag, (198, 202, 210, 255), tr_tag)

print("block height", block_h, "safe band 423")

# soft shadow behind the whole lockup for legibility
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shadow.putalpha(layer.split()[-1].filter(ImageFilter.GaussianBlur(26)).point(lambda p: int(p * 0.85)))
canvas = Image.alpha_composite(canvas, shadow)
canvas = Image.alpha_composite(canvas, layer)

canvas.convert("RGB").save(OUT)
print("saved", OUT, canvas.size)

# safe-area proof
proof = canvas.convert("RGB").copy()
pd = ImageDraw.Draw(proof)
pd.rectangle([(W - SAFE_W) / 2, (H - SAFE_H) / 2, (W + SAFE_W) / 2, (H + SAFE_H) / 2], outline=(255, 0, 90), width=4)
proof.save("/home/claude/siphon-files/brand/banner_safearea_proof.png")
print("proof saved")
