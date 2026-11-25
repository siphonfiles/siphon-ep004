"""Transcribe every voice line of ep. 001 and compare it with the text it was generated from.
TTS can drop, swap or slur words; this catches them before the final render.
faster-whisper (MIT) + Whisper small.en weights (MIT), CPU int8.
Usage: python3 scripts/asr_check.py <dir with *.flac + texts.json> <out.md>"""
import difflib, json, os, re, sys
from faster_whisper import WhisperModel

d, out = sys.argv[1], sys.argv[2]
_tj = os.path.join(d, "texts.json")
if os.environ.get("ASR_LINES"):
    texts = {x["id"]: x["text"] for x in json.load(open(os.environ["ASR_LINES"]))}
else:
    texts = json.load(open(_tj))
MODEL = os.environ.get("ASR_MODEL", "small.en")
ONLY = [x for x in os.environ.get("ASR_IDS", "").split(",") if x]
m = WhisperModel(MODEL, device="cpu", compute_type="int8")
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven",
       "8": "eight", "9": "nine", "10": "ten", "11": "eleven", "12": "twelve"}
def norm(s):
    s = s.lower().replace("’", "'").replace("-", " ").replace("—", " ")
    s = re.sub(r"[^a-z0-9' ]", " ", s)
    return [NUM.get(w, w) for w in s.split()]
rows, bad = [], 0
LOW = []
LOWP = float(os.environ.get("ASR_LOWP", "0.5"))
def key(k):
    return (k[0], int(re.sub(r"\D", "", k) or 0), k)
for k in sorted(texts, key=key):
    if ONLY and k not in ONLY:
        continue
    f = os.path.join(d, k + ".flac")
    if not os.path.exists(f):
        f = os.path.join(d, k + ".wav")
    if not os.path.exists(f):
        rows.append(f"| {k} | MISSING FILE | | |"); bad += 1; continue
    segs = list(m.transcribe(f, beam_size=5, language="en", vad_filter=False, word_timestamps=True,
                             condition_on_previous_text=False)[0])
    heard = " ".join(s.text.strip() for s in segs)
    words = [w for s in segs for w in s.words]
    if ONLY:
        print(k, " ".join(f"{w.word.strip()}[{w.start:.2f}-{w.end:.2f} p{w.probability:.2f}]" for w in words), flush=True)
    low = [f"{w.word.strip()}@{w.start:.1f}s p{w.probability:.2f}" for w in words if w.probability < LOWP]
    LOW.append((k, low))
    a, b = norm(texts[k]), norm(heard)
    sm = difflib.SequenceMatcher(a=a, b=b)
    diffs = [f"{' '.join(a[i1:i2]) or '∅'} → {' '.join(b[j1:j2]) or '∅'}" for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    score = sm.ratio()
    flag = "OK" if not diffs else ("CHECK" if score > 0.9 else "BAD")
    bad += flag != "OK"
    rows.append(f"| {k} | {flag} {score:.2f} | {'; '.join(diffs)} | {heard} |")
    print(k, flag, diffs, flush=True)
lowtxt = "\n".join(f"| {k} | {', '.join(l)} |" for k, l in LOW if l)
open(out, "w").write(f"# ASR check ({MODEL})\n\n| line | result | differences (script → heard) | heard |\n|---|---|---|---|\n" + "\n".join(rows)
                     + f"\n\n{bad} lines to look at\n\n## Words heard with low confidence (p < {LOWP})\n\n| line | words |\n|---|---|\n" + lowtxt + "\n")
