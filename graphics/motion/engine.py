"""Siphon Files motion graphics: a tiny, dependency-light engine (pycairo + ffmpeg).

Why not HyperFrames/Chrome: the render box on proprietarul's Mac (and any CI box) may have
no network to install Chrome; pycairo + ffmpeg are enough for cards, numbers, charts,
diagrams and kinetic type, and everything stays deterministic and free.

A scene is a function draw(ctx, t, d, **params): t = seconds since the scene started,
d = scene duration. The renderer composes scenes over a timeline and pipes BGRA frames
into ffmpeg, in parallel over CPU cores.
"""
import math
import os
import subprocess
from multiprocessing import Pool

import cairo

W, H, FPS = 1920, 1080, 30   # layout coordinates (scenes are drawn in this space)
SCALE = int(os.environ.get("SIPHON_SCALE", "2"))   # 2 -> renders 3840x2160 (4K)
OW, OH = W * SCALE, H * SCALE

# --- brand -------------------------------------------------------------------
# Background: #141920, a dark ink-blue. Lifted slightly off the old #0D0F12 because near-black
# bands and blocks under 8-bit video compression; this tone stays clean on Retina/4K screens.
BG = (0x14 / 255, 0x19 / 255, 0x20 / 255)
AMBER = (1.0, 0xB0 / 255, 0x20 / 255)
INK = (0xED / 255, 0xE8 / 255, 0xDF / 255)
GREY = (0x7A / 255, 0x80 / 255, 0x8A / 255)
DIM = (0x2A / 255, 0x2E / 255, 0x35 / 255)
RED = (0xE5 / 255, 0x48 / 255, 0x4D / 255)
GREEN = (0x3D / 255, 0xD6 / 255, 0x8C / 255)
HEAD = "Lato"            # headline face (Black / Bold weights via fontconfig)
MONO = "Noto Sans Mono"  # data, labels, timestamps
SERIF = "Lora"           # quotes

# --- per-episode theme ----------------------------------------------------------
# SIPHON_THEME=ep002 (Bitget, "night shift in the security office"): petrol-slate background with a
# faint surveillance grid and a slow scan line, signal-cyan accent instead of amber, cool white type,
# IBM Plex Sans Condensed / JetBrains Mono / IBM Plex Serif (all OFL, apt: fonts-ibm-plex,
# fonts-jetbrains-mono). Scene code keeps using the names below (AMBER = "the accent").
THEME = os.environ.get("SIPHON_THEME", "")
if THEME == "ep002":
    BG = (0x0E / 255, 0x1A / 255, 0x1D / 255)
    AMBER = (0x3E / 255, 0xE0 / 255, 0xD0 / 255)
    INK = (0xE4 / 255, 0xEF / 255, 0xEE / 255)
    GREY = (0x7C / 255, 0x93 / 255, 0x96 / 255)
    DIM = (0x1E / 255, 0x30 / 255, 0x33 / 255)
    RED = (0xFF / 255, 0x4D / 255, 0x5E / 255)
    HEAD = "IBM Plex Sans Condensed"
    MONO = "JetBrains Mono"
    SERIF = "IBM Plex Serif"
# SIPHON_THEME=ep003 (Coldcard, "inside the vault"): graphite-steel background with faint brushed-metal
# streaks, the slowly turning rings of a combination dial in a corner and a sparse field of flickering
# points (randomness), entropy-green accent, Inter / Fira Code / Noto Serif (OFL, apt: fonts-inter,
# fonts-firacode, fonts-noto-core).
elif THEME == "ep003":
    BG = (0x10 / 255, 0x13 / 255, 0x16 / 255)
    AMBER = (0x3F / 255, 0xE6 / 255, 0xA0 / 255)
    INK = (0xEC / 255, 0xEF / 255, 0xF1 / 255)
    GREY = (0x8A / 255, 0x94 / 255, 0x9C / 255)
    DIM = (0x1E / 255, 0x24 / 255, 0x28 / 255)
    RED = (0xFF / 255, 0x5A / 255, 0x4E / 255)
    HEAD = "Inter"
    MONO = "Fira Code"
    SERIF = "Noto Serif"


