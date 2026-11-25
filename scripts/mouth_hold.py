"""Keep Thomas's mouth closed in the pauses between two lines of a re-synced (LatentSync) clip.

LatentSync redraws the mouth from the audio, but in the silences between two lines it keeps the lips
moving a little, as if Thomas were mouthing words (seen by proprietarul at 1:50, 2:08, 2:46). In each such
pause we take the most closed mouth of the pause and hold it: the patch follows the head (translation
found by phase correlation on the nose/cheek area), is blended with a soft elliptical mask, and fades
in/out over a few frames, so eyes, head and body stay alive and only the lips stop.

Works on the 1872x1080 PNG frames written by thomas_frames.py (frame i <-> clip time i/30 s).
"""
import glob, os
import numpy as np
import cv2

FPS = 30
MOUTH = (965, 352)          # mouth centre in the 1872x1080 clip frame (same framing in every resync clip)
RX, RY = 66, 44
RY_UP = 24             # patch half-size (lips + corners + upper chin)
TRACK = (880, 240, 1050, 330)   # nose / cheeks: moves with the head, not with the jaw
RAMP = 4                    # frames of fade in / out


SEARCH = 40


def _shift(ref_img, img):
    """Where the nose/cheek area of ref_img is in img (template match, sub-pixel peak)."""
    x0, y0, x1, y1 = TRACK
    t = cv2.cvtColor(ref_img[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY)
    s = cv2.cvtColor(img[y0 - SEARCH:y1 + SEARCH, x0 - SEARCH:x1 + SEARCH], cv2.COLOR_RGB2GRAY)
    r = cv2.matchTemplate(s, t, cv2.TM_CCOEFF_NORMED)
    _, _, _, (px, py) = cv2.minMaxLoc(r)
    def sub(a, b, c):
        d = a - 2 * b + c
        return 0.0 if abs(d) < 1e-9 else 0.5 * (a - c) / d
    fx = sub(r[py, px - 1], r[py, px], r[py, px + 1]) if 0 < px < r.shape[1] - 1 else 0.0
    fy = sub(r[py - 1, px], r[py, px], r[py + 1, px]) if 0 < py < r.shape[0] - 1 else 0.0
    return px + fx - SEARCH, py + fy - SEARCH


def _openness(img, dx, dy):
    cx, cy = int(MOUTH[0] + dx), int(MOUTH[1] + dy)
    m = cv2.cvtColor(img[cy - 14:cy + 16, cx - 40:cx + 40], cv2.COLOR_RGB2GRAY).astype(np.float32)
    skin = np.median(cv2.cvtColor(img[cy - 60:cy - 30, cx - 50:cx + 50], cv2.COLOR_RGB2GRAY))
    return float(np.mean(m < 0.55 * skin))      # dark lip gap / inside of the mouth


# Frame (index i <-> f{i+1}.png) with the best closed mouth in each pause, picked by eye (22 nov 2026):
# the automatic pick could choose a pouting lower lip that read as a tongue (Proprietarul, 2:09).
REF = {"thomas_resync_a78": [105], "thomas_resync_b34": [52], "thomas_resync_b78": [258], "thomas_resync_g78": [208]}


def hold(frames_dir, pauses, refs=None):
    files = sorted(glob.glob(os.path.join(frames_dir, "f*.png")))
    rd = lambda i: cv2.cvtColor(cv2.imread(files[i]), cv2.COLOR_BGR2RGB)
    h, w = RY * 2 + 1, RX * 2 + 1
    yy, xx = np.mgrid[-RY:RY + 1, -RX:RX + 1]
    for k, (p0, p1) in enumerate(pauses):
        i0, i1 = int(round(p0 * FPS)) + 2, min(int(round(p1 * FPS)) - 2, len(files) - 1)
        if i1 - i0 < 2 * RAMP:
            continue
        base = rd(i0)
        cand = []
        for i in range(i0, i1 + 1):
            im = rd(i)
            dx, dy = _shift(base, im)
            cand.append((_openness(im, dx, dy), i, im, dx, dy))
        if refs and k < len(refs) and i0 <= refs[k] <= i1:
            _, ri, ref, _, _ = next(c for c in cand if c[1] == refs[k])
        else:
            _, ri, ref, _, _ = min(cand, key=lambda c: c[0])
        # where the lips and the nostrils are in this clip (faces sit a little differently per take)
        g = cv2.cvtColor(ref, cv2.COLOR_RGB2GRAY).astype(np.float32)
        lip = 310 + int(np.argmin(g[310:390, MOUTH[0] - 40:MOUTH[0] + 40].mean(1)))
        reg = g[lip - 75:lip - 12, MOUTH[0] - 45:MOUTH[0] + 45]
        nose = lip - 75 + int(np.unravel_index(np.argmin(reg), reg.shape)[0])
        ry_up = max(12, lip - nose - 14)
        ry = np.where(yy < 0, ry_up, RY)
        mask = np.clip((1.0 - np.sqrt((xx / RX) ** 2 + (yy / ry) ** 2)) / 0.3, 0, 1)
        mask = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 3)[..., None]
        rx, ry0 = float(MOUTH[0]), float(lip)
        cand = [(o, i, im, *_shift(ref, im)) for o, i, im, _, _ in cand]
        # region around the mouth in the chosen frame (the patch source)
        BW, BH = RX + 40, RY + 40
        rbox = cv2.getRectSubPix(ref, (2 * BW + 1, 2 * BH + 1), (rx, ry0))
        rg = cv2.cvtColor(rbox, cv2.COLOR_RGB2GRAY).astype(np.float32)
        for o, i, im, _, _ in cand:
            a = min(1.0, min(i - i0, i1 - i) / RAMP)
            if a <= 0:
                continue
            _, _, _, dx, dy = next(c for c in cand if c[1] == i)
            cx, cy = rx + dx, ry0 + dy
            # fine alignment on the mouth area itself (rotation + shift), so the held lips sit exactly
            # where the current lips are: no double lip line while the two are blended
            cur = cv2.getRectSubPix(im, (2 * BW + 1, 2 * BH + 1), (cx, cy))
            cg = cv2.cvtColor(cur, cv2.COLOR_RGB2GRAY).astype(np.float32)
            W = np.eye(2, 3, dtype=np.float32)
            try:
                _, W = cv2.findTransformECC(cg, rg, W, cv2.MOTION_EUCLIDEAN,
                                            (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5), None, 5)
            except cv2.error:
                pass
            warped = cv2.warpAffine(rbox, W, (2 * BW + 1, 2 * BH + 1),
                                    flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
            p = warped[BH - RY:BH + RY + 1, BW - RX:BW + RX + 1].astype(np.float32)
            x0, y0 = int(round(cx)) - RX, int(round(cy)) - RY
            M = np.float32([[1, 0, cx - round(cx)], [0, 1, cy - round(cy)]])
            p = cv2.warpAffine(p, M, (w, h), borderMode=cv2.BORDER_REFLECT)
            roi = im[y0:y0 + h, x0:x0 + w].astype(np.float32)
            m = mask * a
            im[y0:y0 + h, x0:x0 + w] = np.clip(roi * (1 - m) + p * m, 0, 255).astype(np.uint8)
            cv2.imwrite(files[i], cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
        print(f"  mouth held {p0:.2f}-{p1:.2f}s ({i1 - i0 + 1} frames, ref frame {ri}, lips y {lip}, nostril y {nose})", flush=True)


def resync_pauses(tl, plan_clip_t0):
    """{clip: [(p0, p1) in clip seconds]} — silences > 0.3 s between two lines inside a re-synced clip."""
    v = sorted((e["t"], e["t"] + e["dur"]) for e in tl["events"] if e["kind"] == "voice")
    out = {}
    for n, (a, b) in plan_clip_t0.items():
        ins = [x for x in v if x[1] > a and x[0] < b]
        out[n] = [(ins[k][1] - a, ins[k + 1][0] - a) for k in range(len(ins) - 1) if ins[k + 1][0] - ins[k][1] > 0.3]
    return out
