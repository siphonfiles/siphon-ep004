"""English captions (SRT) for ep. 004, from the exact voice timeline + the spoken lines turned back into
written form (digits, names, tickers). Timing: graphics/motion/ep004_full.timeline.json (voice events).
Usage: python3 scripts/make_captions_ep004.py  ->  episodes/publish/004-captions-en.srt
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
R = [("On the ninth of October", "On 9 October"), ("three hundred and thirty-five wallets", "335 wallets"),
     ("About one hundred and two million dollars", "About $102 million"),
     ("On the twenty-ninth of September", "On 29 September"), ("received eighty coins", "received 80 coins"),
     ("roughly five million dollars", "roughly $5 million"), ("the twenty-four words", "the 24 words"),
     ("Crypto Bilis", "CryptoBilis"), ("the eighty coins", "the 80 coins"), ("The eighty coins", "The 80 coins"),
     ("one hundred and ten other wallets", "110 other wallets"), ("In twenty twenty,", "In 2020,"),
     ("Twenty-four words.", "24 words."), ("an e-SIM", "an eSIM"), ("L T E", "LTE"),
     ("August twenty twenty-five", "August 2025"), ("On the sixteenth of September", "On 16 September"),
     ("Karpeles", "Karpelès"), ("He called it quite an evolution.", "He called it \"quite an evolution\"."),
     ("On the twenty-fourth of September", "On 24 September"), ("From the twenty-fifth", "From the 25th"),
     ("Twenty-one small loops", "21 small loops"), ("Twenty on Ethereum", "20 on Ethereum"),
     ("Bit query", "Bitquery"), ("about six in ten", "about 6 in 10"), ("last ninety days", "last 90 days"),
     ("At four fifty-nine in the morning, UTC, thirty Tron wallets", "At 04:59 UTC, 30 Tron wallets"),
     ("a one hundred T R X fee", "a 100 TRX fee"), ("At seven minutes past five.", "At 05:07."),
     ("Twenty-five Tron wallets", "25 Tron wallets"), ("within three seconds", "within 3 seconds"),
     ("Twenty-nine million dollars leaves in six seconds", "$29 million leaves in 6 seconds"),
     ("B N B Chain", "BNB Chain"), ("At five fifty-four,", "At 05:54,"),
     ("One hundred and eleven wallets", "111 wallets"), ("on the fifteenth of September", "on 15 September"),
     ("lost seven million dollars in Tether", "lost $7 million in Tether"),
     ("thirty-three million dollars", "$33 million"),
     ("one hundred and two million dollars, from three hundred and thirty-five wallets, on six networks",
      "$102 million, from 335 wallets, on 6 networks"),
     ("at nine minutes past noon, UTC", "at 12:09 UTC"), ("Seven hours after", "7 hours after"),
     ("About ten million dollars", "About $10 million"),
     ("Twenty-three point seven million dollars in Tether", "$23.7 million in Tether"), ("U S D D", "USDD"),
     ("Thor Chain", "THORChain"), ("Z-cash", "Zcash"), ("Back on the ninth itself", "Back on the 9th itself"),
     ("On the tenth of October", "On 10 October"), ("On the thirteenth", "On the 13th"),
     ("it blamed a sophisticated criminal group", "it blamed \"a sophisticated criminal group\""),
     ("at least two cases since the tenth of September", "at least 2 cases since 10 September"),
     ("About three point five million Singapore dollars", "About S$3.5 million"),
     ("on the fourteenth of November, at seven forty-three in the evening, UTC, four Tron wallets",
      "on 14 November, at 19:43 UTC, 4 Tron wallets"),
     ("Ten minutes later, nine Bitcoin wallets", "10 minutes later, 9 Bitcoin wallets"),
     ("One point six eight million dollars, from sixteen wallets", "$1.68 million, from 16 wallets"),
     ("On the nineteenth of November", "On 19 November"),
     ("one hundred and two million dollars", "$102 million"), ("on six networks", "on 6 networks")]
TEXT = {}
for d in json.load(open(os.path.join(ROOT, "sound/ep004/ep004_lines.json"))):
    t = d["text"]
    for a, b in R:
        t = t.replace(a, b)
    TEXT[d["id"]] = t
TL = json.load(open(os.path.join(ROOT, "graphics/motion/ep004_full.timeline.json")))
OUT = os.path.join(ROOT, "episodes/publish/004-captions-en.srt")
MAX = 84


def chunks(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    out = []
    for p in parts:
        while len(p) > MAX:
            cut = max(p.rfind(", ", 0, MAX), p.rfind(": ", 0, MAX), p.rfind("; ", 0, MAX))
            if cut < 20:
                cut = p.rfind(" ", 0, MAX)
            out.append(p[:cut + 1].strip())
            p = p[cut + 1:].strip()
        if p:
            out.append(p)
    # merge very short neighbours when they fit on one cue
    merged = []
    for c in out:
        if merged and len(merged[-1]) + 1 + len(c) <= MAX and (len(c) < 30 or len(merged[-1]) < 30):
            merged[-1] = merged[-1] + " " + c
        else:
            merged.append(c)
    return merged


def ts(t):
    t = max(0.0, t)
    h, r = divmod(int(round(t * 1000)), 3600000)
    m, r = divmod(r, 60000)
    s, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    voices = [e for e in TL["events"] if e["kind"] == "voice"]
    cues = []
    for e in voices:
        text = TEXT[e["id"]]
        cs = chunks(text)
        total = sum(len(c) for c in cs)
        t = e["t"]
        for c in cs:
            d = e["dur"] * len(c) / total
            cues.append((t, t + d, c))
            t += d
    # no overlaps, small gap
    fixed = []
    for i, (a, b, c) in enumerate(cues):
        if i + 1 < len(cues):
            b = min(b, cues[i + 1][0] - 0.04)
        fixed.append((a, max(b, a + 0.6), c))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        for i, (a, b, c) in enumerate(fixed, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{c}\n\n")
    print(len(fixed), "cues ->", OUT)


if __name__ == "__main__":
    main()
