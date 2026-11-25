"""Reusable scene templates for Siphon Files (dark editorial style, amber accents)."""
import math
import random

import cairo

from engine import (W, H, BG, AMBER, INK, GREY, DIM, RED, GREEN, HEAD, MONO, SERIF,
                    clamp, ease_out, ease_in_out, prog, fade_io, rgba, text, text_width,
                    wrap, rrect, source_tag, siphon_mark, font)


def black(ctx, t, d):
    """Hard cut to black (used on teaser cuts)."""
    rgba(ctx, (0, 0, 0))
    ctx.paint()


def kinetic(ctx, t, d, line, source=None, cut=True, highlight=()):
    """Spoken line appears word by word (paced on the line duration), editorial type.
    cut=True: no fade-out, the scene ends on a hard cut (teaser fragments)."""
    words = line.split()
    chars = [len(w) + 1 for w in words]
    total = sum(chars)
    speak = d * 0.95
    font(ctx, HEAD, 78)
    lines = wrap(ctx, line, W - 360, HEAD, 78)
    # index words to lines
    y0 = H / 2 - (len(lines) - 1) * 52
    k = 0
    acc = 0
    a_scene = prog(t, 0, 0.2) if cut else fade_io(t, d)
    # thin amber rule that grows with the line
    rgba(ctx, AMBER, 0.9 * a_scene)
    ctx.rectangle(180, y0 - 110, 120 * ease_out(prog(t, 0, 0.6)), 4)
    ctx.fill()
    for li, ln in enumerate(lines):
        x = 180
        for w in ln.split():
            appear = acc / total * speak
            acc += chars[k]
            k += 1
            p = ease_out(prog(t, appear, 0.25))
            col = AMBER if w.strip(".,—-?!") in highlight else INK
            ww = text(ctx, w, x, y0 + li * 104 + (1 - p) * 18, col, p * a_scene, size=78)
            x += ww + text_width(ctx, " ", HEAD, 78)
    if source:
        source_tag(ctx, source, a_scene)


def quote_card(ctx, t, d, quote, who, source):
    a = fade_io(t, d, 0.25, 0.25)
    p = ease_out(prog(t, 0, 0.8))
    rgba(ctx, AMBER, a)
    text(ctx, "“", 200, 430, AMBER, a, face=SERIF, size=260, bold=True)
    lines = wrap(ctx, quote, W - 520, SERIF, 92, True)
    for i, ln in enumerate(lines):
        text(ctx, ln, 330, 500 + i * 118 + (1 - p) * 20, INK, a * p, face=SERIF, size=92, italic=True)
    yb = 500 + len(lines) * 118 + 40
    rgba(ctx, AMBER, a)
    ctx.rectangle(330, yb - 30, 80 * p, 3)
    ctx.fill()
    text(ctx, who, 330, yb + 20, GREY, a * prog(t, 0.3, 0.5), face=MONO, size=32, bold=False)
    source_tag(ctx, source, a)


def title_card(ctx, t, d, title, kicker="SIPHON FILES"):
    a = ease_in_out(prog(t, 0, 0.9)) * (1 - prog(t, d - 0.6, 0.6))   # slow fade in from black
    drop = ease_out(prog(t, 0.3, 0.9))
    siphon_mark(ctx, W / 2, 360, 0.30, a, draw_drop=drop)
    text(ctx, kicker, W / 2, 610, GREY, a * prog(t, 0.6, 0.5), align="center", face=MONO,
         size=30, bold=False, tracking=10)
    p = ease_out(prog(t, 1.1, 1.0))
    ctx.save()
    ctx.rectangle(0, 640, W * p + 1, 140)
    ctx.clip()
    text(ctx, title, W / 2, 735, INK, a, align="center", size=96)
    ctx.restore()
    rgba(ctx, AMBER, a)
    ctx.rectangle(W / 2 - 250 * p, 775, 500 * p, 4)
    ctx.fill()


def presenter(ctx, t, d, image_path, name="THOMAS ARCHER", role="AI NARRATOR",
              lower_third_at=0.0, note=None, clip=None, zoom=None):
    """Thomas on camera.
    clip: dict(frames=dir of PNGs at FPS, start=s into the scene, scale, ox, oy) -> the LongCat video,
          laid exactly over the reference still (same framing), camera locked off.
    zoom: (z, cx, cy) static close-up of the still with a slow push-in (a second 'camera angle')."""
    img = presenter.cache.get(image_path)
    if img is None:
        img = cairo.ImageSurface.create_from_png(image_path)
        presenter.cache[image_path] = img
    fa = 1.0 if clip is not None else (1 - prog(t, d - 0.3, 0.3)) if zoom is not None else fade_io(t, d, 0.4, 0.3)
    cam = clip is not None and zoom is not None   # close-up of the moving clip: a second camera angle
    if cam:
        z, cx, cy = zoom
        z *= 1.0 + 0.025 * ease_in_out(t / max(d, 0.01))
        ctx.save()
        ctx.translate(W / 2, H / 2)
        ctx.scale(z, z)
        ctx.translate(-cx, -cy)
    ctx.save()
    if clip is not None:
        sx = W / img.get_width()
        ctx.scale(sx, sx)
        ctx.set_source_surface(img, 0, 0)
    elif zoom is not None:
        z, cx, cy = zoom
        z *= 1.0 + 0.03 * ease_in_out(t / max(d, 0.01))
        sx = W / img.get_width() * z
        ctx.translate(W / 2, H / 2)
        ctx.scale(sx, sx)
        ctx.translate(-cx * img.get_width() / W, -cy * img.get_height() / H)
        ctx.set_source_surface(img, 0, 0)
    else:
        sc = 1.0 + 0.04 * ease_in_out(t / max(d, 0.01))
        sx = W / img.get_width() * sc
        ctx.translate(W / 2, H / 2)
        ctx.scale(sx, sx)
        ctx.translate(-img.get_width() / 2, -img.get_height() / 2)
        ctx.set_source_surface(img, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_BEST)
    ctx.paint_with_alpha(fa)
    ctx.restore()
    if clip is not None:
        import os
        k = int(round((t - clip["start"]) * 30))
        files = presenter.lists.get(clip["frames"])
        if files is None:
            files = sorted(f for f in os.listdir(clip["frames"]) if f.endswith(".png"))
            presenter.lists[clip["frames"]] = files
        if len(files) <= k < len(files) + 4:   # rounding at the very end of a window: hold the last frame
            k = len(files) - 1
        if 0 <= k < len(files):
            fr = cairo.ImageSurface.create_from_png(os.path.join(clip["frames"], files[k]))
            ctx.save()
            ctx.translate(clip["ox"], clip["oy"])
            ctx.scale(clip["scale"], clip["scale"])
            ctx.set_source_surface(fr, 0, 0)
            ctx.get_source().set_filter(cairo.FILTER_BEST)
            ctx.paint()
            ctx.restore()
    if cam:
        ctx.restore()
    if clip is not None:
        a = 1 - prog(t, d - 0.3, 0.3) if clip.get("fade_out") else 1.0
        if a < 1:
            rgba(ctx, BG, 1 - a)
            ctx.paint()
    lt = prog(t, lower_third_at, 0.5) * (1 - prog(t, lower_third_at + 5.5, 0.5))
    if lt > 0:
        p = ease_out(lt)
        rgba(ctx, BG, 0.82 * lt)
        rrect(ctx, 110, H - 230, 560 * p, 120, 6)
        ctx.fill()
        rgba(ctx, AMBER, lt)
        ctx.rectangle(110, H - 230, 6, 120)
        ctx.fill()
        text(ctx, name, 145, H - 168, INK, lt, size=46)
        text(ctx, role, 145, H - 128, AMBER, lt, face=MONO, size=26, bold=False, tracking=4)
    if note:
        text(ctx, note, W - 60, 60, GREY, 0.6, align="right", face=MONO, size=20, bold=False)


presenter.lists = {}
presenter.cache = {}


