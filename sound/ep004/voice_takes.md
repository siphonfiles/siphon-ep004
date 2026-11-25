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
