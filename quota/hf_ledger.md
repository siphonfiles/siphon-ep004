# Registrul cotei Hugging Face ZeroGPU — ep. 004

Regula: cel mult 40 min de cotă pe zi (plănuit ≤ 38), start la **≥ 25 h** după startul real precedent. Ora României.

| Start real | Ce s-a generat | GPU raportat (s) | Cotă estimată (min) | Eșecuri | Următorul start cel mai devreme |
|---|---|---|---|---|---|
| 2026-11-25 03:31 | (ultima rulare a ep. 003, referință) | — | — | — | 2026-11-26 04:31 |
| 2026-11-26 04:32 | ziua 1: portrete ținută (3, 18 s) · ilustrații set1 (33, 466 s) · birou Qwen (99 s) · LongCat i1+i2 (04:52–05:04, ambele bune) | 583 + 2 clipuri | ~13 + ~21,4 = ~34 | 0 (desk: doar copierea a căzut, fără cotă în plus) | 2026-11-27 05:32 |

## Plan ziua 1 (start cel mai devreme 26 nov 2026, 04:31; programat 04:32)
| pas | estimare cotă |
|---|---|
| outfit-ref portrait: 3 portrete Z-Image (burgundy_crewneck, wine_merino, oxblood_cotton) | ~1 min |
| outfit-ref desk: Qwen-Image-Edit-2511, 40 pași, pe portretul ales | ~3 min |
| illustrations `illustrations/ep004/set1.json`: 33 imagini Z-Image 2048x1152 | ~7,5 min |
| LongCat 720p DBCache faster: `thomas_e4_i1`, `thomas_e4_i2` | ~21,4 min |
| **total** | **~33 min** (≤ 38, fără credite) |

Zilele 2–6: câte 3 clipuri/zi (~32 min), în ordinea i3, a9, a10 · b7, b15, c7 · c10, d9, d15 · e8, f6, g5 · k5, k6 (+ rezervă pentru o refacere).

## Plan ziua 2 (start 27 nov 2026, 05:33)
Refaceri ilustrații t1_sealed_box, a7_empty_wallets, d11_drain (~1 min) + clipurile i3, a9, a10 (~32 min) → ~33 min.

**26 nov, 11:15:** proprietarul vede 32 min consumate (estimarea mea: ~34). Rămân 8 min → 27 de imagini (`set3_extra.json`, ~6,3 min) → total ~38,3 min. Refacerile t1/a7/d11 se mută aici, deci ziua 2 = doar i3, a9, a10 + ce rămâne pe imagini.

**Plan revizuit (26 nov, 11:20):** zilele 2–4 doar clipuri, câte 4/zi (3 în cota gratuită + al 4-lea cu ~$0,30 din credite): ziua 2 i3, a9, a10, b7 · ziua 3 b15, c7, c10, d9 · ziua 4 d15, e8, f6, g5 · ziua 5 k5, k6 (+ rezervă pentru refaceri). Cost estimat: ~$0,30 × 3 = ~$0,90.

**26 nov, 11:15–11:25 (set3_extra):** 27 de imagini, **457,9 s GPU (~7,6 min)** — mai mult decât estimarea (~17 s/imagine, nu 14). Total ziua 1 ≈ 32 (văzut de proprietar) + 7,6 ≈ **~39,6 min**, sub 40. Lecție: pentru calcule folosește ~17 s/imagine.

**26 nov, 11:57:** proprietarul vede **38,2/40 min** → 1,8 min rămase → 5 imagini (~85 s, `set4_tail.json`: b13 refăcută + 4 variante utile) → ~39,6 min. Un clip (~10,7 min) ar fi luat ~$0,9 din credite într-o zi cu imagini → nu.