def countdown(ctx, t, d, label, sub=None):
    """T-MINUS card: big mono type with a flicker, like a case-file clock."""
    a = fade_io(t, d, 0.15, 0.25)
    flick = 1.0 if t > 0.35 else (0.35 if int(t * 30) % 3 == 0 else 1.0)
    text(ctx, "T-MINUS", W / 2, 430, AMBER, a * flick, align="center", face=MONO, size=44,
         bold=False, tracking=14)
    text(ctx, label, W / 2, 600, INK, a * flick, align="center", face=MONO, size=150, bold=True)
    if sub:
        text(ctx, sub, W / 2, 690, GREY, a * prog(t, 0.4, 0.4), align="center", face=MONO,
             size=30, bold=False, tracking=6)
    # ticking seconds bar
    rgba(ctx, AMBER, 0.5 * a)
    for i in range(12):
        on = i <= int(t * 6) % 12
        ctx.rectangle(W / 2 - 300 + i * 50, 760, 30, 6 if on else 2)
        ctx.fill()


def location_card(ctx, t, d, when, where, source=None):
    """Establishing card: abstract crowd of conference lanyard badges drifting in parallax."""
    a = fade_io(t, d)
    rnd = random.Random(3)
    for layer, (sc, alpha, speed) in enumerate(((0.6, 0.18, 14), (0.85, 0.28, 24), (1.15, 0.45, 40))):
        for i in range(16):
            x = (rnd.uniform(-200, W + 200) - t * speed) % (W + 400) - 200
            y = rnd.uniform(140, H - 140)
            w, h = 110 * sc, 150 * sc
            rgba(ctx, DIM, a * alpha * 2)
            rrect(ctx, x, y, w, h, 10 * sc)
            ctx.fill()
            rgba(ctx, AMBER, a * alpha)
            ctx.rectangle(x + w / 2 - 6 * sc, y - 30 * sc, 12 * sc, 30 * sc)
            ctx.fill()
            rgba(ctx, GREY, a * alpha)
            ctx.rectangle(x + 16 * sc, y + 90 * sc, w - 32 * sc, 8 * sc)
            ctx.rectangle(x + 16 * sc, y + 110 * sc, (w - 32 * sc) * 0.6, 8 * sc)
            ctx.fill()
            ctx.arc(x + w / 2, y + 48 * sc, 22 * sc, 0, 2 * math.pi)
            ctx.fill()
    # gradient to keep text readable
    g = cairo.LinearGradient(0, 0, W, 0)
    g.add_color_stop_rgba(0, BG[0], BG[1], BG[2], 0.92 * a)
    g.add_color_stop_rgba(0.6, BG[0], BG[1], BG[2], 0.55 * a)
    g.add_color_stop_rgba(1, BG[0], BG[1], BG[2], 0.2 * a)
    ctx.set_source(g)
    ctx.paint()
    p = ease_out(prog(t, 0.2, 0.8))
    text(ctx, when, 160, 470, AMBER, a * p, face=MONO, size=40, bold=False, tracking=8)
    for i, ln in enumerate(wrap(ctx, where, 1100, HEAD, 96)):
        text(ctx, ln, 160, 590 + i * 112 + (1 - p) * 20, INK, a * p, size=96)
    if source:
        source_tag(ctx, source, a)


def explainer(ctx, t, d, name, lines, source=None):
    """Who/what is X: big name, 1-2 short facts revealed in sequence."""
    a = fade_io(t, d)
    p = ease_out(prog(t, 0.1, 0.7))
    text(ctx, name, 160, 470 + (1 - p) * 20, INK, a * p, size=120)
    rgba(ctx, AMBER, a)
    ctx.rectangle(160, 510, 200 * p, 5)
    ctx.fill()
    for i, (at, ln) in enumerate(lines):
        q = ease_out(prog(t, at, 0.5))
        text(ctx, ln, 160, 600 + i * 70, GREY if i else INK, a * q, face=MONO, size=40, bold=False)
    if source:
        source_tag(ctx, source, a)


def profile_card(ctx, t, d, title, company, verify_at, glitch_at, source=None):
    """Generic professional-profile card (no real site styling): VERIFIED tick, then a glitch."""
    a = fade_io(t, d)
    cx, cy, cw, ch = W / 2 - 430, H / 2 - 230, 860, 460
    jitter = 0
    g = prog(t, glitch_at, 0.6)
    if 0 < g < 1:
        jitter = random.Random(int(t * 30)).uniform(-14, 14)
    ctx.save()
    ctx.translate(jitter, 0)
    rgba(ctx, (0.09, 0.10, 0.12), a)
    rrect(ctx, cx, cy, cw, ch, 18)
    ctx.fill()
    rgba(ctx, DIM, a)
    ctx.set_line_width(2)
    rrect(ctx, cx, cy, cw, ch, 18)
    ctx.stroke()
    # blurred avatar (no real face): soft rings
    for r in range(70, 0, -7):
        rgba(ctx, GREY, a * 0.05)
        ctx.arc(cx + 130, cy + 140, r, 0, 2 * math.pi)
        ctx.fill()
    text(ctx, title, cx + 240, cy + 125, INK, a, size=48)
    text(ctx, company, cx + 240, cy + 178, GREY, a, face=MONO, size=30, bold=False)
    for i, wfrac in enumerate((0.85, 0.7, 0.78, 0.5)):
        rgba(ctx, DIM, a)
        rrect(ctx, cx + 70, cy + 270 + i * 38, (cw - 140) * wfrac, 14, 7)
        ctx.fill()
    v = ease_out(prog(t, verify_at, 0.4))
    if v > 0:
        col = RED if g > 0.5 else GREEN
        lab = "UNVERIFIED" if g > 0.5 else "VERIFIED"
        rgba(ctx, col, a * v)
        rrect(ctx, cx + cw - 300, cy + 40, 250, 60, 30)
        ctx.fill()
        text(ctx, ("✕ " if g > 0.5 else "✓ ") + lab, cx + cw - 175, cy + 82, BG, a * v,
             align="center", face=MONO, size=28, bold=True)
    ctx.restore()
    if 0 < g < 1:  # scanline tear
        rnd = random.Random(int(t * 30) + 7)
        for _ in range(5):
            y = rnd.uniform(cy, cy + ch)
            rgba(ctx, AMBER, 0.25 * a)
            ctx.rectangle(cx - 40, y, cw + 80, rnd.uniform(2, 10))
            ctx.fill()
    if source:
        source_tag(ctx, source, a)


def chat(ctx, t, d, header, messages, months=None, source=None):
    """Generic group-chat window (no app branding), messages popping in on cue."""
    a = fade_io(t, d)
    x0, y0, w, h = W / 2 - 520, 150, 1040, 760
    rgba(ctx, (0.09, 0.10, 0.12), a)
    rrect(ctx, x0, y0, w, h, 22)
    ctx.fill()
    rgba(ctx, DIM, a)
    ctx.rectangle(x0, y0 + 90, w, 2)
    ctx.fill()
    text(ctx, header, x0 + 40, y0 + 58, INK, a, size=36)
    text(ctx, "ILLUSTRATIVE · NOT THE REAL MESSAGES", x0 + w - 40, y0 + 58, GREY, a, align="right", face=MONO,
         size=22, bold=False)
    y = y0 + 150
    for at, mine, msg in messages:
        q = ease_out(prog(t, at, 0.3))
        if q <= 0:
            continue
        font(ctx, HEAD, 32, False)
        bw = min(ctx.text_extents(msg).x_advance + 60, w - 220)
        bx = x0 + w - 40 - bw if mine else x0 + 40
        rgba(ctx, AMBER if mine else DIM, a * q * (0.9 if mine else 1))
        rrect(ctx, bx, y + (1 - q) * 20, bw, 72, 20)
        ctx.fill()
        text(ctx, msg, bx + 30, y + 47 + (1 - q) * 20, BG if mine else INK, a * q, size=32, bold=False)
        y += 100
    if months:
        idx = min(int(t / d * len(months)), len(months) - 1)
        text(ctx, months[idx], x0 + w, y0 + h + 60, AMBER, a, align="right", face=MONO, size=34,
             bold=False, tracking=6)
    if source:
        source_tag(ctx, source, a)


def question(ctx, t, d, q, small=None):
    a = fade_io(t, d, 0.3, 0.3)
    p = ease_out(prog(t, 0, 0.6))
    text(ctx, q, W / 2, H / 2 + 20 + (1 - p) * 16, INK, a * p, align="center", size=104)
    if small:
        text(ctx, small, W / 2, H / 2 + 110, AMBER, a * prog(t, 1.0, 0.6), align="center",
             face=MONO, size=34, bold=False, tracking=4)


