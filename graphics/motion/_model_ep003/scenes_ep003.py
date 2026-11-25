"""Scene templates for ep. 003 (Coldcard). Own look: graphite steel, entropy-green accent (AMBER = the
accent colour of the theme), red only for theft. Same engine and helpers as scenes.py."""
import math
import random

import cairo

from engine import (W, H, AMBER, INK, GREY, DIM, RED, HEAD, MONO, SERIF,
                    clamp, ease_out, ease_in_out, prog, fade_io, rgba, text, text_width,
                    wrap, rrect, source_tag)
from scenes import _panel
from scenes import (quote_card as S_quote_card, explainer as S_explainer, statement as S_statement,
                    countdown as S_countdown, big_number as S_big_number)

STEEL = (0.62, 0.68, 0.74)


def _label(ctx, s, x, y, a, col=GREY, size=26, align="left"):
    text(ctx, s, x, y, col, a, align=align, face=MONO, size=size, bold=False, tracking=6)


def chapter(ctx, t, d, title, kicker="CHAPTER", number=None):
    """Chapter break: a steel plate slides in, the kicker in mono, the title, a dial tick that turns."""
    a = fade_io(t, d, 0.25, 0.3)
    p = ease_out(prog(t, 0.05, 0.7))
    size = 84
    while size > 52 and text_width(ctx, title, HEAD, size) > 1180:
        size -= 2
    pw = max(1040, text_width(ctx, title, HEAD, size) + 160)
    _panel(ctx, W / 2 - pw / 2, 380 + (1 - p) * 30, pw, 330, a * p, 10)
    _label(ctx, kicker, W / 2, 470, a, AMBER, 28, "center")
    text(ctx, title, W / 2, 590 + (1 - p) * 10, INK, a * p, align="center", size=size)
    cx, cy, r = W / 2, 660, 16
    ang = -math.pi / 2 + ease_out(prog(t, 0.3, 1.2)) * math.pi * 1.5
    rgba(ctx, AMBER, a)
    ctx.set_line_width(3)
    ctx.new_path()
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.stroke()
    ctx.new_path()
    ctx.move_to(cx, cy)
    ctx.line_to(cx + r * 0.8 * math.cos(ang), cy + r * 0.8 * math.sin(ang))
    ctx.stroke()
    if number:
        _label(ctx, number, W / 2 + pw / 2 - 40, 420, a, GREY, 24, "right")


def seed_card(ctx, t, d, n=24, source=None):
    """A blank recovery-sheet with numbered lines; the words stay blurred bars (never readable)."""
    a = fade_io(t, d)
    p = ease_out(prog(t, 0, 0.6))
    x0, y0, w, h = 460, 150 + (1 - p) * 30, 1000, 760
    rgba(ctx, (0.88, 0.89, 0.86), 0.95 * a * p)
    rrect(ctx, x0, y0, w, h, 8)
    ctx.fill()
    text(ctx, "RECOVERY WORDS", x0 + 60, y0 + 80, (0.12, 0.14, 0.16), a * p, face=MONO, size=30, tracking=6)
    rnd = random.Random(5)
    for i in range(n):
        col, row = i // 12, i % 12
        x = x0 + 60 + col * 470
        y = y0 + 150 + row * 50
        q = prog(t, 0.4 + i * 0.05, 0.3)
        text(ctx, f"{i + 1:02d}", x, y, (0.35, 0.38, 0.42), a * q, face=MONO, size=24, bold=False)
        bw = rnd.uniform(130, 260)
        g = cairo.LinearGradient(x + 60, 0, x + 60 + bw, 0)
        g.add_color_stop_rgba(0, 0.15, 0.17, 0.2, 0.0)
        g.add_color_stop_rgba(0.15, 0.15, 0.17, 0.2, 0.55 * a * q)
        g.add_color_stop_rgba(0.85, 0.15, 0.17, 0.2, 0.55 * a * q)
        g.add_color_stop_rgba(1, 0.15, 0.17, 0.2, 0.0)
        ctx.set_source(g)
        rrect(ctx, x + 60, y - 18, bw, 18, 9)
        ctx.fill()
    _label(ctx, "ILLUSTRATIVE · WORDS HIDDEN", x0 + w, y0 + h + 50, a * 0.9, GREY, 22, "right")
    if source:
        source_tag(ctx, source, a)


def rng_switch(ctx, t, d, flip_at=1.5, zero_at=None, source=None):
    """'seed generation' asks for randomness; one setting routes it to the hardware generator or to a
    simple software substitute. At flip_at the switch shows 0 and the arrow goes to the substitute."""
    a = fade_io(t, d)
    on = t >= flip_at
    k = ease_in_out(prog(t, flip_at, 0.5))
    # source box
    _panel(ctx, 160, 470, 420, 150, a, 12)
    _label(ctx, "SEED GENERATION", 370, 535, a, INK, 26, "center")
    _label(ctx, "needs random numbers", 370, 580, a, GREY, 20, "center")
    # switch
    cx, cy = 820, 545
    _panel(ctx, cx - 110, cy - 90, 220, 180, a, 14)
    _label(ctx, "SETTING", cx, cy - 100 - 14, a, GREY, 20, "center")
    val = "0" if on else "?"
    text(ctx, val, cx, cy + 42, RED if on else GREY, a, align="center", face=MONO, size=120)
    # targets
    hw = (1340, 330)
    sw = (1340, 760)
    for (x, y), name, sub, col, lit in ((hw, "HARDWARE RANDOM GENERATOR", "built for the job", AMBER, not on),
                                         (sw, "SOFTWARE SUBSTITUTE", "factory ID + timers", GREY, on)):
        _panel(ctx, x - 20, y - 85, 560, 170, a * (1 if lit else 0.55), 12)
        _label(ctx, name, x + 260, y - 10, a * (1 if lit else 0.6), col if lit else GREY, 22, "center")
        _label(ctx, sub, x + 260, y + 35, a * (1 if lit else 0.5), GREY, 20, "center")
    # wires
    ctx.set_line_width(5)
    rgba(ctx, INK, 0.5 * a)
    ctx.new_path()
    ctx.move_to(580, 545)
    ctx.line_to(cx - 110, cy)
    ctx.stroke()
    ty = hw[1] + (sw[1] - hw[1]) * k
    col = AMBER if k < 0.5 else RED
    rgba(ctx, col, a)
    ctx.move_to(cx + 110, cy)
    ctx.curve_to(cx + 260, cy, 1180, ty, hw[0] - 20, ty)
    ctx.stroke()
    ctx.move_to(hw[0] - 40, ty - 14)
    ctx.line_to(hw[0] - 20, ty)
    ctx.line_to(hw[0] - 40, ty + 14)
    ctx.stroke()
    if zero_at is not None and t >= zero_at:
        q = prog(t, zero_at, 0.5)
        text(ctx, "Zero means: use the substitute.", W / 2, 990, INK, a * q, align="center", size=46)
    if source:
        source_tag(ctx, source, a)


