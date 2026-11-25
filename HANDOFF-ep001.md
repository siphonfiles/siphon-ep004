# Siphon Files: predarea după episodul 001 (pentru o sesiune nouă de Claude)

> **Pentru Claude, în sesiunea nouă:** fișierul ăsta rezumă tot ce s-a construit și s-a învățat la episodul 001 (Drift). Citește-l întâi, apoi `CLAUDE.md` din repo-ul atașat. `CLAUDE.md` rămâne sursa de adevăr: are regulile, jurnalul complet de decizii și lecțiile, cu date și cifre exacte. Lucrezi cu proprietarul **în română**. Conținutul canalului (scripturi, titluri, descrieri) e **în engleză**.
>
> Scris pe 22 nov 2026, la finalul episodului 001.

---

## 1. Ce e proiectul, pe scurt

- **Siphon Files** e un canal YouTube în engleză: documentare-investigație despre furturi, fraude și prăbușiri în crypto („unde dispar banii”). Nu face știri, prețuri sau trading.
- **Canalul:** [@siphonfiles](https://www.youtube.com/@siphonfiles), Channel ID `UC_w7oZaLq8wq3absfPkBu2g`, brand account separat.
- **Prezentatorul:** **Thomas Archer**, un personaj AI inventat, cu față și voce sintetice. E declarat AI pe față: „I'm Thomas Archer, the AI narrator of Siphon Files.”
- **Durata țintă a unui episod:** ~10:30–11:30, ca să treacă de pragul de mid-roll de 8 minute. Thomas apare cam 1:30–2:00, restul sunt grafică și ilustrații.
- **Totul se face gratuit.** Se folosesc doar cotele gratuite: GitHub Actions, cota ZeroGPU din abonamentul Hugging Face PRO, Kaggle și Mac-ul proprietarului. Nu se folosesc servicii plătite.

## 2. Reguli care nu se negociază

1. **Fără teste care consumă cotă sau bani** (HF ZeroGPU, Kaggle GPU etc.). Se generează doar ce intră în episod și doar cu acordul proprietarului. Probele de montaj și de aspect se fac pe CPU, din materialul deja generat.
2. **Thomas apare doar în video, niciodată ca imagine fixă.** „A doua cameră” e același clip mărit, nu o poză.
3. **Licențe doar pentru uz comercial** (canalul se monetizează). Lista modelelor permise și excluse e în secțiunea 7 din `CLAUDE.md`. Detectorul InsightFace e **interzis** (modelele lui sunt necomerciale) și se înlocuiește cu YuNet din OpenCV (MIT).
4. **Nu se clonează voci sau fețe de persoane reale.**
5. **Politica editorială:**
   - doar surse primare (comunicate oficiale, post-mortem-uri, dosare de instanță, firme de analiză on-chain);
   - „alleged/charged” până la condamnare;
   - fiecare afirmație are sursă;
   - atribuirea către un stat se spune exact cât e de sigură;
   - mesajele reconstruite sunt marcate „ILLUSTRATIVE”;
   - **proprietarul verifică fiecare script înainte de randare.**
6. **Credențiale:** Claude nu introduce niciodată parole sau tokenuri. Tokenurile stau doar în GitHub Secrets.
7. **Date personale:** nu se scriu în repo numele proprietarului, emailuri, conturi personale sau căi de pe calculatorul lui.
8. **Task-urile lungi rulează în fundal:** randările și workflow-urile de minute întregi se pornesc în Actions, iar Claude răspunde imediat. Proprietarul nu trebuie ținut blocat în chat.
9. **YouTube:** nimic nu se publică fără OK-ul proprietarului.
   - Bifat „altered or synthetic content” / „AI use = Yes”.
   - Fără sfaturi de investiție.
   - Pentru linkuri de afiliere către burse e nevoie întâi de verificare juridică.
10. **Ștergeri:** doar cu confirmarea explicită a proprietarului.
11. **Fiecare episod are repo-ul lui:** `siphonfiles/siphon-epNNN`, privat.

## 3. Unde e totul

Toate repo-urile sunt în organizația GitHub **`siphonfiles`**, private, pe planul Free. Aplicația GitHub „Claude” e instalată pe organizație. Repo-ul personal vechi a fost abandonat.

| Ce | Unde |
|---|---|
| Uneltele comune: motorul grafic, vocea și referințele lui Thomas, sunetul, scripturile, brandul, research-ul | `siphonfiles/siphon-core` |
| Episodul 001 complet | `siphonfiles/siphon-ep001` |
| Ep. 001: randarea finală (4K + 720p) | `siphon-ep001`, Release `ep001-render-10` |
| Ep. 001: pachetul editabil DaVinci | `siphon-ep001`, Release `ep001-resolve-1` |
| Ep. 001: arhiva DaVinci (media 1,66 GB, `.drp`, video-ul final v7 în 3 părți, `SHA256.txt`) | `siphon-ep001`, Release draft `ep001-archive` |
| Ep. 001: sunetul final, rapoartele ASR, cadrele Real-ESRGAN | `siphon-ep001`, branch-ul `renders` |
| Ep. 001: vocile pe replici | `siphon-ep001`, branch-ul `voice-tests` |
| Ep. 001 pe YouTube | video `kOfkyFjkzPY`, programat 29 nov 2026, 17:00 (ora României), cu 20 de piste de dublaj publicate odată cu video-ul |
| Episodul 002 (Bitget): script draft v1 | `siphonfiles/siphon-ep002`, `episodes/002-the-guard-was-the-door.md` + `.ro.md` |

**Episod nou:**
1. Se creează repo-ul `siphon-epNNN`, pornind din `siphon-core`.
2. Se copiază din `siphon-ep001` workflow-urile de randare (`render-episode.yml`, `preview-ep001.yml`, `remux-audio.yml`, `resolve-package.yml`) și fișierul `graphics/motion/ep001.py`, folosit ca model.

### Tokenuri și secrete

Valorile nu apar niciodată în fișiere sau în loguri. Se setează **pe fiecare repo în parte**: Settings › Secrets and variables › Actions. Secretele de organizație nu merg pe repo-uri private pe planul Free.

| Secret | La ce folosește |
|---|---|
| `HF_TOKEN` | Hugging Face: Space-urile ZeroGPU (Z-Image, LongCat, Qwen-Image-Edit), apelate din Actions cu `gradio_client` (`Client(space, token=...)`, **nu** `hf_token=`) |
| `KAGGLE_API_TOKEN` | Kaggle: tokenul nou. Merge cu Python 3.12 + `kaggle>=1.8` + `six`. |
| `KAGGLE_USERNAME` | Numele contului Kaggle. Kernel-urile sunt `<KAGGLE_USERNAME>/siphon-...-t4`. |
| `GITHUB_TOKEN` | Automat. Workflow-urile îl folosesc pentru Release-uri și pentru push pe `renders`. |

Proprietarul pune singur secretele. **Pentru `siphon-ep002`, secretele încă nu sunt puse.**

### Limitele sesiunii Claude (de știut din prima)

- **GitHub:**
  - nu poate crea, edita sau șterge Release-uri (403), dar un workflow din Actions poate;
  - nu poate împinge tag-uri;
  - nu poate schimba setările repo-ului prin API (se fac în browser);
  - GraphQL e blocat, deci folosește `gh api` REST;
  - la push folosește `git -c push.negotiate=true push`;
  - un clone superficial (shallow) nu poate fi împins într-un repo gol.
- **Hugging Face:** shell-ul sesiunii nu ajunge la HF (403 de la proxy). Lucrul cu HF se face din Actions (`HF_TOKEN`) sau din browser.
- **Fișiere între repo-uri:** un workflow le urcă ca artifact, iar un workflow din repo-ul țintă le descarcă cu `actions/download-artifact@v4` (`repository` + `run-id`).
- **Mac-ul proprietarului** e un M5 cu 16 GB RAM, accesat prin bridge-ul desktop.
  - `device_bash` rulează într-un VM Linux (4 nuclee, ~3 GB RAM, fără rețea), cu maximum ~170 s per comandă.
  - Nu se lansează mai multe apeluri `device_bash` în paralel.
  - Procesele lăsate în fundal mor la finalul apelului.
- **Chrome:** proprietarul are extensia Claude in Chrome, folosită pentru YouTube Studio, setările GitHub și Hugging Face. `file_upload` urcă doar fișiere de maximum ~3,8 MB din sesiunea cloud, deci video-ul mare îl alege proprietarul.
- **DaVinci Resolve** (varianta gratuită 21, pe Mac) se controlează prin computer use. Scripting-ul Python merge doar în Studio.

## 4. Thomas Archer: tot ce ține de el

### Identitate

- Britanic, ~44 de ani, calm, precis, în registru de jurnalist. Fără titluri de expert uman („Dr.”, „analyst”).
- Numele a fost verificat pe web: nu există conflicte în crypto, finanțe sau jurnalism.

### Fața

| | |
|---|---|
| Model | Z-Image-Turbo (Tongyi-MAI, Apache-2.0) |
| Setări | seed **596067**, 896x1152, 8 pași, Time Shift 3 |
| Prompt și justificare | `presenter/README.md` |
| Fișier | `presenter/portrait_v1_896x1152.png` |

Limite cunoscute:
- Barba de o zi e fixată în seed. Dacă o scoți din prompt, se schimbă omul.
- Negațiile din prompt activează conceptul negat, deci descrie ce vrei, nu ce nu vrei.

### Decorul

- **„Biroul de investigație”:** Thomas stă la birou, cu mâinile pe un dosar, centrat, în plan mediu. Are o lampă amber la stânga lui, iar în spate un perete de dovezi și un monitor estompate.
- Generat cu **Qwen-Image-Edit-2511** (Apache-2.0), din portret + decor separat. Dacă primește doar portretul, schimbă omul.
- **Referința pentru video:** `presenter/reference/thomas_ref_v1_centered_1920x1080.png`. E cadrul final 16:9 și aceeași imagine în fiecare episod, ca Thomas să arate identic.
- **Unghiul din trei sferturi:** `presenter/reference/thomas_ref_threequarter_final.png`. E oglindit, ca lampa să rămână de partea corectă, iar teancul cu clamă e adăugat din cod. **Nu a fost folosit în ep. 001**, pentru că nu are clip animat (LivePortrait e blocat pe Kaggle, vezi mai jos).

### Vocea: „Siphon Narrator v1”

| | |
|---|---|
| Model | **Zyphra ZONOS3-Mini** (Apache-2.0) |
| Referința | `presenter/voice_ref_v1.wav` (17,4 s) |
| Amprenta | `presenter/siphon_narrator_v1_embedding.pt` (vector de 192 de valori) |
| Setările din Voice Studio | în `presenter/voice.md`. Voce de bază: Rupert en British M 1, Pace maxim, Mood Calm ×4 |

- **Generarea:** pe CPU, în GitHub Actions. Workflow `tts-lines.yml` + `scripts/tts_lines.py`, folosind `Zyphra/ZONOS3-Mini-hf` (transformers). O replică = un WAV, cu seed per replică (implicit 1).
- **Viteza:** factor de timp real ~0,9, deci un episod ≈ 10 min de CPU.
- **Pachetul transformers nu are controalele de stil din Voice Studio.** Stilul vine din amprentă.
- Pe măsurătoare: F0 ~96–103 Hz, ~196 cuvinte/minut, pauze dese.
- **Capcane ZONOS3:**
  - O replică terminată în „—” sau „...” își taie ultimul cuvânt. Generează mereu **cu punct** la final, iar efectul de frază tăiată îl face montajul.
  - Un cuvânt pronunțat greșit (ex. „Siphon” → „Cifen”) se repară revocalizând cu alt seed. Ca ultimă soluție, se lipește fraza întreagă dintr-o replică bună, tăiată într-o liniște, nu la granița dintre cuvinte.
- **Normalizare:** cifrele, datele și tickerele se scriu în cuvinte (lista e în `presenter/voice.md`).

### Animația lui Thomas

**1) LongCat-Video-Avatar 1.6** (Meituan, MIT). Sincronizează buzele, mimica și capul direct din audio.