def checklist(ctx, t, d, title, items, source=None):
    a = fade_io(t, d)
    text(ctx, title, 200, 300, AMBER, a, face=MONO, size=36, bold=False, tracking=6)
    for i, (at, it) in enumerate(items):
        q = ease_out(prog(t, at, 0.35))
        y = 420 + i * 120
        rgba(ctx, DIM, a)
        ctx.set_line_width(3)
        rrect(ctx, 200, y - 50, 60, 60, 8)
        ctx.stroke()
        if q > 0:
            rgba(ctx, AMBER, a * q)
            ctx.set_line_width(8)
            ctx.move_to(212, y - 22)
            ctx.line_to(226, y - 6)
            ctx.line_to(212 + 40 * q, y - 6 - 34 * q)
            ctx.stroke()
        text(ctx, it, 300, y, INK, a * (0.35 + 0.65 * q), size=56, bold=q > 0.5)
    if source:
        source_tag(ctx, source, a)


def big_number(ctx, t, d, value, prefix="$", suffix="+", caption="", count_for=1.2, source=None,
               decimals=0):
    a = fade_io(t, d, 0.2, 0.4)
    v = value * ease_out(prog(t, 0, count_for))
    s = f"{prefix}{v:,.{decimals}f}{suffix if t >= count_for else ''}"
    text(ctx, s, W / 2, H / 2 + 50, AMBER, a, align="center", face=MONO, size=190)
    if caption:
        text(ctx, caption, W / 2, H / 2 + 150, GREY, a * prog(t, count_for, 0.5), align="center",
             face=MONO, size=40, bold=False)
    if source:
        source_tag(ctx, source, a)


def statement(ctx, t, d, line, color=INK):
    """A single line on black, for the turn at the end of an act."""
    rgba(ctx, (0, 0, 0))
    ctx.paint()
    a = fade_io(t, d, 0.5, 0.05)
    lines = wrap(ctx, line, W - 400, SERIF, 72, True)
    for i, ln in enumerate(lines):
        text(ctx, ln, W / 2, H / 2 + i * 92 - (len(lines) - 1) * 46, color, a, align="center",
             face=SERIF, size=72, italic=True)


# ============================================================================
# Acts 2-7 + close (ep. 001), still generic enough to reuse
# ============================================================================
def _panel(ctx, x, y, w, h, a, r=18):
    rgba(ctx, (0.10, 0.12, 0.15), a)
    rrect(ctx, x, y, w, h, r)
    ctx.fill()
    rgba(ctx, DIM, a)
    ctx.set_line_width(2)
    rrect(ctx, x, y, w, h, r)
    ctx.stroke()


def pins_map(ctx, t, d, caption, n_pins=6, source=None):
    """Abstract dotted 'world' with pins lighting one by one (no real cities)."""
    a = fade_io(t, d)
    rnd = random.Random(11)
    for i in range(46):
        for j in range(20):
            x, y = 220 + i * 33, 260 + j * 30
            # blobby land mask from a few soft centres
            v = sum(math.exp(-((x - cx) ** 2 / (2 * sx ** 2) + (y - cy) ** 2 / (2 * sy ** 2)))
                    for cx, cy, sx, sy in ((560, 430, 160, 120), (1000, 380, 150, 90), (1330, 470, 230, 120),
                                           (1050, 640, 100, 110), (650, 680, 90, 90), (1550, 720, 80, 50)))
            if v > 0.35:
                rgba(ctx, DIM, a * 0.9)
                ctx.arc(x, y, 4, 0, 2 * math.pi)
                ctx.fill()
    pins = [(560, 420), (1010, 380), (1330, 450), (1080, 630), (660, 680), (1520, 700)][:n_pins]
    for k, (x, y) in enumerate(pins):
        q = ease_out(prog(t, 0.6 + k * (d - 2.0) / max(n_pins, 1), 0.4))
        if q <= 0:
            continue
        pulse = 1 + 0.6 * ((t * 1.2 + k * 0.3) % 1)
        rgba(ctx, AMBER, a * q * (1.2 - pulse * 0.6) * 0.5)
        ctx.arc(x, y, 18 * pulse, 0, 2 * math.pi)
        ctx.fill()
        rgba(ctx, AMBER, a * q)
        ctx.arc(x, y, 9, 0, 2 * math.pi)
        ctx.fill()
    text(ctx, caption, W / 2, 940, INK, a * prog(t, 0.3, 0.5), align="center", face=MONO, size=40,
         bold=False, tracking=4)
    if source:
        source_tag(ctx, source, a)


def silhouettes(ctx, t, d, caption=None, source=None):
    """Three figures at a café table; a thin amber line runs out of frame to a dark shape."""
    a = fade_io(t, d)
    rgba(ctx, DIM, a)
    ctx.rectangle(560, 700, 800, 14)  # table
    ctx.fill()
    for k, x in enumerate((700, 960, 1220)):
        rgba(ctx, (0.20, 0.23, 0.28), a)
        ctx.arc(x, 470, 62, 0, 2 * math.pi)           # head
        ctx.fill()
        ctx.move_to(x - 120, 700)
        ctx.curve_to(x - 120, 560, x + 120, 560, x + 120, 700)  # shoulders
        ctx.close_path()
        ctx.fill()
    p = ease_in_out(prog(t, 1.0, d * 0.6))
    rgba(ctx, AMBER, a * 0.9)
    ctx.set_line_width(3)
    ctx.move_to(1220, 520)
    ctx.curve_to(1450, 420, 1600, 380, 1220 + (W + 200 - 1220) * p, 360 - 40 * p)
    ctx.stroke()
    g = cairo.RadialGradient(W + 60, 340, 10, W + 60, 340, 380)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9 * a * p)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.paint()
    if caption:
        text(ctx, caption, 160, 940, GREY, a, face=MONO, size=34, bold=False)
    if source:
        source_tag(ctx, source, a)


def two_laptops(ctx, t, d, labels, at=(0.3, 0.6), source=None):
    a = fade_io(t, d)
    for k, (x, lab) in enumerate(zip((560, 1360), labels)):
        q = ease_out(prog(t, d * at[k], 0.5))
        if q <= 0:
            continue
        ctx.save()
        ctx.translate(0, (1 - q) * 30)
        _panel(ctx, x - 220, 330, 440, 280, a * q, 14)
        rgba(ctx, (0.06, 0.07, 0.09), a * q)
        rrect(ctx, x - 200, 350, 400, 240, 8)
        ctx.fill()
        rgba(ctx, DIM, a * q)
        ctx.move_to(x - 270, 630)
        ctx.line_to(x + 270, 630)
        ctx.line_to(x + 240, 610)
        ctx.line_to(x - 240, 610)
        ctx.close_path()
        ctx.fill()
        text(ctx, f"{k + 1}", x, 500, AMBER, a * q, align="center", face=MONO, size=90)
        for i, ln in enumerate(wrap(ctx, lab, 520, HEAD, 44)):
            text(ctx, ln, x, 720 + i * 58, INK, a * q, align="center", size=44)
        ctx.restore()
    if source:
        source_tag(ctx, source, a)


