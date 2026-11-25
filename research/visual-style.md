# Stilul ilustrațiilor (21 nov 2026)

Decizie luată de Claude, la cererea proprietarului, din research psihologic + analiza video-urilor de succes din nișă.

## 1. Ce spune cercetarea (psihologie)

- **B-roll-ul ajută doar dacă ilustrează exact fraza.** Imaginile generice sau doar vag legate nu cresc retenția și uneori o scad (test controlat Opus, 2025). Fiecare imagine = fraza pe care o spune Thomas în acel moment.
- **Schimbare vizuală la fiecare schimbare de idee**, nu la interval fix; pentru documentar 5-10 s pe imagine e normal. Cadru larg → mediu → detaliu ca variație.
- **Concret > abstract** (efectul de concretețe, Paivio; principiul multimedia, Mayer: narațiune + imagine > narațiune singură, d ≈ 1,35). Obiectul din metaforă trebuie arătat literal: sertarul, cecul, seiful.
- **Coerență (Mayer):** puține elemente, un singur subiect principal pe cadru. Fără text în imagine (textul îl pune grafica din cod; text + narațiune identice = redundanță).
- **Fețele captează privirea** cel mai puternic (eye-tracking), dar la noi fețele sunt risc juridic (oameni reali, defăimare) și risc AI (fețe ciudate). Soluție: oameni anonimi — siluete în contra-lumină, din spate, fețe în umbră. Păstrăm semnalul „social” (corpuri, postură, mâini la distanță) fără identitate.
- **Lumină low-key = mister/suspans** (film noir, thriller). Contrast complementar cald/rece = tensiune. Mici zone foarte luminoase în cadre întunecate fac negrul să pară mai adânc și imaginea mai clară.

## 2. Ce folosesc video-urile de succes (YouTube, 21 nov 2026)

| Canal / video | Vizualizări | Stil vizual (din storyboard) |
|---|---|---|
| Gloam — „How Binance Lost $6,300,000,000 in One Night” | 2,57M în 3 săpt. | randări 3D cinematice: seifuri ca metafore pentru portofele, lumini roșii, siluetă cu glugă fără față; alternează cu carduri „hârtie crem” (tweeturi, cronologii, ceasuri) |
| fern — „The Insane Hunt for China's Biggest Scammer” | 3,3M în 3 luni | reconstituiri 3D stilizate, albastru-închis/teal, spoturi de lumină; documente cu text evidențiat; diagrame albe pe negru |
| Lume — „The Hacker Who Stole $1.5 Billion In 2 Minutes” | 560k | birouri 3D cu manechine fără față (oameni anonimizați), monitoare, teal |

Concluzie: canalele mari din nișă **nu folosesc poze de stoc și nici fețe reale**. Folosesc **randări 3D stilizate**, întunecate, cu o singură culoare de accent, **metafore-obiect** și **oameni anonimizați**. Stilul ăsta mai semnalează clar „reconstituire”, nu filmare reală (corect jurnalistic).

## 3. Stilul Siphon Files

- **Randare 3D cinematică, realism stilizat**, materiale mate curate (nu foto-realism de stoc).
- **Paletă:** umbre bleumarin-cărbune (aceeași familie cu fundalul #141920), o singură lumină caldă amber ca accent, contur rece teal discret. **Roșu doar în momentele de pericol** (actul 5, golirea seifului).
- **Compoziție:** un singur subiect principal, straturi clare de adâncime (prim-plan / mijloc / fundal) ca parallax-ul 2.5D să funcționeze, spațiu negativ pentru suprapuneri.
- **Oameni:** doar anonimi — din spate, siluete în contra-lumină, fețe în umbră totală. Niciodată o față clară.
- **Fără text, logo-uri, mărci** în imagine. Ecranele au conținut estompat, ilizibil.
- **Format:** 2048x1152 (16:9, cea mai mare rezoluție a Z-Image-Turbo), 8 pași, Time Shift 3, seed fix per imagine.

## 4. Reguli de prompt (ca să iasă din prima)

1. Prompt în engleză, descriptiv: subiect → acțiune → cadru/unghi → lumină → straturi de adâncime → sufixul de stil fix.
2. **Fără negații** („no text”, „no faces”): la Z-Image negația activează conceptul. Se descrie pozitiv: „plain unmarked”, „faces hidden in deep shadow”, „blurred unreadable screen”.
3. Fără cuvinte care pot apărea scrise (nume de mărci, „crypto”, coduri de culoare hex, cifre).
4. Fără mâini în prim-plan și fără fețe vizibile (zonele clasice de artefacte).
5. Un singur subiect, maxim 3-4 obiecte numite.
6. Sufixul de stil identic la toate imaginile (în `scripts/gen_illustrations.py`).