- Se apelează din Actions prin Space-ul public `victor/LongCat-Video-Avatar-1.6`, endpoint `/generate`.
  - Workflow-uri: `longcat-clip.yml` (un clip) și `longcat-batch.yml` (mai multe, pe rând, cu oprire la prima eroare).
  - Script: `scripts/longcat_clip.py`.
- **Setările folosite:** 480p, seed 42, `vocal_mode` = „Clean speech (fast)”, `acceleration` = „DBCache faster”, clipuri de **5 s**, audio la 24 kHz completat cu liniște până la 5 s.
- **Prompt:** descrie omul și decorul și cere mâinile nemișcate pe dosar. LongCat urmează vocea mai mult decât textul, așa că Thomas gesticulează moderat. **Proprietarul a decis să păstreze gesturile.**
  - Model de job: `presenter/clips/thomas_k7_1_480p.json`.
- **Costul în cotă:**
  - 480p: ~3,4 min de cotă ZeroGPU per clip de 5 s (~0,68 min per secundă).
  - 720p: ~10,7 min per clip.
  - Limita Space-ului e 240 s de GPU per cerere. 720p cu „Exact 8-step” a depășit-o și a pierdut cota fără niciun rezultat.
  - Cota PRO e de 40 min pe zi, pentru tot contul.
