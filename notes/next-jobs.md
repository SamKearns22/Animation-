# Where things stand (project, 10 Nov; no film in progress)

- **Rules that bite next:** 86 (Job H stays inside 5% of a week: Sam, 10 Nov, raised it from 2.5%; about 1.5% spent), 89 (the critique the helper
  will run), 85 (cost watch: on amber, finish the step and hand over).
- **Done (10 Nov, Job H chat 1, design, Opus max, about 1.5%: max effort cost more than the 0.9% planned):** the critique checklist,
  `guides/critique-checklist.md` (33 lines from Sam's past notes, in six parts: every sheet, people, creatures,
  props, sets, movement; how each new note adds or strengthens a line); the helper's design and the build list (this
  file's Job H section). Job G not touched.
- **Next (Job H):** chat 2, the build, **Opus, high effort**: "Job H build: read notes/next-jobs.md Where things stand
  and Build plan H." About 1.5% (Sam, 10 Nov: Job H may go to 5% of a week; 1.5% spent). Sam's overnight chat opens it (chats it starts can't).
- **Job G (chat 4 done, 10 Nov, steps 4-6, Opus high, about 1.3%, stopped on amber):** lying checks: a neck shows,
  no arm held up in the air, each arm on its own side (Sam's lying notes); the kit's lying arms laid flat (elbows bent up
  into the air: Elder Swindon 6's cause); pre-flight now stops a pose seen from an "avoid" view or with no gallery row,
  and checks every lying body; 12 everyday kit poses added to the gallery (hands on hips, pockets, shrug...). Rules
  that bite: 42, 41. **Next for G:** nothing; Job G is finished once Sam numbers the step 6 proposal.
- **Job I proposed (Sam, 10 Nov: "the lying down people don't look right at all ... squiggly balloon people with
  inflated heads, not at all like how our characters look usually"):** rebuild how lying people are DRAWN so they match
  the flat figure rig (views.person: its head size, outlines, jacket, sleeves, circle hands), keeping lying.py's 3D
  skeleton, contacts and the chat 4 checks underneath. Cause: lying.draw paints its own rounded 3D volumes (tubes and
  ellipsoids, a 3D head), a second look nobody compared against the cast. Chat 4 looked at a lying sheet and checked
  only the arms: a miss. Plan, Opus high: side-by-side sheet (standing cast vs lying) first, then the build. About 2-3%.
  **Sam, 10 Nov: Y, for the overnight chat. Test on the newest Vance (Ad-Vanced Notice's cast, as in the posted
  final), standing beside his lying versions; the old test trio (P1, LADY, MAGNATE) only after he looks right.**
  Sam, 10 Nov: no yes needed before the build: make the side-by-side sheet, then build straight on, and send him
  the sheet with the result.
- **Needs Sam:** nothing (10 Nov: Y to Job I and to merging rules 41, 42, 81: written). Was: 1. Merge rules 41, 42 and 81 into one rule (wording in the Job G section, "Step 6 proposal")? Y/N.
- **Read:** this file's Job H section; `guides/critique-checklist.md` (header only).
- **Open rule requests:** none from H (rules 30, 56, 89 written 10 Nov). Job G step 6: rules 41, 42, 81 merged into 41 (Sam: Y, 10 Nov; written).
- **For Claude:** build `source/critique.py` (pack, record, where, before) as the Job H section says; packs in
  `source/data/critique/` (git-ignored); results into the ledger's round files. Job G's own notes: Job G section.

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
  sheet labels; (4) DONE 10 Nov (chat 4): lying: gallery rows and checks (both arms on one
  side, arm curled, neck); (5) DONE (chat 4) pre-flight flags a pose not from the gallery or seen from an AVOID view; new poses
  priced at planning; (6) PROPOSED (chat 4, below) rules 41, 42 and 81 merged, by-hand parts automatic (propose wording to Sam first).
- **Chat 4 (10 Nov):** `lying.body_faults` (neck shown 2 cm+, elbow or hand over 10 cm up with nothing under it, an
  arm crossing to the other shoulder's side on the picture); `lying.gallery` (12 views x 3 people x both ways) in
  `lying.py check`; kit arms laid flat (face down, on the back, curled), `ball` (Ad-Vanced's guard) in the kit,
  `_head_down` rests on the hair too (P1's hair was 1 cm into the floor); `posecheck.py` (wraps the named pose calls,
  views.person and lying.draw; its faults ride on handcheck's frames, "POSE:" lines); kittest `lying_and_pose_checks`.
  New gallery rows passed the automatic check only (not looked at by eye). Still untested kit poses (a film using one
  is stopped): chop, heart, paper, head in hands (real faults in front views).
- **Step 6 (Sam: Y, 10 Nov; WRITTEN as rule 41, rows 42 and 81 removed):** replace rows 41, 42 and 81 with one row 41
  (the rulebook gets two rows shorter):
  "41 | Bodies and hands (Sam, 4-10 Nov). Poses come from the tested gallery (`guides/pose-gallery.md`) and are never
  shown from a view its row says to avoid; a new pose is tested from every view first (standing 6, seated 5, lying 12)
  and its build priced at planning. Every arm ends in a visible hand, every frame, every view; a point shows one
  finger out along the forearm. Arms and body are one piece: one outline from the collar over the shoulder and down
  the arm, no line, cap, notch or step at the join (an armpit crease only when the arm is lifted). Standing at rest
  the legs are straight and the elbows bend a touch outward (`references/figure-rig/`). Lying, a neck shows, a limp
  arm lies flat, and each arm stays on its own side. Every cast sheet draws the arms exactly as the film does. |
  `handcheck.py` every frame (hands, points, hands meeting props, the shoulder seam); `posecheck.py` in pre-flight
  (avoid views, poses with no gallery row, lying bodies); `posegallery.py`, `sitting.py audit`, `lying.py check`;
  `kittests.py` (gallery, point, legs and elbows, seam, held props, lying); by hand: the look on the check sheet."
  This also puts right 81's old check column ("no automatic seam test yet": there is one since chat 2).
- Not done in chat 1, on purpose: old films' own finger copies are unchanged; the kit's cup and phone (moves.py, also
  used by duel.py) now go through `grips.held`; `Carry` is a tool and a test, not yet wired into any film.
- **For chat 4 (from the 10 Nov handover):** `moves.phone_at_ear` (3D slab, `V._hull`); `grips.hidden_by` adds depth tests (head: beyond 0.25 hw;
  torso: beyond half its depth and within 1.25x its screen width); views skips an `on_face` arm hidden by the head;
  `handcheck.held_faults` (PROBE['held'] layer per side, TOUCH 0.12), kittest `held_prop_touches`. Unfinished: a
  "prop hidden" check (keyed prop pixels came back lightened, ~x1.3, in the probe: find why, then AVOID phone reading
  from behind in the dict too); `posegallery._wrap`.

## Job H, critique helper (build plan H; Sam: Y to about 2%; 10 Nov overnight run, his "just go" for H only; cap raised to 5% the same night)
**Estimate (rule 86, firmed 10 Nov):** about 3% of a week; Sam (10 Nov) raised the cap from 2.5% to 5%: stop past 5%. Chat 1, the design (Opus max): about
1.5% (0.9% planned; max effort cost more). Chat 2, the build (Opus high): about 1.5% (the harvest, about 0.4%; one tool
of about 300 lines, its tests, two helper calibration runs at about 0.1% each). No Sonnet stage planned; if chat 2 goes amber, its leftovers go to one. The first trial (the next new
thing) waits for the next film.

**Design (chat 1, DONE 10 Nov):**
1. **The checklist:** `guides/critique-checklist.md`. Six parts (A every sheet; P people; C creatures; O props, text and
   signs; S sets; M movement), 33 lines seeded from Job E's 60 body notes and Sam's other fault notes. Each line is a
   statement the helper confirms on a picture, with Look (what the sheet must show) and Tool (a check that also holds
   it). Its header says how each of Sam's notes adds or strengthens a line (a note a line already covered is a miss:
   say why), at most 12 lines a part.
2. **The helper:** a NEW agent every pass (Agent tool, general-purpose, model opus whatever the chat's model; about
   0.1% a pass). It sees no chat, no code, no claim of what was fixed. Two steps, the second hidden until the first is
   written:
   - Step 1, the cold look: only the numbered panels (no captions). Per panel, 15 words at most: the things, actions
     and feelings it sees and every word exactly as written; never a real person's name. It writes look.md; only
     then does step1.md send it to step2.md (so it cannot read the brief first).
   - Step 2, the check: brief.md (each panel's intent, its acting beat, the views the film uses, its parts of the
     list), the check sheet (each panel beside its references) and checklist.md (A plus the parts on the sheet). Per
     panel: "ok:" with the line ids it confirmed, then each FAULT (panel, where, what) or CAN'T TELL (what picture
     would show it). Then its cold look against brief.md (A1). For each FAULT, the same fault looked for on every
     other panel (A3). In a notes round, per note of Sam's: fixed in AFTER? worse anywhere? the same fault elsewhere?
     Then up to 5 things Sam would flag that no line covers, each with a suggested line. Under 400 words, no praise.
   - The prompt opens: "Someone else made these pictures for a director who has sent back faults in almost every
     first look. Assume there are some: find what he would flag. Don't reassure."
3. **Passes (rule 89):** fix every FAULT or name it to Sam; remake the sheet so every CAN'T TELL is shown; pass 2 is a
   NEW helper; a third only if pass 2 found something real; a fault that survives three goes to an options sheet (87).
4. **Same kind (rule 56):** each of Sam's notes gets its line id and every instance in the film (shot, time, who or
   what). `critique.py where` lists named things per shot from the film's `draw_order(t)` and flags any that start or
   stop mid-shot (it would have caught Elder Swindon 59, 62 and 64). The sheet has a panel per instance.
5. **Before and after:** at the start of a notes round, before any fix, the frames each note touches are saved; after
   the fix, one panel per note: Sam's marked picture (if sent), before, after, the same box at the same scale.
6. **The record:** each pass's look and result go into the ledger's round file; FAULTs per line id (and false alarms
   Claude marks) are tallied in the film's ledger, so Job I sees which lines catch and which only cry wolf.

**Build (chat 2, Opus high), in order:**
1. Harvest (about 0.4%; added with the higher cap): read only the notes tables of the last ten films (the archive and
   Elder Swindon) for Sam's fault notes outside Job E's body groups (creatures, props and text, sets, movement,
   faces, acting). File each under a checklist line (count, Came from) or a new line, by the header's rules: parts
   C, O, S and M rest on one or two notes a line now.
2. `source/critique.py`, with a MAP:
   - `pack FILM SPEC.json`: renders the panels (sheet.py's clean picture), makes `1-look.jpg` (phone-size frames 270 px,
     detail crops 540 px, numbers only, at most 1080 px wide, a second image past 12 panels), `check.jpg` (compare.py:
     each panel beside its references), `brief.md`, `checklist.md` (A plus the parts asked, no "Came from"),
     `step1.md`, `step2.md`, and in a notes round `notes.md` and `beforeafter.jpg`; prints the one-line Agent prompt.
     SPEC: `{"round": R, "panels": [{"t": 12.3 or "img": PATH, "crop": [x0,y0,x1,y1] or null, "is": "...",
     "parts": "PO", "refs": [...], "beat": "...", "views": [...]}], "notes": [{"n": 61, "words": "...",
     "line": "O3", "marked": PATH or null, "t": 20.1, "box": [...]}]}`.
   - `record FILM PACK`: refuses unless look.md was written before result.md, every panel has a look line and every
     line that applies to each panel is answered; saves both into the ledger; tallies per line id.
   - `where FILM NAME...` and `before FILM SPEC`. Packs live in `source/data/critique/` (add it to `.gitignore`).
3. kittests: record refuses a half answer and a look written after the result, passes a whole one; checklist.md holds
   only the parts asked and no "Came from"; where flags a thing that pops in mid-shot (a small made-up film module).
4. Calibration, two helper runs (a third only to recheck a reworded line), no film rendered (stills only): current Elder Swindon frames plus two of Sam's
   old faults put back (the EGG MAYO box mirrored with PIL; a gallery hand moved off its phone the way kittest
   `held_prop_touches` does) beside clean panels. It must flag O1 and P1 and nothing on the clean panels. A miss:
   reword that line or the prompt once and rerun; a second miss is written here as a limit.
5. Pre-flight prints one line: "critique: round R, pass N clean / N faults open / none recorded" (it refuses the
   animatic, rule 89).
6. A kit-catalogue row; the notes template's status column asks for the checklist line (rule 30).
7. Handover: a Next line Sam's overnight chat can start, or "Job H finished" (that chat tells Sam). Fetch and merge
   before every push (Job G's chat pushes to the main line too) and keep Job G's line in Where things stand.

**Rule requests (Sam: Y to all, 10 Nov; written in the rulebook, so the build makes pre-flight refuse, and the notes
template's status column names the checklist line):**
1. Rule 89's check column becomes: "`critique.py`: a fresh helper reads the sheet, references and
   `guides/critique-checklist.md` cold; each pass is saved in the ledger; pre-flight refuses an animatic until the
   round's last pass is clean or its faults are named (`--faults-named`)." A by-hand rule turned into a check.
2. Rule 30, merged (no new rule), adds: "each fault note names its checklist line; a fault no line covers adds one; a
   fault a line already covered is a miss: say why (line unclear, sheet didn't show it, no critique) and fix that."
3. Rule 56's check column: "by hand (check sheet)" becomes "`critique.py where` lists every instance; the critique
   sheet shows each".

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
Order: E, F, G, H, I (the lying redraw), J (each its own chat; fresh chat each; Sam's iPhone only).
**Models (Sam, 9 Nov; type /model to change; a chat on the wrong model stops and says so):**
| Job | Design and diagnosis | Building | Routine (checks, sheets, filing, commit) |
|---|---|---|---|
| E | Opus **high** (the body-note diagnosis decides G) | n/a (no building) | Sonnet |
| F | Opus medium | Opus medium | Sonnet |
| G | Opus **high** | Opus high | Sonnet |
| H | Opus **max**, the checklist design only (one short chat) | Opus high | Sonnet |
| J | Opus **high** (what to cut, rewrite, retire) | Opus medium | Sonnet |
- **E. Measure and diagnose** (~0.7%, Opus high): tokens a new chat loads, by file; which rules ever caught anything; every body note in the last ten films grouped by joint or action (neck, shoulder, elbow, hand-on-prop, lying, seated, mouth, clipping). Output: numbers and a cut list, no building.
- **F. Film ledger** (DONE 9 Nov, 0.4%; `source/ledger.py`) (~0.5%, Opus medium): the cost watch tags each chat with its film and sums per film; writes cost, chats, rounds, notes and repeated notes to a ledger; a 10-line audit at the end of each film (what repeated, what would have caught it, which rules never fired); estimate versus actual closed out.
- **G. Bodies** (~3-5%, Opus high, likely two chats): a pose acceptance test (every gallery pose, every view, automatic seam/gap/hover/clip checks; a film may only use passing poses; new poses are priced at planning); grip points and contacts for picking up, resting and lying; one fix goes into the gallery for every film.
- **H. Critique helper** (design DONE 10 Nov: `guides/critique-checklist.md`; the build list is in the Job H section above) (~2%, Opus high; Max only for the checklist design): a living checklist (people, creatures, props, sets, movement; each note of Sam's adds one line); a fresh helper with a small context reads the sheet, references and checklist cold; the "same kind everywhere" list per note; the before/after crop beside Sam's marked picture. First trial: the next new thing.
- **J. Consolidation** (was I; renamed, Sam 10 Nov: Y; runs after H and I) (~2-3%, Opus high): three layers of reading (one-page core, one job pack per job, rulebook and kit looked up only when named); each of the by-hand rules turned into a check, folded into the critique checklist, or retired (56, 76, 79 fold into 89); a library of new things that passed the critique (views, references, critique) so the next film reuses them; planning splits every film into known (almost free) and new (priced).
