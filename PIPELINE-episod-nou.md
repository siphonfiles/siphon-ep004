# Siphon Files — procesul automat pentru un episod nou (de la research la upload)

> **Pentru Claude, în chatul nou:** citește tot fișierul înainte de orice pas. Descrie procesul complet care se repetă la fiecare episod, așa cum a fost făcut la ep. 001 (Drift), ep. 002 (Bitget) și ep. 003 (Coldcard), plus regulile date de proprietar pe 25 nov 2026.
>
> Sursele de adevăr rămân:
> - `CLAUDE.md` din `siphon-core` (regulile, costurile, licențele, lecțiile din secțiunea 8);
> - `CLAUDE.md` din `siphon-ep003`, cel mai complet jurnal de decizii;
> - `HANDOFF-ep001.md` și `HANDOFF-ep003-coldcard.md`.
>
> Cu proprietarul vorbești **în română**, scurt, cu rezultatul, nu cu pașii. Tot conținutul canalului (script, text pe ecran, titlu, descriere) e **în engleză**.

---

## 0. Ce e bucla și când pornește

Procesul e **recurent**. De fiecare dată când un episod e gata și proprietarul a dat acceptul pentru upload pe YouTube, bucla pornește de la capăt cu episodul următor (pasul 1).

**Prima rulare** pornește pe 25 nov 2026, cu **ep. 004**, programat pentru **luni, 14 decembrie 2026, ora 18:00** (ora României).

| Episod | Publicare |
|---|---|
| ep. 001 | publicat pe 23 nov |
| ep. 002 | 30 nov |
| ep. 003 | programat pe 7 dec |
| ep. 004 | **14 dec**; 4K și upload cel târziu pe 13 dec |

Ritmul: **un episod pe săptămână, lunea la 18:00**. Un episod durează de obicei **3–6 zile**, pentru că singura limită reală e cota zilnică de Hugging Face.

### Ce face proprietarul și ce faci tu

Tu faci tot, cu excepția a cinci lucruri.

| Ce face proprietarul | De ce |
|---|---|
| **Stă la Mac în timpul research-ului** (pasul 1) | Research-ul pe YouTube se face din Chrome-ul lui, prin extensia Claude in Chrome. Înainte să începi, întreabă-l dacă e la Mac. Dacă nu e, așteaptă și pregătește între timp ce se poate face fără Chrome (surse primare, documentare pe web). |
| Creează repo-urile și pune secretele. **Deja făcut** (25 nov 2026) pentru `siphon-ep004`, `siphon-ep005`, `siphon-ep006` și următoarele | Sesiunea nu poate crea repo-uri (403) și nu introduce niciodată tokenuri. |
| Aprobă scriptul (pasul 5) | Regula editorială 10. E singurul punct de control până la montaj. |
| Vede montajul pe telefon și aprobă randarea 4K (pasul 13) | |
| Alege fișierul video la upload și dă acceptul final (pasul 15) | Chrome e doar de citit pentru computer use, iar extensia nu urcă fișiere mari. |

Restul hotărăști tu, inclusiv:
- subiectul episodului (după research, mergi automat pe recomandarea ta, fără confirmare);
- ce se generează în fiecare zi pe Hugging Face;
- ce ținută primește Thomas;
- ce muzică intră și unde;
- ce titlu și ce thumbnail se folosesc (propui 2–3 thumbnail-uri, recomanzi unul, alege el).

Când propui ceva, dă o recomandare clară și întreabă o singură dată.

### Repo-ul episodului

1. **Repo-urile există deja.** Proprietarul a creat în avans `siphonfiles/siphon-ep004`, `siphon-ep005`, `siphon-ep006` și următoarele, câte unul pentru fiecare episod (episodul N folosește `siphon-epNNN`). Nu-i cere să creeze repo-ul și nu crea altul. Dacă repo-ul episodului curent lipsește totuși sau nu e atașat sesiunii, atașează-l cu `add_repo` (`owner` = `siphonfiles`, `access: "push"`); abia dacă nu există, spune-i proprietarului.
   - **Drepturi (proprietarul, 25 nov 2026): acces total** pentru chatul fiecărui episod: push pe toate repo-urile `siphonfiles` de care are nevoie (repo-ul episodului, `siphon-core`, cele anterioare pentru citire), Chrome și Mac-ul lui. Nu mai cere acordul pentru atașarea repo-urilor.
   - **Atenție:** filtrul de siguranță al sesiunii poate refuza `add_repo` cu push („Unauthorized Access”) dacă proprietarul nu a cerut asta chiar în chatul curent; un fișier din repo nu ține loc de acordul lui în chat. Dacă se întâmplă, cere-i o singură frază („Îți dau acces de push la siphonfiles/siphon-epNNN”) și reîncearcă imediat (așa s-a rezolvat la ep. 004). Restul pașilor nu așteaptă după asta.