def code_editor(ctx, t, d, folder="vault-frontend", source=None):
    """Editor window: a folder opens, a tiny process starts in the corner and pulses amber."""
    a = fade_io(t, d)
    x0, y0, w, h = 260, 170, 1400, 740
    _panel(ctx, x0, y0, w, h, a)
    for i, c in enumerate((RED, AMBER, GREEN)):
        rgba(ctx, c, a * 0.7)
        ctx.arc(x0 + 34 + i * 30, y0 + 30, 9, 0, 2 * math.pi)
        ctx.fill()
    rgba(ctx, (0.08, 0.09, 0.11), a)
    ctx.rectangle(x0, y0 + 60, 330, h - 60)
    ctx.fill()
    open_p = ease_out(prog(t, d * 0.25, 0.5))
    text(ctx, ("▾ " if open_p > 0.5 else "▸ ") + folder, x0 + 30, y0 + 110, INK, a, face=MONO, size=26,
         bold=False)
    files = ["README.md", "package.json", "src/", "  vault.ts", "  strategy.ts", ".vscode/", "  tasks.json"]
    for i, f in enumerate(files):
        q = clamp(open_p * len(files) - i)
        col = AMBER if "tasks.json" in f else GREY
        text(ctx, f, x0 + 60, y0 + 160 + i * 42, col, a * q, face=MONO, size=24, bold=False)
    # the open file: an illustrative .vscode/tasks.json (command left out on purpose)
    code = [("{", 0), ('"version": "2.0.0",', 1), ('"tasks": [', 1), ("{", 2), ('"label": "install",', 3),
            ('"type": "shell",', 3), ('"command": "…",', 3), ('"runOptions": {', 3), ('"runOn": "folderOpen"', 4),
            ("}", 3), ("}", 2), ("]", 1), ("}", 0)]
    cx0, cy0, lh = x0 + 390, y0 + 112, 42
    text(ctx, "tasks.json", cx0, y0 + 40, GREY, a * open_p, face=MONO, size=20, bold=False)
    text(ctx, "ILLUSTRATIVE", x0 + w - 30, y0 + 40, DIM, a * open_p, align="right", face=MONO, size=18,
         bold=False, tracking=4)
    hot = prog(t, d * 0.45, 0.4)
    for i, (ln, ind) in enumerate(code):
        q = clamp(open_p * len(code) * 1.2 - i)
        if q <= 0:
            continue
        y = cy0 + i * lh
        x = cx0 + ind * 34
        if "folderOpen" in ln and hot > 0:
            rgba(ctx, AMBER, a * q * 0.16 * hot)
            rrect(ctx, cx0 - 14, y - 30, 760, 40, 6)
            ctx.fill()
        if ":" in ln:
            k, v = ln.split(":", 1)
            kw = text(ctx, k + ":", x, y, INK, a * q, face=MONO, size=24, bold=False) + 14
            col = AMBER if "folderOpen" in v else GREY
            text(ctx, v.strip(), x + kw, y, col, a * q, face=MONO, size=24, bold=False)
        else:
            text(ctx, ln, x, y, GREY, a * q, face=MONO, size=24, bold=False)
    proc = prog(t, d * 0.55, 0.3)
    if proc > 0:
        pul = 0.5 + 0.5 * math.sin(t * 8)
        rgba(ctx, AMBER, a * proc * (0.4 + 0.6 * pul))
        ctx.arc(x0 + w - 60, y0 + h - 50, 14, 0, 2 * math.pi)
        ctx.fill()
        text(ctx, "process started", x0 + w - 90, y0 + h - 40, AMBER, a * proc, align="right", face=MONO,
             size=24, bold=False)
    if source:
        source_tag(ctx, source, a)


def keys_circle(ctx, t, d, title="SECURITY COUNCIL", glow=2, glow_at=0.5, counter=None, red_at=None,
                caption=None, source=None):
    """Five keys in a circle (any two can act); some glow; optional 2/5 counter that turns red."""
    a = fade_io(t, d)
    cx, cy, R = 600, 600, 250
    text(ctx, title, cx, 150, AMBER, a, align="center", face=MONO, size=34, bold=False, tracking=8)
    for k in range(5):
        ang = -math.pi / 2 + k * 2 * math.pi / 5
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        on = k < glow and t > d * glow_at + k * 0.4
        col = AMBER if on else DIM
        if on:
            rgba(ctx, AMBER, a * 0.25)
            ctx.new_path()
            ctx.arc(x + 10, y, 110, 0, 2 * math.pi)
            ctx.fill()
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(1.7, 1.7)
        ctx.translate(-x, -y)
        rgba(ctx, col, a)
        ctx.set_line_width(8)
        ctx.new_path()
        ctx.arc(x - 18, y, 30, 0, 2 * math.pi)       # key bow
        ctx.stroke()
        ctx.new_path()
        ctx.move_to(x + 12, y)
        ctx.line_to(x + 70, y)
        ctx.move_to(x + 50, y)
        ctx.line_to(x + 50, y + 18)
        ctx.move_to(x + 64, y)
        ctx.line_to(x + 64, y + 14)
        ctx.stroke()
        ctx.restore()
    if counter:
        red = red_at is not None and t > d * red_at
        text(ctx, counter, 1420, 560, RED if red else INK, a, align="center", face=MONO, size=170)
        if caption:
            text(ctx, caption, 1420, 660, RED if red else GREY, a * prog(t, d * (red_at or 0), 0.4),
                 align="center", face=MONO, size=40, bold=False)
    elif caption:
        lines = wrap(ctx, caption, 640, MONO, 44, False)
        for i, ln in enumerate(lines):
            text(ctx, ln, 1420, 560 + i * 60, INK, a * prog(t, 0.5, 0.5), align="center", face=MONO,
                 size=44, bold=False)
    if source:
        source_tag(ctx, source, a)


def drawer(ctx, t, d, label="LATER", source=None):
    """A signed document slides into a drawer marked LATER; the drawer locks."""
    a = fade_io(t, d)
    _panel(ctx, 610, 520, 700, 300, a, 10)
    rgba(ctx, DIM, a)
    ctx.rectangle(860, 640, 200, 16)
    ctx.fill()
    text(ctx, label, 960, 770, AMBER, a, align="center", face=MONO, size=48, tracking=10)
    p = ease_in_out(prog(t, 0.4, d * 0.45))
    y = 160 + p * 380
    ctx.save()
    ctx.rectangle(0, 0, W, 560)
    ctx.clip()
    rgba(ctx, INK, a * 0.92)
    rrect(ctx, 760, y, 400, 300, 6)
    ctx.fill()
    for i in range(6):
        rgba(ctx, GREY, a * 0.5)
        ctx.rectangle(800, y + 40 + i * 30, 320 * (0.6 + 0.4 * ((i * 37) % 10) / 10), 8)
        ctx.fill()
    rgba(ctx, BG, a)
    ctx.set_line_width(4)
    ctx.move_to(820, y + 250)
    ctx.curve_to(870, y + 220, 900, y + 270, 960, y + 240)  # signature
    ctx.stroke()
    ctx.restore()
    lock = ease_out(prog(t, d * 0.65, 0.4))
    if lock > 0:
        rgba(ctx, AMBER, a * lock)
        rrect(ctx, 1210, 610, 60, 50, 6)
        ctx.fill()
        ctx.set_line_width(8)
        ctx.arc(1240, 610, 20, math.pi, 0)
        ctx.stroke()
    if source:
        source_tag(ctx, source, a)


def flat_chart(ctx, t, d, label="CVT / USD", value="$1.00", reveal_at=0.6, source=None):
    """A perfectly flat price line; then the 'market' is revealed as two wallets trading a coin."""
    a = fade_io(t, d)
    rv = ease_in_out(prog(t, d * reveal_at, 1.0))
    ca = a * (1 - rv * 0.75)
    _panel(ctx, 220, 200, 1480, 640, ca)
    text(ctx, label, 270, 270, GREY, ca, face=MONO, size=30, bold=False)
    text(ctx, value, 1650, 270, AMBER, ca, align="right", face=MONO, size=44)
    for i in range(5):
        rgba(ctx, DIM, ca * 0.6)
        ctx.rectangle(270, 360 + i * 100, 1380, 1)
        ctx.fill()
    p = prog(t, 0.2, d * 0.5)
    rgba(ctx, AMBER, ca)
    ctx.set_line_width(5)
    ctx.move_to(270, 560)
    ctx.line_to(270 + 1380 * p, 560 + math.sin(t * 9) * 0.6)
    ctx.stroke()
    if rv > 0:
        for k, x in enumerate((700, 1220)):
            _panel(ctx, x - 130, 420, 260, 220, a * rv, 16)
            text(ctx, f"WALLET {'AB'[k]}", x, 560, INK, a * rv, align="center", face=MONO, size=34)
        ph = (t * 1.4) % 1
        cx = 830 + (1090 - 830) * (ph if int(t * 1.4) % 2 == 0 else 1 - ph)
        rgba(ctx, AMBER, a * rv)
        ctx.arc(cx, 530, 26, 0, 2 * math.pi)
        ctx.fill()
        text(ctx, "the ‘market’ = two wallets", W / 2, 760, GREY, a * rv, align="center", face=MONO,
             size=36, bold=False)
    if source:
        source_tag(ctx, source, a)


