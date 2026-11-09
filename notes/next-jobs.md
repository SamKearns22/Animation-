# Where things stand (project, 9 Nov; no film in progress)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 85 (cost watch), 87 (notes restated before fixing).
- **Done (9 Nov):** Job D built: every film's voices now get a gentle polish (warmth, the 2-5 kHz edge and treble eased
  by how bright the take is, a de-esser on s-sounds), and long loud stretches (Ad-Vanced Notice's explosion, 4 dB over)
  are evened in the master. Before/after clip of Ad-Vanced Notice line 9 sent to Sam (17 s, 3.5 MB, not on GitHub).
- **Sam, 9 Nov, on the clip: "It's better, definitely."** Kept as built. Job D closed.
- **Next:** nothing queued.
- **Needs Sam:** nothing.
- **Read:** this file's Job D section only.
- **Open rule requests:** none (S10 was already the riding rule, so the voices rule is S11, written 9 Nov).
- **For Claude:** `mossad_audio.polish` (in `line()`, before `restore_tail`) and `even_out` (in `master` and
  `limit_check`), both under `MA.POLISH` (True). Strength knobs at the top of the softer-voices block: WARMTH_DB,
  EDGE_TARGET, EDGE_CUT, SHELF_DB, DEESS_MAX_DB. `python3 source/mossad_audio.py soft NAME...` prints each take's edge and
  hiss before and after. Cost watch WEEK_USD still to calibrate.

## Job D, softer voices (Sam, 9 Nov: "the audio of my dialogue was too brash and abrasive to listen to", Ad-Vanced Notice)
- Measured 9 Nov: whole-film loudness -16.9 LUFS (same as Islamocommunism -17.4, MidTerminal -17.3); the 2-5 kHz "harsh" band
  and the 6 kHz+ s-sounds are no stronger than in those films; Sam's raw takes are clean (peaks -2.5 to -11 dB, no clipping).
  So nothing is broken; what's missing is any softening at all. `mossad_audio.line` only de-hums, de-hisses and sets every
  line to the same loudness (-20 LUFS): quiet takes (lines 2, 5, 10, 11 at -26 to -28 LUFS) are lifted 6-8 dB with their
  mouth and room noise, shouted lines stay as loud as calm ones, and nothing tames the 2-5 kHz edge or the s-sounds that a
  phone speaker exaggerates. The film also has one stretch (14-17 s) about 4 dB louder than the rest.
- Plan: a gentle voice polish in `mossad_audio` used by every film: a soft treble shelf and a de-esser (s-sounds), a light
  warmth lift, the loud stretches evened; then a before/after clip of Ad-Vanced Notice's line 9 for Sam to judge by ear on
  his phone. Nothing about the voices' timing or pitch changes. Rule proposal comes with it.
- Estimate: about 1% of a week, own chat (rule 86), Opus high. **Sam: Y (9 Nov).** Type: "Build the softer voices tool (Job D in notes/next-jobs.md)".
- **Built 9 Nov (Opus).** Measured on Ad-Vanced Notice: each take's 2-5 kHz edge down 2-4.5 dB (most on the brightest,
  lines 1, 3, 8), the 6 kHz+ hiss down about 8 dB (shelf plus de-esser; the de-esser acts on about 1 frame in 10, the
  s-sounds only, at most 5 dB), warmth +1.5 dB round 220 Hz; every line still -20 LUFS. The 11-17 s explosion stretch now
  sits about 1.5 dB over the rest (was 4); the whole film comes out about 1 dB quieter (-17.7 LUFS, limiting still
  under 3 dB). Word timing moves 0.05 s at most (under a frame at 12 fps); `ad_vanced_notice.py check`: audit clean.
  Ad-Vanced Notice is posted, so it is not re-made; the polish applies from the next film (and any re-render).
