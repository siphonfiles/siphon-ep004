# Presenter voice — spec & pipeline (v1, 2026-11-20)

## CHOSEN VOICE v1 (approved by owner, 2026-11-20)
File: presenter/voice_ref_v1.wav (17.4 s, 44.1 kHz, Ronin test script)
Tool: Zyphra ZONOS3-Mini (Apache-2.0), Voice Studio on huggingface.co/spaces/Zyphra/ZONOS3-Mini
Settings (Cast tab, mode "Shape it"):
- Base voice: Rupert en British M 1; accent pin left at home (Rupert's own British accent)
- WHO: ~44 years, leans masculine; Pitch -0.5; Intonation +0.4
- TEXTURE: centre (untouched)
- ROOM: +5.9 (studio, max)
- DELIVERY: Projection 0.0; Pace STRONG (max); Read<->chatty +0.7; Hesitation 0.0; Liveliness +1.0
- MOOD: Calm x4
Measured: median F0 ~96 Hz (baritone), ~196 wpm incl. 11 pauses >=200 ms (5.4 s of pauses),
noise floor -94 dB (studio clean). Brisk Coin-Bureau-like register but calm.
Direction change vs original spec below: British instead of General American (the owner's choice).
Next: use voice_ref_v1.wav as the cloning reference for every episode.


## Target voice (one paragraph)
Male, sounds 38-45 (matches portrait_v1). General American, neutral, no regional colour.
Low-mid baritone (not booming), smooth (no rasp, no vocal fry), slightly warm.
Delivery: an investigative journalist reading the evidence — calm, precise, quietly
confident, dry understated irony. Never hype, never trailer voice, never radio announcer.

## Why (research notes)
- Audience: crypto users skew male 18-49 (Pew, Jan 2026: men 18-29 38%, men 30-49 40% have used crypto).
- Fraud docs are watched for self-protection + "I'd never fall for that" satisfaction -> voice of a calm
  expert who explains, not a dramatic storyteller.
- Male voices: low pitch is the default preference for dominance/competence; pitch does NOT reliably
  raise perceived economic trustworthiness -> don't over-deepen. Smoothness, brightness and low shimmer
  read as trustworthy.
- Pace: radio narrators ~160 wpm; fast speech boosts credibility but reduces scrutiny of arguments.
  Investigation content needs scrutiny -> target 150-165 wpm with frequent short pauses.
- Naturalness hinges on prosody: reduced F0 variation is what gets voices rated as fake.
  Monotone = AI tell. The stereotyped "deep AI documentary narrator" is now the slop signature.
- British accents were rated more credible in one voice-AI study; we stay General American for the
  core US audience. British = A/B option only.

## Model shortlist (weights commercially usable, checked 2026-11-20)
| Role | Model | License | Notes |
|---|---|---|---|
| Primary | inclusionAI Ming-3.0-tts (0.5B / tiny) | MIT | Best commercial-safe open model on Artificial Analysis arena (~1180 Elo); voice design from text, director/free-form style control, 44.1 kHz |
| Challenger | Zyphra ZONOS3-Mini | Apache-2.0 | Released Nov 2026; up to 10 min per generation, pace control, voice design, 44.1 kHz; no English metrics yet |
| Voice design | Qwen3-TTS-1.7B-VoiceDesign | Apache-2.0 | Design the voice from a description -> export reference clip |
| Fix-ups | stepfun-ai Step-Audio-EditX | Apache-2.0 | Edit emotion/pace/breaths on single lines after generation |

Excluded (non-commercial weights): Fish Audio Drama 3 / S2 Pro, Breeze TTS 2, Higgs Audio V3, Voxtral TTS (CC BY-NC), F5-TTS weights.
Never clone a real person's voice.

## Pipeline
1. Design: generate 5-10 candidates from the description below, pick one by ear.
2. Voice bible: render a 45-60 s reference clip with the chosen voice -> presenter/voice_ref_v1.wav (fixed seed).
3. Per episode: script written for the ear -> normalise text -> TTS per paragraph with the reference -> fix lines with EditX -> master.
4. The mastered audio drives LongCat / re-sync for the face.

## Voice design prompt
A man in his late thirties with a warm, low-mid baritone and a neutral General American accent.
He sounds like an investigative journalist narrating evidence: calm, precise, quietly confident,
with dry, understated irony. Clear articulation, smooth tone, no rasp or vocal fry, natural breaths,
moderate pace with short deliberate pauses. Not a movie-trailer voice, not a radio announcer.

## Test script (~45 s; tests numbers, tickers, irony, pauses)
On March twenty-third, twenty twenty-two, someone walked out of the Ronin bridge with a hundred and
seventy-three thousand six hundred ether and twenty-five and a half million dollars in USDC.
Roughly six hundred and twenty-five million dollars. No alarms. No frozen accounts.
Nobody noticed for six days.
Six days. That's how long it took for a user to try to withdraw five thousand ether... and find out
the money wasn't there.
So how do you lose six hundred million dollars without noticing? You make it easy. Five keys out of
nine. Four of them held by the same company. And one more... that was never switched off.

## Making it sound human
- Short sentences, contractions, spoken rhythm; read every script aloud once.
- Spell out numbers, dates, tickers and addresses the way a person says them (pronunciation list below).
- Generate paragraph by paragraph with the same reference and seed; never one 15-minute block.
- Keep the breaths; add 150-400 ms pauses at commas of emphasis.
- Light room tone, gentle compression, master to -14 LUFS for YouTube.
- Blind test before launch: 3 model outputs + 1 human clip -> 5 listeners guess which is human.

## Pronunciation list (start)
USDC = U-S-D-C · ETH = ether / "eth" · DeFi = dee-fye · Terra/LUNA = TEH-ruh / LOO-nuh ·
FTX = F-T-X · 0x... = "zero-ex" + first 4 chars · Solana = so-LAH-nuh

## Compliance
Synthetic voice + synthetic face -> tick YouTube's "altered or synthetic content" disclosure every
upload. Realism is the quality bar, not a way to pass as human.