def code_guard(ctx, t, d, pass_at=2.5, source=None):
    """The safety check in the build: it only asks whether the setting exists. It does (= 0), so it passes."""
    a = fade_io(t, d)
    _panel(ctx, 330, 230, 1260, 520, a, 14)
    _label(ctx, "BUILD CHECK · ILLUSTRATIVE EXCEPT THE QUOTED LINE", 360, 205, a, GREY, 20)
    rows = [("#ifndef  RNG_SETTING", GREY), ('#error  "get a HW TRNG plz"', AMBER), ("#endif", GREY)]
    for i, (s, c) in enumerate(rows):
        n = int(len(s) * clamp((t - 0.3 - i * 0.5) / 0.6))
        text(ctx, s[:n], 400, 360 + i * 90, c, a, face=MONO, size=46, bold=False)
    q = prog(t, pass_at, 0.4)
    if q > 0:
        _label(ctx, "SETTING EXISTS?", 400, 690, a * q, GREY, 26)
        text(ctx, "YES  (= 0)", 760, 692, INK, a * q, face=MONO, size=34)
        rgba(ctx, AMBER, a * q)
        rrect(ctx, 1240, 640, 300, 70, 10)
        ctx.fill()
        text(ctx, "PASSED", 1390, 690, (0.05, 0.08, 0.08), a * q, align="center", face=MONO, size=36)
    if source:
        source_tag(ctx, source, a)


def bits_compare(ctx, t, d, source=None):
    """40 bits against a proper seed's 128: the bars to scale make the gap obvious."""
    a = fade_io(t, d)
    rows = [("MK2 / MK3 · AFFECTED", 40, RED, 0.2), ("NEWER MODELS · AFFECTED", 72, (1.0, 0.7, 0.35), 0.9),
            ("A PROPER SEED · AT LEAST", 128, AMBER, 1.6)]
    for i, (name, bits, col, at) in enumerate(rows):
        q = ease_out(prog(t, at, 0.9))
        y = 330 + i * 190
        _label(ctx, name, 260, y, a * prog(t, at, 0.3), GREY, 24)
        w = 1300 * bits / 128 * q
        rgba(ctx, col, 0.9 * a)
        rrect(ctx, 260, y + 30, max(w, 2), 56, 8)
        ctx.fill()
        text(ctx, f"{int(bits * q)} bits", 260 + w + 30, y + 75, INK, a * prog(t, at, 0.3), face=MONO, size=44)
    if source:
        source_tag(ctx, source, a)


def sweep(ctx, t, d, n_total=1196, blocks=(960183, 960191), clock=("01:10", "01:51"), source=None,
          collectors=3):
    """The first wave: rows of addresses drain into a few collector points while a block counter and an
    address counter run. Positions are illustrative; counts and block range are from the sources."""
    a = fade_io(t, d)
    u = clamp(t / max(d * 0.85, 0.1))
    rnd = random.Random(9)
    cols, rows = 46, 18
    x0, y0, sx, sy = 120, 210, 26, 34
    done = int(cols * rows * u)
    order = list(range(cols * rows))
    rnd.shuffle(order)
    gone = set(order[:done])
    cx = [W - 260]
    cys = [330 + i * 220 for i in range(collectors)]
    for i in range(cols * rows):
        c, r = i % cols, i // cols
        x, y = x0 + c * sx, y0 + r * sy
        if i in gone:
            rgba(ctx, RED, 0.25 * a)
        else:
            rgba(ctx, AMBER, 0.75 * a)
        ctx.rectangle(x, y, 12, 12)
        ctx.fill()
    # streaks: recently drained boxes fly to a collector
    for k in range(max(0, done - 40), done):
        i = order[k]
        c, r = i % cols, i // cols
        x, y = x0 + c * sx + 6, y0 + r * sy + 6
        ty = cys[i % collectors]
        f = (done - k) / 40.0
        px, py = x + (cx[0] - x) * (1 - f), y + (ty - y) * (1 - f)
        rgba(ctx, RED, 0.5 * a * f)
        ctx.set_line_width(2)
        ctx.new_path()
        ctx.move_to(x, y)
        ctx.line_to(px, py)
        ctx.stroke()
    for y in cys:
        rgba(ctx, RED, 0.85 * a)
        ctx.new_path()
        ctx.arc(cx[0], y, 22 + 6 * math.sin(t * 4), 0, 2 * math.pi)
        ctx.fill()
    blk = int(blocks[0] + (blocks[1] - blocks[0]) * u)
    _label(ctx, f"BLOCK {blk:,}", 120, 150, a, GREY, 26)
    _label(ctx, f"{clock[0]} → {clock[1]} UTC", W - 120, 150, a, GREY, 26, "right")
    text(ctx, f"{int(n_total * u):,} addresses emptied", 120, 900, INK, a, size=52)
    _label(ctx, "POSITIONS ILLUSTRATIVE", W - 120, 900, a * 0.8, GREY, 20, "right")
    if source:
        source_tag(ctx, source, a)


def balance_lines(ctx, t, d, times=("9:36 PM", "9:39 PM", "9:43 PM"), total="≈ C$1.6 million",
                  starts=(0.6, 2.0, 3.4), source=None):
    """Three wallet balance lines on a dark screen turn red one after another (ILLUSTRATIVE)."""
    a = fade_io(t, d)
    _panel(ctx, 360, 200, 1200, 640, a, 16)
    _label(ctx, "WALLET VIEW · ILLUSTRATIVE", 400, 180, a, GREY, 20)
    for i, (tm, st) in enumerate(zip(times, starts)):
        y = 330 + i * 170
        q = prog(t, st, 0.5)
        col = RED if q > 0 else INK
        _label(ctx, f"WALLET {i + 1}", 420, y, a, GREY, 24)
        val = "0.00000000 BTC" if q >= 1 else "•••••• BTC"
        text(ctx, val, 1500, y + 6, col, a, align="right", face=MONO, size=48)
        if q > 0:
            _label(ctx, f"OUT · {tm}", 420, y + 50, a * q, RED, 22)
            rgba(ctx, RED, 0.25 * a * q)
            ctx.rectangle(400, y + 70, 1120 * q, 3)
            ctx.fill()
    if t > starts[-1] + 0.8:
        text(ctx, total, W / 2, 960, INK, a * prog(t, starts[-1] + 0.8, 0.5), align="center", face=MONO, size=58)
    if source:
        source_tag(ctx, source, a)


