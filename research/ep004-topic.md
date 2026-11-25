# Ep. 004 — research de subiect (25 nov 2026)

Metodă: trackerele de hack-uri (DefiLlama, PeckShield, CertiK) și presa de specialitate pentru cazurile din iun–nov 2026, plus candidații rămași din `topic-research-2026-11.md` (siphon-ep003). Concurența pe YouTube verificată din Chrome pe 25 nov 2026, cu `ytInitialData` (titlu | canal | vizualizări | vechime | durată). Cifrele de vizualizări sunt instantanee la data verificării.

Excluse: Drift, Bitget, Coldcard (făcute); Binance $6,3B, Bybit, FTX, Malone Lam, pig butchering (saturate).

## 1. Candidații (10)

| # | Caz | Ce s-a întâmplat (presă, de verificat pe surse primare) | Concurența pe YouTube (25 nov) |
|---|---|---|---|
| 1 | **Ledger — implantul CryptoBilis** (sep–oct 2026) | dispozitive Ledger autentice, deschise, cu un cip ascuns care citea cele 24 de cuvinte de pe ecran la configurare și le trimitea prin LTE (eSIM); vândute prin revânzătorul CryptoBilis (SE Asia); Ledger: Secure Element neatins, totalul pierderilor neconfirmat (~$86–102M în cifrele terților); poliția din Singapore: S$3,5M, 2 cazuri; vânzări suspendate în 7 țări pe 13 oct | **cerere mare:** Mark Karpelès 693k (teardown, nu investigație), Cyber Scrilla 404k (8 min, știre), The CryptoDad 55k ×2, Digital Asset News 48k (live), Boxmining 26k. **Documentare:** Arxxis Docs 8k, Crypto Without Charts 709, Self Custardy 137, Onchain Autopsy 30 → nimeni n-a făcut investigația completă |
| 2 | **Liquid Network** (6 sep 2026, ~4.000 BTC, ~$320M) | „white hats” au scos 4.000 BTC prin un bug în Elements, au negociat cu Blockstream prin mesaje OP_RETURN pe blockchain, au returnat 3.400 BTC și au păstrat ~598 BTC (~$47M) | Meet Kevin 80k, João Trein 6,4k, restul < 1k |
| 3 | **Răpirile pentru crypto (wrench attacks, Franța 2025–2026)** | Chainalysis: >$30M în S1 2026, Franța 30 de incidente în S1 2026 | voidzilla 727k (acum 1 an), SEIZED 420 (2 săpt., 38 min), restul < 1k în 2026 |
| 4 | **HyperVerse** ($1,7–1,9B) | „CEO”-ul prezentat investitorilor era un actor angajat; Sam Lee acuzat | Bloomberg Originals 284k (Dubai, general), Nobody Special 15k (acum 2 ani); 2026: < 100 |
| 5 | **Keplr / Web3Auth** (6–9 nov 2026) | portofelele create cu login Google/Apple: chei private expuse printr-un defect la Web3Auth; >44.000 de portofele, ~$6M; 86% golite după avertisment | Learn Crypto 3,6k, restul < 100 |
| 6 | **Mercado Bitcoin** (2 nov 2026, ~$40M) | cea mai mare bursă din Brazilia suspendă retragerile; cauza nepublicată | doar în portugheză (82k, 15k); în engleză < 200 |
| 7 | **Tectonic** (Q3 2026, ~$120M, Cronos) | exploit de protocol | < 400 |
| 8 | **„Entitatea UE” de $106M** (1 nov 2026, ZachXBT) | bani scoși din conturi la mai multe burse în 21 h | < 30; victima nu e numită → material slab |
| 9 | **Kelp DAO** (apr 2026, $292M) + înghețarea Arbitrum | — | Coin Bureau 202k → acoperit |
| 10 | **Site-ul Ledger infectat prin Optimizely** (16 nov 2026) | script care schimba adresele crypto, 178 de organizații | știri; fond prea mic pentru 10 min, dar poate intra ca „epilog” la #1 |

## 2. Cei 3 finaliști

### A. Ledger — „The Sealed Box” (recomandat)
- **Cine se uită:** oricine are un portofel hardware (exact publicul care a urmărit ep. 003); cumpărătorii din magazine și de pe marketplace-uri.
- **Frica / nevoia:** „am făcut tot ce trebuia: am cumpărat un portofel rece, sigilat, de la un revânzător autorizat”. Auto-protecție directă: ce verifici la cutie, de unde cumperi.
- **Întrebarea precisă:** cum poate un dispozitiv sigilat, care trece testul oficial de autenticitate, să-ți fure fraza? Și cine a pus cipul acolo?
- **De ce acum:** investigația Ledger și a poliției din Singapore e deschisă; totalul pierderilor nu e confirmat; site-ul Ledger a fost și el lovit pe 16 nov.
- **Material:** comunicatele Ledger / Ledger Donjon (9, 10, 13 oct), avizul poliției din Singapore (28 oct), analize on-chain (5 lanțuri), teardown-ul Karpelès. Mecanism vizual excelent (cipul care „citește” ecranul și trimite cuvintele prin LTE).
- **Omul:** de găsit o victimă care a vorbit public (cu fapte). Karpelès apare doar ca cel care a găsit implantul, cu formulare atentă (fostul CEO Mt. Gox).
- **Ironia / amprenta:** testul „Genuine Check” spune „autentic”, pentru că cipul real e neatins; implantul are nevoie de rețea mobilă (eSIM), deci a lăsat urme la un operator.
- **Riscuri:** cine a montat implantul nu e stabilit → doar ce spun Ledger și poliția; revânzătorul = fără acuzații. Al doilea episod la rând despre portofele hardware (7 dec Coldcard, 14 dec Ledger): poate fi un avantaj („toamna în care portofelele reci au cedat”), dar unghiul trebuie să fie diferit (lanțul de livrare, nu criptografia).

### B. Liquid Network — „The Negotiation on the Blockchain”
- **Public:** bitcoineri, oameni de securitate; dilema morală „hoți sau eroi?”.
- **Întrebarea:** cine negociază $320M prin mesaje scrise în tranzacții, și de ce returnezi 85%?
- **Plus:** cronologie la minut (tranzacțiile sunt publice), mesajele OP_RETURN = carton vizual unic.
- **Minus:** publicul larg nu știe ce e Liquid; fără un om de care să-ți pese; post-mortem-ul complet Blockstream trebuie verificat.

### C. Răpirile pentru crypto din Franța
- **Public:** fanii true crime + deținătorii de crypto („casa mea, familia mea”).
- **Întrebarea:** de ce Franța? Cum își aleg țintele?
- **Plus:** cerere dovedită (727k acum un an), recorduri Chainalysis 2026, ofertă recentă aproape zero.
- **Minus:** violență reală, victime și anchete în curs → doar fapte din dosare și presa mare, fără detalii grafice; mai greu de ilustrat fără să pară senzaționalist.

## 3. Recomandarea
**Ep. 004 = Ledger (A).** Cererea e cea mai mare dintre toți candidații (două video-uri de 400k–700k, numai știri și teardown), iar investigația completă lipsește. Mecanismul se explică vizual, faptele de bază vin din comunicatele Ledger și ale poliției. Varianta de rezervă: Liquid Network. Răpirile rămân pentru ep. 005.