# --- easing ------------------------------------------------------------------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp(x)
    return 3 * x * x - 2 * x * x * x


def prog(t, start, dur):
    return clamp((t - start) / dur) if dur > 0 else float(t >= start)


def fade_io(t, d, fi=0.35, fo=0.35):
    return min(prog(t, 0, fi), 1 - prog(t, d - fo, fo))


# --- drawing helpers ---------------------------------------------------------
def rgba(ctx, c, a=1.0):
    ctx.set_source_rgba(c[0], c[1], c[2], a)


def font(ctx, face=HEAD, size=60, bold=True, italic=False):
    ctx.select_font_face(face, cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def text(ctx, s, x, y, color=INK, a=1.0, align="left", face=HEAD, size=60, bold=True,
         italic=False, tracking=0.0):
    """Draw s with its baseline at y. align: left|center|right. Returns width."""
    font(ctx, face, size, bold, italic)
    if tracking:
        widths = [ctx.text_extents(ch).x_advance + tracking for ch in s]
        w = sum(widths) - tracking
    else:
        w = ctx.text_extents(s).x_advance
    x0 = x - w / 2 if align == "center" else x - w if align == "right" else x
    rgba(ctx, color, a)
    if tracking:
        cx = x0
        for ch, cw in zip(s, widths):
            ctx.move_to(cx, y)
            ctx.show_text(ch)
            cx += cw
    else:
        ctx.move_to(x0, y)
        ctx.show_text(s)
    return w


def text_width(ctx, s, face=HEAD, size=60, bold=True):
    font(ctx, face, size, bold)
    return ctx.text_extents(s).x_advance


def wrap(ctx, s, max_w, face=HEAD, size=60, bold=True):
    font(ctx, face, size, bold)
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if ctx.text_extents(trial).x_advance > max_w and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def source_tag(ctx, s, a=1.0):
    """Small source reference, bottom-left (editorial policy: every claim sourced)."""
    text(ctx, s, 80, H - 60, GREY, 0.85 * a, face=MONO, size=24, bold=False)


def siphon_mark(ctx, cx, cy, scale, a=1.0, draw_drop=1.0):
    """The channel mark (S + drop), drawn from brand/mark.svg geometry (800x800 box)."""
    ctx.save()
    ctx.translate(cx - 400 * scale, cy - 400 * scale)
    ctx.scale(scale, scale)
    rgba(ctx, AMBER, a)
    ctx.set_line_width(84)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(516, 236)
    ctx.curve_to(452, 186, 286, 192, 286, 298)
    ctx.curve_to(286, 396, 522, 390, 522, 490)
    ctx.curve_to(522, 596, 356, 602, 292, 552)
    ctx.stroke()
    if draw_drop > 0:
        ctx.translate(0, (1 - draw_drop) * -60)
        rgba(ctx, AMBER, a * draw_drop)
        ctx.move_to(400, 630)
        ctx.curve_to(368, 676, 356, 700, 356, 716)
        ctx.arc_negative(400, 716, 44, math.pi, 0)
        ctx.curve_to(444, 700, 432, 676, 400, 630)
        ctx.close_path()
        ctx.fill()
    ctx.restore()


# --- finishing layers (vignette + film grain), built once per process ---------
_FINISH = {}


def _finish_layers():
    """Soft vignette + fine full-resolution dither (±1-2 levels). The dither is what keeps the
    dark gradients smooth (no banding) after compression; it is far too fine to read as grain."""
    if _FINISH:
        return _FINISH
    import numpy as np
    vig = cairo.ImageSurface(cairo.FORMAT_ARGB32, OW, OH)
    c = cairo.Context(vig)
    g = cairo.RadialGradient(OW / 2, OH / 2, OH * 0.45, OW / 2, OH / 2, OH * 1.1)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.30)
    c.set_source(g)
    c.paint()
    _FINISH["vignette"] = vig
    dith = []
    for k in range(1):  # one static pattern: smooth gradients without costing bitrate every frame
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, OW, OH)
        stride = s.get_stride()
        rng = np.random.default_rng(k)
        white = rng.random((OH, OW)) < 0.5
        al = 5  # premultiplied: white at alpha 5 or black at alpha 5 -> about ±1 level
        arr = np.zeros((OH, stride // 4, 4), dtype=np.uint8)
        arr[:, :OW, 0] = arr[:, :OW, 1] = arr[:, :OW, 2] = np.where(white, al, 0)
        arr[:, :OW, 3] = al
        s.get_data()[:] = arr.tobytes()
        s.mark_dirty()
        dith.append(s)
    _FINISH["dither"] = dith
    return _FINISH


def finish(ctx, frame_idx):
    f = _finish_layers()
    ctx.save()
    ctx.identity_matrix()
    ctx.set_source_surface(f["vignette"], 0, 0)
    ctx.paint()
    ctx.set_source_surface(f["dither"][frame_idx % len(f["dither"])], 0, 0)
    ctx.paint()
    ctx.restore()


def backdrop(ctx, t):
    """ep002 backdrop: faint 60 px surveillance grid, brighter every 5th line, a soft scan band drifting
    down every ~9 s and four thin corner marks (like a monitor in the security office)."""
    ctx.save()
    ctx.set_line_width(1)
    for k, x in enumerate(range(0, W + 1, 60)):
        ctx.set_source_rgba(AMBER[0], AMBER[1], AMBER[2], 0.06 if k % 5 == 0 else 0.025)
        ctx.move_to(x + 0.5, 0)
        ctx.line_to(x + 0.5, H)
        ctx.stroke()
    for k, y in enumerate(range(0, H + 1, 60)):
        ctx.set_source_rgba(AMBER[0], AMBER[1], AMBER[2], 0.06 if k % 5 == 0 else 0.025)
        ctx.move_to(0, y + 0.5)
        ctx.line_to(W, y + 0.5)
        ctx.stroke()
    y = (t / 9.0 % 1.0) * (H + 300) - 150
    g = cairo.LinearGradient(0, y - 150, 0, y + 150)
    g.add_color_stop_rgba(0, AMBER[0], AMBER[1], AMBER[2], 0)
    g.add_color_stop_rgba(0.5, AMBER[0], AMBER[1], AMBER[2], 0.035)
    g.add_color_stop_rgba(1, AMBER[0], AMBER[1], AMBER[2], 0)
    ctx.set_source(g)
    ctx.rectangle(0, y - 150, W, 300)
    ctx.fill()
    ctx.set_source_rgba(AMBER[0], AMBER[1], AMBER[2], 0.35)
    ctx.set_line_width(2)
    for cx, cy, dx, dy in ((40, 40, 1, 1), (W - 40, 40, -1, 1), (40, H - 40, 1, -1), (W - 40, H - 40, -1, -1)):
        ctx.move_to(cx, cy + dy * 36)
        ctx.line_to(cx, cy)
        ctx.line_to(cx + dx * 36, cy)
        ctx.stroke()
    ctx.restore()


_VAULT = {}


def backdrop_vault(ctx, t):
    """ep003 backdrop: brushed-steel streaks (static), the rings and ticks of a combination dial turning
    very slowly in the lower right, and a sparse field of points that flicker at random (entropy)."""
    import random as _r
    if "streaks" not in _VAULT:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        c = cairo.Context(s)
        rnd = _r.Random(3)
        for _ in range(420):
            y = rnd.uniform(0, H)
            x = rnd.uniform(-200, W)
            ln = rnd.uniform(120, 900)
            c.set_source_rgba(1, 1, 1, rnd.uniform(0.006, 0.02))
            c.set_line_width(rnd.uniform(0.6, 1.6))
            c.move_to(x, y)
            c.line_to(x + ln, y)
            c.stroke()
        _VAULT["streaks"] = s
        rp = _r.Random(11)
        _VAULT["pts"] = [(rp.uniform(0, W), rp.uniform(0, H), rp.uniform(0.3, 2.0), rp.uniform(0, 6.28)) for _ in range(90)]
    ctx.save()
    ctx.set_source_surface(_VAULT["streaks"], 0, 0)
    ctx.paint()
    cx, cy = W - 170, H + 40
    ctx.set_line_width(1.2)
    for k, r in enumerate((300, 360, 430, 520)):
        ctx.set_source_rgba(AMBER[0], AMBER[1], AMBER[2], 0.05 if k != 1 else 0.08)
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        ctx.stroke()
    ang = t * 0.035
    for i in range(100):
        a0 = ang + i * 2 * math.pi / 100
        r0, r1 = (360, 380) if i % 10 else (350, 392)
        ctx.set_source_rgba(AMBER[0], AMBER[1], AMBER[2], 0.10 if i % 10 == 0 else 0.05)
        ctx.move_to(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0))
        ctx.line_to(cx + r1 * math.cos(a0), cy + r1 * math.sin(a0))
        ctx.stroke()
    for x, y, hz, ph in _VAULT["pts"]:
        k = math.sin(t * hz + ph)
        if k > 0.55:
            ctx.set_source_rgba(AMBER[0], AMBER[1], AMBER[2], 0.25 * (k - 0.55) / 0.45)
            ctx.rectangle(x, y, 2, 2)
            ctx.fill()
    ctx.restore()


# --- rendering ---------------------------------------------------------------
_TIMELINE = None


def _render_frame(i):
    t = i / FPS
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, OW, OH)
    ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    ctx.scale(SCALE, SCALE)
    rgba(ctx, BG)
    ctx.paint()
    if THEME == "ep002":
        backdrop(ctx, t)
    elif THEME == "ep003":
        backdrop_vault(ctx, t)
    for start, end, fn, params in _TIMELINE:
        if start <= t < end:
            ctx.save()
            fn(ctx, t - start, end - start, **params)
            ctx.restore()
    finish(ctx, i)
    surf.flush()
    return bytes(surf.get_data())