- **Clipuri în lanț, ca trecerile să nu se vadă:**
  - fiecare clip pornește din cadrul exact al clipului anterior (`continue_from`, extras cu ffmpeg);
  - cusăturile cad în pauze;
  - planul e în `presenter/clips/inputs/ep001_chain_plan.json`.
- **În ep. 001:** 12 clipuri HF (i1, intro→i2_2, punte→d2→d3, k7→k8) + outro-ul la 720p.

**2) LatentSync 1.5** pe Kaggle T4 (cod Apache-2.0, greutăți OpenRAIL++). Redesenează doar gura pe filmarea lui Thomas deja generată, ca să existe mai multe secvențe cu el fără cotă HF.

- 8 secvențe noi, ~68 s în total.
- Detectorul InsightFace e înlocuit cu YuNet.
- Kernel `siphon-latentsync-t4`, workflow `kaggle-latentsync.yml`, rezultatele se aduc cu `kaggle-fetch.yml`.
- Filmarea sursă e făcută din „duble” continue din clipurile în lanț, iar fiecare secvență ia o fereastră dintr-o dublă care apare departe în episod (`scripts/make_resync_inputs.py`).
- Capcane rezolvate: `transformers<5`, `huggingface_hub<1`, pachetele ffmpeg-python/imageio/librosa/soundfile, audio citit cu librosa (decord nu merge pe Python 3.13), dataset montat sub `/kaggle/input/datasets/...` (se caută recursiv).

