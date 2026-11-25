# Ep. 004 — vocea lui Thomas (ZONOS3-Mini, CPU în Actions)

## ep004-v1 (25 nov 2026, run 45659403357, seed 1)
93 de replici, 8,26 min de voce. ASR: `voice-tests:reports/asr_1_medium.en.md` + `asr_2_large-v3.md`.

Diferențe ignorate (doar scriere): cifre („eighty” → 80), „dollars” → „$”, sigle (LTE, BNB, USDD, TRX), Crypto Bilis/CryptoBillis, Bit query/BitQuery, Thor Chain/ThorChain, authorised/authorized, cash/cache (omofone în engleza britanică), f1 „four Tron” (large-v3 corect). Finalul canalului: k6 „Siphon Files” corect la ambele modele; i1 corect.

| replică | problemă | acțiune |
|---|---|---|
| d10 | „seven minutes past five, twenty-five” se aude ca „5:25” / „Tron Wallet signed” | text nou cu punct după „five” (și în script) → seed 2/3/4 |
| c4 | „Karpeles” → „Carpelli's” (large-v3) | seed 2/3/4 |
| e4b | „Karpeles” → „Coppolaes” (medium.en) | seed 2/3/4 |
| f7 | „tampered” → „tempered” (medium.en) | seed 2/3/4 |
| f8 | „Ledger” → „Leger”, „Vierzon” → „Viers en” (medium.en) | seed 2/3/4 |
| e4 | „moved” → „move” (large-v3) | seed 2/3/4 |

## ep004-fix1
`sound/ep004/ep004_fix1_lines.json` (18 variante). Alegerea: varianta pe care ambele modele o aud corect, cu durata cea mai apropiată de v1.

### Rezultat fix1 (ASR rulările 3 medium.en + 4 large-v3)
| replică | ales | durată (v1 → nou) | de ce |
|---|---|---|---|
| e4b | `ep004-fix1/e4b_s3.wav` | 7,0 → 7,0 s | „Karpeles” corect la ambele modele |
| d10 | `ep004-fix1/d10_s4.wav` | 6,1 → 6,2 s | ambele aud „7 minutes past 5, 25 Tron wallets sign” |
| f7 | `ep004-fix1/f7_s2.wav` | 8,5 → 8,5 s | „tampered” corect la ambele |
| f8 | `ep004-fix1/f8_s2.wav` | 5,7 → 5,7 s | „Vierzon” corect la ambele; medium.en aude „Leger” la toate variantele (aproape omofon), large-v3 corect |
| e4 | `ep004-fix1/e4_s2.wav` | 6,3 → 6,9 s | „moved” corect la ambele; Tornado Cash/cache e omofon |
| c4 | — | — | „Karpeles” greșit la large-v3 în toate variantele → **fix2**: seed 5/6/7 + scriere fonetică „Kar-peh-less” seed 2/3/4 |

Toate celelalte replici: `ep004-v1/<id>.wav`.

### Rezultat fix2 (ASR 5 + 6)
| replică | ales | durată | de ce |
|---|---|---|---|
| c4 | `ep004-fix2/c4_s6.wav` | 6,4 → 6,5 s | „Karpeles” corect la ambele modele (și s5, s7); scrierea fonetică „Kar-peh-less” iese mai rău |

### ep004-new1 (script v1.2: e1b, h1–h4; seed 1 și 2)
ASR pornit (rapoartele 7 și 8).

### Rezultat new1 (ASR 7 + 8)
Atenție: id-urile nu aveau sufix de seed, deci seed 2 a suprascris seed 1. Fișierele rămase (seed 2) trec la ambele modele: `ep004-new1/{e1b,h1,h2,h3,h4}.wav`.

## Dosarul final de voci (mix v1, 25 nov 2026)
`ep004-v1/*` + `fix1/e4b_s3→e4b, d10_s4→d10, f7_s2→f7, f8_s2→f8, e4_s2→e4` + `fix2/c4_s6→c4` + `new1/{e1b,h1–h4}` (98 de replici).

## Coloana sonoră v1
`sound/ep004/ep004_mix.py` → **10:02,3** (602,3 s). Master ffmpeg loudnorm în două treceri: **-14,0 LUFS, vârf -1,5 dBFS**, 48 kHz, AAC 256k → `renders:audio/ep004_audio.m4a`. Cronologia: `graphics/motion/ep004_full.timeline.json`.