def tx_pattern(ctx, t, d, rows=7, highlight_at=1.0, title="WAVE 1 · EVERY TRANSACTION", source=None):
    """Identical rows: same fee rate, no change output. The repeating columns light up."""
    a = fade_io(t, d)
    _label(ctx, title, 260, 230, a, AMBER, 26)
    heads = ("TX", "INPUTS", "FEE RATE", "CHANGE BACK")
    xs = (260, 620, 980, 1360)
    for x, h in zip(xs, heads):
        _label(ctx, h, x, 300, a, GREY, 22)
    rnd = random.Random(4)
    q = prog(t, highlight_at, 0.6)
    for i in range(rows):
        y = 370 + i * 80
        p = prog(t, 0.15 + i * 0.12, 0.3)
        tx = "".join(rnd.choice("0123456789abcdef") for _ in range(8)) + "…"
        text(ctx, tx, xs[0], y, INK, a * p, face=MONO, size=34, bold=False)
        text(ctx, str(rnd.randint(1, 9)), xs[1], y, INK, a * p, face=MONO, size=34, bold=False)
        text(ctx, "same", xs[2], y, AMBER if q > 0 else INK, a * p, face=MONO, size=34)
        text(ctx, "none", xs[3], y, AMBER if q > 0 else INK, a * p, face=MONO, size=34)
    if q > 0:
        for x in (xs[2], xs[3]):
            rgba(ctx, AMBER, 0.6 * a * q)
            ctx.set_line_width(2)
            rrect(ctx, x - 24, 330, 260, rows * 80 + 20, 10)
            ctx.stroke()
    _label(ctx, "LAYOUT ILLUSTRATIVE · PATTERN PER GALAXY RESEARCH", W - 160, 990, a * 0.8, GREY, 20, "right")
    if source:
        source_tag(ctx, source, a)


def waves(ctx, t, d, source=None, total_at=None):
    """Four waves on a day axis, 30 Jul to 3 Aug: wave 1 big and still, later waves smaller."""
    a = fade_io(t, d)
    days = ("THU 30 JUL", "FRI 31 JUL", "SAT 1 AUG", "SUN 2 AUG", "MON 3 AUG")
    x0, x1, y = 220, W - 220, 760
    rgba(ctx, GREY, 0.6 * a)
    ctx.rectangle(x0, y, x1 - x0, 2)
    ctx.fill()
    for i, dd in enumerate(days):
        x = x0 + (x1 - x0) * i / 4
        _label(ctx, dd, x, y + 50, a, GREY, 20, "center")
    bars = [(0.02, 1.0, "WAVE 1", RED), (0.27, 0.45, "WAVE 2", (1.0, 0.55, 0.45)),
            (0.45, 0.35, "WAVE 3", (1.0, 0.55, 0.45)), (0.98, 0.3, "WAVE 4", (1.0, 0.55, 0.45))]
    for i, (fx, h, name, col) in enumerate(bars):
        q = ease_out(prog(t, 0.3 + i * 0.6, 0.6))
        x = x0 + (x1 - x0) * fx
        hh = 420 * h * q
        rgba(ctx, col, 0.85 * a)
        rrect(ctx, x - 40, y - hh, 80, hh, 6)
        ctx.fill()
        _label(ctx, name, x, y - hh - 20, a * q, INK, 22, "center")
    if total_at is not None and t >= total_at:
        q = prog(t, total_at, 0.5)
        text(ctx, "≈ 1,816 BTC · 5,200+ addresses", W / 2, 220, INK, a * q, align="center", face=MONO, size=52)
    _label(ctx, "HEIGHTS NOT TO SCALE", W - 220, 900, a * 0.7, GREY, 18, "right")
    if source:
        source_tag(ctx, source, a)


def rbf_race(ctx, t, d, replace_at=2.0, source=None):
    """A waiting transaction gets replaced by one paying a higher fee: the bait comes back."""
    a = fade_io(t, d)
    _label(ctx, "WAITING TO BE CONFIRMED", W / 2, 260, a, GREY, 24, "center")
    q = ease_in_out(prog(t, replace_at, 0.8))
    for k, (who, fee, col, y) in enumerate((("THIEF'S BOT", "fee: low", RED, 420), ("OWNER", "fee: higher", AMBER, 640))):
        vis = 1.0 if k == 0 else prog(t, replace_at - 0.6, 0.5)
        x = 460 + (k == 0) * 0 - (k == 0) * 600 * q
        al = a * vis * (1 - 0.85 * q if k == 0 else 1)
        _panel(ctx, x, y - 70, 1000, 140, al, 12)
        _label(ctx, who, x + 40, y - 5, al, col, 26)
        _label(ctx, fee, x + 40, y + 40, al, GREY, 22)
        text(ctx, "bait", x + 960, y + 20, INK, al, align="right", face=MONO, size=40, bold=False)
    if q >= 1:
        text(ctx, "Replaced. He wins the bait back.", W / 2, 900, INK, a * prog(t, replace_at + 0.8, 0.5),
             align="center", size=48)
    _label(ctx, "ILLUSTRATIVE", W - 160, 990, a * 0.7, GREY, 18, "right")
    if source:
        source_tag(ctx, source, a)


def lookup_log(ctx, t, d, match_at=2.5, source=None):
    """Left: guesses being looked up (the attack). Right: a provider's request log. They line up."""
    a = fade_io(t, d)
    rnd = random.Random(12)
    _label(ctx, "THE ATTACK · LOOKUPS", 220, 230, a, GREY, 22)
    _label(ctx, "A PAID DATA ACCOUNT · LOG", 1060, 230, a, GREY, 22)
    q = prog(t, match_at, 0.6)
    for i in range(10):
        y = 300 + i * 62
        p = prog(t, 0.2 + i * 0.12, 0.3)
        addr = "bc1q" + "".join(rnd.choice("acdefghjkmnpqrstuvwxyz023456789") for _ in range(10)) + "…"
        text(ctx, addr, 220, y, INK, a * p, face=MONO, size=30, bold=False)
        text(ctx, f"req {1000 + i * 7:,} · 01:0{i % 10}", 1060, y, INK, a * p, face=MONO, size=30, bold=False)
        if q > 0:
            rgba(ctx, AMBER, 0.45 * a * q)
            ctx.set_line_width(2)
            ctx.new_path()
            ctx.move_to(760, y - 10)
            ctx.line_to(1040, y - 10)
            ctx.stroke()
    if q > 0:
        text(ctx, "“with extraordinary specificity”", W / 2, 1000, AMBER, a * q, align="center",
             face=SERIF, size=46, italic=True)
    _label(ctx, "ILLUSTRATIVE", W - 120, 180, a * 0.7, GREY, 18, "right")
    if source:
        source_tag(ctx, source, a)