**3) Real-ESRGAN `realesr-general-x4v3`** (BSD-3) pe Kaggle T4. Mărește clipurile 480p la 1872x1080, adică exact scara din montaj.

- **Rețeta finală:** 60% ESRGAN (fără varianta „wdn”, care dă piele de ceară) + 40% mărire Lanczos. Se aplică automat în `scripts/thomas_frames.py`.
- Kernel `siphon-esrgan-t4`, workflow `kaggle-esrgan.yml`.

**4) `scripts/mouth_hold.py`:** în pauzele de peste 0,3 s din secvențele cu două replici, ține gura cea mai închisă din pauză, urmărind capul. Altfel buzele s-ar mișca fără sunet.

**Ce NU a mers** (nu repeta fără motiv):
- **LongCat pe Kaggle T4.** Întâi a rămas fără memorie (OOM). După reparații, primul pas a dat NaN, pentru că T4 nu are bf16, iar în fp16 calculul depășește intervalul. Ar fi durat ~25 min per clip.
- **LivePortrait pe Kaggle.** Sesiunea e anulată de Kaggle la ~30–45 s, exact când pornește calculul pe față, probabil de un filtru automat pentru reanimarea fețelor. S-a oprit, **fără încercări de ocolire**.
- **Modele video locale pe Mac** (Wan, LTX). Cer cel puțin 32 GB RAM, iar Mac-ul are 16 GB.

