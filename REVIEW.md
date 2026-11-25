# Review complet înainte de implementare — 20 nov 2026

Scop: tot ce s-a decis până acum, verificat cap-coadă, cu riscurile și golurile înainte de a construi pipeline-ul.

## A. Ce e solid (validat cu teste sau surse)
| Element | Stare |
|---|---|
| Nișă, poziționare, reguli YouTube | definite în `README.md` |
| Brand (marcă, culori, avatar, banner, watermark) | gata, în `brand/` |
| Fața lui Thomas Archer | aleasă, rețetă reproductibilă (seed 596067) |
| Vocea (ZONOS3-Mini, Apache-2.0) | aprobată; **generată în CI pe CPU, testat: ~0,9× timp real, gratuit** |
| Grafica de date (HyperFrames, Apache-2.0) | **demo randat în CI, testat: ~3× durata, gratuit** |
| Stil vizual „documentar ilustrat” | decis; neimplementat |
| Licențele modelelor alese | verificate (vezi corecțiile de mai jos) |

## B. Neconcordanțe în documentație — reparate în acest commit
1. Fluxul A→Z (CLAUDE.md §5) încă spunea „video pe Modal”; decizia ulterioară e ZeroGPU PRO, Modal doar rezervă.
2. Jurnalul de decizii avea „Modal pentru video” fără mențiunea că a fost înlocuit.
3. `README.md` (stiva) listă MOSS-Image pentru imagini; în practică folosim Z-Image-Turbo.
4. LatentSync era tratat implicit ca Apache: **codul e Apache-2.0, dar greutățile sunt OpenRAIL / OpenRAIL++** (uz comercial permis, cu restricții de utilizare). Corectat în tabelul de licențe.

## C. Riscuri mari — de tratat înainte de primul episod
1. **Politica YouTube (cel mai mare risc de business).** Categoria „AI personas related to sensitive topics” (finanțe) + pipeline automat pe șabloane („generic or repetitive”). Sancțiunea e la nivel de canal.
   Mitigare: Thomas declarat AI în fiecare video; zero sfaturi de investiție; surse pe ecran și în descriere; fiecare episod cu cercetare originală și structură vizuală variată (nu același șablon în aceeași ordine); venit construit pe afiliere/sponsorizări, nu pe AdSense.
2. **Defăimare și acuratețe.** Investigațiile numesc persoane și firme. O afirmație greșită despre cineva real e risc juridic, nu doar de reputație (exemplu concret: în demo adresa portofelului atacatorului avea inițial sufixul greșit — prinsă la verificare).
   Mitigare (politică editorială, vezi CLAUDE.md §2): doar fapte din surse primare (dosare de instanță, comunicate oficiale, rapoarte post-mortem, date on-chain); „alleged/charged” până la condamnare; fără speculații despre intenții; **verificare umană obligatorie a fiecărui script înainte de randare**; lista de surse în descriere.
3. **Afilierea la burse crypto.** În UK, FCA consideră linkurile de afiliere către produse financiare/crypto „financial promotions”; promovarea fără aprobarea unei entități autorizate poate fi infracțiune, iar ASA cere etichetarea ca reclamă. În UE se aplică regulile MiCA pentru marketing.
   Mitigare: începem cu afiliere la hardware wallets (produs fizic, nu investiție); burse doar după verificare juridică; disclosure clar „affiliate link / ad”.
4. **Fața + vocea + mișcarea, împreună — netestate.** Cel mai mare necunoscut tehnic: cum arată Thomas vorbind (LongCat), cât consumă din cotă, dacă barba/puloverul produc artefacte.

## D. Riscuri tehnice
- **Dependență de Space-uri terțe.** Space-urile publice se pot schimba, adormi sau dispărea. Soluție: Space-uri ZeroGPU proprii (PRO permite 10), cu cod fixat.
- **Limite ZeroGPU.** Durată maximă per apel → generare în bucăți; rulările eșuate consumă; cota e comună cu folosirea manuală a proprietarului din browser.
- **Stocarea media în git.** MP4-urile/WAV-urile publicate pe branch-urile `renders` și `voice-tests` rămân pentru totdeauna în istoric și umflă repo-ul (acum 11 MB; un episod complet ar avea sute de MB). Soluție: media finale în Cloudflare R2; în git doar demo-uri mici.
- **Vocea în CI fără controale de stil** (pachetul transformers nu are steering). Stabilitatea pe 10-12 minute netestată; verificarea automată prin transcriere (ASR) neimplementată.
- **Licențe de reverificat la implementare:** termenii completi ai licenței comunitare LTX-2.x (pragul de $10M + restricții de utilizare); licența fiecărei animații Lottie; seturile de ilustrații „CC0”; termenii de utilizare DefiLlama.

## E. Goluri — lucruri neacoperite deloc până acum
| Lipsă | De ce contează |
|---|---|
| **Thumbnail-uri** | factorul nr. 1 pentru click-uri; trebuie un șablon (Thomas + cifră/titlu) generat automat |
| **Muzică și efecte sonore** | documentarele au fond sonor; trebuie surse cu licență clară (YouTube Audio Library, CC0) |
| **Flux editorial** | alegere subiect → research cu surse → script → fact-check → aprobare; acum există doar producția tehnică |
| **Titluri, descrieri, capitole, SEO** | se pot genera din script, dar trebuie definite reguli |
| **Subtitrări** | ușor: SRT din script + timpii vocii |
| **Calendar de publicare** | ritmul realist (ex. 1 video/săptămână la început) dictează și bugetul de cotă |

## F. Ordinea recomandată de implementare
1. `HF_TOKEN` în GitHub Secrets → **test Thomas 10 s** cu LongCat pe ZeroGPU (cel mai mare necunoscut).
2. Space ZeroGPU propriu (LongCat + Z-Image + LTX).
3. Biblioteca de șabloane HyperFrames + aliniere pe cuvinte (Whisper).
4. Stil „documentar ilustrat”: imagini → parallax pe CPU.
5. Cloudflare R2 pentru media; scoatem media din branch-urile git.
6. Pipeline complet de episod (script → MP4) + thumbnail + subtitrări + muzică.
7. Episodul pilot, revizuit integral de proprietar înainte de publicare.

## G. Decizii care rămân la proprietarul
- Ritmul de publicare la început.
- Dacă acceptăm costuri peste cotă (și plafonul lunar).
- Afiliere: doar hardware wallets la început, sau și burse după verificare juridică.
- Primul subiect pentru episodul pilot.
