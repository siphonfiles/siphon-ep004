"""Episode 004 (Ledger, the CryptoBilis implant) visuals, cut to the sound timeline from sound/ep004/ep004_mix.py.

Usage:
  python3 ep004.py <timeline.json> <audio|none> <out.mp4> [--still T out.png ...] [--from S --to E]
Scenes are anchored on the voice-line ids, so a new audio mix re-times the picture automatically.

Thomas: only ever as moving video (rule 18b). Every Thomas line has a non-Thomas picture underneath; the LongCat
clips in presenter/clips/inputs/ep004_clip_plan.json are laid over it when their frames exist
(presenter/clips/frames/<name>/*.png at 30 fps, made by scripts/ep004_clip_frames.sh).
No illustration and no card design is used twice (owner rule, 24 Nov 2026): see check_unique().
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
import scenes as S  # noqa: E402
import scenes_ep004 as E  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
THOMAS_REF = os.path.join(ROOT, "presenter", "reference", "thomas_ref_ep004_1920x1080.png")
_IMG = os.path.join(ROOT, "illustrations", "ep004", "img")
S.ILL_DIR = _IMG
CLIPS = os.path.join(ROOT, "presenter", "clips", "frames")
CLIP_PLAN = os.path.join(ROOT, "presenter", "clips", "inputs", "ep004_clip_plan.json")
CLOSE = (1.3, 960.0, 440.0)
FIT720 = dict(scale=1920 / 1312, ox=0.0, oy=25.0)

UV = (0.62, 0.48, 1.0)
PALE = (0.85, 0.82, 1.0)
REDL = (1.0, 0.15, 0.2)


def thomas_shots(tl):
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
        out.append((a, b, fr, t0, c.get("camera", "M")))
    out.sort(key=lambda x: x[0])
    for i in range(len(out) - 1):
        if out[i][1] > out[i + 1][0]:
            out[i] = (out[i][0], out[i + 1][0]) + out[i][2:]
    return out


def _clip_len(fr):
    return len([f for f in os.listdir(fr) if f.endswith(".png")]) / 30.0


def _absorb_slivers(T, shots):
    shots = [list(x) for x in shots]
    for a, b, fn, p in T:
        for sh in shots:
            sa, sb, fr, t0 = sh[0], sh[1], sh[2], sh[3]
            if a < sb < b and b - sb < 1.0 and not any(o[0] <= sb < o[1] for o in shots if o is not sh):
                n = _clip_len(fr)
                if b <= t0 + (n if n > 1 else 5.0) - 0.02:
                    sh[1] = b
    return [tuple(x) for x in shots]


def _off(fn, off):
    def g(ctx, t, d, **p):
        return fn(ctx, t + off, d + off, **p)
    g.base = getattr(fn, "base", fn)
    return g


def overlay_thomas(T, shots):
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
                out.append((pa, pb, S.black, {}))        # a sliver would flash: black instead
            elif pa == a:
                out.append((pa, pb, fn, p))
            else:
                out.append((pa, pb, _off(fn, pa - a), p))
    first = min((x[0] for x in shots), default=None)
    for a, b, fr, t0, cam in shots:
        clip = dict(frames=fr, start=t0 - a, **FIT720)
        lt = 0.6 if a == first else 99
        out.append((a, b, S.presenter, dict(image_path=THOMAS_REF, lower_third_at=lt, clip=clip,
                                             zoom=CLOSE if cam == "C" else None)))
    return out


def _have(name):
    return all(os.path.exists(os.path.join(_IMG, f)) for f in (f"{name}.jpg", f"{name}_depth.png"))


def nxt_after(lst, after):
    return min(x for x in lst if x >= after - 1e-6)


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

    def IL(a, b, name, move="in", **p):
        if _have(name):
            T.append((a, b, S.illus, dict(name=name, move=move, **p)))
        else:
            add(a, b, S.statement, line=p.get("statement") or p.get("line") or p.get("kicker") or " ", color=S.GREY)

    s = lambda k: v[k][0]
    e = lambda k: v[k][1]
    frac = lambda k, f: v[k][0] + f * (v[k][1] - v[k][0])
    card = lambda after: nxt_after(cards, after)
    OUT = dict(motes=False)                                  # exterior: no dust
    lamp = lambda x, y, r=300, **k: dict(kind="flicker", color=PALE, base=0.22, x=x, y=y, r=r, **k)
    fl = lambda x, y, r=320, mode="flicker", depth=0.3, seed=1: dict(
        lights=[dict(x=x, y=y, r=r, thr=0.55, amb=0.5)], mode=mode, depth=depth, seed=seed)

    # ---------------- TEASER ----------------
    IL(0.0, s("t2"), "t1_sealed_box_v2", "in", fi=0.6, fo=0.0, warm=False)
    IL(s("t2"), s("t3"), "t2_plastic_seal", "right", fo=0.0, warm=False)
    IL(s("t3"), s("t4"), "t3_open_tray", "in", fo=0.0, warm=False, kicker="INSIDE", line="A genuine hardware wallet.")
    c = card(e("t4"))
    IL(s("t4"), c, "t4_many_devices", "out", fo=0.0, warm=False, kicker="9 OCTOBER 2026", line="335 wallets emptied.",
       source="[S4]")
    add(c, s("t5"), E.big_number_v, v=1, value=335, prefix="", suffix="", caption="wallets · one morning",
        count_for=0.7, source="[S4]")
    add(s("t5"), s("t6"), E.big_number_v, v=0, value=102_000_000, prefix="$", suffix="",
        caption="by one on-chain count · Bitquery", count_for=1.4, source="[S4]")
    IL(s("t6"), s("t7"), "t6_unbroken_chip", "in", fo=0.0, warm=False, statement="Nobody broke the chip.")
    h = nxt_after(hits, e("t7"))
    IL(s("t7"), h, "t7_screen_glow", "in", fo=0.0, warm=False, statement="Someone just read the screen.",
       flick=fl(880, 620, 420, "slow", 0.45, 2))
    c = card(h)
    add(h, c, S.black)
    add(c, s("i1"), S.title_card, title="THE SEALED BOX")

    # ---------------- THOMAS (intro) ----------------
    add(s("i1"), s("i2"), E.statement_v, v=1, line="Thomas Archer · the AI narrator of Siphon Files", color=S.GREY)
    add(s("i2"), s("i3"), E.statement_v, v=2, line="Every claim has a source. They're all in the description.", color=S.GREY)
    c = card(e("i3"))
    add(s("i3"), c, E.statement_v, v=0, line="Ledger hasn't confirmed the totals. So we'll tell you who counted.")

    # ---------------- ACT 1 ----------------
    add(c, s("a1"), E.chapter_v, v=0, title="The man who did everything right", kicker="29 SEPTEMBER 2026")
    IL(s("a1"), s("a2"), "a1_bitcoin_arrival", "in", kicker="29 SEPTEMBER · ONE BITCOIN ADDRESS", line="80 BTC arrive.",
       source="[S4]", ripple=dict(thr=70, guard=16, amp=5.0, wl=560.0, speed=1.0, drift=0.0))
    IL(s("a2"), s("a3"), "a2_coins_stack", "in", kicker="AT THE TIME", line="Roughly $5 million.", source="[S8]", warm=False)
    IL(s("a3"), s("a4"), "a3_device_hand", "in", kicker="A HARDWARE WALLET", line="Keys kept away from the internet.",
       warm=False)
    IL(s("a4"), s("a5"), "a4_paper_words", "left", kicker="THE ADVICE EVERYONE GETS",
       line="Buy a cold wallet. Write the 24 words on paper.", warm=False)
    IL(s("a5"), s("a6"), "a5_reseller_shop", "in", kicker="CRYPTOBILIS · AUTHORISED LEDGER RESELLER",
       line="Listed for Malaysia, Indonesia and the Philippines.", source="[S16]",
       flick=fl(1200, 250, 380, "slow", 0.4, 3), **OUT)
    IL(s("a6"), s("a7"), "a6_ten_days", "in", statement="Ten days later, the 80 coins were gone.", warm=False,
       flick=fl(1300, 60, 380, "flicker", 0.28, 4))
    IL(s("a7"), s("a8"), "a7_empty_wallets_v2", "right", kicker="9 OCTOBER · ONE BITCOIN BLOCK",
       line="Emptied with 110 other wallets.", source="[S4]", warm=False,
       glows=[dict(kind="pulse", x=300, y=560, r=420, color=REDL, min=0.0, max=0.05, hz=0.25)])
    IL(s("a8"), s("a9"), "a8_no_link", "in", statement="No phishing. No fake call. No malware.", warm=False)
    add(s("a9"), s("a10"), S.statement, line="How do you rob a wallet that never goes online?")
    c = card(e("a10"))
    IL(s("a10"), c, "b15_just_a_box", "in", statement="We have to open the box.", warm=False,
       flick=fl(1024, 130, 420, "flicker", 0.3, 5))

    # ---------------- ACT 2: THE BOX ----------------
    add(c, s("b1"), E.chapter_v, v=1, title="The box", kicker="CHAPTER 1")
    IL(s("b1"), s("b2"), "b1_two_chips", "in", statement="A Ledger has two brains.", warm=False)
    IL(s("b2"), s("b3"), "b2_vault_chip", "in", kicker="THE SECURE CHIP", line="Holds your keys. Built never to let them out.",
       warm=False)
    add(s("b3"), s("b4"), E.two_brains, second_at=0.3, screen_at=frac("b3", 0.72) - s("b3"))
    c = card(e("b4"))
    IL(s("b4"), c, "b4_old_rulebook", "in", kicker="LEDGER · 2020 · THE NANO X", line="A rule, written down.",
       source="[S15]", warm=False)
    add(c, s("b5"), E.quote_v, v=1, quote="…can be fully compromised while funds… remain secure.",
        who="LEDGER DONJON · SECURITY BULLETIN 013 · ON THE SECOND CHIP", source="[S15]")
    IL(s("b5"), s("b6"), "b13_untouched_chip_v2", "in", statement="The secret never leaves the secure chip. Except once.",
       warm=False)
    IL(s("b6"), s("b7"), "b6_setup_screen", "in", kicker="SETUP", line="24 words. On the screen.", warm=False,
       flick=fl(1060, 300, 420, "flicker", 0.28, 6))
    IL(s("b7"), s("b8"), "b7_secret_display", "in", statement="For a few minutes, your secret is on display.", warm=False,
       flick=fl(1100, 720, 380, "slow", 0.45, 7))
    k = frac("b9", 0.42)
    IL(s("b8"), k, "b9_teardown", "in", kicker="TAMPERED UNITS · OPENED BY RESEARCHERS",
       line="An extra board, where padding should be.", source="[S5][S7]", warm=False,
       flick=fl(1210, 120, 380, "flicker", 0.28, 8))
    add(k, s("b10"), E.explainer_v, v=0, name="THE EXTRA BOARD",
        lines=[(0.3, "A microcontroller"), (frac("b9", 0.62) - k, "A cellular modem"), (frac("b9", 0.78) - k, "An antenna"),
               (frac("b9", 0.9) - k, "An eSIM")], source="[S2][S5]")
    IL(s("b10"), s("b11"), "b10_two_batteries", "in", kicker="TO MAKE ROOM", line="A smaller battery.", source="[S7]",
       warm=False)
    IL(s("b11"), s("b12"), "b11_lab_bench", "in", kicker="LEDGER DONJON · 13 OCTOBER",
       line="Ledger's own security team described it.", source="[S2]", warm=False,
       flick=fl(1270, 340, 300, "slow", 0.4, 9))
    add(s("b12"), s("b13"), E.screen_tap, decode_at=frac("b12", 0.32) - s("b12"), send_at=frac("b12", 0.6) - s("b12"),
        source="[S2]")
    IL(s("b13"), s("b14"), "b12_signal_rings", "in", kicker="WHAT IT LEAVES ALONE",
       line="The secure chip. Every transaction.", source="[S2]", warm=False)
    IL(s("b14"), s("b15"), "b14_cell_tower", "up", kicker="ITS OWN CONNECTION", line="No laptop. No phone.", warm=False,
       fog=dict(density=0.3, color=(0.4, 0.36, 0.55), speed=24, haze=0.12),
       flick=fl(1444, 330, 90, "slow", 0.5, 10), **OUT)
    add(s("b15"), s("b16"), S.statement, line="No virus. No link. Just a box.")
    c = card(e("b16"))
    add(s("b16"), c, E.explainer_v, v=1, name="LEDGER'S GENUINE CHECK",
        lines=[(0.5, "Built to test the secure chip"), (frac("b16", 0.55) - s("b16"), "The secure chip was the real one")],
        source="[S2]")

    # ---------------- ACT 3: THE WARNING ----------------
    add(c, s("c1"), E.chapter_v, v=2, title="The warning", kicker="CHAPTER 2")
    IL(s("c1"), s("c2"), "k2_gloved_box", "in", statement="This board wasn't new.", warm=False,
       flick=fl(960, 150, 460, "flicker", 0.28, 11))
    IL(s("c2"), s("c3"), "c2_forum_warning", "in", kicker="AUGUST 2025 · REDDIT",
       line="The first public warning about a tampered Nano X.", source="[S5]", warm=False)
    IL(s("c3"), s("c4"), "c3_stage_teardown", "in", kicker="2026 · JOE GRAND", line="Taken apart on stage.",
       source="[S7]", warm=False, glows=[dict(kind="beam", poly=[(600, 0), (880, 0), (1180, 620), (300, 620)],
                                              color=PALE, base=0.07)])
    add(s("c4"), s("c5"), E.quote_v, v=2, quote="Quite an evolution.",
        who="MARK KARPELÈS · ON X · 16 SEPTEMBER 2026 · ON A NEWER VERSION", source="[S5]")
    IL(s("c5"), s("c6"), "c5_marketplace_parcel", "in", kicker="THE RESEARCH UNITS",
       line="From marketplaces in Japan. Not from CryptoBilis.", source="[S5][S17]",
       flick=fl(1150, 80, 420, "flicker", 0.3, 12), **OUT)
    add(s("c6"), s("c7"), E.explainer_v, v=2, name="BY SEPTEMBER 2026",
        lines=[(0.4, "The implant: public"), (frac("c6", 0.45) - s("c6"), "A wave of real losses: not yet shown")])
    add(s("c7"), s("c8"), S.statement, line="That was about to change.")
    IL(s("c8"), s("c9"), "c8_shop_shutter", "in", kicker="MARCH 2026 · CRYPTOBILIS", line="The shop changes hands.",
       source="[S6]", **OUT)
    IL(s("c9"), s("c10"), "c9_handshake_papers", "in", kicker="THE FOUNDERS' ACCOUNT",
       line="Sold to a new team. Buyer not named. They deny any involvement.", source="[S6]", warm=False,
       flick=fl(1740, 140, 380, "flicker", 0.28, 13))
    c = card(e("c10"))
    add(s("c10"), c, S.statement, line="Who owned the shop by October? Nobody has said publicly.")

    # ---------------- ACT 4: T-MINUS ----------------
    add(c, s("d1"), E.chapter_v, v=3, title="The preparation", kicker="CHAPTER 3")
    IL(s("d1"), s("d2"), "d1_receipts_chain", "left", statement="The blockchain kept the receipts.", warm=False)
    IL(s("d2"), s("d3"), "d2_exchange_withdrawal", "in", kicker="24 SEPTEMBER · BYBIT → TRON",
       line="A withdrawal lands in a Tron wallet.", source="[S4]", warm=False)
    add(s("d3"), s("d4"), E.big_number_v, v=2, value=14512, prefix="", suffix=" TRX", count_for=0.8,
        caption="LATER PAID THE ATTACK'S FEES", source="[S4]")
    IL(s("d4"), s("d5"), "d4_test_loops", "in", kicker="FROM 25 SEPTEMBER · TESTS",
       line="21 loops on Tron. 20 on Ethereum.", source="[S4]", warm=False)
    c = card(e("d5"))
    IL(s("d5"), c, "d5_control_key", "in", statement="One Tron address. The control wallet.", warm=False,
       glows=[dict(kind="beam", poly=[(900, 0), (1130, 0), (1280, 1152), (760, 1152)], color=UV, base=0.08)])
    add(c, s("d6"), E.address_card, note="REMEMBER THIS ONE", source="[S4]")
    IL(s("d6"), s("d7"), "d6_wallets_filling", "right", kicker="BITQUERY",
       line="About 6 in 10 drained wallets: first funded in the last 90 days.", source="[S4]", warm=False)
    c1 = card(e("d7"))
    IL(s("d7"), c1, "d7_waiting_figure", "in", statement="Someone had the keys. And waited.", warm=False,
       ripple=dict(thr=70, guard=16, amp=5.0, wl=560.0, speed=1.0, drift=0.0))
    c2 = card(c1 + 0.1)
    add(c1, c2, E.countdown_v, v=0, label="10 DAYS", sub="29 SEPTEMBER · 80 BTC ARRIVE")
    add(c2, s("d8"), E.countdown_v, v=1, label="8 MIN", sub="9 OCTOBER 2026 · 04:59:57 UTC")
    IL(s("d8"), s("d9"), "d8_locks_changed", "in", kicker="04:59 UTC · TRON",
       line="30 wallets get a new key. 100 TRX each.", source="[S4]", warm=False)
    c = card(e("d9"))
    IL(s("d9"), c, "d9_locks", "in", statement="The thief changed the locks.", warm=False)
    add(c, s("d10"), E.countdown_v, v=2, label="0", sub="9 OCTOBER 2026 · 05:07:48 UTC")
    k = s("d10") + 2.3
    IL(s("d10"), k, "d10_clock_507", "in", kicker="05:07 UTC", line="Seven minutes past five.", warm=False, fo=0.0)
    add(k, s("d12"), E.drain_counter, amount_at=s("d11") - k, source="[S4]")
    IL(s("d12"), s("d13"), "d12_chains_network", "out", kicker="THEN", line="BNB Chain. Polygon. Ethereum. Solana.",
       source="[S4]", warm=False)
    IL(s("d13"), s("d13b"), "d13_one_block", "in", kicker="05:54 UTC · ONE BITCOIN BLOCK",
       line="111 wallets, emptied together.", source="[S4]", warm=False,
       glows=[dict(kind="pulse", x=1210, y=880, r=420, color=REDL, min=0.0, max=0.06, hz=0.3)])
    IL(s("d13b"), s("d13c"), "d11_drain_v2", "in", kicker="A WALLET FIRST FUNDED ON 15 SEPTEMBER",
       line="7 million USDT. One transaction.", source="[S4]", warm=False)
    add(s("d13c"), s("d14"), E.explainer_v, v=3, name="ONE TRON WALLET",
        lines=[(0.4, "$33 million taken in since October began"), (frac("d13c", 0.7) - s("d13c"), "It looked like a business")],
        source="[S4]")
    add(s("d14"), s("d15"), E.chain_bars, title="BITQUERY'S COUNT · 9 OCTOBER 2026",
        rows=[("TRON", 79.3, "151 wallets"), ("BITCOIN", 16.8, "122 wallets · 203.8 BTC"),
              ("4 OTHER NETWORKS", 5.9, "62 wallets")],
        total_line="$102.0M · 335 wallets · 6 networks", source="[S4]")
    c = card(e("d15"))
    add(s("d15"), c, S.statement, line="Most of it was gone before anyone raised the alarm.")

    # ---------------- ACT 5: THE CHASE ----------------
    add(c, s("e1"), E.chapter_v, v=4, title="The chase", kicker="CHAPTER 4")
    IL(s("e1"), s("e1b"), "e1_frozen_coins", "in", statement="Stablecoins can be frozen.", warm=False)
    add(s("e1b"), s("e2"), E.clock_card, time_s="12:09", label="FIRST FREEZE · UTC · 9 OCTOBER",
        sub="7 HOURS AFTER THE FIRST WALLETS WERE DRAINED", source="[S4]")
    IL(s("e2"), s("e3"), "e2_locked_vault", "in", kicker="TETHER", line="About $10 million stayed locked.",
       source="[S4]", warm=False)
    add(s("e3"), s("e4"), E.freeze_split, swap_at=frac("e3", 0.3) - s("e3"), source="[S4]")
    IL(s("e4"), s("e4b"), "e4_mixer_maze", "out", kicker="THE REST", line="THORChain. Chainflip. Tornado Cash. Zcash.",
       source="[S4]", warm=False)
    IL(s("e4b"), s("e5"), "e4b_shrinkwrap_open", "in", kicker="9 OCTOBER · MARK KARPELÈS",
       line="A Nano X sent from Malaysia. Still in its shrink-wrap.", source="[S5]", warm=False,
       flick=fl(1830, 600, 420, "flicker", 0.28, 14))
    add(s("e5"), s("e6"), S.timeline, title="LEDGER", source="[S2]",
        points=[("10 OCT", "Confirms an implant in one victim's device"), ("13 OCT", "Describes the LTE board"),
                ("13 OCT ·", "Confirmed losses: devices sold through CryptoBilis")])
    k = frac("e6", 0.36)
    IL(s("e6"), k, "e5_announcement", "in", kicker="15 OCTOBER · LEDGER", line="“A sophisticated criminal group.”",
       source="[S13]", warm=False, glows=[dict(kind="beam", poly=[(1180, 0), (1420, 0), (1700, 1000), (1200, 1000)],
                                                color=UV, base=0.07)])
    IL(k, s("e7"), "e6_counter_rules", "in", kicker="NEW RULES FOR RESELLERS",
       line="No devices on display. Handed over at purchase. No resale of returns.", source="[S13]", warm=False,
       flick=fl(1000, 250, 520, "flicker", 0.25, 15))
    IL(s("e7"), s("e7b"), "e7_city_shops", "in", kicker="SINGAPORE POLICE · 28 OCTOBER",
       line="At least 2 cases since 10 September. About S$3.5 million.", source="[S1]", **OUT)
    IL(s("e7b"), s("e8"), "e7b_store_aisle", "in", kicker="EUROPE · MEDIAMARKT", line="Ledger sales paused.",
       source="[S19]", warm=False, flick=fl(1700, 80, 420, "flicker", 0.25, 16))
    c = card(e("e8"))
    add(s("e8"), c, S.statement, line="Not just one reseller, in one country.")

    # ---------------- ACT 6: THE RETURN ----------------
    add(c, s("f1"), E.chapter_scan, v=0, title="The return", kicker="CHAPTER 5")
    IL(s("f1"), s("f2"), "f1_night_return", "in", kicker="14 NOVEMBER · 19:43 UTC", line="4 Tron wallets emptied.",
       source="[S14]", **OUT)
    add(s("f2"), s("f3"), E.explainer_v, v=4, name="TEN MINUTES LATER",
        lines=[(0.5, "9 Bitcoin wallets · one block"), (frac("f2", 0.75) - s("f2"), "Then more")], source="[S14]")
    k = frac("f3", 0.6)
    IL(s("f3"), k, "f3_airport_box", "in", kicker="NOT SOUTHEAST ASIA", line="A Ledger Flex and a Stax bought in Dubai.",
       source="[S14]", warm=False)
    IL(k, s("f4"), "f3b_winter_city", "in", kicker="AND", line="A Flex bought in Berlin.", source="[S14]", snow=True, **OUT)
    add(s("f4"), s("f5"), E.explainer_v, v=5, name="14–16 NOVEMBER",
        lines=[(0.3, "$1.68 million"), (frac("f4", 0.7) - s("f4"), "From 16 wallets")], source="[S14]")
    IL(s("f5"), s("f6"), "g4_shelf_one_red", "in", kicker="IN THE SAME BLOCK AS THE DRAIN",
       line="One Tron address paid the network fees.", source="[S14]", warm=False,
       glows=[dict(kind="pulse", x=1010, y=600, r=160, color=REDL, min=0.02, max=0.08, hz=0.3)])
    add(s("f6"), s("f7"), E.address_card, match=True, source="[S4][S14]")
    add(s("f7"), s("f8"), E.status_board, title="LEDGER · 19 NOVEMBER 2026",
        rows=[("THE DUBAI AND BERLIN CASES", "the same incident"), ("WHERE", "outside Southeast Asia"),
              ("MORE DEVICES", "may be found")], source="[S13]")
    c = card(e("f8"))
    IL(s("f8"), c, "f8_xray", "in", kicker="VIERZON, FRANCE", line="Ledger offers owners an X-ray inspection.",
       source="[S13]", warm=False)

    # ---------------- IF YOU OWN ONE ----------------
    add(c, s("h1"), E.chapter_scan, v=1, title="If you own one", kicker="SINGAPORE POLICE ADVICE")
    IL(s("h1"), s("h2"), "h1_owner_kitchen", "in", kicker="BOUGHT FROM A SHOP OR A RESELLER?",
       line="Here's what the police advise.", source="[S1]", warm=False,
       flick=fl(470, 820, 160, "slow", 0.45, 17))
    add(s("h2"), s("h3"), S.checklist, title="IF YOU SUSPECT THE DEVICE", source="[S1]",
        items=[(0.3, "Stop using it"), (frac("h2", 0.35) - s("h2"), "Don't type your recovery phrase into it"),
               (frac("h2", 0.68) - s("h2"), "Contact the maker through official support")])
    add(s("h3"), s("h4"), S.flow_map, left="OLD WALLET", mid="NEW PHRASE", right="NEW WALLET", source="[S1]",
        lines=[(0.5, "If the words may have leaked: move what's left"), (frac("h3", 0.7) - s("h3"), "Set up on a device you trust")])
    c = card(e("h4"))
    add(s("h4"), c, S.kinetic, line="Never share those words. With anyone.", highlight=("Never",), source="[S1]")

    # ---------------- WHO? ----------------
    add(c, s("g3"), S.dossier, stamp="AS OF LATE\nNOVEMBER 2026", source="[S13][S18]",
        lines=[(0.3, "ARRESTS · CHARGES: none public"), (s("g2") - c + 0.2, "WHO FITTED THE BOARDS: unknown"),
               (frac("g2", 0.6) - c, "WHO BOUGHT CRYPTOBILIS: not named")])
    IL(s("g3"), s("g4"), "g3_unknown_count", "in", kicker="LEDGER HASN'T CONFIRMED", line="How many devices. How much was lost.",
       source="[S13]", warm=False, flick=fl(1210, 60, 300, "flicker", 0.28, 18))
    IL(s("g4"), s("g5"), "g1_empty_desk", "in", statement="We don't know if it's over.", warm=False,
       flick=fl(690, 640, 300, "flicker", 0.3, 19))
    c = card(e("g5"))
    add(s("g5"), c, S.statement, line="The chip was never broken.")

    # ---------------- FINALE ----------------
    IL(c, s("k2"), "k1_box_window", "in", statement="Plastic tight. Seal intact.", warm=False, fi=0.6)
    add(s("k2"), s("k3"), S.question, q="Who closed the box?", small="A SEAL ONLY PROVES NOBODY OPENED IT SINCE")
    add(s("k3"), s("k4"), E.quote_v, v=3, quote="Exchanges keep records.",
        who="THE TRAIL STARTS WITH AN EXCHANGE WITHDRAWAL · 24 SEPTEMBER", source="[S4]")
    add(s("k4"), s("k5"), E.quote_v, v=4, quote="Whether those records lead to a name, no one has said.", who="SO FAR",
        source=None)
    add(s("k5"), s("k6"), S.statement, line="Before you trust a seal, ask who sealed it.")
    add(s("k6"), e("k6") + .6, S.statement, line="This was Siphon Files.", color=S.GREY)
    add(e("k6") + .6, total, S.end_card)

    check_unique(T)
    out = overlay_thomas(T, thomas_shots(tl))
    check_no_flash(out)
    return out, total


def check_unique(T):
    """Owner rule: no illustration twice; no card design twice (statement under Thomas excepted)."""
    names = [p["name"] for a, b, fn, p in T if fn is S.illus]
    dup = sorted({n for n in names if names.count(n) > 1})
    designs = [(fn.__name__, p.get("v")) for a, b, fn, p in T
               if fn not in (S.illus, S.statement, S.black) and fn is not E.statement_v]
    dd = sorted({d for d in designs if designs.count(d) > 1 and d[0] != "address_card"}, key=str)
    if dup or dd:
        raise SystemExit(f"REPEAT: illustrations {dup} designs {dd}")


def check_no_flash(T):
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