def vault_drain(ctx, t, d, total=285_000_000, labels=("USDC", "JLP", "cbBTC", "SOL"), small=None,
                source=None):
    """Vault emptying in bursts; asset labels flicker past; counter climbs."""
    a = fade_io(t, d)
    _panel(ctx, 200, 220, 600, 640, a, 20)
    bursts = 31
    k = min(bursts, int(prog(t, 0.3, d * 0.85) * bursts))
    level = 1 - k / bursts
    rgba(ctx, AMBER, a * 0.85)
    ctx.rectangle(240, 260 + 560 * (1 - level), 520, 560 * level)
    ctx.fill()
    text(ctx, "VAULT", 500, 205, GREY, a, align="center", face=MONO, size=28, bold=False, tracking=8)
    lab = labels[int(t * 6) % len(labels)]
    text(ctx, lab, 1000, 360, GREY, a * (0.5 + 0.5 * math.sin(t * 12)), face=MONO, size=44)
    text(ctx, f"${total * k / bursts:,.0f}", 1000, 560, AMBER, a, face=MONO, size=110)
    text(ctx, f"withdrawals: {k} / 31", 1000, 650, INK, a, face=MONO, size=40, bold=False)
    if small:
        text(ctx, small, 1000, 720, GREY, a * 0.8, face=MONO, size=28, bold=False)
    if source:
        source_tag(ctx, source, a)


def flow_map(ctx, t, d, left="SOLANA", mid="BRIDGE", right="ETHEREUM", lines=(), source=None):
    a = fade_io(t, d)
    nodes = [(380, 480, left), (960, 480, mid), (1540, 480, right)]
    for x, y, lab in nodes:
        _panel(ctx, x - 170, y - 90, 340, 180, a, 90)
        text(ctx, lab, x, y + 15, INK, a, align="center", face=MONO, size=40)
    rgba(ctx, DIM, a)
    ctx.set_line_width(4)
    ctx.move_to(550, 480)
    ctx.line_to(790, 480)
    ctx.move_to(1130, 480)
    ctx.line_to(1370, 480)
    ctx.stroke()
    for i in range(10):
        ph = (t * 0.6 + i / 10) % 1
        x = 550 + ph * 820
        if 790 < x < 1130:
            continue
        rgba(ctx, AMBER, a)
        ctx.arc(x, 480, 10, 0, 2 * math.pi)
        ctx.fill()
    for i, (at, ln) in enumerate(lines):
        text(ctx, ln, W / 2, 720 + i * 64, AMBER if i == 0 else GREY, a * prog(t, at, 0.5), align="center",
             face=MONO, size=40, bold=i == 0)
    if source:
        source_tag(ctx, source, a)


def chat_deleted(ctx, t, d, header="Firm × Drift contributors", source=None):
    """The group chat, then everything is deleted line by line."""
    a = fade_io(t, d)
    x0, y0, w, h = W / 2 - 520, 170, 1040, 720
    _panel(ctx, x0, y0, w, h, a, 22)
    text(ctx, header, x0 + 40, y0 + 58, INK, a, size=36)
    text(ctx, "ILLUSTRATIVE · NOT THE REAL MESSAGES", x0 + w - 40, y0 + 58, GREY, a, align="right", face=MONO,
         size=22, bold=False)
    msgs = ["Strategy deck for the vault, attached.", "Thanks, looks solid. Call Thursday?",
            "Vault integration: next steps below.", "Sounds good. Let's keep going.", "See you at the conference."]
    for i, m in enumerate(msgs):
        gone = prog(t, d * 0.35 + i * 0.35, 0.3)
        y = y0 + 150 + i * 100
        if gone < 1:
            rgba(ctx, DIM, a * (1 - gone))
            rrect(ctx, x0 + 40, y, 700, 72, 20)
            ctx.fill()
            text(ctx, m, x0 + 70, y + 47, INK, a * (1 - gone), size=30, bold=False)
        else:
            text(ctx, "message deleted", x0 + 60, y + 47, GREY, a * 0.6, face=MONO, size=26, bold=False,
                 italic=True)
    if t > d * 0.35 + len(msgs) * 0.35 + 0.4:
        text(ctx, "GROUP NO LONGER EXISTS", W / 2, y0 + h + 70, RED, a, align="center", face=MONO, size=36,
             tracking=6)
    if source:
        source_tag(ctx, source, a)


def dossier(ctx, t, d, stamp, lines=(), source=None):
    a = fade_io(t, d)
    rgba(ctx, (0.80, 0.74, 0.62), a * 0.9)
    rrect(ctx, 460, 150, 1000, 780, 8)
    ctx.fill()
    for i in range(12):
        rgba(ctx, (0.45, 0.40, 0.33), a * 0.5)
        ctx.rectangle(540, 300 + i * 46, 840 * (0.5 + 0.5 * ((i * 53) % 10) / 10), 10)
        ctx.fill()
    for i, (at, ln) in enumerate(lines):
        text(ctx, ln, 540, 280 + i * 60, (0.12, 0.12, 0.12), a * prog(t, at, 0.4), face=MONO, size=34)
    s = ease_out(prog(t, 0.5, 0.35))
    if s > 0:
        ctx.save()
        ctx.translate(960, 700)
        ctx.rotate(-0.12)
        ctx.scale(1 + (1 - s) * 0.6, 1 + (1 - s) * 0.6)
        rgba(ctx, (0.85, 0.45, 0.05), a * s * 0.9)
        ctx.set_line_width(8)
        rrect(ctx, -440, -70, 880, 140, 10)
        ctx.stroke()
        for i, ln in enumerate(stamp.split("\n")):
            text(ctx, ln, 0, -10 + i * 52, (0.85, 0.45, 0.05), a * s, align="center", face=MONO, size=40,
                 tracking=4)
        ctx.restore()
    if source:
        source_tag(ctx, source, a)


def flashback(ctx, t, d, title, items=(), source=None):
    """Desaturated flashback panel with a file icon (e.g. a zipped PDF)."""
    a = fade_io(t, d)
    rgba(ctx, (0.16, 0.16, 0.16), a)
    ctx.paint()
    text(ctx, "FLASHBACK", 160, 200, GREY, a, face=MONO, size=30, bold=False, tracking=10)
    text(ctx, title, 160, 300, INK, a, size=90)
    for i, (at, ln) in enumerate(items):
        q = ease_out(prog(t, at, 0.5))
        x = 220 + i * 520
        rgba(ctx, (0.85, 0.85, 0.85), a * q)
        ctx.move_to(x, 450)
        ctx.line_to(x + 180, 450)
        ctx.line_to(x + 240, 510)
        ctx.line_to(x + 240, 720)
        ctx.line_to(x, 720)
        ctx.close_path()
        ctx.fill()
        text(ctx, ln, x + 120, 800, INK, a * q, align="center", face=MONO, size=34, bold=False)
    if source:
        source_tag(ctx, source, a)


def code_names(ctx, t, d, rows, source=None):
    a = fade_io(t, d)
    for i, (code, what) in enumerate(rows):
        q = ease_out(prog(t, 0.2 + i * 0.5, 0.5))
        text(ctx, code, 480, 470 + i * 160, AMBER, a * q, face=MONO, size=96)
        text(ctx, what, 1120, 470 + i * 160, GREY, a * q, face=MONO, size=40, bold=False)
    text(ctx, "MANDIANT DESIGNATIONS", 480, 330, INK, a, face=MONO, size=32, bold=False, tracking=6)
    if source:
        source_tag(ctx, source, a)


def dominoes(ctx, t, d, labels, source=None):
    a = fade_io(t, d)
    n = len(labels)
    for i, lab in enumerate(labels):
        x = 360 + i * 240
        fall = ease_in_out(prog(t, 0.5 + i * 0.35, 0.5))
        ctx.save()
        ctx.translate(x + 50, 760)
        ctx.rotate(fall * 1.25)
        rgba(ctx, AMBER if i == 0 else (0.22, 0.25, 0.30), a)
        rrect(ctx, -50, -300, 90, 300, 8)
        ctx.fill()
        ctx.restore()
        text(ctx, lab, x + 45, 840, GREY if i else AMBER, a, align="center", face=MONO, size=28, bold=False)
    if source:
        source_tag(ctx, source, a)