**Montajul cu două camere:** la fiecare cusătură se alternează plan mediu ↔ prim-plan (același clip, zoom 1,3, `CLOSE` în `ep001.py`). Ce acoperă Thomas se taie din grafică (`cut_in_thomas`).

## 5. Cum s-a produs episodul 001, pas cu pas

1. **Subiectul.** Competiția se verifică pe YouTube din Chrome (`window.ytInitialData`). Drift avea cel mult ~3,5k vizualizări pe temă, deci a fost ales. Bitget și Kelp DAO au tot competiție mică.
2. **Scriptul** e în `episodes/001-the-firm-that-never-existed.md` (+ `.ro.md` pentru verificarea proprietarului). Structura urmează regulile de retenție din `research/retention-psychology.md`:
   - teaser cu fraze tăiate;
   - primele 30 s confirmă titlul și thumbnail-ul;
   - numărătoare inversă T-minus;
   - un gol de informație mic per act, închis mereu;
   - relansare la 60–90 s;
   - maximum 2–3 cifre rostite pe secțiune;
   - sursele [S1]… sunt în script și în descriere;
   - etichete în script: `[MUSIC: …]`, cartoane, momentele cu Thomas.
3. **Vocea:** `tts-lines.yml` pe CPU, apoi **verificare ASR** cu `asr-check.yml` (faster-whisper small.en/medium.en/large-v3 pe CPU, raport pe `renders:reports/`), apoi revocalizarea replicilor greșite.
4. **Sunetul**, făcut 100% din cod (`sound/`):
   - **Mixajul:** `episode_mix.py` (`PLAN_FULL`, `MORE_MUSIC=1`, `TIGHT` pentru pauzele dintre replicile legate). Produce cronologia `*.timeline.json`, pe care se sincronizează videoul.
   - **Muzica „de jaf”:** `heist_design.py` (112 BPM, re minor), cu piesele `vault_run` (124 BPM, mi minor) și `memory_piano` în `heist_tracks.py`.
     - Apare în teaser, la jaf și la final, plus 6 locuri sub narațiune, niciodată sub Thomas.
     - Nivelul e -12 dB sub narațiune și -10 dB la momentele-vedetă.
     - Intră lin în ~3 s și iese lin în ~4–5 s, niciodată brusc.
   - **Loviturile de bas (sub ~D1)** cad pe tăieturile din teaser, pe cartoanele T-minus și pe cifrele mari (`sting_design.py`, `teaser_mix.py`).
   - **Efecte sonore sintetizate:** `sfx_layer.py`.
   - **Masterul:** -14 LUFS, vârf ≤ -1,7 dBTP.
