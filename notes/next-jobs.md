# Where things stand (project, 10 Nov; no film in progress)

- **Rules that bite next:** 85 (cost watch: chat 3 went amber after step 3, so it handed over), 41 (the hand check now
  also tests a hand against what it holds, on the picture), 86 (Job G stays inside its 3.5-4%).
- **Done (10 Nov, Job G chat 3, steps 2-3, Opus high, about 1.5%):** phone at the ear redone (hand at the cheek, the
  phone flat along the side of the head, elbow forward; passes all 6 views; the left hand by default); a hand at the
  far cheek is now hidden behind the head (it was drawn across his face side on); phone reading from three-quarter back
  no longer sits over his back (hidden by it: the gallery notes say avoid that view); new automatic check: a hand must
  touch its prop on the picture (a test proves it catches a gap); sheet labels no longer run into the next column.
- **Next:** Job G chat 4, new chat, **Opus, high effort**. Type: "Job G chat 4: read notes/next-jobs.md Where things
  stand and the Job G section." Steps 4-6, about 1%. After G: Job H (critique helper, about 2%): first chat Opus, max
  effort; type "Job H: critique helper. Read notes/next-jobs.md Where things stand and Build plan H. Estimate first
  (rule 86)."
- **Needs Sam:** nothing.
- **Read:** this file's Job G section; `guides/pose-gallery.md` top paragraph.
- **Open rule requests:** none. Step 6 proposes merging rules 41, 42 and 81 (81's check column still says "no
  automatic seam test yet": put right in that proposal).
- **For Claude:** `moves.phone_at_ear` (3D slab, `V._hull`); `grips.hidden_by` adds depth tests (head: beyond 0.25 hw;
  torso: beyond half its depth and within 1.25x its screen width); views skips an `on_face` arm hidden by the head;
  `handcheck.held_faults` (PROBE['held'] layer per side, TOUCH 0.12), kittest `held_prop_touches`. Unfinished: a
  "prop hidden" check (keyed prop pixels came back lightened, ~x1.3, in the probe: find why, then AVOID phone reading
  from behind in the dict too); `posegallery._wrap`.

## Job G (Sam: Y, 9 Nov, about 3.5-4% over two chats)
Found first: the gallery's "OK" meant only "a hand is visible"; it passed faults Sam would flag (sheet sent 9 Nov).
- **Chat 1 DONE (9 Nov, about 1.7%):** 6 views (mirrored) cropped round the whole body; checks: hand through the body,
  inside it, off its arm; point unreadable, bent, finger hidden; resting hand hovering/sinking/off the edge, hand off
  its grip; flip through front on and behind (fixed in views: never mirrored there). Grips: `grips.held` (any held prop
  in the right order for each view; hand over it), `Table` + `on_table`, `Carry` (a handed-over prop never jumps).
  Fixed in the kit: phone read, cup, cup sip (from behind they were drawn over his back), three-quarter back hands
  behind the body (palms together showed a hand on his back), points straightened (`views.aim`), the one-piece finger
  (Ad-Vanced 39b) is now the house finger. New gallery rows: hands on a table (drawn), phone reading, cup in hand,
  cup sipping. AVOID lists updated (pointing three-quarter back, pointing both ways three views, cup behind).
- **Chat 2 (about 1.5-2%), in order:** (1) DONE 10 Nov (chat 2): the shoulder-seam check, automatic, and the gap's
  cause fixed (a leftover body); (2) DONE 10 Nov (chat 3): phone at the ear redone, in the gallery; (3) DONE 10 Nov
  (chat 3): the on-picture hand-meets-prop check; phone reading from three-quarter back fixed (now hidden: avoid);
  sheet labels; (4) lying: gallery rows and checks (both arms on one
  side, arm curled, neck); (5) pre-flight flags a pose not from the gallery or seen from an AVOID view; new poses
  priced at planning; (6) rules 41, 42 and 81 merged, by-hand parts automatic (propose wording to Sam first).
- Not done in chat 1, on purpose: old films' own finger copies are unchanged; the kit's cup and phone (moves.py, also
  used by duel.py) now go through `grips.held`; `Carry` is a tool and a test, not yet wired into any film.

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
Order: E, F, G, H, I (each its own chat; fresh chat each; Sam's iPhone only).
**Models (Sam, 9 Nov; type /model to change; a chat on the wrong model stops and says so):**
| Job | Design and diagnosis | Building | Routine (checks, sheets, filing, commit) |
|---|---|---|---|
| E | Opus **high** (the body-note diagnosis decides G) | n/a (no building) | Sonnet |
| F | Opus medium | Opus medium | Sonnet |
| G | Opus **high** | Opus high | Sonnet |
| H | Opus **max**, the checklist design only (one short chat) | Opus high | Sonnet |
| I | Opus **high** (what to cut, rewrite, retire) | Opus medium | Sonnet |
- **E. Measure and diagnose** (~0.7%, Opus high): tokens a new chat loads, by file; which rules ever caught anything; every body note in the last ten films grouped by joint or action (neck, shoulder, elbow, hand-on-prop, lying, seated, mouth, clipping). Output: numbers and a cut list, no building.
- **F. Film ledger** (DONE 9 Nov, 0.4%; `source/ledger.py`) (~0.5%, Opus medium): the cost watch tags each chat with its film and sums per film; writes cost, chats, rounds, notes and repeated notes to a ledger; a 10-line audit at the end of each film (what repeated, what would have caught it, which rules never fired); estimate versus actual closed out.
- **G. Bodies** (~3-5%, Opus high, likely two chats): a pose acceptance test (every gallery pose, every view, automatic seam/gap/hover/clip checks; a film may only use passing poses; new poses are priced at planning); grip points and contacts for picking up, resting and lying; one fix goes into the gallery for every film.
- **H. Critique helper** (~2%, Opus high; Max only for the checklist design): a living checklist (people, creatures, props, sets, movement; each note of Sam's adds one line); a fresh helper with a small context reads the sheet, references and checklist cold; the "same kind everywhere" list per note; the before/after crop beside Sam's marked picture. First trial: the next new thing.
- **I. Consolidation** (~2-3%, Opus high): three layers of reading (one-page core, one job pack per job, rulebook and kit looked up only when named); each of the by-hand rules turned into a check, folded into the critique checklist, or retired (56, 76, 79 fold into 89); a library of new things that passed the critique (views, references, critique) so the next film reuses them; planning splits every film into known (almost free) and new (priced).
