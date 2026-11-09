# Where things stand (project, 9 Nov; no film in progress)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 44 (12% a film), 85 (cost watch).
- **Done (9 Nov):** Ad-Vanced Notice posted (notes archived); Elder Scrolls Swindon final sent; sitting kit closed (Sam); Job C approved (Sam: Y).
- **Next:** Job C, chat 1 of 2: Opus high, new chat: "Tidy the rules and guides, chat 1 (Job C in notes/next-jobs.md)". Then Job D (below): estimate first.
- **Needs Sam:** Y/N on Job D's estimate; numbers for the efficiency proposals E1-E4 (below).
- **Read:** this file only; then the rulebook and CLAUDE.md in full (Job C chat 1 needs them).
- **Open rule requests:** E1-E4 below (proposed 9 Nov, waiting for Sam's numbers); Job D's rule comes with its build.
- **For Claude:** sitting kit `source/sitting.py` (closed); cost watch `.claude/hooks/costwatch.py` (WEEK_USD still to calibrate).

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
- Estimate: about 1% of a week, own chat (rule 86), Opus high. Type: "Build the softer voices tool (Job D in notes/next-jobs.md)".

## Efficiency proposals, 9 Nov (waiting for Sam's numbers)
- E1 Start every chat with the Animation- repository selected (the session's own folder). On 9 Nov a chat started in an empty
  folder: the cost watch and the tool install never ran until the repository was added by hand.
- E2 Status questions, quick answers and filing jobs run on Sonnet, not Opus (about half the price per step).
- E3 Finished films' notes move to notes/archive/ on the day Sam says posted (Ad-Vanced Notice's was 11,000 words, nearly
  three times the 4,000 limit, and was read by every chat that touched the project).
- E4 Batch quick decisions: Sam's yes/no answers on several jobs are taken in one message at the start of a chat, so no chat
  is spent waiting for one answer.

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
