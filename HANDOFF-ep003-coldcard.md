# Siphon Files — predarea completă pentru o sesiune nouă de Claude (ep. 003: Coldcard)

> **Pentru Claude, în sesiunea nouă:** citește tot fișierul înainte de orice. Rezumă proiectul complet, cu stadiul de pe **23 nov 2026, ~19:30 (ora României)**. Sursa de adevăr rămâne `CLAUDE.md` din fiecare repo, cu reguli, jurnal de decizii și lecții, plus `HANDOFF-ep001.md` din `siphon-core`, cu detaliile tehnice ale primului episod.
>
> **Chatul ăsta e doar pentru episodul 003 (Coldcard).** Episodul 002 (Bitget) se continuă în chatul lui, separat. Nu te atinge de `siphon-ep002` decât dacă îți cere proprietarul.
>
> Vorbești cu proprietarul **în română**. Tot conținutul canalului (scripturi, titluri, descrieri, text pe ecran) e **în engleză**.

---

## 1. Proiectul pe scurt

- **Siphon Files** e un canal YouTube în engleză cu documentare-investigație despre furturi, fraude și prăbușiri în crypto („unde dispar banii”). Nu face știri, prețuri, trading sau sfaturi de investiții.
- **Canalul:** [@siphonfiles](https://www.youtube.com/@siphonfiles), Channel ID `UC_w7oZaLq8wq3absfPkBu2g`, brand account separat, creat pe 20 nov 2026.
- **Prezentatorul este Thomas Archer**, personaj AI inventat, cu față și voce sintetice. E declarat AI explicit: „I'm Thomas Archer, the AI narrator of Siphon Files.” Britanic, ~44 de ani, calm, precis, registru de jurnalist. Nu primește titluri de expert uman („Dr.”, „analyst”).
- **Ritmul (decis 23 nov 2026):** un episod pe săptămână. Se lucrează în paralel: ep. 002 se termină în chatul lui, ep. 003 începe aici.
- **Durata țintă:** ~10:30–11:30, ca să treacă sigur de pragul de mid-roll de 8 minute fără umplutură. Thomas pe ecran: cel puțin ~1:30–2:00. Pentru ep. 002 proprietarul a cerut minimum 2 minute. Restul e grafică din cod și ilustrații animate.
- **Costul:** se folosesc doar cotele gratuite (GitHub Actions, ZeroGPU din Hugging Face PRO, Kaggle, Mac-ul proprietarului). Orice cheltuială se face numai cu acordul lui explicit.

## 2. Cum lucrează proprietarul (citește atent)

- **Limba:** română, scurt și la obiect. Nu povesti pașii, spune rezultatul. Când propui ceva, dă o recomandare clară și întreabă o singură dată.
- **Task-urile lungi rulează în fundal.** Randări, workflow-uri, generări: le pornești în GitHub Actions, răspunzi imediat și verifici prin verificări programate (`send_later`). **Nu-l ține blocat în chat.** Și-a exprimat clar nemulțumirea când s-a întâmplat.
- **Nu consuma cotă sau bani pe teste.** Nimic „de probă” pe Hugging Face ZeroGPU, pe Kaggle GPU sau pe orice serviciu cu cotă sau plată. Se generează doar ce intră efectiv în episod și doar cu acordul lui. Probele de aspect și montaj se fac pe CPU (GitHub Actions), din materialul existent.
- **Vrea calitate impecabilă și creativitate.** Fiecare episod trebuie să aibă identitate vizuală proprie („fii creativ, nu identic cu ep. 1”). Nu acceptă repetiții vizuale inutile (aceeași ilustrație de mai multe ori) și nici flash-uri de text în montaj.
- **Totul se salvează în git**, imediat: imagini, variante, scripturi, rezultate. Media mare (video de episod) merge în Releases.
- **Verifică singur fiecare script înainte de randare** și primește traducerea în română (`.ro.md`).
- **Vrea transparență la cost.** Înainte de orice consum de cotă, spune-i cât costă (minute de cotă sau dolari) și cât durează.
- **Dacă o rulare pică, repar-o singur,** fără să-l întrebi, dacă nu costă cotă. Îi spui doar rezultatul. Dacă îți semnalează „a picat ceva pe git”, verifici imediat și repari.
- Nu scrie în repo date personale (numele lui, emailuri, conturi personale, căi de pe Mac-ul lui).

## 3. Reguli fixe (din `CLAUDE.md`, secțiunea 2)

1. **Licențe doar cu uz comercial** (canalul se monetizează). Lista e în `CLAUDE.md` §7. Verifică licența înainte de orice model. InsightFace e interzis (necomercial); se folosește YuNet (OpenCV, MIT).
2. **Nu clona și nu imita voci sau fețe de persoane reale.**
3. **Politica editorială:**
   - doar surse primare: comunicate oficiale, rapoarte post-mortem, dosare de instanță, firme de analiză on-chain;
   - „alleged/charged” până la condamnare;
   - fiecare afirmație are sursă ([S1]… în script, lista completă în descriere);
   - fără speculații despre intenții;
   - mesajele reconstruite poartă eticheta „ILLUSTRATIVE”;
   - fără oameni sau scene inventate.
4. **YouTube:**
   - „altered or synthetic content” / „AI use = Yes” la fiecare upload;
   - fără sfaturi de investiții;
   - afiliere către burse doar după verificare juridică;
   - upload-ul îl aprobă proprietarul.
5. **Thomas apare doar în video, niciodată ca imagine fixă** (regula 18b). Prim-planul („a doua cameră”) e același clip mărit.
6. **Thomas pe Hugging Face doar la 720p**, niciodată la 480p, nici pentru economie (regula permanentă 18d, 23 nov 2026).
7. **Fiecare episod are repo-ul lui:** `siphonfiles/siphon-epNNN`, privat.
8. **Ștergeri** (Release-uri, fișiere, branch-uri) doar cu confirmarea explicită a proprietarului.
9. **Credențiale:** nu introduci niciodată parole sau tokenuri. Proprietarul pune singur secretele în GitHub.

## 4. Unde e totul

### GitHub, organizația `siphonfiles` (toate repo-urile private, plan Free)

Aplicația GitHub „Claude” e instalată pe organizație, cu acces la toate repo-urile.

| Repo | Conținut |
|---|---|
| `siphonfiles/siphon-core` | uneltele comune: motorul grafic (`graphics/motion/engine.py`, `scenes.py`), vocea și referințele lui Thomas (`presenter/`), sunetul (`sound/`), scripturile (`scripts/`), brandul (`brand/`), research-ul (`research/`), `HANDOFF-ep001.md`, acest fișier |
| `siphonfiles/siphon-ep001` | episodul 001 (Drift), complet: script, ilustrații, clipuri Thomas, `ep001.py`, sunet, metadate YouTube, subtitrări, proiectul DaVinci, workflow-urile de randare. Release-uri: `ep001-render-10` (4K + 720p), `ep001-resolve-1` (pachet editabil DaVinci), draftul `ep001-archive` (media 1,66 GB + `.drp` + video final v7 în 3 părți + `SHA256.txt`) |
| `siphonfiles/siphon-ep002` | episodul 002 (Bitget), în lucru. Se continuă în celălalt chat |
| `siphonfiles/siphon-ep003` | **de creat pentru Coldcard** (vezi §11) |

Branch-uri folosite în fiecare repo de episod:
- `renders`: audio final, rapoarte, rezultate Kaggle, previzualizări, PNG-urile ilustrațiilor;
- `voice-tests`: vocile pe replici.

### Secrete GitHub

Se pun **pe fiecare repo în parte**: Settings › Secrets and variables › Actions. Secretele de organizație nu merg pe repo-uri private pe planul Free. Valorile nu apar niciodată în fișiere sau în loguri.

| Secret | La ce folosește |
|---|---|
| `HF_TOKEN` | Hugging Face, doar citire: Space-urile ZeroGPU (Z-Image, LongCat, Qwen-Image-Edit) apelate din Actions cu `gradio_client` (`Client(space, token=...)`, **nu** `hf_token=`), plus modelele cu acces condiționat |
| `HF_WRITE_TOKEN` | Hugging Face cu drept de scriere: crearea și urcarea de Space-uri proprii (`space-deploy.yml`) |
| `KAGGLE_API_TOKEN` | tokenul nou Kaggle (merge cu Python 3.12 + `kaggle>=1.8` + `six`) |
| `KAGGLE_USERNAME` | numele contului Kaggle; kernel-urile se numesc `<KAGGLE_USERNAME>/siphon-...-t4` |
| `GITHUB_TOKEN` | automat, pentru Release-uri și push pe `renders` |

Licențe acceptate deja pe contul HF: `stabilityai/stable-audio-open-small` (pe 23 nov 2026).

**La crearea `siphon-ep003`:** dă-i proprietarului linkul `https://github.com/siphonfiles/siphon-ep003/settings/secrets/actions` și cere-i să pună `HF_TOKEN`, `KAGGLE_API_TOKEN`, `KAGGLE_USERNAME` (și `HF_WRITE_TOKEN` dacă e nevoie). `KAGGLE_USERNAME` e numele din URL-ul profilului de Kaggle (`kaggle.com/<nume>`). Valorile nu le ai și nu le ceri în chat.

### Episoadele

| Episod | Stare |
|---|---|
| **001: „Inside the Drift Hack: The Trading Firm That Never Existed”** (Drift Protocol, 1 apr 2026, ~$285M, atribuit Coreei de Nord) | **Publicat public luni 23 nov 2026, ~19:02** (ora României), video `kOfkyFjkzPY`, https://youtu.be/kOfkyFjkzPY. 11:04, -13,5 LUFS. Thumbnail „$285M. / 12 MINUTES.” pe seiful gol. Subtitrare EN; titlu și descriere traduse automat în 20 de limbi, verificate și corectate. **Dublajul automat YouTube a fost abandonat** (prea rapid, spus de un vorbitor nativ) și oprit la nivel de canal. Ecranul de final se adaugă după al doilea episod. Fișierul final pe Mac: `~/Movies/DaVinci Resolve/siphon-ep001-resolve/siphon_files_ep001_v7.mp4` |
| **002: „Inside the $388M Bitget Hack”** (Bitget, 24 sep 2026, ~$388M, intrare prin produse de securitate ale unor terți, nicio cheie furată) | În montaj: script v3 aprobat, voce v2, sunet master, identitate vizuală proprie, montaj 1080p Release `ep002-render-5`. Mai sunt de făcut: clipuri cu Thomas (3 în noaptea de 23/24 nov, apoi altele în nopțile următoare), 8 ilustrații noi (în coadă pe Kaggle), efecte sonore Stable Audio (în generare), muzică nouă. **Continuă în chatul lui** |
| **003: Coldcard** | **Ales de proprietar pe 23 nov 2026.** Începe în chatul ăsta (§10–§11) |

## 5. Platformele și conturile

| Platformă | Ce folosim | Limite și capcane |
|---|---|---|
| **GitHub Actions** (org `siphonfiles`, Free) | aproape totul: voce TTS, ASR, mixaj, hărți de adâncime, decupaje, randări, apeluri către HF și Kaggle | pe repo-uri private, 2.000 min/lună pe organizație; o randare completă de episod ≈ 75 min de Actions. Runner-ele n-au GPU (2 vCPU, 7 GB RAM, ~14 GB disc liber; eliberează disc dacă instalezi PyTorch). Pune `pip --retries 10 --timeout 120` și fixează varianta CPU de PyTorch cu un fișier de constrângeri, altfel vin roțile CUDA și umplu discul |
| **Hugging Face PRO** | cota **ZeroGPU: 40 min/zi pe tot contul** (placă Blackwell), Space-uri publice + un Space propriu | cota se resetează la 24 h după prima folosire. Peste cotă se plătește automat din credite: $1 / 10 min. Credite PRO rămase ~$1,32, expiră pe 1 dec; reîncărcarea automată e oprită, deci cardul nu e atins. Pe 23 nov s-a depășit cota (45,6/40 min, ~$0,56): **verifică întotdeauna cota înainte de o generare**. Shell-ul sesiunii Claude NU ajunge la HF (403), se lucrează doar din Actions sau din browser. Space propriu: `siphon-seedvr2-video` (SeedVR2; proprietarul **nu** mai vrea SeedVR2) |
| **Kaggle** (GPU gratuit, ~30 h/săpt., T4 x2, sesiuni max. 12 h) | Real-ESRGAN, LatentSync (resincronizarea buzelor), Z-Image în bf16 (în coadă) | coada poate dura ore. **T4 nu are bf16 nativ**: modelele mari dau NaN (imagine neagră) în fp16, deci se rulează direct în bf16 (emulat, mai lent, aceeași calitate). **LivePortrait e blocat de Kaggle** (sesiunea e anulată la ~30 s), nu încerca ocoliri. LongCat pe T4 nu merge (OOM, apoi NaN) |
| **Modal** | rezervă | fără credite luna asta (se reîncarcă lunar, $30) |
| **Lightning AI** | — | nu mai acceptă înregistrări (verificat de proprietar pe 23 nov) |
| **WaveSpeed** | rezervă plătită pentru LongCat 720p | ~$0,08 per secundă de video; doar cu acordul proprietarului |
| **YouTube Studio** | upload, metadate, subtitrări, thumbnail | proprietarul alege fișierul video (extensia Chrome urcă max. ~3,8 MB). Thumbnail-ul personalizat e activ (canal verificat prin telefon). „Advanced features” (linkuri în descriere, Test & Compare): verificarea video a fost trimisă pe 22 nov, în review |
| **Chrome cu extensia Claude** | YouTube (research de concurență, Studio), setările GitHub, Hugging Face | concurența se citește din `window.ytInitialData` pe pagina de căutare YouTube (titlu, canal, vizualizări, vechime, durată); `fetch` din pagină e blocat |
| **Mac-ul proprietarului** (M5, 16 GB RAM), prin bridge-ul desktop | DaVinci Resolve 21 gratuit (prin computer use), randări 4K la nevoie | `device_bash` = VM Linux, ~170 s pe comandă, fără apeluri în paralel. Modelele video locale (Wan, LTX) cer ≥32 GB, deci nu merg |

**Limitele sesiunii Claude:**
- nu poate crea, edita sau șterge Release-uri și nu poate împinge tag-uri, dar un workflow din Actions poate (`delete-releases.yml`, `copy-releases.yml`);
- GraphQL e blocat, se folosește `gh api` REST, inclusiv pentru pornirea workflow-urilor (`POST .../dispatches`);
- la push se folosește `git -c push.negotiate=true push`;
- nu poate citi secretele;
- nu poate șterge sau dezactiva verificări programate (refuzat de clasificator).

## 6. Thomas Archer: față, voce, animație

**Fața de bază**
- Z-Image-Turbo (Apache-2.0), seed **596067**, 896x1152, 8 pași, Time Shift 3; promptul e în `presenter/README.md`.
- Barba de o zi e fixată în seed.
- Negațiile din prompt activează conceptul negat, deci descrie ce vrei, nu ce nu vrei.

**Decorul:** „biroul de investigație”. Thomas stă centrat, în plan mediu, cu mâinile pe dosar, lampa amber lângă el, iar în spate un perete de dovezi și un monitor, estompate. Decorul se generează cu **Qwen-Image-Edit-2511** (Apache-2.0) din portret plus decor dat separat (doar din portret, schimbă omul).

**Referințe**
- `presenter/reference/thomas_ref_v1_centered_1920x1080.png`: pulover gri, ep. 001.
- `presenter/reference/thomas_ref_ep002_1920x1080.png`: **cămașă bleumarin**, ep. 002, cu obiecte legate de caz pe birou. Ținuta se schimbă pe episod cu aceeași rețetă de față (`scripts/gen_outfit_portrait.py`, `gen_outfit_desk.py`, workflow `outfit-ref.yml`). Puloverul negru cu guler înalt și bluza ardezie **au schimbat omul**, deci au fost respinse.
- Unghiul din trei sferturi: `presenter/reference/thomas_ref_threequarter_final.png`. Nefolosit, pentru că nu are clip.
- **Nu atinge `set-refs.yml`**: pornește singur la push și consumă cotă.

**Vocea „Siphon Narrator v1”**
- Zyphra **ZONOS3-Mini** (Apache-2.0), referința `presenter/voice_ref_v1.wav`, amprenta `presenter/siphon_narrator_v1_embedding.pt`.
- Generare pe CPU în Actions: `tts-lines.yml` + `scripts/tts_lines.py`, o replică = un WAV.
- Urmează verificarea **ASR** (`asr-check.yml`, faster-whisper medium.en/large-v3) și revocalizarea cu alt seed a replicilor greșite.

Capcanele vocii:
- o replică terminată în „—” sau „...” își taie ultimul cuvânt, deci pune mereu punct;
- după replici de 2–3 cuvinte modelul inventează silabe, deci le tai la prima pauză sau le lipești de următoarea;
- „Bitget” s-a auzit „bitch get”/„Bichette” și a cerut 2–3 seed-uri;
- cifrele și tickerele se scriu în cuvinte („T R X”, „U S D T”, „Zach X B T”, „Thor Chain”), lista e în `presenter/voice.md`.

**Animația: LongCat-Video-Avatar 1.6** (Meituan, MIT), din Actions, prin Space-ul public `victor/LongCat-Video-Avatar-1.6`.
- Workflow-uri `longcat-clip.yml` / `longcat-batch.yml` (cu `dest`), script `scripts/longcat_clip.py`.
- **Doar 720p**, „DBCache faster”, seed 42, clipuri de **5 s** (1312x704).
- Audio: 0,3 s liniște + replica + liniște până la 5 s, la 24 kHz.
- **~10,7 min de cotă per clip** și ~315 s timp real, deci **~3 clipuri pe noapte** din cele 40 de minute.
- Replicile lui Thomas trebuie gândite în bucăți de **≤ 4,7 s**. Una mai lungă cere 2 clipuri în lanț (`continue_from`, cusăturile în pauze).
- Thomas gesticulează moderat. Proprietarul a acceptat gesturile.

**Montaj**
- Prim-plan = același clip mărit ×1,3, alternat plan mediu ↔ prim-plan la cusături.
- `_absorb_slivers` + garda **`check_no_flash`**: niciun rest de scenă sub 1 s după un clip, altfel textul de dedesubt „clipește”. Copiază garda în `epNNN.py` la fiecare episod.
- Unde nu există clip, cadrul trece pe grafică sau ilustrație (niciodată poză cu Thomas).

## 7. Pipeline-ul complet al unui episod (cum l-am făcut la 001 și 002)

1. **Subiectul:** research de cerere și concurență pe YouTube (Chrome + `ytInitialData`), plus verificarea surselor primare.
2. **Scriptul:** `episodes/NNN-slug.md` + `.ro.md`, construit după regulile din:
   - `research/retention-psychology.md`;
   - `research/suspense-storytelling.md`;
   - `research/title-psychology.md`.

   Regulile pe scurt:
   - prima frază = o imagine mică și concretă;
   - primele 30 s confirmă titlul și thumbnail-ul;
   - teaser cu fraze tăiate și lovitură de bas pe fiecare tăietură;
   - numărătoare inversă T-minus;
   - un om de care să-ți pese, doar din fapte;
   - între scene „dar”/„așa că”, niciodată „și apoi”;
   - nicio secțiune nu se termină pe o concluzie;
   - „noi știm, ei nu”;
   - detaliile-cheie plantate înainte de vârf;
   - maximum 2–3 cifre rostite pe secțiune;
   - finalul revine la prima imagine;
   - sursele [S1]….
3. **Titlul:** cadrul „Inside the …” merge (vidIQ: ~2,5×). Fără titluri-întrebare. ~5 cuvinte. Textul de pe thumbnail completează titlul, nu îl repetă. Numele cazului apare pe thumbnail. Cifra din titlu = cifra din primele 30 s. **Test & Compare** cu 3 variante la publicare, când e activă funcția.
4. **Vocea:** `tts-lines.yml` → `voice-tests:lines/epNNN-vN` → ASR → revocalizări.
5. **Sunetul, din cod:** `sound/` (`episode_mix.py` / `epNNN_mix.py`, `heist_design.py`, `heist_tracks.py`, `sting_design.py`, `teaser_mix.py`, `sfx_layer.py`).
   - muzica nu stă sub tot episodul, doar în teaser, la vârf și la final, plus câteva locuri sub narațiune, **niciodată sub Thomas**;
   - intră lin ~3 s și iese lin ~4–5 s, niciodată brusc;
   - lovituri de bas pe cartoane și pe cifrele mari;
   - master **-14 LUFS**, vârf ≤ -1,7 dBTP;
   - rezultatul e cronologia `*.timeline.json`, pe care se sincronizează videoul;
   - **proprietarul vrea muzică nouă la fiecare episod, nu aceleași piese ca la ep. 001.** Pentru ep. 002 i-a plăcut doar `withdrawal_rush` (bas + tobe, ~20 s; varianta `withdrawal_rush_v2` din `siphon-ep002/sound/ep002/ep002_tracks.py`).
6. **Ilustrațiile:** Z-Image-Turbo prin ZeroGPU (`illustrations.yml` + `scripts/gen_illustrations.py`, joburi `illustrations/epNNN/*.json`).
   - 2048x1152, 8 pași, ~13 s de cotă per imagine; alternativ pe Kaggle în bf16 (`kaggle-zimage.yml`, gratuit, dar cu coadă).
   - Sufix de stil fix: randare cinematică întunecată, umbre bleumarin, un accent cald, ceață, straturi de adâncime.
   - **Oamenii doar din spate sau în siluetă**, descriși pozitiv. Fără text, fără logo-uri reale, fără numărători exacte.
   - Iese prost: efectele fizice complexe, „un obiect diferit într-un grup”, râuri care se despart, bariere ridicate. Iese bine: un obiect sub spot, încăperi goale, siluete.
7. **Hărțile de adâncime:** Depth Anything V2 **Small** (Apache-2.0) pe CPU (`depth-maps.yml`), 8-bit 1024x576, puternic estompate.
8. **Grafica și animația:** motor propriu **Python + Cairo + numpy + ffmpeg** în `graphics/motion/`: `engine.py`, `scenes.py`, `scenes_epNNN.py`, iar `epNNN.py` = lista de scene legată de replici.
   - **Scena `illus`:** parallax 2.5D + praf + ceață (`fog=`) + lumini (`glows=`: pulse/flicker/beam).
   - **Identitate proprie pe episod** (`SIPHON_THEME`). La ep. 002: fundal petrol #0E1A1D cu grilă de supraveghere, accent cyan #3EE0D0, roșu de alarmă #FF4D5E, fonturi IBM Plex Sans Condensed / JetBrains Mono / IBM Plex Serif.
9. **Obiecte decupate (nou la ep. 002):** **BiRefNet** (MIT) pe CPU (`birefnet.yml` + `scripts/birefnet_cut.py`, ~40 s/imagine).
   - Obiectul din ilustrație se pune peste grafica din cod: diagrame cu obiectul real, ecuson clonat, telefon cu notificare, seif la capătul unui lanț de sisteme.
   - Arată mult mai „documentar” decât slideshow-ul de imagini AI (YouTube penalizează slideshow-urile AI).
10. **Efecte sonore (în curs la ep. 002):** **Stable Audio Open Small** (Stability Community License, gratuit sub $1M/an) pe CPU (`sfx-gen.yml` + `scripts/sfx_gen.py`): câte 3 variante per efect, iar proprietarul alege după ureche.
11. **Randarea:**
    - `render-epNNN.yml`: 18 joburi CPU în paralel, Release `epNNN-render-N` cu 1080p + previzualizare 720p, ~11 min;
    - `preview-segments.yml`: randează doar intervale, pentru verificări rapide;
    - `remux-audio.yml`: pune un sunet nou peste o randare existentă;
    - `delete-releases.yml`: curăță Release-urile vechi, cu acordul proprietarului.
12. **Verificare pe cadre** (extragi cadre cu ffmpeg și le privești) înainte să trimiți ceva proprietarului.
13. **DaVinci Resolve** pe Mac (opțional, pentru finisare): `resolve-package.yml` (straturi + FCPXML). Nivelul sunetului îl dă Limiter-ul de pe Bus 1, iar loudness-ul se verifică cu ffmpeg ebur128.
14. **Upload:** metadatele în `episodes/publish/NNN-youtube.md` (titlu, descriere cu capitole și surse, tag-uri, EN (UK), Education, AI use = Yes), plus subtitrarea `make_captions.py`.
    - Verifică traducerile automate ale titlului și descrierii: capitolele cu cifre ASCII, „cine pe cine păcălește”, atribuiri prea categorice.
    - Fără dublaj automat.
15. **Arhiva:** `.drp` în git, media în Release `epNNN-archive`.

## 8. Modelele folosite și licențele lor (detaliile în `CLAUDE.md` §7)

| Rol | Model | Licență |
|---|---|---|
| Imagini | Z-Image-Turbo | Apache-2.0 |
| Editare imagini (decor, ținută) | Qwen-Image-Edit-2511 | Apache-2.0 |
| Voce | ZONOS3-Mini | Apache-2.0 |
| Thomas animat | LongCat-Video-Avatar 1.6 | MIT |
| Resincronizarea buzelor (Kaggle) | LatentSync 1.5 | cod Apache-2.0, greutăți OpenRAIL++ |
| Mărire video | Real-ESRGAN realesr-general-x4v3 | BSD-3 |
| Adâncime | Depth Anything V2 Small | Apache-2.0 (Base/Large nu) |
| Decupaje | BiRefNet | MIT |
| Efecte sonore | Stable Audio Open Small | Stability Community (gratuit sub $1M/an) |
| ASR | faster-whisper | MIT |

**Respinse de proprietar sau nefolosite:**
- SeedVR2: nu-l mai vrea.
- Voice Isolator: vocea e deja curată.
- Kokoro: nu avem text real pentru o a doua voce.
- Video Depth Anything: ilustrațiile sunt statice.

**De luat în calcul:**
- ACE-Step 1.5 (MIT, muzică, pe Kaggle);
- TRELLIS.2 / Pixal3D / Idol (imagine → obiect 3D cu camera în jurul lui; cotă HF);
- Wan 2.2 / LTX-2 (clipuri-cheie animate; cotă HF).

**Excluse definitiv:** InsightFace, FLUX.1-dev, Qwen-Image-2.1, NanoAvatar, Fish Audio, Voxtral, F5-TTS (toate necomerciale).

## 9. Research-ul de subiecte (23 nov 2026), de ce Coldcard

Fișierul complet: `siphon-core/research/topic-research-2026-11.md`.

**Ce spun datele despre public**
- FBI IC3 2025: pierderi crypto raportate $11,4 mld (peste jumătate din cele $20,9 mld de fraude online); persoanele de peste 60 de ani au pierdut $4,4 mld.
- Psihologia „morbid curiosity” (Scrivner): oamenii urmăresc crime și fraude ca simulare sigură a pericolului; 76% dintre fanii true crime cred că îi ajută să evite situații similare.
- Concluzia: **subiectele care ating direct banii privitorului** (portofelul lui, casa lui) au cea mai mare cerere. Poveștile cu un om în centru bat hack-urile de protocol (Malone Lam: 2–5 milioane de vizualizări pe mai multe canale).

**Concurența pe YouTube (23 nov)**
- **Coldcard:** cea mai mare cerere fără documentar. Fireship 681k (o știre de 5 min), Simply Bitcoin („inside job”) 37k, restul 0,1–18k. Niciun documentar-investigație.
- **Ledger cu cip spion:** Mark Karpelès 679k, restul sub 55k.
- **Saturate, de evitat:** Binance $6,3B (Gloam 2,6M), Malone Lam, pig butchering, Chen Zhi.

**Ordinea propusă:** **003 Coldcard** → 004 cipul spion din Ledger (CryptoBilis, oct 2026, ~$86–103M) → 005 valul de răpiri pentru crypto (Franța 2025–2026) → apoi Liquid Network („white hats” care au păstrat $47M) și HyperVerse (CEO-ul era un actor angajat, $1,89 mld).

## 10. Episodul 003: Coldcard (punctul de plecare)

**Faptele principale (de reverificat pe surse primare înainte de script):**
- Începând cu **30 iulie 2026**, un atacator a golit **~1.816 BTC (~$116M)** din **5.200+ adrese** de portofele hardware Coldcard (Coinkite), în **4 valuri** (30 iul – 3 aug). Cifrele sunt de la TRM Labs și Galaxy Research; unele estimări merg la $130M.
- **Primul val: 1.083 BTC din 1.196 adrese în ~41 de minute** (30 iul, 01:10:20–01:51:26 UTC).
- **Cauza:** o eroare de build din firmware-ul **4.0.0 (martie 2021)**. La generarea cheii, dispozitivul ocolea cipul hardware de aleatoriu și folosea un substitut software previzibil. Seed-urile aveau doar ~40 de biți de entropie și puteau fi ghicite **offline**.
- **Atacatorul n-a atins niciun dispozitiv.** Fără interceptare în lanțul de livrare, fără acces fizic. Defectul a stat ascuns ~5 ani. Patch de urgență pe **31 iulie 2026**.
- **Nimeni nu e identificat public.** Circulă teorii de „inside job” (Simply Bitcoin, BTC Sessions). Ele **se menționează doar ca teorii, fără acuzații**.
- Coinkite / CEO-ul Rodolfo Novak le-a cerut utilizatorilor să-și mute fondurile și a pus o parte din vină pe un code review asistat de AI (Forbes). De verificat exact ce a spus.
- O victimă cunoscută: C$1,6 milioane (Forbes, „I did everything right”).

**De ce e un subiect bun**
- Lovește direct teama publicului țintă: „am făcut totul corect (cold storage) și tot am pierdut”.
- Cerere dovedită, fără documentar.
- Cronologie precisă la minut.
- Mister nerezolvat.
- Ironie puternică: aparatul făcut să fie „cel mai sigur” era previzibil de cinci ani.
- Detaliu de amprentă plantabil înainte de vârf: cei 40 de biți.

**Unghiuri și structură propuse (de discutat cu proprietarul)**
- **Deschidere:** o imagine mică. Un Coldcard sigilat într-un sertar, neatins din 2021. „On the night of July 30th, nobody touched it.”
- **Titlu:** „Inside the Coldcard Hack” + un al doilea rând de testat. Thumbnail de tipul „$116M. / NOBODY TOUCHED IT.” sau „5 YEARS. 41 MINUTES.”
- **Om de care să-ți pese:** proprietarul care „a făcut totul corect”, doar din declarații publice reale (Forbes etc.), fără inventări.
- **„Noi știm, ei nu”:** spectatorul află de bug înainte ca victimele să afle că au pierdut.
- **Numărătoare T-minus:** spre 01:10:20 UTC, 30 iulie.
- **Final:** revine la dispozitivul din sertar + ce poate face privitorul (mutarea fondurilor, verificarea firmware-ului), formulat **fără sfaturi de investiții**.
- **Pereche cu ep. 004 (Ledger):** „anul în care portofelele reci au cedat”.

**Riscuri editoriale**
- Teoria „inside job”: fără acuzații.
- Explicația tehnică a entropiei trebuie simplă și exactă (de verificat cu raportul Coinkite și cu analizele TRM/Galaxy).
- Atenție la mărcile reale: niciun logo Coldcard sau Coinkite în ilustrații; numele apar doar în text, ca fapt.

**Surse găsite până acum (de citit și verificat)**
- TRM Labs, Galaxy Research (Alex Thorn).
- Forbes: https://www.forbes.com/sites/boazsobrado/2026/08/04/i-did-everything-right-ai-warning-after-116-million-bitcoin-hack/
- crypto.news: https://crypto.news/coldcard-hack-bitcoin-self-custody-entropy/
- Defimon: https://defimon.xyz/blog/coldcard-hack-july-2026
- Blockspot: https://blockspot.io/coldcard-hack-explained/
- Breitbart/Bloomberg (3 aug).
- Comunicatele Coinkite (de găsit).

## 11. Primii pași în chatul nou

1. Citește `CLAUDE.md` din `siphon-core`, `HANDOFF-ep001.md` și acest fișier.
2. **Creează repo-ul `siphonfiles/siphon-ep003`** pornind din `siphon-core`. Copiază din `siphon-ep002` ce e reutilizabil:
   - `graphics/motion/ep002.py` și `scenes_ep002.py` ca model;
   - workflow-urile `render-ep002.yml`, `preview-segments.yml`, `longcat-batch.yml`, `birefnet.yml`, `sfx-gen.yml`, `kaggle-zimage.yml`, `kaggle-fetch.yml`, `delete-releases.yml`, `tts-lines.yml`, `asr-check.yml`, `depth-maps.yml`, `illustrations.yml`;
   - `scripts/` (`longcat_clip.py`, `birefnet_cut.py`, `sfx_gen.py`, `gen_illustrations.py`, `tts_lines.py`, `make_captions.py`);
   - garda `check_no_flash` + `_absorb_slivers`.

   Notează în `CLAUDE.md` din repo-ul nou.
3. Cere proprietarului să pună secretele (linkul din §4).
4. **Research pe surse primare** pentru Coldcard, apoi **scriptul draft v1** (`episodes/003-….md` + `.ro.md`, ~1.550 de cuvinte, Thomas ~1:30–2:00 în replici de ≤ 4,7 s), cu sursele [S1]…. Proprietarul îl verifică înainte de orice generare.
5. Propune o **identitate vizuală nouă** pentru ep. 003 (alt fundal, alt accent, alte fonturi OFL) și o **ținută nouă pentru Thomas**, cu aceeași față.
6. Abia după aprobarea scriptului: voce → ASR → sunet → ilustrații → clipuri Thomas (doar 720p, ~3 pe noapte, cu acordul lui) → montaj → verificare pe cadre → randare.

**Atenție la cota Hugging Face:** în nopțile de după 23 nov, cota merge întâi pe clipurile cu Thomas pentru ep. 002 (3 pe noapte). Pentru ep. 003 cere acordul proprietarului și verifică pagina cotei înainte de orice generare.
