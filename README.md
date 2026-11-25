# Siphon Files

Canal YouTube: **[@siphonfiles](https://www.youtube.com/@siphonfiles)** · Channel ID `UC_w7oZaLq8wq3absfPkBu2g`

Repo privat cu tot ce ține de canal: identitate vizuală, poziționare, decizii, materiale de producție.

---

## Poziționare

**„Unde dispar banii în crypto — și cum."** Furturi, fraude și prăbușiri, explicate ca investigații, nu ca știri.

Descriere publică a canalului:

> Investigations into where money disappears — exchange hacks, scams and collapses, taken apart step by step. How the money moved, who moved it, and what it means for anyone holding their own funds.
>
> No price predictions, no trading calls. Explainers and investigations only — nothing here is financial advice.

### Ce intră
- Hack-uri de burse și protocoale: cronologie, vector de atac, urmărirea fondurilor
- Mecanisme de fraudă disecate: pig butchering, rug pull, wallet drainer, suport fals
- Prăbușiri: mecanismul financiar din spate, nu povestea de presă
- Urmărire on-chain explicată pe cazuri reale
- Protecție practică: custodie, verificarea unei tranzacții, primele ore după o compromitere

### Ce nu intră, niciodată
- Prețuri, predicții, „ce urmează pentru Bitcoin"
- Analiză tehnică, grafice, niveluri
- Recenzii de proiecte sau tokenuri
- Știri de piață în ziua evenimentului
- Orice formulare de tip „ar trebui să cumperi"

Lista a doua nu e stilistică. E ce ține canalul în afara categoriei pe care YouTube o demonetizează.

---

## Constrângerea de politică

Politica YouTube de „inauthentic content", rescrisă în iulie 2026, numește trei categorii nemonetizabile. A treia: personaje AI care se prezintă ca expert uman care dă sfaturi pe sănătate, chestiuni juridice, **finanțe** sau politică. Sancțiunea e la nivel de canal.

Canalul folosește un prezentator AI, deci regula se aplică direct. Ieșirea din categorie cere trei condiții simultane:

1. Prezentatorul e declarat AI, nu se prezintă ca expert uman
2. Zero recomandări de investiție
3. Fiecare afirmație e atribuită unei surse

Plus: bifarea „altered or synthetic content" la fiecare upload. Eticheta în sine nu reduce reach-ul și nu afectează monetizarea.

---

## Structura de conținut

| Pilon | Pondere | Format |
|---|---|---|
| Post-mortem de incident | 40% | 10-14 min, cronologie + mecanism + consecințe, unul la 1-2 săptămâni |
| Disecție de mecanism | 40% | 8-12 min, evergreen, trafic din căutare |
| Ghid practic de protecție | 20% | custodie, verificare, reacție la compromitere |

Structura hook-ului, dedusă din videoclipurile cu cele mai multe vizualizări din nișă:

| Interval | Conținut |
|---|---|
| 0:00-0:07 | Scenă concretă, moment precis, zero preambul |
| 0:07-0:20 | Escaladare, apoi cifra |
| 0:20-0:33 | Superlativ care fixează miza, apoi legătura cu interesul privitorului |
| 0:33-0:40 | Întrebarea care devine promisiunea videoclipului |
| 0:40-0:46 | Harta: ce acoperă videoclipul, enumerat |
| 0:46-0:53 | Identitatea, în două secunde |

Capitole la fiecare 60-90 de secunde, fiecare încheiat cu o întrebare care deschide următorul.

---

## Monetizare

Ordinea reală, nu cea intuitivă:

1. **Afiliere** — de la primul video. Burse: revenue share pe viață, 20-50% din taxe. Hardware wallets: produsul natural pentru conținut despre furturi.
2. **Sponsorizări** — după ~20-30k vizualizări medii. Nișa e în topul platformei la CPM de sponsorizare.
3. **AdSense** — bonus, nu fundament. RPM-ul crypto e corelat cu prețul Bitcoin și a scăzut mult față de vârf.

Consecință importantă: pentru că venitul nu stă pe reclame, o eventuală demonetizare e o lovitură, nu o execuție.

---

## Identitate vizuală

Vezi `brand/`.

| Element | Fișier | Spec |
|---|---|---|
| Avatar | `brand/avatar_800.png` | 800x800 PNG |
| Watermark | `brand/watermark_150.png` | 150x150 PNG, alfa |
| Banner | `brand/banner_2048x1152.png` | 2048x1152 PNG |
| Sursă marcă | `brand/mark.svg`, `brand/mark_white.svg` | SVG |

**Culori**

| Rol | Hex |
|---|---|
| Fundal | `#0D0F12` |
| Accent | `#FFB020` |
| Text pe fundal închis | `#FFFFFF` |

**Marca**: un S cu o picătură care cade — siphon. Testat pentru lizibilitate până la 48px.

---

## Stiva de producție

> Versiunea la zi a stivei și a deciziilor e în `CLAUDE.md`; tabelul de mai jos e doar rezumatul inițial.

| Etapă | Unealtă | Notă |
|---|---|---|
| Base loop prezentator | LongCat-Video-Avatar 1.6 (MIT) | o dată per look, nu per video |
| Re-sync pe audio | Chanjing-Avatar-V2V-1.3B (Apache-2.0) sau InfiniteTalk | cost marginal în cenți |
| Imagini | Z-Image-Turbo (Apache-2.0); MOSS-Image-SFT ca alternativă | vezi nota de licențe |
| Montaj | DaVinci Resolve | nu face lip-sync, doar montaj și compoziting |

### Note de licențe (verificate 20 nov 2026)

- **MOSS-Image-SFT / Base** — Apache-2.0. Utilizabil.
- **MiniMax-H3-Image** — cel mai bun model de imagine, dar licența exclude explicit Uniunea Europeană din teritoriul aplicabil, inclusiv pentru afișarea rezultatelor. **Nu se poate folosi din România.**
- **Qwen-Image-2.1** — Qwen Research License, „for non-commercial purposes only". **Nu se poate folosi comercial.**
- **FLUX.1-schnell** — Apache-2.0, utilizabil. **FLUX.1-dev** nu.
- **NanoAvatar** — CC BY-NC. Doar necomercial.

---

## De făcut

- [ ] Handle `@siphonfiles` pe X
- [ ] Domeniu `siphonfiles.com`
- [ ] Adresă de email dedicată pentru contact de business
- [ ] Primele 10 subiecte
- [ ] Conturi de afiliere la burse și la un producător de hardware wallet
