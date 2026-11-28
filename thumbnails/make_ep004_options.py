"""Ep. 004 thumbnail options (CPU, from existing illustrations). The text completes the title, never repeats it.
No Ledger logo or real device design. Font: Anton (OFL), path in $ANTON (downloaded by thumbs-ep004.yml).
Usage: ANTON=/path/Anton-Regular.ttf python3 thumbnails/make_ep004_options.py
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "illustrations", "ep004", "img")
OUT = os.path.join(HERE, "ep004")
ANTON = os.environ.get("ANTON", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
W, H = 1280, 720
WHITE = (246, 244, 250)
UV = (176, 148, 255)
RED = (255, 79, 94)


def base(name, crop=None, gain=1.0, sat=1.0):
    im = Image.open(os.path.join(IMG, name + ".jpg")).convert("RGB")
    if crop:
        im = im.crop(crop)
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    g = a.mean(2, keepdims=True)
    a = (g + (a - g) * sat) * gain
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def side_shade(im, side="left", amount=0.8, width=0.62):
    x = np.linspace(0, 1, W)
    if side == "right":
        x = x[::-1]
    g = np.clip(1 - x / width, 0, 1) ** 1.3 * amount
    a = np.asarray(im).astype(np.float32) * (1 - g[None, :, None])
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def text_block(im, x, y, lines, anchor="la"):
    for text, size, col, dy in lines:
        f = ImageFont.truetype(ANTON, size)
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x + 4, y + dy + 6), text, font=f, fill=(0, 0, 0, 210), anchor=anchor)
        sh = sh.filter(ImageFilter.GaussianBlur(9))
        im.paste(sh, (0, 0), sh)
        ImageDraw.Draw(im).text((x, y + dy), text, font=f, fill=col, anchor=anchor)
    return im


def violet_screens(im):
    """Shift the greenish device screens of the Z-Image output to the episode's ultraviolet."""
    hsv = np.asarray(im.convert("HSV")).astype(np.float32)
    h = hsv[..., 0] * 360 / 255
    m = np.clip(1 - np.abs(h - 150) / 45, 0, 1) * np.clip((hsv[..., 1] - 40) / 60, 0, 1)
    hsv[..., 0] = (h * (1 - m) + 262 * m) * 255 / 360
    return Image.fromarray(hsv.clip(0, 255).astype(np.uint8), "HSV").convert("RGB")


def inset(name, x, y, scale=0.8, gain=1.5, sat=1.1, shade=0.6):
    """The picture set smaller and to the right on a blurred copy of itself: room for the words on the left."""
    full = violet_screens(base(name, gain=gain, sat=sat))
    bg = Image.blend(full.filter(ImageFilter.GaussianBlur(45)), Image.new("RGB", (W, H), (10, 6, 20)), 0.5)
    w, h = int(W * scale), int(H * scale)
    small = full.resize((w, h), Image.LANCZOS)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rectangle((70, 60, w - 70, h - 60), fill=255)
    bg.paste(small, (x, y), m.filter(ImageFilter.GaussianBlur(50)))
    return side_shade(bg, "left", shade, 0.5)


def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    im.save(os.path.join(OUT, name), quality=93)
    print(name)


def main():
    # A: the sealed box (first image of the episode), set smaller on the left so the words stay clear of it
    full = base("t1_sealed_box_v2", gain=1.55, sat=1.15)
    bg = full.filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (10, 6, 20)), 0.45)
    small = full.resize((1000, 562), Image.LANCZOS)
    m = Image.new("L", (1000, 562), 0)
    ImageDraw.Draw(m).rectangle((60, 50, 940, 512), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(45))
    bg.paste(small, (-130, 110), m)
    im = side_shade(bg, "right", 0.55, 0.5)
    text_block(im, W - 50, 120, [("SEALED.", 190, WHITE, 0), ("ALREADY", 150, RED, 215), ("ROBBED.", 150, RED, 375)], "ra")
    save(im, "ep004_thumb_A_sealed_already_robbed.jpg")
    # B: the teardown, the number from the first 30 seconds
    im = base("b9_teardown", crop=(0, 190, 1400, 978), gain=1.45, sat=1.1)
    im = side_shade(im, "left", 0.85, 0.55)
    text_block(im, 60, 120, [("$102M", 215, WHITE, 0), ("THE CHIP", 110, UV, 255), ("WAS FINE.", 110, UV, 375)])
    save(im, "ep004_thumb_B_102m_chip_was_fine.jpg")
    # C: the X-ray
    im = base("f8_xray", gain=1.1, sat=1.15)
    im = side_shade(im, "left", 0.9, 0.62)
    text_block(im, 60, 170, [("IT READ", 190, WHITE, 0), ("THE SCREEN.", 128, UV, 222)])
    save(im, "ep004_thumb_C_it_read_the_screen.jpg")
    # D, E: a slim generic hardware wallet (no logo, not a copy of a real product) + the word LEDGER as plain text
    im = inset("th_slim_wallet_box", 330, 90)
    text_block(im, 50, 40, [("LEDGER", 215, WHITE, 0), ("SEALED.", 125, UV, 250), ("ALREADY", 125, RED, 385),
                            ("ROBBED.", 125, RED, 520)])
    save(im, "ep004_thumb_D_ledger_sealed_robbed.jpg")
    im = inset("th_slim_wallet_open", 310, 80)
    text_block(im, 50, 90, [("LEDGER", 215, WHITE, 0), ("THE CHIP", 135, UV, 260), ("WAS FINE.", 135, UV, 405)])
    save(im, "ep004_thumb_E_ledger_chip_was_fine.jpg")


if __name__ == "__main__":
    main()