def status_board(ctx, t, d, rows, title="STATUS AS OF LATE NOVEMBER 2026", source=None):
    """The dated status card (rule 14a): what is known and not known as the video is made."""
    a = fade_io(t, d)
    _panel(ctx, 320, 200, 1280, 160 + len(rows) * 110, a, 14)
    _label(ctx, title, W / 2, 280, a, AMBER, 30, "center")
    for i, (k, v) in enumerate(rows):
        p = prog(t, 0.4 + i * 0.35, 0.4)
        y = 400 + i * 110
        _label(ctx, k, 380, y, a * p, GREY, 24)
        text(ctx, v, 1540, y + 4, INK, a * p, align="right", size=40)
    if source:
        source_tag(ctx, source, a)


def dice_finale(ctx, t, d, line="At least 50 dice rolls of their own.", source=None):
    """Dice tumble in, land, and the line appears: the owners the bug couldn't reach."""
    a = fade_io(t, d)
    rnd = random.Random(21)
    for i in range(9):
        x = 560 + i * 100 + rnd.uniform(-20, 20)
        land = 0.2 + i * 0.12
        q = ease_out(prog(t, land, 0.6))
        y = 300 + 260 * q + rnd.uniform(-20, 20)
        ang = (1 - q) * rnd.uniform(-3, 3)
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(ang)
        rgba(ctx, (0.93, 0.94, 0.92), a)
        rrect(ctx, -36, -36, 72, 72, 12)
        ctx.fill()
        rgba(ctx, (0.1, 0.12, 0.14), a)
        n = rnd.randint(1, 6)
        pos = {1: [(0, 0)], 2: [(-14, -14), (14, 14)], 3: [(-16, -16), (0, 0), (16, 16)],
               4: [(-15, -15), (15, -15), (-15, 15), (15, 15)],
               5: [(-15, -15), (15, -15), (0, 0), (-15, 15), (15, 15)],
               6: [(-15, -16), (15, -16), (-15, 0), (15, 0), (-15, 16), (15, 16)]}[n]
        for px, py in pos:
            ctx.new_path()
            ctx.arc(px, py, 6, 0, 2 * math.pi)
            ctx.fill()
        ctx.restore()
    q = prog(t, 1.6, 0.6)
    text(ctx, line, W / 2, 830, INK, a * q, align="center", size=56)
    if source:
        source_tag(ctx, source, a)


# ---------------- one-off designs (24 Nov 2026): no graphic design is used twice ----------------

def devices_offline(ctx, t, d, n=3, source=None):
    """Teaser: an open safe-deposit box seen from above, three plain devices inside, each with a crossed-out
    signal icon. Generic shapes, no brand."""
    a = fade_io(t, d)
    p = ease_out(prog(t, 0, 0.3))
    bx, by, bw, bh = 470, 260 + (1 - p) * 30, 980, 520
    rgba(ctx, STEEL, 0.55 * a)
    ctx.set_line_width(4)
    rrect(ctx, bx, by, bw, bh, 18)
    ctx.stroke()
    rgba(ctx, (0.09, 0.11, 0.13), 0.9 * a)
    rrect(ctx, bx + 12, by + 12, bw - 24, bh - 24, 12)
    ctx.fill()
    for i in range(n):
        q = ease_out(prog(t, 0.15 + i * 0.25, 0.4))
        dx = bx + 110 + i * 290
        dy = by + 130 + (1 - q) * 40
        rgba(ctx, (0.22, 0.25, 0.28), a * q)
        rrect(ctx, dx, dy, 200, 280, 16)
        ctx.fill()
        rgba(ctx, (0.05, 0.07, 0.08), a * q)
        rrect(ctx, dx + 24, dy + 26, 152, 92, 6)
        ctx.fill()
        for k in range(3):
            for j in range(3):
                rgba(ctx, (0.3, 0.33, 0.36), a * q)
                ctx.new_path()
                ctx.arc(dx + 55 + j * 45, dy + 160 + k * 36, 11, 0, 2 * math.pi)
                ctx.fill()
        # crossed signal arcs above each device
        cx, cy = dx + 100, dy - 40
        rgba(ctx, GREY, 0.8 * a * q)
        ctx.set_line_width(3)
        for r in (14, 26, 38):
            ctx.new_path()
            ctx.arc(cx, cy + 20, r, math.pi * 1.25, math.pi * 1.75)
            ctx.stroke()
        rgba(ctx, RED, a * prog(t, 1.2 + i * 0.25, 0.25))
        ctx.set_line_width(4)
        ctx.new_path()
        ctx.move_to(cx - 36, cy - 14)
        ctx.line_to(cx + 36, cy + 26)
        ctx.stroke()
    _label(ctx, "NEVER CONNECTED TO THE INTERNET", W / 2, by + bh + 90, a * prog(t, 2.0, 0.4), AMBER, 28, "center")
    _label(ctx, "ILLUSTRATIVE", bx + bw, by - 24, a * 0.7, GREY, 18, "right")
    if source:
        source_tag(ctx, source, a)


def code_age(ctx, t, d, start="MARCH 2021", end="JULY 2026", source=None):
    """Teaser: a year ruler; a marker sits on 2021 while the 'today' line slides to 2026."""
    a = fade_io(t, d)
    x0, x1, y = 260, W - 260, 600
    years = list(range(2021, 2027))
    rgba(ctx, GREY, 0.5 * a)
    ctx.rectangle(x0, y, x1 - x0, 2)
    ctx.fill()
    for i, yr in enumerate(years):
        x = x0 + (x1 - x0) * i / (len(years) - 1)
        rgba(ctx, GREY, 0.7 * a)
        ctx.rectangle(x - 1, y - 18, 2, 36)
        ctx.fill()
        _label(ctx, str(yr), x, y + 70, a, GREY, 24, "center")
    mx = x0 + (x1 - x0) * (2 / 12) / 5
    rgba(ctx, RED, a)
    rrect(ctx, mx - 70, y - 190, 140, 110, 10)
    ctx.fill()
    text(ctx, "{ }", mx, y - 118, (0.08, 0.05, 0.05), a, align="center", face=MONO, size=44)
    rgba(ctx, RED, 0.8 * a)
    ctx.rectangle(mx - 1, y - 80, 2, 80)
    ctx.fill()
    _label(ctx, start, mx, y - 220, a, RED, 22, "center")
    u = ease_in_out(prog(t, 0.4, max(d - 1.2, 0.6)))
    nx = mx + (x0 + (x1 - x0) * (4 + 7 / 12) / 5 - mx) * u
    rgba(ctx, AMBER, 0.25 * a)
    ctx.rectangle(mx, y - 8, nx - mx, 16)
    ctx.fill()
    rgba(ctx, AMBER, a)
    ctx.rectangle(nx - 2, y - 60, 4, 120)
    ctx.fill()
    if u > 0.95:
        _label(ctx, end, nx, y - 90, a * prog(t, d - 1.0, 0.4), AMBER, 22, "center")
    text(ctx, "In public code. In plain sight.", W / 2, 860, INK, a * prog(t, 0.8, 0.5), align="center",
         face=SERIF, size=48, italic=True)
    if source:
        source_tag(ctx, source, a)