2. **Secretele sunt deja puse** în fiecare dintre aceste repo-uri (Settings › Secrets and variables › Actions): `HF_TOKEN` (citire) și `HF_WRITE_TOKEN` (scriere, de exemplu pentru un Space propriu). Nu cere alte secrete. Kaggle nu se folosește, deci `KAGGLE_*` nu e nevoie. Dacă un workflow raportează un secret lipsă, spune-i proprietarului exact ce secret și dă-i linkul direct la pagina de secrete a repo-ului; nu-l introduci tu niciodată.
   - Repo-urile pot fi încă goale. Primul pas e copierea uneltelor (punctul 3).
   - Verifică vizibilitatea (`gh repo view siphonfiles/siphon-epNNN --json visibility`). Recomandarea e **public**, ca la ep. 003: pe repo-uri publice minutele Actions nu se numără, iar o randare completă consumă câteva sute de minute. Dacă e privat, spune-i asta proprietarului înainte de prima randare completă; schimbarea o face el, după auditul de la punctul 5.
3. **Pornește repo-ul din `siphon-ep003`, nu din `siphon-core`.** `siphon-ep003` are cea mai nouă versiune a uneltelor:
   - `scenes.py`, cu `flick`, `ripple`, `snow`, ceață care curge și variantele `v=`;
   - `scripts/screen_content.py`;
   - garda `check_no_flash`;
   - `build_captions_ep003.py` și `make_captions_ep003.py`;
   - `thumbnails/make_ep003_options.py`;
   - `sound/ep003/ep003_mix.py`;
   - workflow-ul `render-ep003.yml`.

   Copiază tot ce e generic și redenumește `ep003` → `epNNN`. **Nu** copia materialul episodului (ilustrații, clipuri, voce). Nu copia workflow-urile care pornesc singure la push sau pot consuma cotă: `set-refs.yml`, `graphics-demo.yml`, `space-api.yml`, `voice-test.yml`.
4. Toate workflow-urile rămân **doar `workflow_dispatch`** (fără `pull_request`). Pe repo public nu intră niciodată în fișiere sau în loguri secrete sau date personale ale proprietarului: nume, emailuri, conturi, căi de pe Mac.
5. Înainte ca repo-ul să devină public, fă auditul ca la ep. 003: tot istoricul fără tokenuri și fără date personale.

---

## 1. Research de subiect (proprietarul la Mac)

Scopul e un caz cu **cerere reală** și **ofertă slabă**. Pot fi cazuri noi (ultimele 1–6 luni) sau mai vechi, pe care nimeni nu le-a acoperit bine.

1. **Lista de candidați (8–12).** Surse:
   - DefiLlama (hacks);
   - Rekt.news;
   - rapoartele Chainalysis, TRM Labs, Elliptic, SlowMist, Halborn;
   - comunicatele DOJ, FBI, SEC și CFTC;
   - procese colective;
   - post-mortem-urile publicate de firme.

   Pornește de la `research/topic-research-2026-11.md`: are candidații rămași de data trecută. Exclude subiectele deja făcute (Drift, Bitget, Coldcard) și cazurile saturate (de exemplu Binance $6,3B, Bybit, FTX), dacă nu există un unghi complet nou.
2. **Cererea și concurența, pe YouTube, din Chrome.** Pe pagina de căutare, citește `window.ytInitialData` cu `javascript_tool`: titlu, canal, vizualizări, vechime, durată. `fetch` din pagină e blocat.

   | Semnal | Cum îl citești |
   |---|---|
   | Cerere | vizualizări mari la video-uri mici sau vechi; comentarii cu întrebări rămase fără răspuns; căutări sugerate (autocomplete) |
   | Ofertă slabă | maximum câteva mii de vizualizări pe cel mai bun video dedicat cazului; nimeni nu a făcut investigația completă |
   | Concurență | canalele de urmărit: Coin Bureau, Gloam, fern, Lume, Crumb, DW, Patrick Boyle |

   Notează unghiurile pe care concurența le-a folosit deja, ca să le eviți.
3. **Psihologia audienței** pentru fiecare dintre cei 3 finaliști:
   - **cine** se uită: bărbați de 18–49 de ani, deținători de crypto, oameni pasionați de securitate, fani true crime;
   - **ce frică sau ce nevoie** atinge cazul: „poate să mi se întâmple și mie”, auto-protecție, satisfacția „eu n-aș fi căzut”, curiozitatea „cum e posibil”;
   - **ce întrebare precisă** își pune spectatorul și o poate închide video-ul;
   - **de ce acum**: un proces în curs, fonduri care încă se mișcă, o lecție practică pentru oricine are un portofel.

   Bazează-te pe `research/retention-psychology.md`, `research/suspense-storytelling.md` și `research/title-psychology.md`. Adaugă studii noi dacă găsești. Fii creativ: caută în fiecare caz omul de care să-ți pese, ironia, momentul, amprenta.
