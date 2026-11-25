"""English captions (SRT) for ep. 001, from the exact voice timeline + the TTS line texts.
Numbers/acronyms are turned back into written form; times are shifted for the two Resolve trims in v7
(-1.3 s after 503.6 s, -2.1 s after 555.2 s, original timeline). Usage: python3 scripts/make_captions.py"""
import json, re, glob
T = {}
for f in ['ep001_teaser_lines', 'ep001_open_lines', 'ep001_rest_lines', 'ep001_i1_285', 'ep001_t2_fix', 'ep001_b5b']:
    for d in json.load(open(f'sound/teaser/{f}.json')):
        T[d['id']] = d['text']
T['t3'] = next(d['text'] for d in json.load(open('sound/teaser/ep001_t3_variants.json')) if d['id'] == 't3b')
tl = json.load(open('graphics/motion/ep001_full.timeline.json'))
R = [("April twenty twenty-six", "April 2026"), ("two hundred and eighty-five million dollars", "$285 million"),
     ("twelve minutes", "12 minutes"), ("Fall, twenty twenty-five", "Fall 2025"), ("March twenty-third", "March 23"),
     ("T R M Labs", "TRM Labs"), ("two-of-five", "2-of-5"), ("March eleventh", "March 11"), ("ten ether", "10 ether"),
     ("nine o'clock", "9:00"), ("Thirty-one withdrawals", "31 withdrawals"), ("forty percent", "40%"), ("U S D C", "USDC"),
     ("Zach X B T", "ZachXBT"), ("SEAL nine-one-one", "SEAL 911"), ("September twenty twenty-four", "September 2024"),
     ("fifty million dollars", "$50 million"), ("In twenty twenty-four, a P D F", "In 2024, a PDF"),
     ("In twenty twenty-six", "In 2026"), ("F B I", "FBI"), ("V S Code", "VS Code"), ("A I ", "AI "), ("D-tex", "DTEX"),
     ("a hundred and twenty-seven and a half million dollars", "$127.5 million"), ("ten percent", "10%"),
     ("twenty twenty-eight", "2028"), ("another hundred and nine million dollars' worth", "another $109 million's worth"),
     ("six point three billion dollars", "$6.3 billion"), ("twenty minutes", "20 minutes"), ("co-C E O", "co-CEO"),
     ("a hundred and thirty-eight million dollars", "$138 million"), ("about one dollar", "about $1"),
     ("one-dollar price tag", "$1 price tag"), ("reads like a spy novel", "\"reads like a spy novel\""),
     ("this wasn't one mistake or one breach. It was a months-long campaign.",
      "\"This wasn't one mistake or one breach. It was a months-long campaign.\""),
     ("Six hours is how long Circle had to freeze stolen funds, he wrote.",
      "\"Six hours is how long Circle had to freeze stolen funds,\" he wrote."),
     ("medium-high confidence", "\"medium-high\" confidence"), ("worth about...", "worth about—"),
     ("April the first,", "April the first—"), ("Someone.", "Someone—")]
MAX = 84


def fix(s):
    for a, b in R:
        s = s.replace(a, b)
    return s


def adj(t):
    return t - 2.1 if t > 555.2 else t - 1.3 if t > 503.6 else t


def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def split_long(c):
    if len(c) <= MAX:
        return [c]
    cuts = [m.end() for m in re.finditer(r'[,;:]\s', c)] or [m.end() for m in re.finditer(r'\s', c)]
    k = min(cuts, key=lambda i: abs(i - len(c) / 2))
    return split_long(c[:k].strip()) + split_long(c[k:].strip())


def wrap(c):
    if len(c) <= 42:
        return c
    w = c.split(' ')
    return min((('\n'.join([' '.join(w[:k]), ' '.join(w[k:])]), max(len(' '.join(w[:k])), len(' '.join(w[k:]))))
                for k in range(1, len(w))), key=lambda x: x[1])[0]


cues = []
for e in tl['events']:
    if e['kind'] != 'voice':
        continue
    txt = fix(T[e['id']]); t0 = adj(e['t'])
    chunks = []
    for p in re.split(r'(?<=[.?!—])\s+', txt):
        if chunks and len(chunks[-1]) + 1 + len(p) <= MAX:
            chunks[-1] += ' ' + p
        else:
            chunks.append(p)
    chunks = [x for c in chunks for x in split_long(c)]
    tot = sum(len(c) for c in chunks); t = t0
    for c in chunks:
        d = e['dur'] * len(c) / tot; cues.append((t, t + d, c)); t += d
open('episodes/publish/001-captions-en.srt', 'w').write(
    '\n'.join(f"{n}\n{ts(a)} --> {ts(b - 0.02)}\n{wrap(c)}\n" for n, (a, b, c) in enumerate(cues, 1)))
print(len(cues), max(len(c) for _, _, c in cues))
