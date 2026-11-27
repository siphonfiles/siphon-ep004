"""Put content on the blank screens of three ep. 004 illustrations (CPU only; owner rule: no empty screens).

b6_setup_screen   small device on the desk: one recovery word being shown ("Word 7 of 24").
b7_secret_display the device alone: a numbered word list (invented words, labelled ILLUSTRATIVE).
h1_owner_kitchen  laptop behind the held device: a wallet app asking to connect the device.

Flat content -> perspective warp onto the screen quad -> feathered mask -> blended into the photo.
The untouched originals are kept next to the result as <name>_blank.jpg (made on the first run).
"""
import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
IMG = os.path.join(ROOT, "illustrations", "ep004", "img")
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"
MONO = os.path.join(ROOT, "fonts", "NotoSansMono-%s.ttf")
WORDS = ["harbour", "violet", "lantern", "copper", "meadow", "signal", "orbit", "candle", "river", "marble",
         "walnut", "silver"]


def F(path, size):
    return ImageFont.truetype(path, size)


def one_word(W=900, H=700):
    im = Image.new("RGB", (W, H), (96, 226, 196))
    d = ImageDraw.Draw(im)
    dark = (10, 46, 44)
    d.text((W / 2, 150), "WORD 7 OF 24", font=F(MONO % "Bold", 62), fill=(24, 92, 84), anchor="mm")
    d.text((W / 2, 360), "orbit", font=F(SANS % "-Bold", 210), fill=dark, anchor="mm")
    for i in range(24):
        x = 96 + i * 30
        d.rounded_rectangle((x, 560, x + 20, 580), 5, fill=dark if i < 7 else (60, 170, 150))
    return im


def word_list(W=1300, H=1000):
    g = np.linspace(0, 1, H)[:, None] + np.zeros((1, W))
    im = Image.fromarray(np.dstack([40 + 22 * g, 26 + 14 * g, 78 + 34 * g]).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.text((80, 96), "RECOVERY PHRASE", font=F(MONO % "Bold", 58), fill=(214, 200, 255), anchor="lm")
    d.text((W - 80, 96), "1 - 12", font=F(MONO % "Regular", 46), fill=(160, 140, 220), anchor="rm")
    d.line((80, 160, W - 80, 160), fill=(140, 112, 230), width=4)
    for i, w in enumerate(WORDS):
        x = 80 + (i // 6) * 620
        y = 250 + (i % 6) * 112
        d.text((x, y), "%2d" % (i + 1), font=F(MONO % "Regular", 50), fill=(150, 128, 220), anchor="lm")
        d.text((x + 110, y), w, font=F(SANS % "-Bold", 70), fill=(244, 240, 255), anchor="lm")
    d.text((W / 2, H - 50), "ILLUSTRATIVE · NOT A REAL PHRASE", font=F(MONO % "Regular", 34),
           fill=(170, 150, 230), anchor="mm")
    return im


def wallet_app(W=1500, H=1000):
    im = Image.new("RGB", (W, H), (20, 18, 30))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 70), fill=(12, 11, 20))
    for i, c in enumerate([(200, 84, 96), (190, 160, 90), (110, 150, 120)]):
        d.ellipse((28 + i * 44, 22, 54 + i * 44, 48), fill=c)
    d.text((W / 2, 36), "Wallet", font=F(SANS % "", 30), fill=(150, 146, 170), anchor="mm")
    d.rectangle((0, 70, 300, H), fill=(15, 14, 24))
    for i, t in enumerate(["Portfolio", "Accounts", "Send", "Receive", "Settings"]):
        d.text((50, 150 + i * 80), t, font=F(SANS % "", 34), fill=(120, 116, 146) if i else (200, 190, 255),
               anchor="lm")
    cx = 300 + (W - 300) / 2 + 160
    d.rounded_rectangle((cx - 90, 250, cx + 90, 560), 26, outline=(157, 123, 255), width=8)
    d.rounded_rectangle((cx - 58, 290, cx + 58, 400), 8, outline=(157, 123, 255), width=5)
    d.ellipse((cx - 22, 462, cx + 22, 506), outline=(157, 123, 255), width=5)
    d.text((cx, 660), "Connect your device", font=F(SANS % "-Bold", 62), fill=(236, 232, 250), anchor="mm")
    d.text((cx, 740), "Unlock it and open the app", font=F(SANS % "", 38), fill=(150, 146, 176), anchor="mm")
    d.rounded_rectangle((cx - 170, 810, cx + 170, 890), 40, fill=(157, 123, 255))
    d.text((cx, 850), "Continue", font=F(SANS % "-Bold", 38), fill=(20, 16, 34), anchor="mm")
    return im


def put(name, content, quad, alpha=0.94, feather=5, blur=1.2, occl=None, gain=1.0):
    """quad: TL, TR, BR, BL in full-image pixels. occl: polygon that stays in front of the screen."""
    path = os.path.join(IMG, name + ".jpg")
    blank = os.path.join(IMG, name + "_blank.jpg")
    if not os.path.exists(blank):
        shutil.copy(path, blank)
    base = cv2.imread(blank).astype(np.float32)
    h, w = base.shape[:2]
    src = cv2.cvtColor(np.asarray(content), cv2.COLOR_RGB2BGR)
    sh, sw = src.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]]), np.float32(quad))
    warped = cv2.warpPerspective(src, M, (w, h), flags=cv2.INTER_AREA).astype(np.float32) * gain
    warped = cv2.GaussianBlur(warped, (0, 0), blur)
    mask = np.zeros((h, w), np.float32)
    cv2.fillConvexPoly(mask, np.int32(quad), 1.0)
    mask = cv2.erode(mask, np.ones((feather, feather), np.uint8))
    if occl is not None:
        cv2.fillPoly(mask, [np.int32(occl)], 0.0)
    mask = cv2.GaussianBlur(mask, (0, 0), feather * 0.6)[..., None] * alpha
    out = base * (1 - mask) + warped * mask
    cv2.imwrite(path, out.clip(0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])
    return out


if __name__ == "__main__":
    put("b6_setup_screen", one_word(), [(512, 638), (717, 615), (782, 764), (578, 797)], feather=4, blur=0.8)
    put("b7_secret_display", word_list(), [(680, 372), (1100, 385), (1168, 705), (742, 735)], blur=1.0, gain=0.92)
    occ = [(795, 800), (900, 585), (940, 570), (945, 540), (1002, 532), (1020, 585), (1070, 612), (1072, 650),
           (1055, 770), (1050, 800), (1050, 900), (795, 900)]
    put("h1_owner_kitchen", wallet_app(), [(908, 372), (1488, 388), (1435, 790), (850, 770)], alpha=0.9,
        feather=7, blur=1.4, occl=occ, gain=0.8)
