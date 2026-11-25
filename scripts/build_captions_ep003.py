"""Build translated SRTs for ep. 003 from one-line-per-cue text files and check them.

Input:  episodes/publish/captions003/<lang>.txt  (167 lines, same order as the English SRT)
Output: episodes/publish/captions003/003-captions-<lang>.srt (same timings as 003-captions-en.srt)

Checks (printed, non-zero exit on hard errors):
  - exactly as many non-empty lines as English cues
  - every number in an English sentence group appears in the translated group
    (thousand separators, decimal commas and 12h->24h times normalised)
  - proper names from the English group survive (Latin-script languages only)
  - reading speed: characters per second per cue (warning above 25 cps)
"""
import re, sys, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIR = ROOT / "episodes/publish/captions003"
EN_SRT = ROOT / "episodes/publish/003-captions-en.srt"

blocks = EN_SRT.read_text().strip().split("\n\n")
times = [b.split("\n")[1] for b in blocks]
en = [" ".join(b.split("\n")[2:]) for b in blocks]
N = len(en)

def secs(t):
    h, m, s = t.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

dur = [secs(t.split(" --> ")[1]) - secs(t.split(" --> ")[0]) for t in times]

# sentence groups: a cue continues into the next when it doesn't end a sentence
groups, cur = [], []
for i, line in enumerate(en):
    cur.append(i)
    if re.search(r'[.?!…"”]\s*$', line):
        groups.append(cur); cur = []
if cur:
    groups.append(cur)

NAMES = ["Coldcard", "Coinkite", "Bitcoin Core", "Mk2", "Mk3", "Chainalysis", "Bitkey",
         "Galaxy", "TRM Labs", "Siphon Files", "Thomas Archer", "Goodman", "Toronto",
         "Will Owens", "Alex Thorn", "FBI", "Facebook", "Ontario", "AI", "Block"]
TIME_MAP = {"9:36": "21:36", "9:43": "21:43", "9:51": "21:51"}
NON_LATIN = {"ru", "ja", "ko", "hi"}

def nums(text):
    out = []
    text = re.sub(r"(\d{1,2})[\s\u00a0\u202f]?h[\s\u00a0\u202f]?(\d{2})", r"\1:\2", text)
    for m in re.finditer(r"\d[\d.,:   ]*\d|\d", text):
        tok = m.group(0).strip()
        mt = re.fullmatch(r"(\d{1,2})[.h](\d{2})", tok)
        if ":" in tok or (mt and 13 <= int(mt.group(1)) <= 23) or "h" in tok:
            tok = re.sub(r"[.h]", ":", tok)
            out.append(TIME_MAP.get(tok, tok)); continue
        tok = re.sub(r"[   ]", "", tok)
        if re.fullmatch(r"\d{1,3}([.,]\d{3})+", tok):
            tok = re.sub(r"[.,]", "", tok)
        tok = tok.replace(",", ".")
        out.append(tok)
    return sorted(out)

def build(lang):
    lines = [l.rstrip() for l in (DIR / f"{lang}.txt").read_text().split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    errs, warns = [], []
    if len(lines) != N:
        errs.append(f"{len(lines)} lines, expected {N}")
        return errs, warns
    for i, l in enumerate(lines):
        if not l.strip():
            errs.append(f"cue {i+1} empty")
    for g in groups:
        e = " ".join(en[i] for i in g)
        t = " ".join(lines[i] for i in g)
        ne, nt = nums(e), nums(t)
        if ne != nt:
            warns.append(f"cues {g[0]+1}-{g[-1]+1} numbers en={ne} {lang}={nt}")
        if lang not in NON_LATIN:
            tn = unicodedata.normalize("NFD", t)
            tn = "".join(c for c in tn if not unicodedata.combining(c))
            for n in NAMES:
                if re.search(r"\b" + re.escape(n) + r"\b", e) and n not in tn:
                    if n == "AI" and re.search(r"\b(IA|YZ|AI|KI|TTNT)\b|yapay zek", tn):
                        continue
                    warns.append(f"cues {g[0]+1}-{g[-1]+1} missing name {n!r}")
    for i, l in enumerate(lines):
        cps = len(l) / max(dur[i], 0.5)
        en_cps = len(en[i]) / max(dur[i], 0.5)
        if cps > max(25, en_cps * 1.2):
            warns.append(f"cue {i+1} {cps:.0f} cps ({len(l)} chars / {dur[i]:.1f}s)")
    srt = "\n\n".join(f"{i+1}\n{times[i]}\n{lines[i]}" for i in range(N)) + "\n"
    (DIR / f"003-captions-{lang}.srt").write_text(srt)
    return errs, warns

if __name__ == "__main__":
    langs = sys.argv[1:] or sorted(p.stem for p in DIR.glob("*.txt") if p.stem != "en")
    bad = False
    for lang in langs:
        errs, warns = build(lang)
        print(f"== {lang}: {len(errs)} errors, {len(warns)} warnings")
        for x in errs:
            print("  ERROR", x)
        for x in warns:
            print("  warn ", x)
        bad |= bool(errs)
    sys.exit(1 if bad else 0)