def tornado_trace(ctx, t, d, caption, batches=5, source=None):
    a = fade_io(t, d)
    cx, cy = 1350, 520
    for r in range(6):
        rgba(ctx, GREY, a * (0.15 + r * 0.05))
        ctx.set_line_width(3)
        ctx.arc(cx, cy, 40 + r * 22, t * (1 + r * 0.3), t * (1 + r * 0.3) + 4.5)
        ctx.stroke()
    text(ctx, "MIXER", cx, cy + 230, GREY, a, align="center", face=MONO, size=30, bold=False, tracking=8)
    for i in range(batches):
        y = 260 + i * 110
        _panel(ctx, 260, y, 260, 70, a, 12)
        text(ctx, f"0x…{(i * 7919) % 9999:04x}", 390, y + 47, INK, a, align="center", face=MONO, size=26,
             bold=False)
        ph = (t * 0.5 + i * 0.2) % 1
        rgba(ctx, AMBER, a)
        ctx.arc(520 + ph * (cx - 120 - 520), y + 35 + (cy - y - 35) * ph, 8, 0, 2 * math.pi)
        ctx.fill()
    text(ctx, caption, W / 2, 960, INK, a * prog(t, 0.6, 0.5), align="center", face=MONO, size=38, bold=False)
    if source:
        source_tag(ctx, source, a)


def timeline(ctx, t, d, points, title=None, source=None):
    """Horizontal timeline: points [(label, sub)] revealed in order."""
    a = fade_io(t, d)
    if title:
        text(ctx, title, 200, 300, AMBER, a, face=MONO, size=34, bold=False, tracking=6)
    n = len(points)
    x0, x1, y = 260, 1660, 560
    p = ease_in_out(prog(t, 0.2, d * 0.7))
    rgba(ctx, DIM, a)
    ctx.rectangle(x0, y - 2, x1 - x0, 4)
    ctx.fill()
    rgba(ctx, AMBER, a)
    ctx.rectangle(x0, y - 2, (x1 - x0) * p, 4)
    ctx.fill()
    for i, (lab, sub) in enumerate(points):
        x = x0 + (x1 - x0) * i / max(n - 1, 1)
        q = clamp((p - i / max(n - 1, 1)) * 4 + 1)
        rgba(ctx, AMBER if q > 0.5 else DIM, a)
        ctx.arc(x, y, 14, 0, 2 * math.pi)
        ctx.fill()
        text(ctx, lab, x, y - 50, INK, a * q, align="center", face=MONO, size=40)
        for j, ln in enumerate(wrap(ctx, sub, 320, MONO, 26, False)):
            text(ctx, ln, x, y + 70 + j * 36, GREY, a * q, align="center", face=MONO, size=26, bold=False)
    if source:
        source_tag(ctx, source, a)


def end_card(ctx, t, d):
    a = ease_in_out(prog(t, 0, 1.0))
    siphon_mark(ctx, 960, 330, 0.26, a)
    text(ctx, "SIPHON FILES", 960, 560, INK, a, align="center", size=64, tracking=6)
    text(ctx, "Follow the money. It always leaves a trail.", 960, 640, AMBER, a * prog(t, 0.6, 0.6),
         align="center", face=SERIF, size=44, italic=True)
    text(ctx, "Sources in the description · Narrated by Thomas Archer, an AI presenter", 960, 930, GREY,
         a * prog(t, 1.0, 0.6), align="center", face=MONO, size=26, bold=False)


# ============================================================================
# Illustrations (Z-Image stills) animated in 2.5D: depth-based parallax + camera move
# ============================================================================
ILL_DIR = None   # set by the episode script: folder with <name>.jpg and <name>_depth.png


def _ill_load(name):
    c = _ill_load.cache
    if c.get("name") == name:
        return c
    import numpy as np
    from PIL import Image
    import os
    img = np.asarray(Image.open(os.path.join(ILL_DIR, name + ".jpg")).convert("RGB"), dtype=np.float32)
    h, w, _ = img.shape
    from PIL import ImageFilter
    # heavily smoothed depth: the warp field must be smooth, otherwise it tears at object edges
    dep = Image.open(os.path.join(ILL_DIR, name + "_depth.png")).convert("L").filter(ImageFilter.GaussianBlur(14))
    dep = dep.resize((w, h), Image.BILINEAR)
    dep = np.asarray(dep, dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    c.clear()
    c.update(name=name, img=img.reshape(-1, 3), w=w, h=h, d=dep, xx=xx, yy=yy, dm=float(np.median(dep)))
    return c


_ill_load.cache = {}

MOVES = {   # (zoom start, zoom end, pan x px, pan y px, depth zoom, depth pan) in source pixels
    # The camera move itself is rigid (no distortion). The depth terms stay small: the per-pixel
    # difference between near and far must stay under ~6 px, otherwise straight edges bend and
    # heads smear into the background (seen in render 4 with 0.16 / 1.3).
    "in": (1.05, 1.20, 0, 0, 0.015, 0.0),
    "out": (1.20, 1.05, 0, 0, -0.015, 0.0),
    "left": (1.13, 1.16, 110, 0, 0.005, 0.15),
    "right": (1.13, 1.16, -110, 0, 0.005, 0.15),
    "up": (1.13, 1.17, 0, 50, 0.005, 0.15),
    "down": (1.13, 1.17, 0, -50, 0.005, 0.15),
}


def flick_level(t, mode="flicker", seed=0):
    """How far a light is dimmed at time t, 0..1. 'slow' = a calm breathing, 'flicker' = a lamp that
    mostly holds and now and then stutters (short irregular dips)."""
    ph = seed * 1.7
    if mode == "slow":
        return 0.5 + 0.5 * math.sin(2 * math.pi * 0.35 * t + ph) * math.sin(2 * math.pi * 0.13 * t + 1.1 + ph)
    base = 0.12 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.5 * t + ph))
    n = (math.sin(t * 7.1 + ph) + math.sin(t * 11.3 + 2.0 + ph) + math.sin(t * 17.9 + 4.1 + ph)) / 3.0
    burst = clamp((math.sin(t * 0.9 + ph) - 0.35) / 0.4)            # stutters come in short spells
    return clamp(base + burst * clamp((n + 0.15) / 0.5))


def _light_mask(name, lights):
    """Where the lights of a still are: bright pixels near each light, plus the soft light they throw around."""
    import numpy as np
    key = (name, repr(lights))
    if key in _light_mask.cache:
        return _light_mask.cache[key]
    c = _ill_load(name)
    w, h = c["w"], c["h"]
    img = c["img"].reshape(h, w, 3)
    mx = img.max(axis=2) / 255.0
    yy, xx = c["yy"], c["xx"]
    m = np.zeros((h, w), dtype=np.float32)
    for L in lights:
        g = np.exp(-((xx - L["x"]) ** 2 + (yy - L["y"]) ** 2) / (2.0 * L["r"] ** 2))
        thr = L.get("thr", 0.55)
        hot = np.clip((mx - (thr - 0.12)) / 0.2, 0, 1)
        m = np.maximum(m, g * (hot + L.get("amb", 0.35) * (1 - hot)))
    _light_mask.cache.clear()
    _light_mask.cache[key] = m.reshape(-1)
    return _light_mask.cache[key]


_light_mask.cache = {}


def _ripple_mask(name, rp):
    """Bright screen areas only, pulled in from dark edges (silhouettes) so their pixels are never moved."""
    import numpy as np
    from PIL import Image, ImageFilter
    key = (name, repr(rp))
    if key in _ripple_mask.cache:
        return _ripple_mask.cache[key]
    c = _ill_load(name)
    w, h = c["w"], c["h"]
    lum = c["img"].reshape(h, w, 3).mean(axis=2)
    m = (lum > rp.get("thr", 70)).astype(np.uint8) * 255
    im = Image.fromarray(m).filter(ImageFilter.MinFilter(2 * rp.get("guard", 14) + 1)).filter(
        ImageFilter.GaussianBlur(rp.get("guard", 14) / 2))
    m = np.asarray(im, dtype=np.float32) / 255.0
    if "y1" in rp:
        m[int(rp["y1"]):] = 0
    _ripple_mask.cache.clear()
    _ripple_mask.cache[key] = m
    return m


_ripple_mask.cache = {}


