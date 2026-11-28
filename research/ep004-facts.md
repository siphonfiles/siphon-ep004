# Ep. 004 — Ledger / CryptoBilis: fapte, cronologie, ce nu se știe

Stadiu: **documentare verificată, 25 nov 2026, 19:30**. Marcaj: **[P]** = citit de noi direct la sursa primară; **[s]** = deocamdată doar din presă, de confirmat pe sursa primară înainte de script. Nicio cifră cu [s] nu intră în script fără confirmare.

## Surse

| # | Sursă | Tip | Stadiu |
|---|---|---|---|
| S1 | Singapore Police Force, „Police Advisory On Tampered Cryptocurrency Hardware Wallets”, 28 oct 2026 — police.gov.sg/media-hub/news/2026/10/20261028_police_advisory_on_tampered_cryptocurrency_hardware_wallets | oficial | **[P]** citit |
| S2 | Ledger (@Ledger / @Ledger_Support) pe X: 9 oct (cerere de suspendare CryptoBilis), 10 oct („one of the impacted users' devices contained an unauthorized hardware implant”), 11 oct (update 72 h), 13 oct (update Donjon, text integral) | firma | **[P]** 13 oct + 11/12 oct citite în X |
| S3 | (inclus în S2) Ledger Donjon, update 13 oct: implantul stă în carcasă, citește ecranul, decodează cele 24 de cuvinte la configurare, le trimite prin LTE cu un eSIM provizionat; nu modifică Secure Element, OS, tranzacții sau semnături; „We have not confirmed the total number of affected users or the total value lost” | firma | [s] (citat identic în Forklog/Decrypt/Cointelegraph) |
| S4 | Bitquery, investigația on-chain (9–10 oct: $93,2M / 315 portofele / 6 lanțuri; 16 oct: ~$102M / 335 portofele); pe lanțuri: TRON $70,5M, BTC 203,8 BTC ≈ $16,8M, ETH $3,7M | analiză on-chain | **[P]** bitquery.io/investigations/ledger-cryptobilis-hack (cifre verificate 16 oct, modificat 18 nov) |
| S5 | Mark Karpelès / Tibane Labs: postarea din 16 sep („Spy implant in @Ledger Nano X…”), teardown-ul din 9 oct (Nano X din Malaezia, sigilat, modul LTE + antenă + eSIM + microcontroler pe magistrala SPI a ecranului), pagina de research Tibane Labs (3 generații, primul raport public aug 2025 pe Reddit; baterie mai mică ca să facă loc) | cercetător | confirmat concordant (BleepingComputer, Gizmodo, CryptoSlate, Decrypt); raportul Tibane: exemplarele lor cumpărate din Japonia (Yahoo! Auctions, Amazon Japan), nu de la CryptoBilis; nu leagă cele două |
| S6 | Arravind Prabu (fost co-fondator CryptoBilis), LinkedIn 10 oct: firma vândută în martie 2026 unei noi echipe; el și Vimalatheethan au predat operațiunile; anunțul public al schimbării era programat prin contract pentru mijlocul lui octombrie | declarație | confirmat concordant (Bitcoin.com News, Odaily, Phemex: LinkedIn 10 oct) |
| S7 | Joe Grand (Grand Idea Studio): slide-uri „Ledger hardware implant” (baterie redusă, rezistor fix în locul termistorului); a anunțat Ledger pe 4 mar 2026 despre un Nano X cumpărat de pe Lazada Thailand în aug 2025 | cercetător | **[P]** slide-urile (Tropicon 2026, hardwear.io USA 2026); data alertei din 4 mar nu e folosită în script |
| S8 | Victima cu 80 BTC (a mutat monedele pe un Ledger cumpărat de la CryptoBilis, fraza scrisă de mână ținută în seif) | victimă | adresa: **[P]** Bitquery (80 BTC primiți pe 29 sep, goliți în blocul de la 05:54); valoarea ~$5,2M: Crypto Briefing; detaliul cu seiful NU intră în script |
| S9 | Tether: ~$10M USDT înghețați pe adresele atacatorului | firma | **[P]** prin Bitquery (blocare de la ~12:09 UTC, ~$10,0M rămași) |
| S10 | Arkham: drainerul încă mută fonduri ($13,84M în 48 h, ~$95,35M urmărit) | on-chain | [s] |
| S11 | Optimizely / Report URI (Scott Helme): pe 16 nov 2026, script malițios pe site-ul Ledger și alte 177 de organizații (schimba adrese crypto); Ledger: reparat | cercetător + firma | [s] |
| S12 | Ledger CEO Pascal Gauthier: revizuirea controalelor pe vânzarea directă și la revânzători | firma | [s] |

## Cronologie (de confirmat orele exacte pe [P])

| Data (UTC) | Ce | Sursă |
|---|---|---|
| aug 2025 | primul raport public despre un Nano X cu implant (Reddit, după rezumatul Tibane Labs) | S5 [s] |
| aug 2025 | Joe Grand cumpără un Nano X de pe Lazada Thailand (implant găsit ulterior) | S7 [s] |
| 4 mar 2026 | Joe Grand anunță Ledger | S7 [s] |
| mar 2026 | CryptoBilis e preluat de o echipă nouă, nenumită; fondatorii predau operațiunile | S6 [s] |
| 10 sep 2026 | primul dintre cazurile raportate în Singapore | S1 **[P]** |
| 16 sep 2026 | Karpelès publică poze cu implantul din Nano X („quite an evolution”) | S5 [s] |
| 9 oct, ~04:59 | încep golirile coordonate; ~$80,6M în 51 de minute (de confirmat) | S4/S10 [s] |
| 9 oct | Karpelès publică teardown-ul Nano X din Malaezia; Ledger cere CryptoBilis să oprească vânzările și livrările; sfătuiește cumpărătorii din ultimele 90 de zile să nu-și configureze dispozitivul | S2/S5 [s] |
| 10 oct | Ledger confirmă implantul într-un dispozitiv al unui utilizator afectat; Prabu: firma fusese vândută în martie | S2/S6 [s] |
| 11 oct | update-ul Ledger de 72 h: toate cazurile confirmate = CryptoBilis; canalele proprii neafectate | S2 [s] |
| 13 oct | update-ul Donjon (mecanismul LTE/eSIM); Ledger suspendă vânzările prin revânzători în SE Asia + Hong Kong | S2/S3 [s] |
| 16 oct | Bitquery: ~$102M / 335 portofele | S4 [s] |
| 28 oct | avizul poliției din Singapore: ≥2 cazuri din 10 sep, ~S$3,5M, magazine din Singapore | S1 **[P]** |
| 16 nov | site-ul Ledger servește script malițios prin Optimizely (alt incident, posibil epilog) | S11 [s] |

## Mecanismul (pentru grafică)
1. Dispozitiv Ledger autentic → deschis → bateria înlocuită cu una mai mică → placă nouă în locul spumei din spatele ecranului (microcontroler + modul LTE + eSIM + antenă) → resigilat (S5, S7).
2. La configurare, dispozitivul arată cele 24 de cuvinte pe ecran. Implantul citește datele care merg spre ecran, recunoaște ecranele cu cuvinte, le decodează (S3).
3. Le trimite prin rețeaua mobilă. Nu trece prin calculatorul sau telefonul victimei → antivirusul nu vede nimic (S3).
4. Secure Element-ul e cel original → „Genuine Check” trece (S3/S5; formularea exactă de confirmat).
5. Atacatorii nu golesc imediat: așteaptă ca victimele să încarce bani, apoi golesc sute de portofele aproape simultan (S4).

## Ce NU se știe (se spune explicit în video)
- cine a montat implanturile și unde, în lanțul de livrare;
- cine a cumpărat CryptoBilis în martie 2026 (fondatorii nu numesc cumpărătorul);
- numărul total de dispozitive și suma totală (Ledger nu le-a confirmat; estimările terților: $72M–$103M);
- legătura dintre implanturile găsite de cercetători în alte canale (Japonia, Thailanda, Germania) și golirile din 9 oct;
- de ce golirea a început exact pe 9 oct, ziua teardown-ului (coincidență sau reacție) — **doar ca întrebare, fără speculații**;
- recuperări (în afară de ~$10M înghețați de Tether), despăgubiri.

## Linia editorială
- CryptoBilis: fără acuzații; doar „devices sold through CryptoBilis” (formularea Ledger). Fondatorii neagă orice implicare; se spune.
- Afirmația lui CZ că „hackerii au cumpărat CryptoBilis” = doar dacă e citată ca afirmație a lui, nu ca fapt (mai bine scoasă).
- Karpelès: prezentat ca cercetător care a desfăcut dispozitivele; mențiunea Mt. Gox doar factual, fără ironie.
- Victimele: niciun nume privat; „one buyer”, cu ce a spus public.
- Victima care conducea o fraudă cu „task-uri” (60 BTC): doar dacă se confirmă din sursă primară; altfel nu intră.

| S13 | Ledger Support, „Update on the Hardware Implant Incident Investigation” (19 nov) + „Ledger's Response…” (15 oct) | firma | **[P]** |
| S14 | Bitquery, „The CryptoBilis thief came back” (18–19 nov) | on-chain | **[P]** |
| S15 | Ledger Donjon LSB-013 (9 iul 2020) | firma | **[P]** |
| S19 | MediaMarkt Saturn a oprit vânzările Ledger (13 oct), anunțat de Ledger pe X | firma | confirmat concordant (crypto.news, CryptoTicker, The Block) |


**URL-uri verificate (28 nov 2026):** S13 = https://support.ledger.com/article/Update-on-the-Hardware-Implant-Incident-Investigation · S14 = https://www.bitquery.io/investigations/ledger-hack-dubai-berlin · S15 = https://donjon.ledger.com/lsb/013/ · S7 = https://grandideastudio.com/portfolio/security/ledger-hardware-implant/. Fără adresă exactă încă: S2, S5, S6, S19 (postări X / LinkedIn). Nuanță S13: Berlin = confirmat; Dubai = două rapoarte în investigare la 19 nov → cartonul f7 și descrierea reformulate.