4. **Testul de material.** Cazul trebuie să aibă:
   - surse primare suficiente pentru ~10 minute;
   - o cronologie precisă (ideal la minut);
   - cel puțin un om real care a vorbit public, cu fapte;
   - un mecanism care se poate explica vizual;
   - un final deschis sau o ironie.

   Fără surse primare, cazul cade.
5. **Livrabilul pasului:** `research/epNNN-topic.md`, cu cei 3 finaliști, datele de concurență, psihologia audienței și recomandarea ta, plus un rezumat de 5–8 rânduri pentru proprietar. **Subiectul îl alegi tu (proprietarul, 25 nov 2026):** după research, mergi automat pe recomandarea ta și treci direct la pasul 2, fără să-i ceri confirmarea. Îi trimiți doar rezumatul, ca informare.

## 2. Documentarea cazului

1. Citește **direct** sursele primare: comunicatul firmei, post-mortem-ul, raportul tehnic, dosarul de instanță, explorerele de blocuri. Ce nu se poate citi din sesiune se citește din Chrome. Presa e doar pentru context. Fiecare cifră și fiecare dată se verifică pe cel puțin o sursă primară.
2. Construiește:
   - cronologia (în UTC, cu ora României unde contează);
   - lista de fapte, fiecare cu sursă `[S1]…[Sn]`;
   - ce **nu** se știe (identitate, atribuire, recuperări). Se spune explicit în video.
3. **Atribuirea și acuzațiile:** „alleged/charged” până la condamnare; atribuirea doar așa cum o formulează sursa (de exemplu „Chainalysis believes”); fără speculații despre intenții; fără oameni sau scene inventate.
4. **Faptele datate (regula 14a):** orice se mai poate schimba (arestări, fonduri nemișcate, procese, despăgubiri, cifre finale) se spune cu marcaj de timp: „as we make this video”, „so far”, „as of the latest public tracking”. În video apare un carton „STATUS AS OF <lună an>”.

## 3. Povestea

Scrii pe tiparul episoadelor 001–003 (regula 14 din `CLAUDE.md` și cele două fișiere de research):

1. **Prima frază e o imagine mică și concretă.** La ep. 003 a fost caseta de valori, la ep. 002 testul de 93 TRX.
2. **Teaser-ul (~30–40 s):** fraze tăiate, plătite mai târziu, cu bas pe fiecare tăietură. Primele 30 s **confirmă exact titlul și thumbnail-ul**: aceeași cifră, același cârlig.
3. **Rezultatul la început**, apoi „cum s-a ajuns aici”, cu o **numărătoare inversă T-minus** spre momentul-cheie.
4. **Un om de care să-ți pese**, doar cu fapte (victimă care a vorbit public, angajat, firmă). Ca Jonathan Goodman la ep. 003.
5. Între scene: **„dar” / „așa că”**, niciodată „și apoi”. Nicio secțiune nu se termină pe o concluzie, ci pe o problemă nouă.
6. **Disparitatea de cunoaștere:** „noi știm, ei nu”.
7. **Amprenta** (detaliul care îl trădează pe hoț) se plantează înainte de vârf.
8. **Un gol de informație mic și precis per act**, închis mereu. Relansare la fiecare 60–90 s. Scene concrete, nu rezumate. Cel mult 2–3 cifre rostite pe secțiune.
9. **Finalul revine la prima imagine** și se termină pe un ac („om în groapă”), formulat corect, fără promisiuni neplătite.
10. **Thomas** are replici scurte (**≤ 12 cuvinte**, ~4,5 s), câte un clip de 5 s pe replică. Mai multe în tabelul din pasul 8.
11. **Identitatea vizuală a episodului** se hotărăște acum:
    - temă nouă `SIPHON_THEME=epNNN`: fundal, culoare de accent, fonturi cu licență OFL, motiv de fundal legat de caz;
    - ținuta lui Thomas și obiectele de pe birou.

    Ep. 002 a avut petrol și cyan (camera de supraveghere), ep. 003 grafit și verde smarald (seiful). Nu repeta niciuna.

## 4. Scriptul și verificarea lui

1. Scriptul se scrie în `episodes/NNN-slug.md` (engleză), cu:
   - etichete `[MUSIC: …]`;
   - replicile lui Thomas marcate;
   - sursele `[Sn]`;
   - o listă „Changes” la fiecare versiune.

   Traducerea în română merge în `episodes/NNN-slug.ro.md`.