def _ill_frame(name, u, move, t=0.0, fog=None, flick=None, ripple=None):
    """Backward warp with bilinear sampling: near pixels (depth ~1) zoom and slide more than far ones."""
    import numpy as np
    c = _ill_load(name)
    z0, z1, px, py, kz, kp = MOVES[move]
    e = ease_in_out(u)
    z = z0 + (z1 - z0) * e
    w, h, d, dm = c["w"], c["h"], c["d"], c["dm"]
    im = c["img"]
    arr = np.empty((h, w, 4), dtype=np.uint8)
    arr[..., 3] = 255
    off = (e - 0.5)
    fogA = _fog_alpha(name, t, fog, d, w, h) if fog else None
    if fog:
        fc = np.array(fog.get("color", (0.6, 0.65, 0.72)), dtype=np.float32) * 255.0
    lm = _light_mask(name, flick["lights"]) if flick else None
    dip = flick.get("depth", 0.3) * flick_level(t, flick.get("mode", "flicker"), flick.get("seed", 0)) if flick else 0.0
    rm = _ripple_mask(name, ripple) if ripple else None
    band = 144   # rows per band: keeps temporaries small (the render box has 3 GB for 2 workers + 2 encoders)
    for r0 in range(0, h, band):
        r1 = min(h, r0 + band)
        db = d[r0:r1]
        zz = z * (1.0 + kz * e * (db - dm)) if kz >= 0 else z * (1.0 + (-kz) * (1 - e) * (db - dm))
        sx = w / 2 + (c["xx"][r0:r1] - w / 2) / zz - px * off * (1.0 + kp * (db - dm))
        sy = h / 2 + (c["yy"][r0:r1] - h / 2) / zz - py * off * (1.0 + kp * (db - dm))
        if rm is not None:   # bands on the screens drift as a slow wave; dark shapes stay put
            ix = np.clip(sx, 0, w - 1).astype(np.int32)
            iy = np.clip(sy, 0, h - 1).astype(np.int32)
            k = rm[iy, ix]
            amp, wl, sp = ripple.get("amp", 6.0), ripple.get("wl", 520.0), ripple.get("speed", 0.6)
            sy = sy + amp * k * np.sin(2 * math.pi * (sx / wl - sp * t / 6.0))
            sx = sx - ripple.get("drift", 18.0) * k * math.sin(2 * math.pi * 0.05 * t)
        np.clip(sx, 0, w - 1.001, out=sx)
        np.clip(sy, 0, h - 1.001, out=sy)
        x0 = sx.astype(np.int32)
        y0 = sy.astype(np.int32)
        fx = (sx - x0)[..., None]
        fy = (sy - y0)[..., None]
        i = y0 * w + x0
        top = im[i] * (1 - fx) + im[i + 1] * fx
        bot = im[i + w] * (1 - fx) + im[i + w + 1] * fx
        out = top * (1 - fy) + bot * fy
        if lm is not None and dip > 0:
            out = out * (1.0 - dip * lm[i])[..., None]
        if fogA is not None:
            a = fogA[r0:r1, :, None]
            out = out * (1 - a) + fc * a
        arr[r0:r1, :, 0] = out[..., 2]
        arr[r0:r1, :, 1] = out[..., 1]
        arr[r0:r1, :, 2] = out[..., 0]
    data = bytearray(arr.tobytes())
    return cairo.ImageSurface.create_for_data(data, cairo.FORMAT_RGB24, w, h, w * 4), data


def _fog_noise(seed, gw=512, gh=288):
    """Tileable smooth noise in [0,1] (low-pass filtered random field, periodic by construction)."""
    import numpy as np
    key = (seed, gw, gh)
    if key in _fog_noise.cache:
        return _fog_noise.cache[key]
    rng = np.random.default_rng(seed)
    f = np.fft.fft2(rng.standard_normal((gh, gw)))
    ky = np.fft.fftfreq(gh)[:, None]
    kx = np.fft.fftfreq(gw)[None, :]
    k = np.sqrt(kx * kx + ky * ky)
    f *= np.exp(-(k / 0.018) ** 2)
    n = np.real(np.fft.ifft2(f))
    n = (n - n.min()) / (n.max() - n.min())
    _fog_noise.cache[key] = n.astype(np.float32)
    return _fog_noise.cache[key]


_fog_noise.cache = {}


def _fog_alpha(name, t, fog, d, w, h):
    """Drifting fog, placed with the depth map (far = behind the subject) and/or near the floor.
    fog: density, color, speed (px/s at 512 wide), far (depth below which fog sits), floor (0..1 start of floor band)."""
    import numpy as np
    from PIL import Image
    gw, gh = 512, 288
    acc = np.zeros((gh, gw), dtype=np.float32)
    yy, xx = np.mgrid[0:gh, 0:gw].astype(np.float32)
    sp = fog.get("speed", 14.0)
    rise = fog.get("rise", 0.0)                   # steam: wisps that climb instead of lying flat
    st = fog.get("stretch", (0.4, 1.3))
    for k, (sc, vx, vy, wgt) in enumerate(((1.0, sp, sp * (0.15 + rise), 0.6), (0.55, -sp * 0.6, sp * (0.1 + rise * 0.8), 0.4))):
        n = _fog_noise(1000 + k + sum(map(ord, name)))
        sx = (xx * sc * st[0] + vx * t) % gw          # stretched sideways: fog lies in horizontal banks
        sy = (yy * sc * st[1] + vy * t) % gh
        x0 = sx.astype(np.int32); y0 = sy.astype(np.int32)
        fx = sx - x0; fy = sy - y0
        x0 %= gw; y0 %= gh   # float modulo can land exactly on gw
        x1 = (x0 + 1) % gw; y1 = (y0 + 1) % gh
        v = (n[y0, x0] * (1 - fx) + n[y0, x1] * fx) * (1 - fy) + (n[y1, x0] * (1 - fx) + n[y1, x1] * fx) * fy
        acc += wgt * v
    hz = fog.get("haze", 0.35)
    acc = hz + (1 - hz) * np.clip((acc - 0.3) / 0.5, 0, 1)    # a light even haze plus soft drifting banks
    A = np.asarray(Image.fromarray(acc).resize((w, h), Image.BILINEAR), dtype=np.float32)
    mask = np.ones((h, w), dtype=np.float32)
    if "far" in fog:                                           # only behind the subject
        mask *= np.clip((fog["far"] - d) / 0.15, 0, 1)
    if "floor" in fog:                                         # low-lying fog
        ys = np.linspace(0, 1, h, dtype=np.float32)[:, None]
        mask *= np.clip((ys - fog["floor"]) / fog.get("soft", 0.2), 0, 1)
    return np.clip(fog.get("density", 0.3) * A * mask, 0, 0.85)


def _cam_point(name, u, move, x, y):
    """Where a point of the source image (pixels) lands on screen (layout units) under the camera move."""
    c = _ill_load(name)
    z0, z1, px, py, kz, kp = MOVES[move]
    e = ease_in_out(u)
    z = z0 + (z1 - z0) * e
    off = e - 0.5
    w, h = c["w"], c["h"]
    ox = w / 2 + (x + px * off - w / 2) * z
    oy = h / 2 + (y + py * off - h / 2) * z
    return ox * W / w, oy * W / w, z * W / w