5. **Ilustrațiile:**
   - Z-Image-Turbo prin ZeroGPU: `illustrations.yml` + `scripts/gen_illustrations.py`, joburile în `illustrations/ep001/*.json`.
   - 2048x1152, 8 pași, ~13 s de cotă per imagine.
   - Sufixul de stil e fix: randare cinematică, umbre bleumarin, un singur accent amber, ceață.
   - Oamenii apar doar din spate sau în contra-lumină. Fără text și fără logo.
   - Ce iese prost: numărătorile exacte, efectele fizice complexe, „un singur obiect diferit într-un grup”.
   - Ce iese bine: un obiect sub spot, încăperile goale, siluetele.
   - Rezultat: ~33 de imagini folosite. Lista e în `illustrations/ep001/README.md`.
6. **Hărțile de adâncime:** Depth Anything V2 **Small** (Apache-2.0; Base/Large nu sunt Apache), pe CPU (`depth-maps.yml`).
7. **Grafica și animația:** motor propriu în **Python + Cairo + numpy + ffmpeg**, în `graphics/motion/` (`engine.py`, `scenes.py`, iar `ep001.py` = lista de scene a episodului). HyperFrames și Remotion au fost doar idei, nefolosite.
   - **Scenele:** cartoane, cifre mari, chat-uri, hărți, cronologii, `vault_drain`, `flow_map`, `tornado_trace`, `code_editor`, `dossier`, `countdown`, `end_card` etc.
   - **Scena `illus`:** parallax 2.5D din harta de adâncime + praf în lumină + ceață (`fog=`) + lumini (`glows=`: pulse/flicker/beam).
     - Ca să nu se deformeze imaginea: adâncimea e netezită puternic, iar diferența aproape/departe e de maximum ~6 px. Mișcarea vizibilă vine din camera rigidă.
   - **Aspectul:** fundal #141920, accent #FFB020, fonturile Lora / Noto Sans Mono / Lato, randare **4K H.264 10-bit, BT.709**.
8. **Randarea:** `render-episode.yml`.
   - 17 joburi CPU în paralel, bucăți de 20 s, apoi lipire, sunet și o previzualizare 720p, totul publicat ca Release `epNNN-render-N`.
   - Durează ~17 min și consumă ~2 h de minute Actions.
   - **Atenție:** pe repo-uri private, minutele Actions se numără (2.000 pe lună pentru organizație). Randarea 4K completă se poate face și pe Mac (`render_part.sh`).
   - `preview-ep001.yml` face previzualizări parțiale. `remux-audio.yml` pune un sunet nou peste o randare existentă, fără re-randare.
9. **DaVinci Resolve** (proiectul „Siphon Files ep001”, timeline-ul „ep001 master”):
   - `resolve-package.yml` produce straturile V1 grafică / V2 Thomas și A1 voce / A2 muzică / A3 bas / A4 efecte, plus fișierul FCPXML (`make_fcpxml.py`).
   - Media trebuie să stea în `~/Movies/DaVinci Resolve/...`, adică în locația de Media Storage.
   - **Corecții aplicate:** culoarea pe Thomas (umbre mai reci), EQ + compresor + de-esser pe voce, push-in lent pe planurile lungi și pe cartoanele statice, tăierea liniștilor moarte.
   - **Sunetul la export:** normalizarea din Deliver e **oprită** (bloca Resolve). Nivelul îl dă un Limiter pe Bus 1: Input +7 dB, Ceiling -1,7 dBTP. După export se **verifică cu ffmpeg ebur128**.
   - **Fișierul final:** `siphon_files_ep001_v7.mp4`, 11:04, -13,5 LUFS.
10. **Thumbnail:**
    - Făcut din cod (PIL + fontul Anton), pornind de la ilustrații: `thumbnails/make_ep001_options.py`.
    - Textul de pe thumbnail completează titlul, nu îl repetă.
    - Ales: „$285M. / 12 MINUTES.” pe seiful gol.
    - **Titlul:** „Inside the Drift Hack: The Trading Firm That Never Existed”.