- **Rule S11 (written 9 Nov; was proposed as S10, goes in the rulebook's "Notes, review and sound"):** "Every film's voices get the
  softer polish (a little warmth; the 2-5 kHz edge and the treble eased, more on a bright take; the s-sounds tamed),
  and long loud stretches are evened in the master; it is turned off only if Sam asks (Sam, 9 Nov, Ad-Vanced Notice:
  'too brash and abrasive'). | automatic (`mossad_audio.POLISH`, on by default; `mossad_audio.py soft` shows each take
  before and after)"

## Efficiency proposals, 9 Nov (Sam: Y to all; written in CLAUDE.md, P13-P16)
- E1 Start every chat with the Animation- repository selected (the session's own folder). On 9 Nov a chat started in an empty
  folder: the cost watch and the tool install never ran until the repository was added by hand.
- E2 Status questions, quick answers and filing jobs run on Sonnet, not Opus (about half the price per step).
- E3 Finished films' notes move to notes/archive/ on the day Sam says posted (Ad-Vanced Notice's was 11,000 words, nearly
  three times the 4,000 limit, and was read by every chat that touched the project).
- E4 Batch quick decisions: Sam's yes/no answers on several jobs are taken in one message at the start of a chat, so no chat
  is spent waiting for one answer.

## Job C done 9 Nov (chat 1: rulebook and CLAUDE.md; chat 2: the guides)

## Efficiency rules: written 9 Nov (rules 44, 86, 87, 88; Sam: Y)
- **Job C, tidy the rules and guides** without losing film quality: merge rules that say the same thing, drop dead ones, a contents
  list at the top of each guide, handovers name sections to read. Own chat, Opus high effort; estimate first (about 1-2% of a week),
  build on Sam's yes (rule 86). Type: "Tidy the rules and guides (Job C in notes/next-jobs.md)".
- **Job C estimate (9 Nov, waiting for Sam's yes, rule 86):** about 2% of a week, in two chats of about 1% each so neither
  goes amber. Chat 1: the rulebook (90 rules) and CLAUDE.md: a list of merges and drops goes to Sam first (dropping a rule
  removes something he agreed), then applied, plus a contents list. Chat 2: the guides: satire.md vs best-practice.md
  Part 2 overlap, the "Added 8 Oct" tail of quick-video.md folded in, contents lists, research/roadmap pages moved out of
  guides/. Nothing about how a film looks is changed. Sam said "92%" at the start (taken as: 92% of this week used).
- **To do:** next time Sam gives his weekly % figure, calibrate WEEK_USD in `.claude/hooks/costwatch.py` to match.

## Build plan (Sam, 9 Nov: everything proposed in the audit chat is a Y except the bill estimate and the extra-ideas question)
Done in that chat: shorter replies, branch wording, reference fallback and "every new rule replaces one" (CLAUDE.md); rule 89 critique before every send (rulebook). Estimates below are first cuts; each job's chat firms its own estimate and waits for Sam's yes (rule 86). Outside any film's 12%. Total about 8-12% of a week, including about 0.25% to start each chat.
Order: E, F, G, H, I (each its own chat; Opus high unless said; fresh chat each; Sam's iPhone only).
- **E. Measure and diagnose** (~0.7%, Opus high): tokens a new chat loads, by file; which rules ever caught anything; every body note in the last ten films grouped by joint or action (neck, shoulder, elbow, hand-on-prop, lying, seated, mouth, clipping). Output: numbers and a cut list, no building.
- **F. Film ledger** (~0.5%, Opus medium): the cost watch tags each chat with its film and sums per film; writes cost, chats, rounds, notes and repeated notes to a ledger; a 10-line audit at the end of each film (what repeated, what would have caught it, which rules never fired); estimate versus actual closed out.
- **G. Bodies** (~3-5%, Opus high, likely two chats): a pose acceptance test (every gallery pose, every view, automatic seam/gap/hover/clip checks; a film may only use passing poses; new poses are priced at planning); grip points and contacts for picking up, resting and lying; one fix goes into the gallery for every film.
- **H. Critique helper** (~2%, Opus high; Max only for the checklist design): a living checklist (people, creatures, props, sets, movement; each note of Sam's adds one line); a fresh helper with a small context reads the sheet, references and checklist cold; the "same kind everywhere" list per note; the before/after crop beside Sam's marked picture. First trial: the next new thing.
- **I. Consolidation** (~2-3%, Opus high): three layers of reading (one-page core, one job pack per job, rulebook and kit looked up only when named); each of the by-hand rules turned into a check, folded into the critique checklist, or retired (56, 76, 79 fold into 89); a library of new things that passed the critique (views, references, critique) so the next film reuses them; planning splits every film into known (almost free) and new (priced).
