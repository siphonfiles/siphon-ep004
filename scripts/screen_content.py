"""Put content on blank screens in two ep. 003 illustrations (CPU only).

c40_phone_nightstand: landscape night clock at 9:51 PM, Wednesday 29 July, no notifications.
c37_empty_desk_glow:  code editor where a scan has just flagged one line (illustrative code).

The content is drawn flat, warped onto the screen with a perspective transform,
masked by the original bright screen area (keeps the notch and rounded corners),
then softened and lit so it sits in the photo. Originals are read from git HEAD~
style backups: <name>_blank.jpg (created on first run).
"""
import os, shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

IMG = os.path.join(os.path.dirname(__file__), "..", "illustrations", "ep003", "img")
INTER = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
MONO = os.path.join(os.path.dirname(__file__), "..", "fonts", "NotoSansMono-%s.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def lock_screen(W=1950, H=900):
    """Landscape night clock, as a phone shows while lying on a nightstand."""
    g = np.linspace(0, 1, H)[:, None]
    x = np.linspace(-1, 1, W)[None, :]
    glow = np.exp(-((x + 0.35) ** 2) * 2.5 - ((g - 0.45) ** 2) * 6)
    r = 8 + 10 * glow + 0 * x
    gg = 12 + 20 * glow + 0 * x
    b = 26 + 55 * glow + 8 * (1 - g) + 0 * x
    im = Image.fromarray(np.dstack([r, gg, b]).clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    white = (236, 240, 246)
    cx = 640
    d.text((cx, 400), "9:51", font=F(INTER % "SemiBold", 330), fill=white, anchor="mm")
    d.text((cx, 640), "Wednesday 29 July", font=F(INTER % "SemiBold", 66), fill=(200, 208, 222), anchor="mm")
    px = 1450
    d.rounded_rectangle((px - 30, 300, px + 30, 350), 9, fill=(170, 180, 196))
    d.arc((px - 21, 262, px + 21, 320), 180, 360, fill=(170, 180, 196), width=9)
    d.text((px, 440), "No notifications", font=F(INTER % "Medium", 56), fill=(150, 160, 178), anchor="mm")
    return im


def editor(W=1600, H=1200):
    bg = (12, 22, 20)
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    mono = F(MONO % "Regular", 30)
    monob = F(MONO % "Bold", 30)
    small = F(INTER % "Medium", 26)
    # title bar + tabs
    d.rectangle((0, 0, W, 56), fill=(8, 15, 14))
    for i, c in enumerate([(220, 90, 80), (225, 180, 70), (80, 190, 110)]):
        d.ellipse((24 + i * 38, 18, 46 + i * 38, 40), fill=c)
    d.rectangle((150, 8, 470, 56), fill=bg)
    d.text((176, 32), "entropy.c", font=small, fill=(200, 220, 212), anchor="lm")
    d.text((520, 32), "seed.c", font=small, fill=(110, 130, 124), anchor="lm")
    # sidebar
    d.rectangle((0, 56, 250, H), fill=(9, 17, 16))
    for i, n in enumerate(["firmware/", "  boot/", "  crypto/", "    entropy.c", "    seed.c", "  ui/", "  usb/"]):
        col = (63, 230, 160) if "entropy" in n else (120, 140, 134)
        d.text((24, 96 + i * 44), n, font=small, fill=col, anchor="lm")
    code = [
        ("// collect randomness for a new seed", "c"),
        ("static void fill_seed(uint8_t *out, size_t n)", "k"),
        ("{", "p"),
        ("    uint8_t pool[64];", "p"),
        ("    mix_sources(pool, sizeof(pool));", "p"),
        ("", "p"),
        ("    if (!source_ready(SRC_TRNG)) {", "k"),
        ("        use_fallback(pool, sizeof(pool));", "hit"),
        ("    }", "p"),
        ("", "p"),
        ("    hash_into(out, n, pool, sizeof(pool));", "p"),
        ("    wipe(pool, sizeof(pool));", "p"),
        ("}", "p"),
    ]
    cols = {"c": (90, 120, 110), "k": (120, 200, 240), "p": (205, 222, 214), "hit": (255, 255, 255)}
    y0, lh, x0 = 100, 54, 330
    for i, (t, k) in enumerate(code):
        y = y0 + i * lh
        if k == "hit":
            d.rectangle((260, y - 6, W, y + lh - 10), fill=(120, 30, 34))
            d.rectangle((260, y - 6, 268, y + lh - 10), fill=(255, 77, 94))
        d.text((300, y + 18), str(40 + i), font=mono, fill=(255, 200, 204) if k == "hit" else (70, 95, 88), anchor="rm")
        d.text((x0, y + 18), t, font=monob if k == "hit" else mono, fill=cols[k], anchor="lm")
    # finding pop-up next to the flagged line
    py = y0 + 7 * lh + 60
    d.rounded_rectangle((760, py, 1560, py + 150), 14, fill=(20, 40, 34), outline=(63, 230, 160), width=3)
    d.text((790, py + 42), "1 finding", font=F(INTER % "Bold", 34), fill=(63, 230, 160), anchor="lm")
    d.text((790, py + 100), "Predictable randomness when the source is off",
           font=F(INTER % "Medium", 28), fill=(205, 222, 214), anchor="lm")
    # bottom terminal
    d.rectangle((250, H - 260, W, H), fill=(6, 12, 11))
    d.line((250, H - 260, W, H - 260), fill=(30, 50, 44), width=2)
    for i, (t, c) in enumerate([("$ scan ./firmware --deep", (205, 222, 214)),
                                ("  2,418 functions checked", (110, 140, 130)),
                                ("  ! entropy.c:47  weak seed path", (255, 120, 128)),
                                ("$ _", (63, 230, 160))]):
        d.text((280, H - 225 + i * 52), t, font=mono, fill=c, anchor="lm")
    d.text((W - 30, H - 225), "ILLUSTRATIVE", font=F(INTER % "SemiBold", 24), fill=(90, 120, 110), anchor="rm")
    return im


def apply(name, content, dst, thr, gain, blur, glow, clean=()):
    path = os.path.join(IMG, name + ".jpg")
    blank = os.path.join(IMG, name + "_blank.jpg")
    if not os.path.exists(blank):
        shutil.copy(path, blank)
    im = cv2.imread(blank).astype(np.float32)
    H, W = im.shape[:2]
    c = cv2.cvtColor(np.array(content), cv2.COLOR_RGB2BGR).astype(np.float32)
    h, w = c.shape[:2]
    dst = np.float32(dst)
    dst = dst.mean(0) + (dst - dst.mean(0)) * 1.04
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), dst)
    warp = cv2.warpPerspective(c, M, (W, H), flags=cv2.INTER_AREA)
    warp = cv2.GaussianBlur(warp, (0, 0), blur) * gain
    g = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    m = (g > thr).astype(np.uint8) * 255
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
    m = ((lab == k) * 255).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    m = cv2.dilate(m, np.ones((7, 7), np.uint8))
    a = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 1.2)[..., None]
    out = im * (1 - a) + warp * a
    # soft light spill from the new screen, replacing the old flat glow a little
    spill = cv2.GaussianBlur(warp * a, (0, 0), glow)
    out = out + spill * 0.35
    for (sx, sy, sr) in clean:
        mm = np.zeros((H, W), np.uint8); cv2.circle(mm, (sx, sy), sr, 255, -1)
        out = cv2.inpaint(out.clip(0, 255).astype(np.uint8), mm, 12, cv2.INPAINT_TELEA).astype(np.float32)
    # grain like the rest of the photo
    out += np.random.default_rng(3).normal(0, 2.2, out.shape)
    cv2.imwrite(path, out.clip(0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])


if __name__ == "__main__":
    # phone: top of the phone (notch) points right; far long side = left of the screen
    apply("c40_phone_nightstand", lock_screen(),
          [[751, 813], [1373, 702], [1662, 762], [1013, 888]], thr=100, gain=1.0, blur=0.8, glow=40, clean=[(1410, 618, 30)])
    apply("c37_empty_desk_glow", editor(),
          [[920, 318], [1394, 301], [1382, 672], [905, 647]], thr=100, gain=1.0, blur=0.7, glow=60)