11. **Upload-ul în YouTube Studio:**
    - Proprietarul alege fișierul video. Restul l-a completat Claude în Chrome, după `episodes/publish/001-youtube.md`:
      - titlul, descrierea cu capitole și surse;
      - tag-urile;
      - limba English (UK), categoria Education;
      - AI use = Yes;
      - subtitrările în engleză din cronologie (`make_captions.py` → `001-captions-en.srt`).
    - Thumbnail-ul personalizat a cerut verificarea canalului prin telefon (făcută). Linkurile din descriere care se pot accesa cer verificarea „advanced features”, trimisă și în review.
    - **Dublajul automat e activat**, cu review manual. La fiecare episod:
      - se verifică traducerile automate ale titlului și descrierii: capitolele trebuie să aibă cifre ASCII, sensul „cine pe cine păcălește” trebuie să fie corect, iar atribuirea să nu fie prea categorică;
      - pistele dublate se publică odată cu video-ul.
    - Ecranul de final se adaugă când există al doilea episod.
12. **Arhiva:** `.drp`-ul în git (`resolve/ep001/`), iar media într-un Release `epNNN-archive`.

## 6. Bugetul real al ep. 001

- **Bani: $0.**
- **Cotă HF ZeroGPU:**
  - Thomas: ~13 clipuri × ~3,4 min ≈ 45 min la 480p, plus outro-ul la 720p (10,7 min), repartizate pe ~2 zile de cotă;
  - ilustrațiile: ~8 min;
  - referințele de decor: ~8 min.
- **Kaggle:** ~1,5–2 h de GPU T4 (LatentSync ~22 min, ESRGAN ~45 min, plus încercările eșuate).
- **GitHub Actions:** voce, ASR, adâncime, randări (repo-ul era public pe atunci, deci gratuit).

## 7. Unde a rămas episodul 002 (Bitget)

- Repo `siphonfiles/siphon-ep002`. Scriptul draft v1 e în `episodes/002-the-guard-was-the-door.md` (+ `.ro.md`), ~1.550 de cuvinte, Thomas ~1:35, sursele S1–S19.
- **Faptele verificate:**
  - $387,5M luați din hot/warm wallets pe 24 sep 2026 (UTC);
  - nicio cheie furată (Mandiant);
  - intrare printr-un zero-day în produse de securitate ale unor terți (producător nenumit, fără CVE);
  - prima activitate pe 31 aug (SlowMist), deci intrusul a stat cel puțin 24 de zile;
  - golirea a durat 2 h 52 min (18:31–21:23 UTC);
  - semnarea a continuat 2 h 39 min după alarmă.
- **Atribuirea nu e oficială.** Firmele de analiză înclină spre Coreea de Nord, CEO-ul a revenit la „indicii preliminare”, niciun guvern n-a atribuit atacul, iar Mandiant nu atribuie.
- **Titlul recomandat:** „Inside the Bitget Hack: $388 Million Out, Not a Single Key Stolen”. Thumbnail propus: „$388M. / NO KEY.”
- **Pașii următori, în ordine:**
  1. Proprietarul verifică scriptul și alege titlul.
  2. Proprietarul pune cele 3 secrete în `siphon-ep002`.
  3. Vocea pe CPU, apoi ASR.
  4. Sunetul.
  5. Ilustrațiile și clipurile cu Thomas, doar cu acordul lui, pentru că consumă cotă.
  6. `ep002.py`, randarea, DaVinci, upload-ul.
- De decis: detaliile care vin dintr-o singură analiză (DFNS: semnătura de gas, comenzile șterse) se formulează „according to one analysis”.

## 8. De făcut, în general

- `voice_ref_v2.wav` (45–60 s), dacă vocea v1 nu ține stilul pe texte lungi.
- Space ZeroGPU propriu (durată mai mare per cerere), Cloudflare R2 pentru media, alinierea automată pe cuvinte cu Whisper.
- După publicarea ep. 001 (29 nov): test A/B pe thumbnail cu variantele B și C, plus ecranul de final.
- Primele 10 subiecte de episod, handle-ul pe X, domeniul `siphonfiles.com`, emailul de business.
