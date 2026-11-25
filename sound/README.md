# Siphon Files: sonic identity

Status: **v1 drafts, 20 nov 2026**. Waiting for proprietarul to pick one.

Every sound is synthesized from scratch in `sting_design.py` (numpy/scipy, CPU, no samples, no AI models). That makes the stings 100% original and free of licensing or Content ID risk. Loudness is normalized to about -16 LUFS, with true peak at or below -1.5 dBFS.

| File | Idea | Elements |
|---|---|---|
| `stings/A_the_drain.wav` (5.0 s) | "The Drain": cold, investigative | descending A-minor glass bells (E5→C5→A4), sub hit, A2 drone, the logo's droplet with one echo |
| `stings/B_outflow.wav` (4.6 s) | "Outflow": more cinematic | noise riser, hit, synth gliding down (money draining), triple droplet |
| `stings/C_case_file.wav` (5.2 s) | "Case File": ties to the T-minus cards | 3 clock ticks, muted piano G-minor descent (D4→Bb3→G3), drone, droplet |

**v2: discreet variants (Proprietarul wanted something much more discreet).** Short and soft, mixed at about -23 LUFS so they sit under the voice:

| File | Elements |
|---|---|
| `stings/D_two_notes.wav` (3.2 s) | two soft falling notes (E4→A3) + a quiet droplet |
| `stings/E_single_note.wav` (2.8 s) | one muted piano note (A3) + a quiet droplet |
| `stings/F_drop_only.wav` (2.6 s) | just the droplet over a faint low hum |

**v3: low and discreet (Proprietarul wanted more bass, still discreet).** Notes an octave lower, a soft sub-bass swell around 55 Hz with no hit, and a deeper droplet, at about -23 LUFS:

| File | Elements |
|---|---|
| `stings/G_low_two_notes.wav` (3.4 s) | two low soft notes (E3→A2) + sub swell + deep droplet |
| `stings/H_low_single_note.wav` (3.0 s) | one low muted piano note (A2) + sub swell + deep droplet |
| `stings/I_low_drop.wav` (2.8 s) | deep swell + low droplet with one echo |

**v4: low, discreet, suspense (Proprietarul wanted it more suspenseful).** These use unresolved intervals and pulses, at about -22 LUFS:

| File | Elements |
|---|---|
| `stings/J_heartbeat.wav` (3.6 s) | two soft heartbeats + a low semitone rub (A2+Bb2) that never resolves + deep droplet |
| `stings/K_tritone.wav` (3.6 s) | trembling low drone + low A2 then Eb3 (tritone), left hanging + deep droplet |
| `stings/L_inhale.wav` (3.0 s) | reversed swell "breathed in" (the siphon), hard stop on a thump, droplet in the silence |

**v5: bass only (Proprietarul wanted nothing but bass).** Everything is low-passed at 220 Hz, at about -22 LUFS:

| File | Elements |
|---|---|
| `stings/M_bass_heartbeat.wav` (2.4 s) | two deep heartbeat thumps |
| `stings/N_bass_swell.wav` (3.4 s) | slow sub swell, A1 + Bb1 beating against each other |
| `stings/O_bass_inhale.wav` (2.8 s) | sub pressure rising slowly, stopping on one deep thump |

**v6: cinematic sub accents (Proprietarul pointed at the DOAC cold-open style, 20 nov 2026).**
We analysed a 1:41 screen recording of a DOAC cold open. This was analysis only: nothing from it is copied or stored in the repo. It has about 15 low accents in 100 s, roughly one every 6–8 s, placed on the cuts between clips. Most are a sub "boom" around 31–34 Hz that comes in fast (+20 dB in about 0.15 s), holds about 1.2–1.5 s, then fades. The opening accent is a pitch drop from about 86 Hz to 30 Hz over about 1.2 s. Ours are synthesized and tuned to C#1 (34.6 Hz), with a faint 2nd and 3rd harmonic so phones still hint at them.

