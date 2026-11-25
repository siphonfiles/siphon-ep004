"""Ep. 003 thumbnail options: "OFFLINE BITCOIN. GUESSED." (CPU, from existing illustrations).

Title on YouTube: "Inside the $116M Coldcard Hack". The thumbnail completes it, never repeats it.
No Coldcard logo or real device design; the bitcoin symbol is drawn in code.
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "illustrations", "ep003", "img")
OUT = os.path.join(HERE, "ep003")
ANTON = "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf"
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
W, H = 1280, 720
WHITE = (244, 246, 248)
GREEN = (63, 230, 160)
ORANGE = (247, 147, 26)


def clean_green(im):
    """Remove stray green specks left by the Z-Image style suffix."""
    a = np.array(im).astype(np.int16)
    ex = a[..., 1] - np.maximum(a[..., 0], a[..., 2])
    m = ((ex > 8).astype(np.uint8) * 255)
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    out = cv2.inpaint(np.array(im), m, 12, cv2.INPAINT_TELEA)
    return Image.fromarray(out)


def base(name, crop=None, dark=0.0):
    im = Image.open(os.path.join(IMG, name + ".jpg")).convert("RGB")
    if crop:
        im = im.crop(crop)
    im = im.resize((W, H), Image.LANCZOS)
    im = clean_green(im)
    if dark:
        im = Image.blend(im, Image.new("RGB", im.size, (0, 0, 0)), dark)
    return im


def side_shade(im, side="left", amount=0.8, width=0.62):
    x = np.linspace(0, 1, W)
    if side == "right":
        x = x[::-1]
    g = np.clip(1 - x / width, 0, 1) ** 1.3 * amount
    a = np.array(im).astype(np.float32) * (1 - g[None, :, None])
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def coin(r):
    """A bitcoin coin with the ₿ sign, drawn at 4x then reduced (smooth edges)."""
    s = r * 8
    c = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    yy, xx = np.mgrid[0:s, 0:s] / s
    shade = 1.15 - 0.55 * np.hypot(xx - 0.35, yy - 0.3)
    body = np.dstack([np.full((s, s), ORANGE[0]), np.full((s, s), ORANGE[1]), np.full((s, s), ORANGE[2])]) * shade[..., None]
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
    c = Image.fromarray(np.dstack([body.clip(0, 255), np.full((s, s), 255)]).astype(np.uint8), "RGBA")
    c.putalpha(mask)
    d = ImageDraw.Draw(c)
    rim = s // 22
    d.ellipse((rim, rim, s - rim, s - rim), outline=(255, 200, 120, 255), width=s // 40)
    f = ImageFont.truetype(INTER_B, int(s * 0.66))
    d.text((s / 2 + s * 0.01, s / 2 + s * 0.02), "₿", font=f, fill=(255, 250, 240, 255), anchor="mm")
    return c.resize((r * 2, r * 2), Image.LANCZOS)


def glow_under(im, cx, cy, r, color=ORANGE, strength=0.55):
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse((cx - r * 2.2, cy - r * 2.2, cx + r * 2.2, cy + r * 2.2), fill=255)
    g = g.filter(ImageFilter.GaussianBlur(r * 0.9))
    a = np.array(im).astype(np.float32)
    k = np.array(g).astype(np.float32)[..., None] / 255 * strength
    a = a + k * np.array(color)[None, None, :] * 0.6
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def text_block(im, x, y, lines, anchor="la"):
    d = ImageDraw.Draw(im)
    for text, size, col, dy in lines:
        f = ImageFont.truetype(ANTON, size)
        # soft shadow
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x + 4, y + dy + 6), text, font=f, fill=(0, 0, 0, 190), anchor=anchor)
        im.paste(sh.filter(ImageFilter.GaussianBlur(8)), (0, 0), sh.filter(ImageFilter.GaussianBlur(8)))
        d = ImageDraw.Draw(im)
        d.text((x, y + dy), text, font=f, fill=col, anchor=anchor)
    return im


def option_a():
    """Device under a glass dome (sealed, offline) + coin + text left."""
    im = base("c33_device_under_glass", crop=(520, 150, 2048, 1010), dark=0.1)
    im = side_shade(im, "left", 0.9, 0.55)
    im = glow_under(im, 900, 250, 70)
    c = coin(70)
    im.paste(c, (900 - 70, 250 - 70), c)
    return text_block(im, 60, 80, [("OFFLINE", 145, WHITE, 0), ("BITCOIN.", 145, WHITE, 150),
                                    ("GUESSED.", 145, GREEN, 310)])


def option_b():
    """Empty vault at night + coin in the light beam + text right."""
    im = base("c01_vault_night", dark=0.05)
    im = side_shade(im, "right", 0.85, 0.6)
    im = glow_under(im, 360, 500, 85, strength=0.6)
    c = coin(85)
    im.paste(c, (360 - 85, 500 - 85), c)
    return text_block(im, W - 70, 60, [("OFFLINE", 150, WHITE, 0), ("BITCOIN.", 150, WHITE, 150),
                                         ("GUESSED.", 150, GREEN, 320)], anchor="ra")


def option_c():
    """Sealed box (never opened) + coin on the lid + text top."""
    im = base("c31_sealed_box_dust", crop=(0, 120, 2048, 1152), dark=0.15)
    a = np.array(im).astype(np.float32)
    g = np.clip(1 - np.linspace(0, 1, H) / 0.5, 0, 1)[:, None, None] * 0.8
    im = Image.fromarray((a * (1 - g)).clip(0, 255).astype(np.uint8))
    im = glow_under(im, 1090, 470, 80, strength=0.6)
    c = coin(80)
    im.paste(c, (1090 - 80, 470 - 80), c)
    d = text_block(im, W // 2, 40, [("OFFLINE BITCOIN.", 140, WHITE, 0)], anchor="ma")
    return text_block(d, W // 2, 40, [("GUESSED.", 140, GREEN, 150)], anchor="ma")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, fn in (("A_glass", option_a), ("B_vault", option_b), ("C_box", option_c)):
        fn().save(os.path.join(OUT, f"ep003_thumb_{k}_offline_bitcoin_guessed.jpg"), quality=92)