def model_cards(ctx, t, d, source=None):
    """Ring gauges: MK2/MK3 ≈40 bits, newer models ≈72 bits, a proper seed 128+ (arcs to scale of 128)."""
    a = fade_io(t, d)
    items = [("MK2 / MK3", 40, RED, "≈ 40 BITS", ""),
             ("NEWER MODELS", 72, (1.0, 0.7, 0.35), "≈ 72 BITS", "NO PUBLIC EVIDENCE OF DRAINING · SO FAR"),
             ("A PROPER SEED", 128, AMBER, "128+ BITS", "")]
    for i, (name, bits, col, val, note) in enumerate(items):
        cx, cy, r = 400 + i * 560, 520, 170
        q = ease_out(prog(t, 0.3 + i * 0.5, 1.0))
        rgba(ctx, DIM, a)
        ctx.set_line_width(26)
        ctx.new_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        ctx.stroke()
        rgba(ctx, col, 0.95 * a)
        ctx.new_path()
        ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * min(bits, 128) / 128 * q)
        ctx.stroke()
        text(ctx, val, cx, cy + 16, INK, a * prog(t, 0.3 + i * 0.5, 0.4), align="center", face=MONO, size=40)
        _label(ctx, name, cx, cy + r + 80, a, GREY, 24, "center")
        if note:
            _label(ctx, note, cx, cy + r + 125, a * prog(t, 1.6, 0.5), INK, 17, "center")
    if source:
        source_tag(ctx, source, a)


def wave_clock(ctx, t, d, start_min=10, end_min=51, n_total=1196, source=None):
    """A clock face from 9:10 to 9:51 PM Toronto (01:10–01:51 UTC): the arc of the first wave fills,
    the counter runs to ~1,200 addresses."""
    a = fade_io(t, d)
    cx, cy, r = 700, 540, 300
    rgba(ctx, STEEL, 0.35 * a)
    ctx.set_line_width(3)
    ctx.new_path()
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.stroke()
    for m in range(60):
        ang = -math.pi / 2 + 2 * math.pi * m / 60
        L = 26 if m % 5 == 0 else 10
        rgba(ctx, GREY, 0.7 * a)
        ctx.set_line_width(3 if m % 5 == 0 else 1.5)
        ctx.new_path()
        ctx.move_to(cx + (r - L) * math.cos(ang), cy + (r - L) * math.sin(ang))
        ctx.line_to(cx + r * math.cos(ang), cy + r * math.sin(ang))
        ctx.stroke()
    u = ease_in_out(prog(t, 0.2, max(d * 0.8, 0.5)))
    a0 = -math.pi / 2 + 2 * math.pi * start_min / 60
    a1 = a0 + 2 * math.pi * (end_min - start_min) / 60 * u
    rgba(ctx, RED, 0.35 * a)
    ctx.new_path()
    ctx.move_to(cx, cy)
    ctx.arc(cx, cy, r - 40, a0, a1)
    ctx.close_path()
    ctx.fill()
    rgba(ctx, RED, a)
    ctx.set_line_width(5)
    ctx.new_path()
    ctx.move_to(cx, cy)
    ctx.line_to(cx + (r - 50) * math.cos(a1), cy + (r - 50) * math.sin(a1))
    ctx.stroke()
    mins = int(start_min + (end_min - start_min) * u)
    text(ctx, f"9:{mins:02d} PM", 1180, 420, INK, a, face=MONO, size=72)
    _label(ctx, "TORONTO · 01:10 → 01:51 UTC", 1180, 480, a, GREY, 22)
    text(ctx, f"{int(n_total * u):,}", 1180, 660, RED, a, face=MONO, size=96)
    _label(ctx, "ADDRESSES EMPTIED · WAVE 1", 1180, 720, a, GREY, 22)
    if source:
        source_tag(ctx, source, a)


