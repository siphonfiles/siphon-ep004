# Prezentatorul — Thomas Archer

Portretul oficial: `portrait_v1_896x1152.png` — ales pe 20 nov 2026.

## Rețeta de generare

| Parametru | Valoare |
|---|---|
| Model | Tongyi-MAI/Z-Image-Turbo (Apache-2.0) |
| Space | huggingface.co/spaces/Tongyi-MAI/Z-Image-Turbo |
| Seed | **596067** |
| Rezoluție | 896x1152 (7:9) |
| Steps | 8 |
| Time Shift | 3 |

Prompt:

```
Photorealistic studio portrait photograph of a man in his late thirties. Short dark brown hair, neatly cut, clean-shaven face with no beard or stubble, no glasses. Composed, calm expression at rest, with the faintest upward set at the corners of the mouth, mouth closed, relaxed brows, open and clearly defined eyes, looking straight into the camera. Defined but not heavy jawline, no aggressive features. He wears a plain dark charcoal crew-neck sweater, no pattern, no logo. Medium shot from the chest up, centred in frame, facing the camera square on. Even soft frontal key light with gentle fill, no harsh shadows and no side lighting across the face. Plain empty seamless dark grey studio background, slightly darker toward the edges, nothing else in frame. Shot on an 85mm lens, shallow depth of field, natural skin texture and pores, neutral colour grade, documentary news presenter portrait.
```

## De ce fața asta

Specificația, derivată din cercetarea de percepție facială (Oosterhof & Todorov) și demografia audienței (bărbați ~28-45):

- bărbat, ~38-42 ani
- valență ușor pozitivă în repaus: colțurile gurii abia ridicate, gura închisă, sprâncene relaxate
- dominanță moderată: maxilar definit, nu masiv, fără arcadă grea
- privire directă, lumină frontală uniformă, fundal gol
- registru de jurnalist, nu de crypto hype

Teste trecute: lizibil la 15% din mărime; fața rămâne coerentă la 512 px.

## Limite cunoscute

- **Barbă de o zi**, deși prompt-ul cere ras. La seed-ul ăsta e fixată în față — prompt-uri care o elimină schimbă omul. La 256 px devine zgomot în zona gurii. → pentru re-sync, preferă LatentSync (512 px) în locul MuseTalk (256 px), sau elimină barba prin editare.
- **Pulover tricotat** — textură fină sub zona feței; risc mic de licărire la video-to-video.

## Lecții de la generare

- Cota ZeroGPU e pe cont, nu pe Space: schimbarea Space-ului nu o resetează. Rulările eșuate consumă și ele.
- Z-Image-Turbo are diversitate scăzută: același seed + prompt ușor modificat păstrează omul; schimbări mari îl pierd.
- Negațiile („no stubble") activează conceptul negat. Descrie ce vrei, nu ce nu vrei.
- Fără ancoră de trăsături, Z-Image alunecă spre fețe est-asiatice când condiționarea se schimbă (model antrenat masiv pe date chinezești).

## Pasul următor

Base loop cu LongCat-Video-Avatar 1.6 (MIT), modul ai2v. Apoi re-sync per episod cu Chanjing-Avatar-V2V-1.3B (Apache-2.0) sau InfiniteTalk.