2. **Durata:** **cel mult 11:00** (regula proprietarului). Ținta e 10:00–11:00: peste pragul de mid-roll de 8 min, fără umplutură. Calculează din numărul de cuvinte (~150 de cuvinte/min la vocea lui Thomas cu pauze) și verifică pe vocea generată.
3. **Verificarea, înainte să-l dai proprietarului:**
   - **faptele:** fiecare propoziție cu cifră, dată sau nume are o sursă primară citită de tine;
   - **gramatica și sensul:** LanguageTool (`lt-check.yml`, en-GB) pe replici și pe textele de pe ecran, plus o lectură a ta, rând cu rând, pentru logică;
   - **lista de întrebări:** fiecare întrebare pe care o deschide video-ul (în teaser, în titlu, pe thumbnail, la finalul actelor) e într-un tabel cu momentul în care primește răspuns. Unde răspunsul nu se cunoaște, video-ul **spune explicit** asta („we don't know yet”, „no one has said”). Nicio întrebare nu rămâne fără răspuns sau fără mențiunea că nu se știe. Tabelul intră în `episodes/NNN-slug.md`, secțiunea „Open questions”.
   - **forma pentru voce:** cifre, date și tickere scrise în cuvinte, după lista de pronunții din `presenter/voice.md`. Replicile se termină cu punct, nu cu „—” sau „...” (ZONOS taie ultimul cuvânt).

## 5. Aprobarea scriptului (proprietarul)

Trimite-i scriptul și traducerea în română, plus 3–5 rânduri: unghiul, durata estimată, câte replici are Thomas, ce nu se știe. Pornești vocea și generările doar după aprobare.

## 6. Vocea (CPU, $0)

1. Aceeași voce: **Siphon Narrator v1** (ZONOS3-Mini, amprenta `presenter/siphon_narrator_v1_embedding.pt`, referința `presenter/voice_ref_v1.wav`), cu `tts-lines.yml`. Replicile sunt în `sound/epNNN/epNNN_lines.json`, rezultatele pe branch-ul `voice-tests`.
2. **Verificarea, într-o buclă până iese perfect:**
   - ASR cu **două modele** (faster-whisper `large-v3` și `medium.en`, `asr-check.yml`) pe vocile curate;
   - o problemă reală înseamnă că ambele modele aud același cuvânt greșit, că un nume e greșit sau că ASR-ul are încredere mică. Cifrele scrise altfel nu contează;
   - replicile cu probleme se refac cu alte seed-uri sau cu numele scris în silabe („Bit-get”), apoi se verifică din nou automat;
   - ce greșește ZONOS des: „Siphon Files” la final (se lipește „-iphon Files” din replica de prezentare, păstrând durata), nume de firme și replici foarte scurte (inventează silabe; lipește-le de replica vecină);
   - fiecare variantă și motivul ei se notează în `sound/epNNN/voice_takes.md`.
3. Abia când **toate** replicile sunt curate pe ambele modele trec la mixaj.

## 7. Muzica și sunetul (CPU, $0)

Mixajul e în `sound/epNNN/epNNN_mix.py`, pornit din `sound/ep003/ep003_mix.py`. Cronologia rezultată merge în `graphics/motion/epNNN_full.timeline.json`.

1. **Piesele:** de preferință cele din episoadele 1–3, toate originale, sintetizate în cod:
   - piesa de jaf (`heist_design.py`, 112 BPM, re minor) pentru teaser, cursă și final;
   - `vault_run` (`heist_tracks.py`, 124 BPM, mi minor) pentru momentul-cheie al furtului;
   - `memory_piano` pentru partea umană sau tristă;
   - loviturile de bas și sub drop-ul (`sting_design.py`) pentru teaser, cartoanele T-minus, cifrele mari și finalurile de act.

   Poți crea o temă nouă în același stil, dacă se potrivește cazului. Fără muzică „de înmormântare” (ambientul a fost respins).
2. **Unde intră muzica:** teaser-ul, momentul-cheie, 4–6 porțiuni de narațiune care cer tensiune și finalul (~20 s). **Nu** stă în fundal tot episodul.
3. **Muzica nu se suprapune niciodată cu Thomas în cadru.** Se termină înainte ca el să înceapă să vorbească și reintră după.
4. **Volumul:** intrare lină de la minim (~3 s; ~2 s când intră doar tobele), creștere pe parcurs, ieșire lină la minim (~4–5 s), terminată **înainte** de replica-cheie, nu tăiată. Nivelul sub narațiune e ~-12 dB, iar piesele de moment ~-10 dB.
5. **Masterul:** -14 LUFS, vârful sub -1,5 dBFS, verificat cu `ffmpeg ebur128`. Rezultatul merge în `renders:audio/epNNN_audio.m4a`.

## 8. Hugging Face: cota, calendarul și regulile (cel mai important pas)

### Regulile

| Regula | Ce înseamnă |
|---|---|
| Ce se generează | **Doar** clipurile cu Thomas, **doar la 720p** (LongCat-Video-Avatar 1.6, Space-ul `victor/LongCat-Video-Avatar-1.6`, DBCache faster, seed 42), **doar pe Hugging Face**. Plus imaginile (Z-Image-Turbo) și referința nouă a lui Thomas (Z-Image + Qwen-Image-Edit-2511). Fără Kaggle. Fără clipuri video cu altceva decât Thomas. |
| Cota | **Cel mult 40 de minute de cotă ZeroGPU pe zi, cu tot cu imaginile.** Plănuiește **≤ 38 de minute** (2 minute de rezervă). Fără credite plătite: nimic peste cota gratuită. |
| Teste | **Nimic de probă.** Se generează doar ce intră în episod. Probele de aspect se fac pe CPU, din materialul existent. |
| Ora de start | Fiecare zi de generare pornește **la cel puțin 25 de ore după startul precedent**: cota se resetează la 24 h după prima folosire, plus o oră de rezervă. |
| Durata totală | Toate clipurile cu Thomas ale unui episod se generează în **cel mult 6 zile**. |
| Cine decide | Tu hotărăști ce se generează în fiecare zi. Proprietarul primește la final un mesaj scurt cu ce s-a generat și cât a consumat. |

**Exemplul proprietarului:** generarea a pornit pe 25 nov 2026 la 03:31. Deci următoarea pornește cel mai devreme pe 26 nov la 04:31, apoi pe 27 nov la 05:31, 28 nov la 06:31, și tot așa.
- Startul se ia după **ora reală de pornire** a rulării precedente, din registru, nu după ora planificată.
- Dacă o zi se sare, următoarea poate porni oricând după +25 h față de ultimul start real.
- Dacă ora ajunge prea târziu în zi, se poate reveni mai devreme doar printr-o zi fără generare, cu +25 h respectate de fiecare dată.
- Atenție: cota e **una pe cont**. Dacă proprietarul a folosit Hugging Face din browser, se numără și asta. Întreabă-l sau verifică pagina de billing din Chrome când e la Mac.

### Registrul de cotă (obligatoriu)

Fișierul `quota/hf_ledger.md` din repo-ul episodului, actualizat după fiecare rulare, cu câte un rând pe rulare:
- ora reală de start (ora României);
- ce s-a generat;
- secundele de GPU raportate de workflow;
- cota estimată consumată;
- eșecurile (și ele consumă cotă).

Din registru se calculează ora de start a zilei următoare și ce încape în ea. Înainte de prima generare a unui episod, ia ultimul start din registrul episodului precedent: la ep. 004 asta e **25 nov 2026, 03:31**.

### Costul măsurat în cotă

| Ce | Cotă | Observații |
|---|---|---|
| Clip Thomas 720p, 5 s | **~10,7 min** (GPU „xlarge”, ~2× timpul real) | Maximum **3 clipuri pe zi** (~32 min). 4 clipuri nu încap. |
| Clip pierdut | ~11 min | O cerere care depășește 240 s de GPU se pierde integral. Un clip generat dar nedescărcat se plătește de două ori. Descărcarea se face cu reîncercări (reparat după b8 la ep. 003). |
| Ilustrație Z-Image, 2048x1152, 8 pași | **~13–18 s** | Plănuiește 18 s. 30 de imagini ≈ 9 min. |
| Portret Z-Image cu ținută nouă | ~10–20 s per variantă | 3 variante ≈ 1 min |
| Biroul cu Qwen-Image-Edit-2511 (40 de pași) | ~100 s de ceas, **plănuiește ~3,5 min de cotă** | |

### Câte clipuri cu Thomas

Proprietarul vrea **minimum 1 minut, maximum 2 minute** de Thomas, în **cel mult 6 zile** de generare. La 3 clipuri/zi, limita reală e:

| Zile | Clipuri | Thomas pe ecran |
|---|---|---|
| 5 | 13 | ~1:00 (minimul) |
| 6 | 17 | ~1:20–1:25 (maximul care încape în 6 zile) |

**2 minute (~24 de clipuri) cer 8 zile și nu încap în 6.** Țintește 15–17 clipuri. Spune-i asta proprietarului în planul de producție, ca să nu se aștepte la 2 minute.

### Calendarul tip

| Zi | Ce se generează | Cotă plănuită |
|---|---|---|
| Ziua 1 | ținuta nouă (3 portrete + birou) + **toate ilustrațiile** (~30–35) + **2 clipuri** | ~1 + 3,5 + ~10 + 21,4 ≈ **36 min** |
| Zilele 2–6 | **3 clipuri** pe zi + înlocuiri de imagini respinse sau imagini noi pentru scene care le cer (cel mult ~15 imagini) | ≤ 32,1 + 4,5 ≈ **36,6 min** |

Total: 2 + 5 × 3 = **17 clipuri**.
- Dacă vocea e gata abia după ziua 1, ziua 1 face doar ținuta și imaginile, iar clipurile pornesc în ziua 2. Totalul tot nu trece de 6 zile.
- Un clip refăcut din cauza unui defect intră în zilele rămase, nu adaugă zile.

### Ordinea dependențelor

1. Clipurile cer **vocea finală** (fiecare clip e replica lui + 0,3 s de liniște la început, completat cu liniște până la 5 s) și **referința nouă**.
2. Referința nouă cere ținuta aleasă.
3. Imaginile cer lista de scene din scriptul aprobat.
4. Deci: script aprobat → voce verificată → ziua 1 de generare.

### Ținuta lui Thomas, la fiecare episod

1. **E mereu același om** din episoadele 1–3. Singura imagine de referință pentru clipuri e cea a episodului. Ca punct de plecare: `presenter/reference/thomas_ref_ep003_1920x1080.png` și rețeta ei (`presenter/outfits/ep003/portrait_log.json`, `desk_log.json`).
2. **Ținuta e nouă la fiecare episod**, legată discret de caz, fără logo-uri, etichete sau accesorii. Până acum:
   - pulover gri-cărbune (ep. 001);
   - cămașă bleumarin (ep. 002);
   - cămașă verde-oliv (ep. 003).
3. **Portretele:** `outfit-ref.yml` (step=portrait), cu `scripts/gen_outfit_portrait.py`. Aceeași rețetă Z-Image: seed **596067**, 896x1152, 8 pași, time shift 3, **același prompt**, se schimbă doar fraza despre haine. Descrie hainele pozitiv, fără negații. Fă **3 variante**.
4. **Alegerea:** păstrezi varianta în care fața e aceeași. La ep. 003, 2 din 3 variante au schimbat omul. Verifici:
   - vizual, pe o comparație cu portretul original (`compare_original_vs_3_outfits.jpg`);
   - cu similaritatea feței (OpenCV YuNet + SFace, pe CPU) față de `presenter/portrait_v1_896x1152.png`.

   Dacă niciuna nu păstrează fața, nu continui cu clipurile până nu rezolvi. Înlocuirea se face tot în bugetul zilei.
5. **Biroul:** `outfit-ref.yml` (step=desk), Qwen-Image-Edit-2511, cu portretul ales și decorul `presenter/set_candidates/plate_20251120.png`, seed 11, 40 de pași.
   - Decorul rămâne același. Se schimbă doar câteva obiecte de pe birou, legate de caz (la ep. 003: trei dispozitive negre fără logo, zaruri, placa de oțel, cheia de seif).
   - Lampa rămâne în aceeași parte. Verifică de ce parte a lui Thomas stă fiecare obiect.
   - Se aduce la 1920x1080 → `presenter/reference/thomas_ref_epNNN_1920x1080.png`.

### Clipurile

- Sunt joburi JSON în `presenter/clips/inputs/`, generate de `scripts/make_epNNN_clip_inputs.py` (după `make_ep003_clip_inputs.py`), și rulează cu `longcat-batch.yml`, pe rând, cu oprire la prima eroare.
- **Thomas doar în video, niciodată imagine fixă.** Prim-planul („a doua cameră”) e același clip mărit. Planul mediu și prim-planul se alternează între replicile consecutive.
- Fiecare clip se verifică pe cadre (0,2 / 2 / 4,5 s): aceeași față, aceeași ținută, obiectele stabile, nicio deformare. Gesturile moderate cu mâinile sunt acceptate de proprietar.

### Programarea

- Fiecare zi de generare se programează cu `send_later` (mesaj înapoi în același chat), la ora calculată din registru.
- La declanșare:
  - verifici registrul și ora;
  - pornești workflow-ul (sau workflow-urile, pe rând, în grupul de concurență `zerogpu` / `longcat`);
  - programezi o verificare (`send_later`) după ~30–60 min;
  - verifici rezultatele;
  - scrii registrul;
  - programezi ziua următoare.
- Nu aștepta în chat.

## 9. Ce se face pe CPU între timp (GitHub Actions, $0)

- **Ilustrațiile.** Joburile sunt în `illustrations/epNNN/*.json`, cu sufixul de stil fix din `gen_illustrations.py`. Regulile:
  - un subiect per cadru;
  - oameni **doar din spate sau în siluetă**, fără fețe;
  - fără text și fără logo-uri;
  - accentul de culoare cerut **doar pe un obiect anume** (altfel apar pete rătăcite);
  - de evitat numărători exacte, efecte fizice complexe și „fotografii cu fața în jos”.
- Fiecare ilustrație se verifică la generare. Ce se repară pe CPU:
  - petele de culoare rătăcite: OpenCV `inpaint` sau scăderea profilului radial al strălucirii;
  - **niciun ecran gol:** `scripts/screen_content.py`, cu conținut legat de scenă, lizibil din unghiul camerei, iar codul inventat etichetat ILLUSTRATIVE. Originalul se păstrează ca `*_blank.jpg`.
- **Hărțile de adâncime:** `depth-maps.yml` (Depth Anything V2 Small), 8-bit, 1024x576, netezite. Diferența aproape/departe rămâne mică (fără deformări).
- **Animarea ilustrațiilor** (scena `illus` din `scenes.py`):
  - parallax 2.5D cu mișcare rigidă de cameră;
  - **orice sursă de lumină pâlpâie** (`flick=`, `mode="flicker"` sau `"slow"`), iar raza desenată pâlpâie odată cu ea;
  - praf doar în interior; **în exterior `motes=False`**, cu ninsoare (`snow=True`) unde e iarnă și ceață care se vede că trece (`fog` cu `speed` ~25, `haze` ~0,15);
  - abur sau ceață pe apă doar dacă se potrivește scenei;
  - `ripple=` pe ecrane și benzi de lumină;
  - `glows` (pulse, flicker, beam) unde e cazul.
- **Grafica din cod:** scene noi în `graphics/motion/scenes_epNNN.py`, create pentru cazul ăsta. Fii creativ.
  - **Nimic nu se repetă:** nicio ilustrație, niciun design de grafic, niciun carton. Capitolele, citatele, explicațiile, T-minus, cifrele mari și frazele au fiecare varianta lor (`v=`).
  - **Cartonul apare exact pe cuvintele lui** și stă cât se vorbește despre el, cu animație lentă, ușor de urmărit.
  - Mesajele reconstruite se etichetează „ILLUSTRATIVE · NOT THE REAL MESSAGES”.
- **Montajul:** `graphics/motion/epNNN.py`, cu scenele ancorate pe replici din cronologie. Garda **`check_no_flash`** rămâne activă: niciun rest sub 1 s după Thomas. Probele se fac pe segmente scurte (`preview-segments.yml`) sau pe cadre (`render-epNNN.yml` cu `stills`), înainte de randarea completă.

## 10. Montajul 1080p și verificarea finală

1. Randarea completă cu `render-epNNN.yml` (scale 1 = 1080p + previzualizare 720p) produce un Release `epNNN-render-N`. Rulează în fundal.
2. **Verificări automate, toate obligatorii înainte să-i trimiți ceva:**
   - **loudness:** -14 LUFS, vârful sub -1,5 dBFS (`ebur128`);
   - **repetiții:** cadre la 0,5 s, comparate între ele. Nicio pereche de planuri asemănătoare la momente diferite, în afară de Thomas;
   - **flash-uri și negru:** `blackdetect` / `freezedetect`; negrul doar unde e plănuit;
   - **ASR pe mixul final:** fiecare replică tăiată din coloana sonoră (`cut_mix_lines.py` + `asr-mix.yml`), cu cele două modele. Muzica nu acoperă nicio replică;
   - **textele de pe ecran:** LanguageTool pe fișierele de scene;
   - **cadrele:** stills la toate momentele-cheie (teaser, titlu, fiecare clip Thomas, fiecare carton nou, final). Le verifici tu, vizual;
   - **durata:** ≤ 11:00.
3. Tot ce pică se repară și se re-verifică. Abia apoi treci la pasul 13.

## 11. Titlul (research)

1. Research pe concurență pentru cazul ales: ce titluri și unghiuri există deja. Pe acelea le eviți.
2. Regulile (`research/title-psychology.md`):
   - **afirmație, nu întrebare**;
   - 5–8 cuvinte;
   - numele cazului (pentru căutare) + miza;
   - curiozitate precisă, nu vagă;
   - „Inside X” a mers bine (≈2,5× în studiul vidIQ);
   - cifra din titlu = cifra din primele 30 s;
   - fără clickbait neplătit în video.
3. 3–5 propuneri cu argumentul fiecăreia. Recomanzi una.

## 12. Thumbnail-uri

- 3 variante pe CPU, după modelul `thumbnails/make_ep003_options.py` (PIL + fontul Anton), din ilustrațiile episodului, fără cotă.
- Textul are **3–5 cuvinte** și **completează titlul, nu-l repetă** (de exemplu, suma din titlu nu apare și pe thumbnail).
- Fără logo-uri reale și fără dispozitive care să semene cu cele reale. Simbolul ₿, desenat în cod, se poate folosi.
- Elementul cheie stă separat de lumina spotului sau a felinarului, ca să iasă în evidență.
- Lizibil pe mobil (verifică la 320 px lățime).
- Recomanzi varianta cea mai bună, cu argument; proprietarul alege. Cea aleasă devine `thumbnails/epNNN/epNNN_thumbnail_FINAL.jpg`.

## 13. Link pentru telefon, apoi 4K

1. Trimite-i proprietarului **linkul către previzualizarea 720p** din Release, care se deschide pe telefon din aplicația GitHub sau din browser. Pune și 3–5 rânduri despre ce să urmărească.
2. Îți dă observațiile **pe rând**. Nu schimbi nimic până nu spune că a terminat. Corecturile se probează pe segmente, apoi urmează o randare 1080p nouă și din nou link.
3. **Îi ceri acordul explicit pentru 4K.** Abia apoi pornești `render-epNNN.yml` cu scale 2.
   - În Release-ul 4K pun și thumbnail-ul, descrierea, subtitrările și fișa de upload.
   - Fișierul 4K trebuie să rămână **sub 2 GB** (limita Release-urilor).
   - Randează 4K cu cel puțin o zi înainte de publicare.

## 14. Pachetul de upload YouTube

Modelul e `siphon-ep003` › `episodes/publish/003-youtube.md` + `003-description.txt`. Fișierele noi:

- **`episodes/publish/NNN-youtube.md`:**
  - titlul și thumbnail-ul;
  - playlistul **„Crypto Heists, Investigated | Siphon Files”** (`PLEnuhe2RTLmg`);
  - audiență: nu e pentru copii;
  - paid promotion: No;
  - **Altered or synthetic content / AI use = Yes**;
  - capitolele automate, locurile și conceptele: off;
  - tag-uri (sub 500 de caractere);
  - limba English (UK);
  - categoria Education;
  - licența Standard;
  - ecranul de final (1 video + 1 subscribe, ultimele 20 s);
  - programarea;
  - verificarea din ziua publicării.
- **`episodes/publish/NNN-description.txt`** (sub 5.000 de caractere):
  - rezumatul;
  - „STATUS AS OF <lună an>”;
  - declarația că prezentatorul e AI;
  - capitolele (verificate pe cadrele din versiunea finală);
  - toate sursele `[S1…Sn]`;
  - fără sfaturi de investiții.
- **Subtitrările:**
  - `NNN-captions-en.srt`, din cronologia vocii (`make_captions_ep003.py` adaptat);
  - traducerile în **14 limbi** (ro, es, pt-BR, de, fr, it, pl, tr, ru, id, vi, hi, ja, ko), pe fraze întregi, cu aceiași timpi, construite și verificate cu `build_captions_ep003.py` adaptat. Se verifică cifrele, numele, viteza de citire și formatele locale.

## 15. Upload, programare, publicare (cu proprietarul)

1. Proprietarul descarcă fișierul 4K și îl alege în YouTube Studio. Restul completezi tu din Chrome:
   - descrierea, cu `execCommand('insertText')`;
   - thumbnail-ul și subtitrarea EN, prin inputurile ascunse;
   - toate câmpurile din fișă;
   - ecranul de final și playlistul.
2. Subtitrările în cele 14 limbi: Languages → Add language → Subtitles → Upload file (cu timpi) → Publish. **După fiecare limbă verifică tabelul**: la ep. 003, japoneza n-a fost salvată din prima.
3. Programarea: **luni, la 18:00 (GMT+2)**, în slotul săptămânal liber.
4. **În ziua publicării, dimineața:** reverifici faptele datate și actualizezi paragraful STATUS din descriere dacă s-a schimbat ceva. Verifici și rezultatul verificărilor YouTube (drepturi de autor, restricții).
5. Când proprietarul dă **acceptul pentru upload**, episodul e închis și **bucla repornește de la pasul 1** pentru episodul următor.

## 16. Reguli care se aplică peste tot

- **Licențe doar cu uz comercial** (`CLAUDE.md` §7). InsightFace e interzis (se folosește YuNet).
- **Fără voci sau fețe de persoane reale.** Fără fotografii ale persoanelor publice în video.
- **Task-urile lungi rulează în fundal:** pornești, răspunzi imediat, verifici cu `send_later`. Proprietarul nu stă blocat în chat.
- **Dacă o rulare pică pe CPU, o repari singur** și îi spui doar rezultatul. Dacă pică pe Hugging Face, notezi în registru cota pierdută și refaci doar dacă încape în bugetul zilei.
- **Totul se salvează imediat în git:** imagini, variante, scripturi, rezultate. Media mare (video de episod) merge în Releases. Arhiva: `.drp` în git, media în Release `epNNN-archive`, dacă se lucrează în DaVinci.
- **Ștergeri** (Release-uri vechi, fișiere) doar cu confirmarea explicită a proprietarului.
- **Credențiale:** niciodată. Proprietarul se loghează singur.
- **`CLAUDE.md`** din repo-ul episodului (și din `siphon-core`, pentru reguli generale) se actualizează după fiecare decizie, cu commit.
- Preferințele noi ale proprietarului, primite la vizionare, intră în `siphon-core` › `CLAUDE.md` › secțiunea 8 și se aplică din prima la episodul următor.