def fee_scatter(ctx, t, d, title="NO ONE ELSE USED IT · THE MONTH BEFORE", source=None):
    """Fee rates of ordinary transactions over the month before scatter freely; wave 1 sits alone on one line."""
    a = fade_io(t, d)
    x0, x1, y0, y1 = 220, W - 220, 260, 860
    rgba(ctx, GREY, 0.5 * a)
    ctx.rectangle(x0, y1, x1 - x0, 2)
    ctx.fill()
    ctx.rectangle(x0, y0, 2, y1 - y0)
    ctx.fill()
    _label(ctx, "FEE RATE", x0 - 20, y0 - 20, a, GREY, 20)
    _label(ctx, "JULY 2026 →", x1, y1 + 50, a, GREY, 20, "right")
    rnd = random.Random(21)
    line_y = y0 + (y1 - y0) * 0.37
    for i in range(420):
        x = x0 + 20 + rnd.random() * (x1 - x0 - 200)
        y = y0 + 20 + rnd.random() * (y1 - y0 - 40)
        if abs(y - line_y) < 14:
            continue
        q = prog(t, 0.1 + i * 0.0025, 0.3)
        rgba(ctx, GREY, 0.45 * a * q)
        ctx.new_path()
        ctx.arc(x, y, 4, 0, 2 * math.pi)
        ctx.fill()
    q = prog(t, 1.0, 0.6)
    rgba(ctx, AMBER, 0.35 * a * q)
    ctx.rectangle(x0, line_y - 1, x1 - x0, 2)
    ctx.fill()
    for i in range(36):
        x = x1 - 170 + (i % 6) * 22
        rgba(ctx, RED, a * prog(t, 1.2 + i * 0.02, 0.2))
        ctx.new_path()
        ctx.arc(x, line_y + ((i // 6) - 2.5) * 3, 6, 0, 2 * math.pi)
        ctx.fill()
    _label(ctx, "WAVE 1", x1 - 110, line_y - 40, a * q, RED, 22, "center")
    _label(ctx, title, W / 2, 200, a, AMBER, 26, "center")
    _label(ctx, "POSITIONS ILLUSTRATIVE", W - 220, 980, a * 0.7, GREY, 18, "right")
    if source:
        source_tag(ctx, source, a)


def wallet_check(ctx, t, d, total="Gone since Wednesday night.", source=None):
    """A phone in portrait: the wallet app refreshes and shows three empty wallets."""
    a = fade_io(t, d)
    p = ease_out(prog(t, 0, 0.6))
    px, py, pw, ph = W / 2 - 230, 120 + (1 - p) * 40, 460, 840
    rgba(ctx, (0.06, 0.07, 0.08), a)
    rrect(ctx, px, py, pw, ph, 54)
    ctx.fill()
    rgba(ctx, STEEL, 0.4 * a)
    ctx.set_line_width(3)
    rrect(ctx, px, py, pw, ph, 54)
    ctx.stroke()
    sx, sy, sw = px + 30, py + 80, pw - 60
    spin = prog(t, 0.4, 0.9)
    if spin < 1:
        rgba(ctx, AMBER, a)
        ctx.set_line_width(5)
        ctx.new_path()
        ang = t * 6
        ctx.arc(W / 2, sy + 300, 40, ang, ang + 4.2)
        ctx.stroke()
        _label(ctx, "REFRESHING…", W / 2, sy + 400, a, GREY, 18, "center")
    else:
        for i in range(3):
            q = prog(t, 1.3 + i * 0.25, 0.3)
            y = sy + 60 + i * 170
            rgba(ctx, (0.12, 0.14, 0.16), a * q)
            rrect(ctx, sx, y, sw, 140, 18)
            ctx.fill()
            _label(ctx, f"WALLET {i + 1}", sx + 24, y + 44, a * q, GREY, 18)
            text(ctx, "0.00000000", sx + 24, y + 104, RED, a * q, face=MONO, size=40)
            _label(ctx, "BTC", sx + sw - 24, y + 104, a * q, GREY, 18, "right")
    _label(ctx, "ILLUSTRATIVE", px + pw + 30, py + 60, a * 0.7, GREY, 18)
    text(ctx, total, W / 2, py + ph + 70, INK, a * prog(t, 2.3, 0.5), align="center", face=SERIF, size=46,
         italic=True)
    if source:
        source_tag(ctx, source, a)


def coin_stack(ctx, t, d, total=1816, addrs="from 5,200+ addresses", source=None):
    """A single stack of coins rises while the counter climbs to the total; the addresses line follows."""
    a = fade_io(t, d)
    u = ease_out(prog(t, 0.2, max(d * 0.6, 0.6)))
    cx, base = 640, 900
    n = int(46 * u)
    for i in range(n):
        y = base - i * 14
        rgba(ctx, (0.55, 0.42, 0.18), a)
        ctx.save()
        ctx.translate(cx, y)
        ctx.scale(1, 0.28)
        ctx.new_path()
        ctx.arc(0, 0, 150, 0, 2 * math.pi)
        ctx.restore()
        ctx.fill()
        rgba(ctx, (0.85, 0.68, 0.3), a)
        ctx.save()
        ctx.translate(cx, y - 6)
        ctx.scale(1, 0.28)
        ctx.new_path()
        ctx.arc(0, 0, 150, 0, 2 * math.pi)
        ctx.restore()
        ctx.fill()
    text(ctx, f"≈ {int(total * u):,} BTC", 1000, 520, INK, a, face=MONO, size=96)
    _label(ctx, "TAKEN IN ALL WAVES", 1000, 580, a, GREY, 22)
    text(ctx, addrs, 1000, 700, RED, a * prog(t, 0.2 + d * 0.6, 0.5), face=MONO, size=40)
    if source:
        source_tag(ctx, source, a)


# ---------------- format cards: every instance gets its own layout (24 Nov 2026) ----------------

def _mono(ctx, s, x, y, a, col=GREY, size=28, align="left", track=6):
    text(ctx, s, x, y, col, a, align=align, face=MONO, size=size, bold=False, tracking=track)


def _bar(ctx, x, y, w, h, a, col=AMBER):
    rgba(ctx, col, a)
    ctx.rectangle(x, y, w, h)
    ctx.fill()


def _fit(ctx, s, face, size, max_w, bold=True, lo=40):
    while size > lo and text_width(ctx, s, face, size) > max_w:
        size -= 2
    return size


def chapter_v(ctx, t, d, title, kicker, v=0):
    """Six different chapter breaks."""
    if v == 0:
        return chapter(ctx, t, d, title, kicker)
    a = fade_io(t, d, 0.25, 0.3)
    p = ease_out(prog(t, 0.05, 0.7))
    if v == 1:      # left aligned, tall emerald bar, title rises
        _bar(ctx, 220, 380, 8, 300 * p, a)
        _mono(ctx, kicker, 270, 450, a, AMBER, 28)
        sz = _fit(ctx, title, HEAD, 110, 1400)
        text(ctx, title, 270, 600 + (1 - p) * 30, INK, a * p, size=sz)
    elif v == 2:    # typewriter title in mono, caret, kicker under a ruled line
        n = int(len(title) * clamp(prog(t, 0.1, 0.9)))
        sz = _fit(ctx, title, MONO, 88, 1500)
        text(ctx, title[:n] + ("▌" if int(t * 3) % 2 == 0 else ""), W / 2, 560, INK, a, align="center",
             face=MONO, size=sz)
        _bar(ctx, W / 2 - 400 * p, 620, 800 * p, 2, a * 0.6, GREY)
        _mono(ctx, kicker, W / 2, 680, a * prog(t, 0.6, 0.4), AMBER, 26, "center")
    elif v == 3:    # dial ring on the left, text on the right
        cx, cy, r = 470, H / 2, 170
        rgba(ctx, STEEL, 0.5 * a)
        ctx.set_line_width(4)
        ctx.new_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        ctx.stroke()
        rgba(ctx, AMBER, a)
        ctx.set_line_width(10)
        ctx.new_path()
        ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * p)
        ctx.stroke()
        _mono(ctx, kicker, 760, 470, a, AMBER, 26)
        sz = _fit(ctx, title, HEAD, 104, 1050)
        text(ctx, title, 760, 600, INK, a * p, size=sz)
    elif v == 4:    # a row of box doors slides apart to reveal the title
        gap = 520 * p
        for side in (-1, 1):
            for k in range(4):
                x = W / 2 + side * (gap / 2 + k * 150) - (140 if side < 0 else 0)
                rgba(ctx, (0.17, 0.19, 0.21), a)
                rrect(ctx, x, 360, 140, 360, 6)
                ctx.fill()
                rgba(ctx, STEEL, 0.4 * a)
                ctx.new_path()
                ctx.arc(x + 70, 540, 10, 0, 2 * math.pi)
                ctx.fill()
        sz = _fit(ctx, title, HEAD, 80, max(gap - 40, 200))
        text(ctx, title, W / 2, 560, INK, a * p, align="center", size=sz)
        _mono(ctx, kicker, W / 2, 800, a * p, AMBER, 24, "center")
    else:           # bracketed kicker top-left, large serif italic title, a scan line
        _mono(ctx, f"[ {kicker} ]", 180, 300, a, AMBER, 26)
        sz = _fit(ctx, title, SERIF, 120, 1560)
        text(ctx, title, 180, 600, INK, a * p, face=SERIF, size=sz, italic=True)
        y = 280 + (H - 400) * clamp(t / max(d, 0.1))
        _bar(ctx, 0, y, W, 2, 0.25 * a)


def quote_v(ctx, t, d, quote, who, source, v=0):
    """Seven different quote cards."""
    if v == 0:
        return S_quote_card(ctx, t, d, quote, who, source)
    a = fade_io(t, d, 0.25, 0.25)
    p = ease_out(prog(t, 0, 0.8))
    if v == 1:      # centred, thin frame
        lines = wrap(ctx, quote, 1300, SERIF, 80, True)
        h = len(lines) * 104 + 200
        y0 = H / 2 - h / 2
        rgba(ctx, STEEL, 0.5 * a)
        ctx.set_line_width(2)
        rrect(ctx, W / 2 - 760, y0, 1520, h, 4)
        ctx.stroke()
        for i, ln in enumerate(lines):
            text(ctx, ln, W / 2, y0 + 130 + i * 104, INK, a * p, align="center", face=SERIF, size=80, italic=True)
        _mono(ctx, who, W / 2, y0 + h + 60, a * prog(t, 0.4, 0.5), GREY, 24, "center")
    elif v == 2:    # right aligned, vertical bar on the right
        lines = wrap(ctx, quote, 1200, SERIF, 86, True)
        for i, ln in enumerate(lines):
            text(ctx, ln, W - 300, 430 + i * 112, INK, a * p, align="right", face=SERIF, size=86, italic=True)
        _bar(ctx, W - 250, 360, 6, (len(lines) * 112 + 40) * p, a)
        _mono(ctx, who, W - 300, 430 + len(lines) * 112 + 40, a, GREY, 24, "right")
    elif v == 3:    # transcript panel, typed in mono
        _panel(ctx, 260, 300, W - 520, 480, a, 10)
        _mono(ctx, "TRANSCRIPT · " + who, 300, 280, a, GREY, 20)
        n = int(len(quote) * clamp(prog(t, 0.2, max(d * 0.5, 0.6))))
        lines = wrap(ctx, quote[:n], W - 640, MONO, 56, False)
        for i, ln in enumerate(lines):
            text(ctx, ln, 320, 420 + i * 80, AMBER, a, face=MONO, size=56, bold=False)
    elif v == 4:    # who as kicker on top, words appear one by one
        _mono(ctx, who, 220, 330, a, AMBER, 24)
        words = quote.split()
        k = int(len(words) * clamp(prog(t, 0.2, max(d * 0.5, 0.6)))) + 1
        lines = wrap(ctx, " ".join(words[:k]), 1480, HEAD, 96, True)
        for i, ln in enumerate(lines):
            text(ctx, ln, 220, 480 + i * 120, INK, a, size=96)
    elif v == 5:    # light paper card with dark serif text
        lines = wrap(ctx, quote, 1100, SERIF, 76, True)
        h = len(lines) * 100 + 220
        x0, y0 = W / 2 - 680, H / 2 - h / 2 + (1 - p) * 30
        rgba(ctx, (0.88, 0.89, 0.86), 0.95 * a)
        rrect(ctx, x0, y0, 1360, h, 6)
        ctx.fill()
        for i, ln in enumerate(lines):
            text(ctx, ln, x0 + 100, y0 + 130 + i * 100, (0.1, 0.12, 0.14), a, face=SERIF, size=76, italic=True)
        text(ctx, "— " + who, x0 + 100, y0 + h - 50, (0.35, 0.38, 0.42), a, face=MONO, size=22, bold=False)
    else:           # huge single line, centred low, with a sweeping underline
        sz = _fit(ctx, quote, SERIF, 120, W - 300)
        text(ctx, quote, W / 2, 600, INK, a * p, align="center", face=SERIF, size=sz, italic=True)
        _bar(ctx, W / 2 - 300, 650, 600 * ease_out(prog(t, 0.4, 0.8)), 4, a)
        _mono(ctx, who, W / 2, 730, a * prog(t, 0.6, 0.4), GREY, 24, "center")
    if source:
        source_tag(ctx, source, a)


def explainer_v(ctx, t, d, name, lines, source=None, v=0):
    """Seven different explainer cards. lines = [(at, text), ...]."""
    if v == 0:
        return S_explainer(ctx, t, d, name, lines, source)
    a = fade_io(t, d)
    p = ease_out(prog(t, 0.1, 0.7))
    if v == 1:      # folder tab
        x0, y0, w, h = 300, 340, W - 600, 120 + len(lines) * 90 + 60
        rgba(ctx, AMBER, a)
        tw = text_width(ctx, name, MONO, 28) + 60
        rrect(ctx, x0, y0 - 56, tw, 70, 8)
        ctx.fill()
        text(ctx, name, x0 + 30, y0 - 10, (0.05, 0.08, 0.08), a, face=MONO, size=28)
        _panel(ctx, x0, y0, w, h, a, 8)
        for i, (at, ln) in enumerate(lines):
            text(ctx, ln, x0 + 60, y0 + 110 + i * 90, INK, a * ease_out(prog(t, at, 0.5)), size=52)
    elif v == 2:    # two columns: name left, facts right with ticks
        sz = _fit(ctx, name, HEAD, 84, 700)
        for k, part in enumerate(wrap(ctx, name, 700, HEAD, sz, True)):
            text(ctx, part, 200, 470 + k * (sz + 14), INK, a * p, size=sz)
        _bar(ctx, 960, 360, 2, 400, a * 0.5, GREY)
        y = 470
        for i, (at, ln) in enumerate(lines):
            q = ease_out(prog(t, at, 0.5))
            _mono(ctx, "✓", 1020, y, a * q, AMBER, 40, track=0)
            for k, part in enumerate(wrap(ctx, ln, W - 1080 - 160, HEAD, 44, True)):
                text(ctx, part, 1080, y + k * 56, INK, a * q, size=44)
                last = k
            y += 56 * (last + 1) + 50
    elif v == 3:    # vertical timeline with nodes
        _mono(ctx, name, 300, 300, a, AMBER, 30)
        _bar(ctx, 320, 360, 3, 100 + len(lines) * 140 * p, a * 0.6, GREY)
        for i, (at, ln) in enumerate(lines):
            q = ease_out(prog(t, at, 0.5))
            y = 420 + i * 140
            rgba(ctx, AMBER, a * q)
            ctx.new_path()
            ctx.arc(321, y, 14, 0, 2 * math.pi)
            ctx.fill()
            text(ctx, ln, 380, y + 18, INK, a * q, size=56)
    elif v == 4:    # centred name, facts as pills
        sz = _fit(ctx, name, HEAD, 100, 1600)
        text(ctx, name, W / 2, 420, INK, a * p, align="center", size=sz)
        for i, (at, ln) in enumerate(lines):
            q = ease_out(prog(t, at, 0.5))
            tw = text_width(ctx, ln, MONO, 34) + 80
            y = 540 + i * 110
            rgba(ctx, (0.13, 0.17, 0.17), a * q)
            rrect(ctx, W / 2 - tw / 2, y, tw, 76, 38)
            ctx.fill()
            text(ctx, ln, W / 2, y + 50, AMBER, a * q, align="center", face=MONO, size=34, bold=False)
    elif v == 5:    # numbered steps, big numerals
        sz = _fit(ctx, name, HEAD, 56, 1500)
        text(ctx, name, 220, 300, INK, a * p, size=sz)
        for i, (at, ln) in enumerate(lines):
            q = ease_out(prog(t, at, 0.5))
            y = 470 + i * 160
            text(ctx, f"{i + 1:02d}", 220, y + 20, AMBER, a * q, face=MONO, size=96)
            text(ctx, ln, 420, y, INK, a * q, size=54)
    else:           # terminal: name as a comment, facts printed as output
        _panel(ctx, 220, 260, W - 440, 560, a, 10)
        text(ctx, "# " + name, 270, 340, GREY, a, face=MONO, size=30, bold=False)
        for i, (at, ln) in enumerate(lines):
            q = prog(t, at, 0.4)
            n = int(len(ln) * q)
            text(ctx, "> " + ln[:n], 270, 440 + i * 80, AMBER, a, face=MONO, size=46, bold=False)
    if source:
        source_tag(ctx, source, a)


def statement_v(ctx, t, d, line, color=INK, v=0):
    """Four different single-line statements."""
    if v == 0:
        return S_statement(ctx, t, d, line, color)
    rgba(ctx, (0, 0, 0))
    ctx.paint()
    a = fade_io(t, d, 0.5, 0.05)
    if v == 1:
        sz = _fit(ctx, line, HEAD, 64, W - 400)
        text(ctx, line, 200, H / 2 + 20, color, a, size=sz)
        _bar(ctx, 200, H / 2 + 60, 120, 4, a)
    elif v == 2:
        sz = _fit(ctx, line.upper(), MONO, 40, W - 300)
        _mono(ctx, line.upper(), W / 2, H / 2, a, color, sz, "center", 10)
    else:
        sz = _fit(ctx, line, SERIF, 60, W - 400)
        text(ctx, line, W / 2, H - 260, color, a, align="center", face=SERIF, size=sz, italic=True)
        _bar(ctx, W / 2 - 60, H - 220, 120, 2, a * 0.7, GREY)


def countdown_v(ctx, t, d, label, sub=None, v=0):
    """Three different T-minus cards."""
    if v == 0:
        return S_countdown(ctx, t, d, label, sub)
    a = fade_io(t, d, 0.15, 0.25)
    if v == 1:      # flip-clock tiles
        _mono(ctx, "T-MINUS", W / 2, 360, a, AMBER, 36, "center", 14)
        chars = list(label)
        tw = 130 if len(chars) <= 8 else 104
        widths = [(tw + 16) if ch != " " else 50 for ch in chars]
        x = W / 2 - sum(widths) / 2 - widths[0]
        for i, ch in enumerate(chars):
            x += widths[i - 1] if i else widths[0]
            if ch == " ":
                continue
            q = prog(t, 0.1 + i * 0.08, 0.25)
            rgba(ctx, (0.15, 0.17, 0.19), a)
            rrect(ctx, x, 420, tw, 200, 10)
            ctx.fill()
            _bar(ctx, x, 519, tw, 2, a, (0.06, 0.07, 0.08))
            text(ctx, ch, x + tw / 2, 580, INK, a * q, align="center", face=MONO, size=130)
        if sub:
            _mono(ctx, sub, W / 2, 720, a * prog(t, 0.5, 0.4), GREY, 26, "center")
    else:           # dial: a hand sweeps to zero, label inside
        cx, cy, r = W / 2, H / 2 - 20, 260
        rgba(ctx, STEEL, 0.4 * a)
        ctx.set_line_width(3)
        ctx.new_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        ctx.stroke()
        u = ease_in_out(prog(t, 0.1, max(d - 0.6, 0.5)))
        rgba(ctx, AMBER, a)
        ctx.set_line_width(8)
        ctx.new_path()
        ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * (1 - u) + 0.001)
        ctx.stroke()
        _mono(ctx, "T-MINUS", cx, cy - 70, a, AMBER, 30, "center", 12)
        sz = _fit(ctx, label, MONO, 140, 420)
        text(ctx, label, cx, cy + 50, INK, a, align="center", face=MONO, size=sz)
        if sub:
            _mono(ctx, sub, cx, cy + r + 80, a * prog(t, 0.4, 0.4), GREY, 24, "center")


def big_number_v(ctx, t, d, value, prefix="$", suffix="+", caption="", count_for=1.2, source=None,
                 decimals=0, v=0):
    """Three different big-number cards."""
    if v == 0:
        return S_big_number(ctx, t, d, value, prefix, suffix, caption, count_for, source, decimals)
    a = fade_io(t, d, 0.2, 0.4)
    val = value * ease_out(prog(t, 0, count_for))
    s = f"{prefix}{val:,.{decimals}f}{suffix if t >= count_for else ''}"
    if v == 1:      # left number, caption block under an amber bar
        sz = _fit(ctx, s, MONO, 170, 1500)
        text(ctx, s, 200, 540, INK, a, face=MONO, size=sz)
        _bar(ctx, 200, 600, 260 * ease_out(prog(t, count_for, 0.5)), 6, a)
        _mono(ctx, caption.upper(), 200, 680, a * prog(t, count_for, 0.5), GREY, 26)
    else:           # number stamped inside a ring
        cx, cy = W / 2, H / 2 - 20
        q = ease_out(prog(t, 0, 0.5))
        rgba(ctx, RED, 0.85 * a)
        ctx.set_line_width(8)
        ctx.new_path()
        ctx.arc(cx, cy, 300 * (1.3 - 0.3 * q), 0, 2 * math.pi)
        ctx.stroke()
        sz = _fit(ctx, s, MONO, 140, 520)
        text(ctx, s, cx, cy + 45, INK, a, align="center", face=MONO, size=sz)
        _mono(ctx, caption, cx, cy + 380, a * prog(t, count_for, 0.5), GREY, 24, "center")
    if source:
        source_tag(ctx, source, a)
