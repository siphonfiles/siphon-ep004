"""Episode 003 (Coldcard) visuals, cut to the sound timeline from sound/ep003/ep003_mix.py.

Usage:
  python3 ep003.py <timeline.json> <audio|none> <out.mp4> [--still T out.png ...] [--from S --to E]
Scenes are anchored on the voice-line ids, so a new audio mix re-times the picture automatically.

Thomas: only ever as moving video (rule 18b). Every Thomas line has a non-Thomas picture underneath
(illustration / card); the LongCat clips listed in presenter/clips/inputs/ep003_clip_plan.json are laid
over it when their frames exist (presenter/clips/frames/<name>/*.png at 30 fps). A clip that was not
generated simply leaves the picture underneath.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
import scenes as S  # noqa: E402
import scenes_ep003 as E  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
THOMAS_REF = os.path.join(ROOT, "presenter", "reference", "thomas_ref_ep003_1920x1080.png")   # ep. 003 outfit (olive shirt)
if not os.path.exists(THOMAS_REF):
    THOMAS_REF = os.path.join(ROOT, "presenter", "reference", "thomas_ref_v1_centered_1920x1080.png")
S.ILL_DIR = os.path.join(ROOT, "illustrations", "ep003", "img")
CLIPS = os.path.join(ROOT, "presenter", "clips", "frames")
CLIP_PLAN = os.path.join(ROOT, "presenter", "clips", "inputs", "ep003_clip_plan.json")
CLOSE = (1.3, 960.0, 440.0)          # second camera: the same moving clip, tighter
FIT720 = dict(scale=1920 / 1312, ox=0.0, oy=25.0)   # 720p LongCat frame laid over the reference (ep. 001)

WARM = (1.0, 0.72, 0.35)
REDL = (1.0, 0.15, 0.12)
COOL = (0.55, 0.75, 1.0)


def thomas_shots(tl):
    """[(a, b, frames_dir, clip_t0, camera)] for every generated clip. clip_t0 = episode time of frame 0."""
    if not os.path.exists(CLIP_PLAN):
        return []
    v = {e["id"]: (e["t"], e["t"] + e["dur"]) for e in tl["events"] if e["kind"] == "voice"}
    out = []
    for c in json.load(open(CLIP_PLAN))["clips"]:
        fr = os.path.join(CLIPS, c["name"])
        if not (os.path.isdir(fr) and any(f.endswith(".png") for f in os.listdir(fr))):
            continue
        if c["first"] not in v or c["last"] not in v:
            continue
        t0 = v[c["first"]][0] - c["lead"]
        a = v[c["first"]][0] - min(c["lead"], 0.35)
        b = v[c["last"]][1] + c.get("tail", 0.35)
        cut = c.get("close_from")           # second camera from this line on
        if cut and cut in v:
            k = v[cut][0] - 0.12
            out += [(a, k, fr, t0, "M"), (k, b, fr, t0, "C")]
        else:
            out.append((a, b, fr, t0, c.get("camera", "M")))
    # back-to-back Thomas lines: cut cleanly at the next shot's start instead of overlapping
    out.sort(key=lambda x: x[0])
    for i in range(len(out) - 1):
        if out[i][1] > out[i + 1][0]:
            out[i] = (out[i][0], out[i + 1][0]) + out[i][2:]
    return out


def _clip_len(fr):
    return len([f for f in os.listdir(fr) if f.endswith(".png")]) / 30.0


def _absorb_slivers(T, shots):
    """A scene left with < 1 s right after a shot would flash (e.g. 1:23). Hold the shot over it instead,
    as long as the clip still has frames there."""
    shots = [list(x) for x in shots]
    for a, b, fn, p in T:
        for sh in shots:
            sa, sb, fr, t0 = sh[0], sh[1], sh[2], sh[3]
            if a < sb < b and b - sb < 1.0 and not any(o[0] <= sb < o[1] for o in shots if o is not sh):
                n = _clip_len(fr)
                if b <= t0 + (n if n > 1 else 5.0) - 0.02:
                    sh[1] = b
    return [tuple(x) for x in shots]


def overlay_thomas(T, shots):
    """Cut the shots into the picture: what they cover is removed; a scene resuming after a shot continues
    where it was. Slivers under 1 s right after a shot are covered by holding the shot (no flash)."""
    shots = _absorb_slivers(T, shots)
    out = []
    for a, b, fn, p in T:
        pieces = [(a, b)]
        for sa, sb, *_ in shots:
            nxt = []
            for pa, pb in pieces:
                if sb <= pa or sa >= pb:
                    nxt.append((pa, pb))
                    continue
                if pa < sa:
                    nxt.append((pa, sa))
                if sb < pb:
                    nxt.append((sb, pb))
            pieces = nxt
        for pa, pb in pieces:
            if pb - pa < 1.0 and (pa, pb) != (a, b):
                fill = S.black if fn is S.black else fn
                out.append((pa, pb, _off(fill, pa - a), p))   # keep continuity, it is short anyway
            elif pa == a:
                out.append((pa, pb, fn, p))
            else:
                out.append((pa, pb, _off(fn, pa - a), p))
    first = min((x[0] for x in shots), default=None)
    for a, b, fr, t0, cam in shots:
        clip = dict(frames=fr, start=t0 - a, **FIT720)
        lt = 0.6 if a == first else 99     # name card on his first appearance only
        out.append((a, b, S.presenter, dict(image_path=THOMAS_REF, lower_third_at=lt, clip=clip,
                                             zoom=CLOSE if cam == "C" else None)))
    return out


def _off(fn, off):
    def g(ctx, t, d, **p):
        return fn(ctx, t + off, d + off, **p)
    return g


_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "illustrations", "ep003", "img")


def pick(new, old):
    """New Kaggle illustration if it (and its depth map) is in the repo, otherwise the old one."""
    ok = all(os.path.exists(os.path.join(_IMG, f)) for f in (f"{new}.jpg", f"{new}_depth.png"))
    return new if ok else old


EMERALD = (0.25, 0.90, 0.63)
PALE = (0.80, 0.88, 1.0)


def _have(name):
    return all(os.path.exists(os.path.join(_IMG, f)) for f in (f"{name}.jpg", f"{name}_depth.png"))


def build(tl):
    ev = tl["events"]
    v = {e["id"]: (e["t"], e["t"] + e["dur"]) for e in ev if e["kind"] == "voice"}
    hits = [e["t"] for e in ev if e["kind"] == "hit"]
    cards = [e["t"] for e in ev if e["kind"] == "card"]
    total = tl["total"]
    T = []

    def add(a, b, fn, **p):
        if b - a > 0.02:
            T.append((a, b, fn, p))

    def IL(a, b, name, move="in", fallback=None, **p):
        """Illustration if it is in the repo; otherwise a plain text statement (never an empty frame)."""
        if _have(name):
            T.append((a, b, S.illus, dict(name=name, move=move, **p)))
        else:
            line = fallback or p.get("statement") or p.get("line") or p.get("kicker") or " "
            add(a, b, S.statement, line=line, color=S.GREY)

    def s(k):
        return v[k][0]

    def e(k):
        return v[k][1]

    def frac(k, f):
        return v[k][0] + f * (v[k][1] - v[k][0])

    C = iter(cards)
    LAMP = dict(kind="flicker", color=WARM, base=0.28)
    PALEB = dict(kind="flicker", color=PALE, base=0.22)
    DUSTBEAM = dict(kind="beam", poly=[(820, 0), (1060, 0), (1260, 1152), (620, 1152)], color=(0.85, 0.92, 1.0), base=0.10)

    # ---------------- TEASER ----------------
    c0 = next(C)
    DEV = s("t1") + 3.55  # "three small devices" (t1 starts with "A bank vault. A safe-deposit box. Inside it,")
    IL(0.0, DEV, "c01_vault_night", "in", fi=0.6, fo=0.0, warm=False, glows=[DUSTBEAM],
       flick=dict(lights=[dict(x=320, y=416, r=520, thr=0.6, amb=0.45)], depth=0.3, seed=1),
       fog=dict(density=0.18, color=(0.45, 0.52, 0.6), speed=8, floor=0.4), fallback="A bank vault.")
    add(DEV, s("t2"), E.devices_offline)
    IL(s("t2"), s("t3"), "c02_drawer_keyhole", "in", fo=0.0, warm=False, kicker="29 JULY · NIGHT",
       line="Nobody opened the box.", glows=[dict(PALEB, x=1020, y=560, r=260)])
    c1 = next(C)
    add(s("t3"), c1, S.kinetic, line="In seven minutes, the bitcoin they protected was gone.",
        highlight=("seven", "gone."), source="[S12][S13]")
    add(c1, s("t4"), S.black)
    add(s("t4"), s("t5"), E.big_number_v, v=0, value=116_000_000, suffix="", caption="taken the same way · within five days",
        count_for=1.4, source="[S7][S8]")
    add(s("t5"), s("t6"), E.code_age, source="[S4]")
    IL(s("t6"), nxt_after(hits, e("t6")), "c26_footprint_snow", "in", fo=0.0, warm=False, motes=False, snow=True,
       statement="One mistake of their own.")
    h = nxt_after(hits, e("t6"))
    c2 = next(C)                                  # title, on the sub drop
    add(h, c2, S.black)
    add(c2, s("i1"), S.title_card, title="NOBODY TOUCHED IT")

    # ---------------- THOMAS (intro) — picture underneath, clips laid over ----------------
    add(s("i1"), s("i2"), E.statement_v, v=1, line="Thomas Archer · the AI narrator of Siphon Files", color=S.GREY)
    add(s("i2"), s("i3"), E.statement_v, v=2, line="Every claim has a source. They're all in the description.", color=S.GREY)
    IL(s("i3"), s("i4"), "c06_vault_corridor_walk", "in", statement="A lock that nobody picked.")
    c3 = next(C)                                  # chapter card after the intro
    IL(s("i4"), c3, "c07_combination_dial", "in", statement="Somebody worked out the combination.",
       glows=[dict(LAMP, x=1024, y=300, r=300)])

    # ---------------- THE MAN WHO DID EVERYTHING RIGHT ----------------
    add(c3, s("a1"), E.chapter_v, v=0, title="The man who did everything right", kicker="TORONTO")
    IL(s("a1"), s("a2"), "c04_city_lake_night", "right", kicker="JONATHAN GOODMAN · TORONTO",
       line="More than $1 million in bitcoin, by his own account.", source="[S13]",
       motes=False)
    IL(s("a2"), s("a3"), "c03_devices_tray", "in", kicker="COLDCARD · COINKITE · CANADA",
       line="Never connected to the internet.", glows=[dict(PALEB, x=1024, y=420, r=380)])
    add(s("a3"), s("a4"), E.seed_card, n=24)
    IL(s("a4"), s("a5"), "c05_stamping_metal", "in", kicker="THREE DEVICES · THREE WALLETS",
       line="Words stamped into metal. Locked in a bank.", source="[S13][S30]",
       glows=[dict(LAMP, x=1024, y=500, r=320)])
    IL(s("a5"), nxt_after(cards, e("a5")), "c34_tiles_spilling", "in",
       statement="How were those words chosen?")

    # ---------------- THE COMBINATION ----------------
    c5 = next(C)
    add(c5, s("b1"), E.chapter_v, v=1, title="The combination", kicker="HOW A SEED IS MADE")
    IL(s("b1"), s("b2"), "c11_dice_midair", "in", kicker="PURE CHANCE",
       line="Hardware built for one job: randomness.", warm=False)
    IL(s("b2"), nxt_after(cards, e("b2")), "c12_endless_boxes", "out", kicker="DONE PROPERLY",
       flick=dict(lights=[dict(x=788, y=570, r=150, thr=0.45, amb=0.6)], mode="slow", depth=0.55, seed=6),
       line="Too many possibilities to ever search.", warm=False,
       fog=dict(density=0.25, color=(0.45, 0.52, 0.6), speed=10, far=0.5))
    c6 = next(C)
    add(c6, s("b3"), E.countdown_v, v=0, label="5Y 4M", sub="MARCH 2021 · FIRMWARE UPDATE")
    add(s("b3"), nxt_after(cards, e("b3")), E.explainer_v, v=0, name="MARCH 2021",
        lines=[(0.5, "New firmware"), (1.6, "The cryptography Bitcoin Core uses")], source="[S1][S2]")
    c7 = next(C)
    add(c7, s("b4"), E.quote_v, v=0, quote="The cryptographic choice was sound. The integration was not.",
        who="COINKITE · TECHNICAL WRITE-UP", source="[S2]")
    add(s("b4"), s("b6"), E.rng_switch, flip_at=s("b5") - s("b4") + 0.8, zero_at=frac("b5", 0.6) - s("b4"),
        source="[S2][S4]")
    c8 = next(C)
    add(s("b6"), s("b8"), E.code_guard, pass_at=s("b7") - s("b6") + 0.4, source="[S4]")
    IL(s("b8"), nxt_after(cards, e("b10")), "c10_smoke_alarm", "up", kicker="THE INSPECTOR",
       line="The alarm is there. Nobody checks it's on.", warm=False,
       glows=[dict(kind="pulse", x=1024, y=560, r=120, color=(1.0, 0.2, 0.15), min=0.0, max=0.05, hz=0.2)])

    # ---------------- FIVE YEARS ----------------
    c9 = next(C)
    add(c9, s("c1"), E.chapter_v, v=2, title="Five years", kicker="MARCH 2021 → JULY 2026")
    IL(s("c1"), s("c2"), "c08_idle_chip", "in", kicker="MK2 · MK3", line="Words from the substitute.",
       warm=False, glows=[dict(kind="pulse", x=1024, y=576, r=200, color=EMERALD, min=0.02, max=0.08, hz=0.25)],
       source="[S1][S4]")
    add(s("c2"), s("c3"), E.bits_compare, source="[S1]")
    IL(s("c3"), s("c5"), "c13_guessing_room", "in", kicker="40 BITS", line="About a trillion. A search that ends.",
       warm=False, glows=[dict(PALEB, x=1024, y=500, r=360)])
    add(s("c5"), s("c6"), E.model_cards, source="[S1]")
    IL(s("c6"), nxt_after(cards, e("c6")), "c09_toggle_switch", "out", kicker="STILL INSIDE EVERY DEVICE",
       flick=dict(lights=[dict(x=555, y=602, r=230, thr=0.6, amb=0.5)], mode="slow", depth=0.45, seed=5),
       line="The hardware generator.", warm=False, source="[S2]")
    c10 = next(C)
    add(c10, s("c7"), E.quote_v, v=1, quote="…just by chance, and only for less important things.",
        who="COINKITE · TECHNICAL WRITE-UP", source="[S2]")
    IL(s("c7"), s("c8"), "c14_reading_code", "in", kicker="WE KNOW · HE DOESN'T",
       line="The code is public.", glows=[dict(PALEB, x=1100, y=420, r=300)])
    IL(s("c8"), s("c9"), "c30_plate_into_box", "out", kicker="2021 → 2026", line="Written down. Locked away.",
       warm=False, glows=[DUSTBEAM])
    add(s("c9"), nxt_after(cards, e("c9")), E.explainer_v, v=1, name="OUTSIDE REVIEWS",
        lines=[(0.5, "2022"), (1.4, "2024"), (2.6, "Paid for by Coinkite, says its CEO")], source="[S3]")
    c11 = next(C)
    add(c11, s("c10"), E.countdown_v, v=1, label="A FEW WEEKS", sub="AN AI REVIEW OF THE CRITICAL CODE")
    add(s("c10"), nxt_after(cards, e("c10")), E.explainer_v, v=2, name="COINKITE · AI-ASSISTED REVIEW",
        lines=[(0.5, "Critical code, a few weeks before the theft")], source="[S3]")
    c12 = next(C)
    add(c12, s("c11"), E.quote_v, v=2, quote="It did not catch this vulnerability.",
        who="COINKITE · ON ITS OWN AI-ASSISTED REVIEW", source="[S3]")
    IL(s("c11"), s("c12"), "c37_empty_desk_glow", "left", statement="Someone else found it first.")
    add(s("c12"), s("c14"), E.explainer_v, v=3, name="COINKITE'S ASSUMPTION",
        lines=[(0.5, "Someone used AI to find it"), (s("c13") - s("c12") + 0.2, "Not proven")], source="[S3]")
    IL(s("c14"), s("c15"), "c39_server_racks", "out", statement="No device needed.", warm=False)
    add(s("c15"), nxt_after(hits, e("c16")), S.checklist, title="THE METHOD",
        items=[(0.2, "Guess a seed"), (frac("c15", 0.35) - s("c15"), "Work out its addresses"),
               (frac("c15", 0.7) - s("c15"), "Check the blockchain"), (s("c16") - s("c15") + 0.3, "A match = the key")])

    # ---------------- 01:10 ----------------
    h = nxt_after(hits, e("c16"))
    c13 = max(x for x in cards if x <= s("d1"))
    add(c13, s("d1"), E.countdown_v, v=2, label="0", sub="30 JULY 2026 · 01:10:20 UTC")
    IL(s("d1"), s("d2"), "c15_cottage_night", "in", kicker="TORONTO · 9:10 PM · WEDNESDAY",
       line="Goodman is at his cottage.", glows=[dict(LAMP, x=1000, y=640, r=260)], motes=False,
       fog=dict(density=0.25, color=(0.45, 0.52, 0.6), speed=10, floor=0.4))
    add(s("d2"), s("d4"), E.sweep, source="[S7][S8]")
    add(s("d4"), s("d6"), E.tx_pattern, highlight_at=1.4, source="[S8]")
    IL(s("d6"), s("d7"), "c16_open_boxes_vault", "in", statement="Then it reaches Goodman.", warm=False)
    add(s("d7"), s("d8"), E.balance_lines, starts=(0.3, (s("d7") + e("d7")) / 2 - s("d7"), e("d7") - s("d7") - 1.2),
        source="[S13]")
    add(s("d8"), s("d9"), E.wave_clock, source="[S7][S8]")
    IL(s("d9"), nxt_after(cards, e("d9")), "c40_phone_nightstand", "out", statement="He has no idea.",
       glows=[dict(LAMP, x=1000, y=640, r=260)])

    # ---------------- I'LL JUST CHECK ----------------
    c14 = max(x for x in cards if x <= s("e1"))
    add(c14, s("e1"), E.chapter_v, v=3, title="“I'll just check”", kicker="THE MORNING AFTER")
    IL(s("e1"), s("e2"), "c38_monitoring_room", "in", kicker="BLOCK ENGINEERING", line="Coins leaving cold wallets.",
       ripple=dict(thr=70, guard=16, amp=7.0, wl=560.0, speed=1.0, drift=0.0))
    IL(s("e2"), s("e3"), "c19_loudspeaker", "in", kicker="COINKITE · FIRST WARNING",
       line="Seeds from affected firmware are at risk.", source="[S1]", warm=False, motes=False,
       flick=dict(lights=[dict(x=1300, y=470, r=380, thr=0.5, amb=0.6)], depth=0.3, seed=3),
       fog=dict(density=0.42, color=(0.55, 0.6, 0.68), speed=26, haze=0.15))
    IL(s("e3"), nxt_after(cards, e("e3")), "c17_library_phone", "in", kicker="31 JULY · A PUBLIC LIBRARY",
       line="A friend's post on Facebook.", source="[S13]", glows=[dict(PALEB, x=1024, y=640, r=240)])
    c15 = max(x for x in cards if x <= s("e4"))
    add(c15, s("e4"), E.quote_v, v=3, quote="There's no way this affects me, but I'll just check.",
        who="JONATHAN GOODMAN · TO WEALTHSIMPLE MAGAZINE", source="[S13]")
    add(s("e4"), nxt_after(cards, e("e4")), E.wallet_check, total="Gone since Wednesday night.",
        source="[S13]")
    c16 = max(x for x in cards if x <= s("e5"))
    add(c16, s("e5"), E.quote_v, v=4, quote="I did everything right.", who="JONATHAN GOODMAN · ON X", source="[S12]")
    IL(s("e5"), s("e6"), "c18_police_desk", "in", kicker="TORONTO",
       line="A police report. And the Ontario Securities Commission.", source="[S13]",
       glows=[dict(LAMP, x=900, y=380, r=280)])
    IL(s("e6"), s("e7"), "c32_viewing_room", "in", statement="Did someone open the box?", warm=False,
       flick=dict(lights=[dict(x=935, y=330, r=420, thr=0.55, amb=0.55)], depth=0.32, seed=2))
    add(s("e7"), nxt_after(cards, e("e7")), E.explainer_v, v=4, name="THE FIX",
        lines=[(0.5, "Nobody opened the box"), (2.0, "A firmware update fixes new seeds"),
               (3.6, "Not the old ones: move to a new seed")], source="[S1]")
    c17 = max(x for x in cards if x <= s("e8"))
    add(c17, s("e8"), E.quote_v, v=5, quote="I'm sorry and I'm devastated.",
        who="RODOLFO NOVAK · COINKITE CEO · ON X · 31 JULY", source="[S28]")
    IL(s("e8"), nxt_after(cards, e("e9")), "c41_two_windows", "out", statement="Owners and thieves hear it at once.",
       warm=False, motes=False)

    # ---------------- THE RACE ----------------
    c18 = max(x for x in cards if x <= s("f1"))
    add(c18, s("f1"), E.chapter_v, v=4, title="The race", kicker="31 JULY → 3 AUGUST")
    add(s("f1"), s("f2"), E.waves, source="[S7][S8]")
    IL(s("f2"), s("f3"), "c20_crowd_fog", "in", kicker="GALAXY RESEARCH", line="At least 15 separate attackers.",
       source="[S8]", warm=False, motes=False, fog=dict(density=0.32, color=(0.5, 0.56, 0.64), speed=14, far=0.4))
    add(s("f3"), s("f5"), E.rbf_race, replace_at=s("f4") - s("f3") + 2.0, source="[S17]")
    IL(s("f5"), s("f6"), "c22_trust_safe", "in", kicker="WHITE HATS", line="About 52 BTC moved into a trust.",
       source="[S18][S31]", glows=[dict(LAMP, x=1024, y=420, r=320)])
    IL(s("f6"), s("f7"), "c23_coins_tunnel", "in", kicker="MIXERS", line="Built to blur the trail.",
       source="[S8]", warm=False, fog=dict(density=0.3, color=(0.45, 0.52, 0.6), speed=16, far=0.5))
    add(s("f7"), s("f8"), E.coin_stack, source="[S7][S8]")
    add(s("f8"), s("g1"), E.big_number_v, v=1, value=1082.57, prefix="", suffix=" BTC", decimals=2, count_for=1.2,
        caption="wave 1 · not moved · as of the latest public tracking", source="[S8][S34]")

    # ---------------- THE MISTAKE ----------------
    IL(s("g1"), s("g4"), "c42_identical_seals", "in", kicker="REMEMBER",
       line="Every wave-one transaction looked the same.", warm=False, source="[S8]")
    add(s("g4"), s("g5"), E.fee_scatter, source="[S8]")
    add(s("g5"), s("g8"), E.lookup_log, match_at=s("g7") - s("g5") + 0.8, source="[S4]")
    IL(s("g8"), s("g10"), "c24_receipt_printer", "in", kicker="A PAID ACCOUNT",
       line="Usually leaves records.", glows=[dict(LAMP, x=1024, y=360, r=280)])
    IL(s("g10"), s("g11"), "c25_card_index", "in", kicker="GALAXY · ALEX THORN",
       line="The identity may be known to investigators.", source="[S8][S17]")
    add(s("g11"), nxt_after(cards, e("g11")), E.explainer_v, v=5, name="AS WE MAKE THIS VIDEO",
        lines=[(0.5, "FBI: no confirmed suspect"), (1.6, "No arrest"), (2.6, "No recovery")], source="[S34]")

    # ---------------- WHO? ----------------
    c19 = max(x for x in cards if x <= s("h1"))
    add(c19, s("h3"), E.status_board, rows=[("NAMED PUBLICLY", "no one"), ("ARREST", "none"),
                                            ("WAVE 1 · 1,082.57 BTC", "not moved"),
                                            ("CLASS ACTION", "proposed · not certified"),
                                            ("COMPENSATION FUND", "none announced")], source="[S34][S35]")
    IL(s("h3"), nxt_after(cards, e("h4")), "c27_courtroom_empty", "in", kicker="ONTARIO · SEPTEMBER",
       line="A proposed class action. Allegations, not findings.", source="[S32]", warm=False,
       glows=[dict(PALEB, x=1024, y=300, r=380)])
    c20 = max(x for x in cards if x <= s("h5"))
    add(c20, s("h5"), E.quote_v, v=6, quote="The math on a class action is brutal.",
        who="JONATHAN GOODMAN · TO THE NEWS BLOCK", source="[S30]")
    add(s("h5"), nxt_after(cards, e("h5")), E.big_number_v, v=2, value=0.17, prefix="~", suffix="%", decimals=2,
        count_for=1.0, caption="of its users affected · Coinkite's CEO", source="[S3]")

    # ---------------- THE BOX, AGAIN ----------------
    c21 = max(x for x in cards if x <= s("k1"))
    add(c21, s("k1"), E.chapter_v, v=5, title="The box, again", kicker="THE ONES WHO ROLLED DICE")
    add(s("k1"), s("k2"), E.dice_finale, source="[S1]")
    IL(s("k2"), s("k3"), "c28_hand_dice", "in", statement="They didn't leave it all to the device.")
    IL(s("k3"), s("k4"), "c31_sealed_box_dust", "in", statement="Never opened.", warm=False, glows=[DUSTBEAM])
    IL(s("k4"), s("k5"), "c33_device_under_glass", "in", statement="Never hacked.", warm=False)
    IL(s("k5"), s("k6"), "c36_unplugged_cable", "in", statement="They never asked.", warm=False)
    add(s("k6"), e("k7") + .35, E.explainer_v, v=6, name="IF YOU MADE A SEED ON AN AFFECTED COLDCARD",
        lines=[(0.5, "Read Coinkite's advisory"), (s("k7") - s("k6") + 0.3, "Treat it as compromised"),
               (s("k7") - s("k6") + 1.6, "Move to a new seed")], source="[S1]")
    IL(e("k7") + .35, s("k9"), "c29_vault_dawn", "in", kicker="1,082.57 BTC · AS OF THE LATEST PUBLIC TRACKING",
       line="Still where the first wave left them.", source="[S8][S34]",
       glows=[dict(LAMP, x=1024, y=300, r=380)])
    IL(s("k9"), s("k10"), "c43_archive_drawer_light", "out", statement="Somewhere, there may be a name.",
       flick=dict(lights=[dict(x=530, y=600, r=240, thr=0.5, amb=0.5), dict(x=476, y=515, r=100, thr=0.4, amb=0.6)],
                  depth=0.32, seed=4))
    add(s("k10"), e("k10") + .6, E.statement_v, v=3, line="This was Siphon Files.", color=S.GREY)
    add(e("k10") + .6, total, S.end_card)
    T = [x for x in T if x is not None]
    out = overlay_thomas(T, thomas_shots(tl))
    check_no_flash(out)
    return out, total


def nxt_after(lst, after):
    return min(x for x in lst if x >= after - 1e-6)


def check_no_flash(T):
    """Montage guard (lesson 23 Nov 2026): no non-black scene may show for < 1 s (it reads as a flash)."""
    bad = [(round(a, 2), round(b, 2)) for a, b, fn, p in T
           if b - a < 1.0 and fn is not S.black and fn is not S.presenter]
    if bad:
        raise SystemExit(f"FLASH: scenes shorter than 1 s at {bad} - fix the cut before rendering")


def main():
    args = sys.argv[1:]
    tl = json.load(open(args[0]))
    T, total = build(tl)
    if "--still" in args:
        i = args.index("--still")
        for k in range(i + 1, len(args), 2):
            if args[k].startswith("--"):
                break
            engine.still(T, float(args[k]), args[k + 1])
            print("still", args[k], args[k + 1])
        return
    frames = None
    if "--from" in args:
        a = float(args[args.index("--from") + 1])
        b = float(args[args.index("--to") + 1])
        frames = range(int(a * engine.FPS), int(min(b, total) * engine.FPS))
    audio = None if args[1] == "none" else args[1]
    engine.render(T, total, args[2], audio=audio, frames=frames)
    print("wrote", args[2])


if __name__ == "__main__":
    main()