def _init(timeline):
    global _TIMELINE
    _TIMELINE = timeline
    _finish_layers()


def _render_segment(job):
    """One worker renders a contiguous frame range straight into its own MP4 (low memory)."""
    a, b, path = job
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
           # 10-bit H.264 (High 10): no banding in dark gradients; YouTube accepts it.
           # BT.709 tags so Macs/Retina show the intended colours and gamma.
           "-vf", "scale=out_color_matrix=bt709:out_range=tv",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p10le",
           "-profile:v", "high10", "-colorspace", "bt709", "-color_primaries", "bt709",
           "-color_trc", "bt709", "-color_range", "tv", "-threads", "2", path]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(a, b):
        ff.stdin.write(_render_frame(i))
    ff.stdin.close()
    ff.wait()
    return path


def render(timeline, total, out_path, audio=None, workers=None, frames=None, seg_seconds=10):
    """timeline: list of (start, end, draw_fn, params). Writes an H.264 MP4 (with audio if given).
    Frames are rendered in ~10 s segments in parallel, then concatenated without re-encoding."""
    n = int(round(total * FPS))
    a0, b0 = (frames.start, frames.stop) if frames is not None else (0, n)
    import tempfile
    tmp = tempfile.mkdtemp(prefix="siphon_parts_")  # outside the project folder
    step = seg_seconds * FPS
    jobs = [(a, min(a + step, b0), os.path.join(tmp, f"seg_{k:04d}.mp4"))
            for k, a in enumerate(range(a0, b0, step))]
    default_workers = 2 if SCALE >= 2 else max(1, (os.cpu_count() or 2) - 1)  # 4K frames need RAM
    with Pool(workers or default_workers, initializer=_init,
              initargs=(timeline,)) as pool:
        parts = pool.map(_render_segment, jobs, chunksize=1)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{os.path.abspath(p)}'\n" for p in parts)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst]
    if audio:
        cmd += ["-ss", str(a0 / FPS), "-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac",
                "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "copy", "-movflags", "+faststart", out_path]
    subprocess.run(cmd, check=True)
    for p in parts:
        os.remove(p)
    os.remove(lst)
    os.rmdir(tmp)
    return out_path


def still(timeline, t, png_path):
    _init(timeline)
    data = _render_frame(int(t * FPS))
    surf = cairo.ImageSurface.create_for_data(bytearray(data), cairo.FORMAT_ARGB32, OW, OH)
    surf.write_to_png(png_path)
    return png_path