def _glows(ctx, t, u, name, move, glows, a, gain=1.0):
    """Light effects in image coordinates: 'pulse' (alarm), 'flicker' (lamp), 'beam' (light shaft)."""
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    for g in glows:
        kind = g["kind"]
        col = g.get("color", (1.0, 0.7, 0.3))
        if kind == "pulse":
            k = 0.5 + 0.5 * math.sin(2 * math.pi * g.get("hz", 0.8) * t)
            inten = g.get("min", 0.15) + (g.get("max", 0.75) - g.get("min", 0.15)) * k * k
        elif kind == "flicker":
            inten = g.get("base", 0.35) * (0.85 + 0.15 * math.sin(t * 13.0) * math.sin(t * 7.3 + 1.0)
                                           + 0.08 * math.sin(t * 29.0))
        else:
            inten = g.get("base", 0.10) * (0.8 + 0.2 * math.sin(t * 1.3) * math.sin(t * 0.7 + 2.0))
        inten *= a * gain
        if kind == "beam":
            pts = [_cam_point(name, u, move, x, y)[:2] for x, y in g["poly"]]
            (ax, ay), (bx, by) = pts[0], pts[-1]
            gr = cairo.LinearGradient((pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2,
                                      (pts[2][0] + pts[3][0]) / 2, (pts[2][1] + pts[3][1]) / 2)
            gr.add_color_stop_rgba(0, col[0], col[1], col[2], inten)
            gr.add_color_stop_rgba(1, col[0], col[1], col[2], inten * 0.15)
            ctx.set_source(gr)
            ctx.move_to(*pts[0])
            for p in pts[1:]:
                ctx.line_to(*p)
            ctx.close_path()
            ctx.fill()
            # dust drifting inside the shaft
            rnd = random.Random(7)
            for i in range(40):
                fu, fv = rnd.random(), rnd.random()
                fv = (fv + t * rnd.uniform(0.01, 0.03)) % 1.0
                top = (pts[0][0] + (pts[1][0] - pts[0][0]) * fu, pts[0][1] + (pts[1][1] - pts[0][1]) * fu)
                bot = (pts[3][0] + (pts[2][0] - pts[3][0]) * fu, pts[3][1] + (pts[2][1] - pts[3][1]) * fu)
                x = top[0] + (bot[0] - top[0]) * fv + 6 * math.sin(t * 0.8 + i)
                y = top[1] + (bot[1] - top[1]) * fv
                r = rnd.uniform(1.0, 2.6)
                al = a * rnd.uniform(0.25, 0.6) * (0.6 + 0.4 * math.sin(t * 2 + i))
                rg = cairo.RadialGradient(x, y, 0, x, y, r * 2)
                rg.add_color_stop_rgba(0, 1, 0.92, 0.75, al)
                rg.add_color_stop_rgba(1, 1, 0.92, 0.75, 0)
                ctx.set_source(rg)
                ctx.arc(x, y, r * 2, 0, 2 * math.pi)
                ctx.fill()
        else:
            x, y, s = _cam_point(name, u, move, g["x"], g["y"])
            r = g.get("r", 120) * s
            rg = cairo.RadialGradient(x, y, 0, x, y, r)
            rg.add_color_stop_rgba(0, col[0], col[1], col[2], inten)
            rg.add_color_stop_rgba(0.35, col[0], col[1], col[2], inten * 0.35)
            rg.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
            ctx.set_source(rg)
            ctx.arc(x, y, r, 0, 2 * math.pi)
            ctx.fill()
    ctx.restore()


def _motes(ctx, t, a, seed, warm=True):
    """Dust in the air, in three depth layers: many small slow specks far away, some brighter ones
    in the middle, a few large soft out-of-focus ones close to the lens. They rise like dust in warm
    air from a lamp and wander on a slow, irregular path instead of a straight line."""
    rnd = random.Random(seed)
    col = (1.0, 0.86, 0.62) if warm else (0.75, 0.85, 1.0)
    #        count, radius,      rise px/s,   drift px/s, wobble px, alpha,        glow
    layers = ((26, (1.0, 2.2), (14, 30), (-10, 10), (6, 18), (0.10, 0.30), 2.2),
              (14, (2.0, 3.4), (30, 55), (-16, 16), (12, 30), (0.16, 0.36), 2.4),
              (5, (6.0, 11.0), (60, 95), (-25, 25), (20, 45), (0.06, 0.12), 1.6))
    for n, (r0, r1), (v0, v1), (d0, d1), (w0, w1), (a0, a1), gl in layers:
        for i in range(n):
            x0, y0 = rnd.uniform(0, W), rnd.uniform(0, H)
            vy = rnd.uniform(v0, v1)
            vx = rnd.uniform(d0, d1)
            r = rnd.uniform(r0, r1)
            amp = rnd.uniform(w0, w1)
            f1, f2 = rnd.uniform(0.15, 0.45), rnd.uniform(0.5, 1.1)
            p1, p2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
            span = H + 80
            x = (x0 + vx * t + amp * math.sin(f1 * t + p1) + amp * 0.35 * math.sin(f2 * t + p2)) % (W + 80) - 40
            y = (y0 - vy * t + amp * 0.3 * math.sin(f2 * 0.7 * t + p1)) % span - 40
            tw = 0.65 + 0.35 * math.sin(t * rnd.uniform(0.8, 2.2) + p2)
            al = a * rnd.uniform(a0, a1) * tw
            rr = r * gl
            g = cairo.RadialGradient(x, y, 0, x, y, rr)
            g.add_color_stop_rgba(0, col[0], col[1], col[2], al)
            g.add_color_stop_rgba(0.45, col[0], col[1], col[2], al * 0.45)
            g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
            ctx.set_source(g)
            ctx.arc(x, y, rr, 0, 2 * math.pi)
            ctx.fill()


def _snow(ctx, t, a, seed):
    """Fine snow: many small flakes far away, fewer bigger soft ones close to the lens, all falling
    slowly on a slight slant and swaying a little."""
    rnd = random.Random(seed)
    #        count, radius,     fall px/s, slant px/s, sway px, alpha
    layers = ((140, (0.8, 1.6), (35, 60), (8, 18), (4, 10), (0.35, 0.6)),
              (60, (1.6, 2.8), (70, 110), (14, 28), (8, 18), (0.45, 0.75)),
              (14, (4.0, 7.0), (140, 200), (25, 45), (14, 30), (0.12, 0.25)))
    for n, (r0, r1), (v0, v1), (s0, s1), (w0, w1), (a0, a1) in layers:
        for i in range(n):
            x0, y0 = rnd.uniform(0, W + 200), rnd.uniform(0, H)
            vy, vx = rnd.uniform(v0, v1), rnd.uniform(s0, s1)
            r, amp = rnd.uniform(r0, r1), rnd.uniform(w0, w1)
            f, ph = rnd.uniform(0.3, 0.9), rnd.uniform(0, 6.28)
            x = (x0 - vx * t + amp * math.sin(f * t + ph)) % (W + 200) - 100
            y = (y0 + vy * t) % (H + 40) - 20
            al = a * rnd.uniform(a0, a1)
            g = cairo.RadialGradient(x, y, 0, x, y, r * 1.8)
            g.add_color_stop_rgba(0, 0.95, 0.97, 1.0, al)
            g.add_color_stop_rgba(0.5, 0.95, 0.97, 1.0, al * 0.6)
            g.add_color_stop_rgba(1, 0.95, 0.97, 1.0, 0)
            ctx.set_source(g)
            ctx.arc(x, y, r * 1.8, 0, 2 * math.pi)
            ctx.fill()


def illus(ctx, t, d, name, move="in", kicker=None, line=None, statement=None, source=None,
          dim=0.0, motes=True, warm=True, fi=0.35, fo=0.35, fog=None, glows=None,
          flick=None, ripple=None, snow=False):
    """An illustration with a slow 2.5D camera move, drifting dust in the light and optional text."""
    a = fade_io(t, d, fi, fo)
    u = clamp(t / max(d, 0.01))
    surf, _keep = _ill_frame(name, u, move, t, fog, flick, ripple)
    ctx.save()
    sc = W / surf.get_width()
    ctx.scale(sc, sc)
    ctx.set_source_surface(surf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint_with_alpha(a)
    ctx.restore()
    if glows:
        gain = 1.0 - flick.get("depth", 0.3) * flick_level(t, flick.get("mode", "flicker"), flick.get("seed", 0)) if flick else 1.0
        _glows(ctx, t, u, name, move, glows, a, gain)
    if motes:
        _motes(ctx, t, a, sum(map(ord, name)), warm)
    if snow:
        _snow(ctx, t, a, sum(map(ord, name)))
    if dim > 0:
        rgba(ctx, (0, 0, 0), dim * a)
        ctx.paint()
    if kicker or line:
        g = cairo.LinearGradient(0, H * 0.45, 0, H)
        g.add_color_stop_rgba(0, 0, 0, 0, 0)
        g.add_color_stop_rgba(1, 0, 0, 0, 0.78 * a)
        ctx.set_source(g)
        ctx.paint()
        p = ease_out(prog(t, 0.3, 0.8))
        y = H - 150
        if line:
            lines = wrap(ctx, line, 1300, HEAD, 64)
            y = H - 130 - (len(lines) - 1) * 76
            for i, ln in enumerate(lines):
                text(ctx, ln, 140, y + i * 76 + (1 - p) * 16, INK, a * p, size=64)
        if kicker:
            text(ctx, kicker, 142, y - 78, AMBER, a * p, face=MONO, size=32, bold=False, tracking=7)
    if statement:
        g = cairo.LinearGradient(0, H * 0.35, 0, H)
        g.add_color_stop_rgba(0, 0, 0, 0, 0)
        g.add_color_stop_rgba(1, 0, 0, 0, 0.8 * a)
        ctx.set_source(g)
        ctx.paint()
        p = ease_out(prog(t, 0.4, 0.9))
        lines = wrap(ctx, statement, W - 400, SERIF, 68, True)
        for i, ln in enumerate(lines):
            text(ctx, ln, W / 2, H - 150 - (len(lines) - 1 - i) * 86, INK, a * p, align="center",
                 face=SERIF, size=68, italic=True)
    if source:
        source_tag(ctx, source, a)