| File | Elements |
|---|---|
| `stings/P_sub_drop.wav` (2.6 s) | opening sub drop, 86 → 31 Hz |
| `stings/Q_sub_boom.wav` (2.2 s) | the boom used on cuts (C#1) |
| `stings/demo_cold_open_rhythm.wav` (30 s) | the rhythm of a cold open: one drop + five booms on imagined cuts |

**Underscore v1 (Proprietarul pointed out that the reference also has music and wants the same style, 20 nov 2026).**
The reference was analysed by looking at its sustained spectrum, not copied. Under the speech sits a dark ambient pad with almost no rhythm. Its tonal centre is D minor with A held on top; mid-way it moves to C/Bb, then comes back. Sub booms land on the cuts.

`underscore_design.py` makes:
- `stings/underscore_cold_open_v1.wav`, 62 s. The progression is Dm → Bb → Csus2 → Dm, with 3-second crossfades. On top: a sparse, lonely piano (one note every 4–5 s), faint high "air", and a felt heartbeat pulse in the last section that builds towards the title card. Under it: a sub drop at the start and booms on the cuts at D1, kept dry.
- `stings/demo_underscore_with_thomas.wav`, 24 s. The same bed sits about 17 dB under Thomas's reference voice, the way it would in an episode.

**Teaser rule (Proprietarul, 20 nov 2026).** In the teaser, a bass hit (sub boom, D1) lands exactly where each cut-off sentence of Thomas is cut. The music bed runs underneath the whole teaser. After the last fragment comes a hard cut to black, about 0.5 s of silence, then the sub drop and the title. `teaser_mix.py` builds it from the voice lines produced by the `tts-lines` workflow. Demo: `stings/demo_teaser_ep001.wav`, the real ep. 001 teaser in Thomas's voice.

**Heist underscore v1 (Proprietarul: the ambient bed sounded like a funeral; he wants a bank-robbery-film feel, 20 nov 2026).**
`heist_design.py` produces `stings/underscore_heist_v1.wav` (43 s). It runs at 112 BPM in D minor over the loop Dm | Bb | Gm | A. Ingredients:
- a driving 8th-note bass ostinato
- a 16th-note muted synth arpeggio
- ticking 16th hi-hats (the "clock")
- finger-snap backbeat and a soft kick
- an intro that builds in layers: hats, then bass, then drums, then arpeggio

Approved by proprietarul. The music never stops abruptly: it fades out over about 5 s at the end of the piece and after the last teaser line. `teaser_mix.py` now uses this bed by default (`[heist|ambient]`). Demo: `stings/demo_teaser_ep001_heist.wav`.

**Episode music plan (approved by proprietarul, 20 nov 2026; revised the same evening: music only in the teaser and at key moments, i.e. the Act 5 heist and the last ~20 s; narration runs dry, with bass hits on cards and reveals).** `episode_mix.py` takes the tempo-locked stems from `heist_design.build_stems()` and switches layers per section, following the `[MUSIC: ...]` tags in the script:
- `full`: teaser, Act 5, close
- `drums`: Acts 3–4
- `pulse` (clock + bass): narration
- `clock`: Thomas on camera
- `out`: before key lines, Acts 6–7
- `fade`: 5 s

Layers ramp in and out over 0.35 s. On a T-minus card the music stops for about 1 s, the card lands on a bass hit, then the music comes back. Demo: `stings/demo_ep001_open_music_plan.wav`, covering ep. 001 from the teaser to the end of Act 1, in Thomas's voice.

**Alternative heist tracks for the key moment (Proprietarul, 21 nov 2026: a different piece at ~5:40, ep. 001 Act 5).** `heist_tracks.py` makes three original candidates, 30 s each, in `stings/track_*.wav`:
- `vault_run`: 124 BPM, E minor, driving 16th bass, string-like stabs, toms.
- `spy_wire`: 118 BPM, A minor, walking bass, brushed snare, twangy tremolo lead.
- `clockwork`: 96 BPM half-time, D minor, big slow drums, rising string ostinato, ticking.

`episode_mix.py` takes a `("track", name)` step in the plan. Act 5 uses `ACT5_TRACK=<name>`, and the close switches back to the opening heist piece.

The script's `__main__` renders only the latest round. The other variant functions are still in the file.

Planned usage per episode (about 9–10 sound moments per 10 minutes):
- **Full sting:** after the teaser, on the title card.
- **Short version (about 1.5 s):** at 1–2 big reveals.
- **Resolving version:** on the end card.
- **Clock tick:** on each T-minus card.
- **Underscore:** a different low bed per act. It drops out completely before the key lines.
