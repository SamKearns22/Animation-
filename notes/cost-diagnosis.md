# Cost diagnosis job (Sam, 13 Nov): why each step got expensive, and how to make it cheap AND good

## Where things stand (the ONE handover)
- **Rules that bite next:** 19 (PASS/FAULT/COULD NOT TEST; one command, short summary), 85 (cost watch), 89.
- **Done (13 Nov, chat 3 of 8, Opus medium): Job C 1, 2, 3, 4, 6 written and tested on Blessed (no film render).**
  1: an elbow folded back across the body stops pre-flight even under the 'skeleton arm' allow (side-on arms excepted:
  no 'across' to read); ARM_FOLD_NAMED faults and `critique.py fixed ... --left N` print a ready "Checks:" line.
  Whole Blessed swept every 0.5 s: clean. 2, 6: CLAUDE.md. 3: rule 19 widened + `source/round.py`. 4: checklist P6,
  P7, P11. Also repaired a half-merged `notes/ledger/blessed.json` on the main line (both entries kept).
- **Sam (13 Nov):** Y to 5's new plan; necks and thighs fixed from the NEXT film, not Blessed. Y to "Never again"
  1-5 (below; rules 24, 85, 19 and CLAUDE.md already written; their tools not built).
- **Next: chat 4 of 8, Opus MEDIUM (building from a clear plan):** build 5 (pre-flight says COULD NOT TEST and stops
  when a film with people has no `solids`/`layers`; give Blessed its list) and the "Never again" tools: the ledger
  stops on real figures at the budget and every 5% (no alarms_off); COULD NOT TEST stops; the after-film comparison
  line. Test on Blessed's files without rendering a film. Hand over.
- **Needs Sam:** nothing.
- **Read:** this file's "Job C proposals" 5 and "Never again"; then only the lines each tool edits (`codemap.py`).
- **Open rule requests:** none unwritten (5 and Never again are written; their tools are chat 4's).
- **For Claude:** figure.NEVER_ALLOWED, figure.named(); preflight sets NAMED_FAULTS_FILE; critique.checks_line();
  `ledger.py app` rebuilds film rows from `notes/ledger/app-costs.tsv`. Never page a whole chat's events.

## Never again (proposed 13 Nov; Sam asked "how can we ensure this never happens again?")
1. Real money only: every handover adds its chat's real app cost to the film; the bottom lines show spent vs budget.
   Replaces: rule 85's estimate-based ledger (Job A built the reading).
2. The budget stops the chain on real figures: once at the budget, then every 5% over; it can be answered, not
   switched off. Replaces: rule 24's forecast alarm.
3. Process changes pay for themselves: every new rule, check, tool or step names its cost per film; after the next
   film, kept only if that film was cheaper or drew fewer notes; adding a step removes one. Widens CLAUDE.md's
   "the rulebook never grows" to tools and steps.
4. Every check passes, fails or says "couldn't test"; couldn't test stops the animatic. Generalises 5. Rule 89.
5. After each film, one line: real cost against the last three films; over 1.5x their average, the next chat's
   first job is finding why, before film work. Replaces the ledger's 10-line audit.

## Job B results (13 Nov): where each step's money goes
- **Prices, fitted to the app's real chat costs:** Opus re-read $0.22/M tokens, write $6.0/M, output $19.8/M;
  Sonnet $0.106, $3.94, $8.2. **Sonnet is about 2x cheaper a word, not 50x:** Job A's Sonnet chats were cheap because
  they were short (90-130k, a few actions), not because of the model. Chat size matters more than model.
- **Every action re-reads the whole history.** Measured (r2 chat 2, at 215k): each action, even an `ls`, costs about
  4.7 cents before it does anything; at 400k (chat 5) about 9 cents. A median Opus film chat is ~78 actions ending
  ~220k, about $5.6: the app's own 80k re-read on every action ~25%; start-up reading ~15%; work history (code
  reads, printouts, pictures, each action adding 0.5-1.6k) ~25%; output (code, thinking, replies) ~20%; writes the rest.
- **The steps that cost most (Blessed, real figures):**
  1. **Rework of faults that came back: about 15% of a week.** Walliams' face took 5 chats, $31.7 (10.9%). Notes N1,
     N6, N8, N11 were repeats; the round fixing them (chat 2 of 8, $8.24) and animatic 4's stop ($2.67 + reruns) ~4%.
  2. **Running long and bundling stages: chat 5, $27.73 (9.6%).** Sam's "don't stop for any Y" was read as a cost
     'override', so it bundled 4 stages (seated rebuild, van sheet, note 48, animatic 3) and ran to 414k. A model change
     inside it re-paid the whole history: the switch to Sonnet rewrote 364k ($1.43); one action on the app's fallback
     model rewrote 414k ($4.37). The same ~290 actions in chats of 200k or less: about $16.7, **saving ~$11 (4%)**.
  3. **Critique helpers: about a quarter of every build chat** (Sam's 11 Nov measure, rule 85); 7 passes on Blessed,
     6-17 faults each, most re-listed every pass as "named, not changed" (ball hands, no necks, no thighs).
  4. **Small actions:** most of a chat's ~78 actions add under 2k each (look at a log, `ls`, one grep, a second
     commit to fix the first handover). Each still pays the full re-read.
  5. Pictures and pre-flight are cheap in tokens (a sheet ~1.6k; Blessed's pre-flight 17 faults, ~1.9k filtered).
- **Did the checks catch what Sam later named? Yes, twice, and both were let through:**
  - Pre-flight (chat 3): "gates2 50.25 s: elbow folded back across the body" = Sam's N1, printed under "allowed: a
    skeleton arm, checked in 3D", so it passed; the film's own arm check then stopped animatic 4 a day later.
  - Critique round 3: "pool player upright, cue flat... pool table reads as desk", and hunt 2 "grey figure sliced at
    left" = Sam's N8 ("a squashed person who clips through a pool table"); the fix only lengthened the cue.
  - So the money is lost after the catch, not in it: a named fault left open costs a full notes round (~2-3%).
  - What no check tests: one body passing through a set object while moving (N8, and note 8 before it).

## Job C proposals (13 Nov; sent to Sam as one numbered message; nothing written until his Y)
1. **A caught fault is fixed or told, never waved through.** Pre-flight stops on an elbow folded back across the body
   (the 3D 'allowed' covers only foreshortening); `critique.py fixed` prints every fault left open as a ready
   "Checks:" line. Saves ~2-3% a film (N1, N8). Risk: more Checks lines. Replaces: CLAUDE.md's by-hand "never send
   something a check flagged without saying so" becomes a check (views.py, critique.py); no new rule.
2. **"Just go" never skips the hand-over.** At red the chat opens the next one, which carries on without asking.
   Saves ~4% (chat 5). Risk: one more chat start (~$0.5). Replaces: CLAUDE.md "Just go ... never the checks" gains
   "or the hand-over"; rule 85 unchanged.
3. **One step, one command.** The film's round script does fix, clip, sheet, checks and save in one run with a short
   summary. A third fewer actions saves ~$1 a chat, ~2.5% a 7-chat film. Risk: a failed run reruns more. Replaces:
   rule 19 widened ("checks print a short summary" becomes "each step is one command with a short summary").
4. **Ball hands, no necks, no thighs: fix or house style?** Y = house style: the critique stops listing them (saves
   reading and answering ~5 faults a pass). N = fixed once in the figure kit (one build job, ~2%), then checked.
   Replaces: a line in `guides/critique-checklist.md`.
5. **No passing through things.** Rule 83 widened from painted objects to people and props in every frame;
   pre-flight tests it (N8 kind). Build ~1% once; saves a notes round (~2-3%) each time. Replaces: rule 83, merged.
6. **Model changes only by hand-over.** Switching a long chat's model re-pays its history (chat 5: $5.80, 2%).
   If you want Sonnet, say "hand over to Sonnet". Replaces: CLAUDE.md's "change model only by starting a new chat",
   which gains the reason; no new line.
- **Together:** a Blessed-sized film at ~7-8 chats of $4-5 with no repeat round is $30-40, 10-14% of a week.

## Job A results (13 Nov, real app figures, list $; % of a week at WEEK_USD 290)
- **Blessed 44.7%** (16 chats from the app $93.6 = 32.3%, plus 12.4% estimated for 11 Nov chats the app cannot show);
  estimate 19%. Chat 5 alone $27.73 (9.6%). **Remakes 30.4%** in the app (19 chats from 10 Nov; the old ledger's
  "45% from Sam's meter" was the whole week's meter, not this film). **Protest Tiers 8.5%** so far (7 chats incl.
  framing research and sketches; plan and research only).
- **Where an Opus chat's money goes** (36 Opus chats, $176, prices fitted to the app's own figures: re-read $0.22/M,
  write $6/M, output $20/M): **re-reading history 49%, writing new history 27%, output 22%.** 26 of 36 Opus chats ended
  at 200k+ history and cost $158 of the $176; the 10 that stayed under 200k cost $18.
- **Sonnet is ~50x cheaper per routine stage:** 6 Sonnet chats (animatics, finals) cost $2.80 in all ($0.13-0.97 each);
  Opus chats that rendered animatics cost $5-28 (Blessed chats 3 and 5, Remakes "animatic completion" $6.50).
- Typical Opus film chat: $4-8 (1.5-3% of a week), ending at 200-300k history. A film at 10-15% is about 5-7 such chats;
  Blessed has used 22 and Remakes 19.

## The facts found (13 Nov)
- **The record misses most of the cost.** `ledger.py auto` commits then runs `git push origin HEAD`; the start-up hook
  (`setup.sh` line 23) tells chats to `git checkout --detach`, and a detached `push origin HEAD` fails (tested). A
  chat that ends on Sam's usage limit never runs the Stop hook at all. Blessed chat 5 (13 Nov, session
  ..WX6ZgL6kQ5WZ2nxNH) cost $27.73 (about 9.6% of a week) and has no row.
- **Real costs, 14 Blessed chats visible from 12 Nov 17:10:** $94.80 (about 33% of a week). Earlier Blessed chats are
  not visible from this account (Sam switched accounts 12 Nov). Per chat: $4.4-8.2, one at $27.7; 12 of 14 on Opus.
- **The cost is re-reading.** Chat 5: 92M tokens re-read, 1.3M written, 177k output; chats end at 200-414k tokens
  of history, and every step re-reads all of it. Job E (notes/job-e-measurements.md): a fresh chat is 80k before
  work, a film round reads 40-55k more.
- **The process grew (main line, words):** rulebook 3,034 (28 Oct) -> 5,898 now; kit catalogue 1,845 -> 5,057; tools
  147 -> 229 files; Blessed's own code 48k words in 6 files. New per-round steps since early Nov: pre-flight
  (15-40 min; one run printed 99 faults, mostly noise), critique helpers (2 hunts per stage, 13-17 faults each),
  name test, check sheets, pictures read into the chat. Every step's output stays in the history that each later
  step re-reads.
- **And mistakes still pass, so we pay twice.** The same faults return each round (ball hands, no necks, no thighs:
  "named, not changed"); the Walliams face took about 5 chats; notes 8, 10, 11 were repeats. The checks look at
  stills and poses, not overlaps or movement (note 8: body through the pool table).
- **Models:** animatics 2 and 3 rendered inside Opus chats; chats bundled stages ("tune, clip, animatic 2"), so the
  model-by-stage rule never fired; Sam switched chats 4 and 5 to Sonnet himself.
- **Earlier films:** Ad-Vanced Notice about 10%, Halo 12-15%, Netan-yahoo 12-18% (archive notes).

## Job A: the real cost record (Sam: Y)
Rebuild the ledger from the app's own per-session figures (above), not the transcript estimate or a git push:
Blessed, Remakes, Protest Tiers. Fix the detached-push loss. Small.

## Job B: where each step's money goes (the real question)
For 2-3 Blessed chats (chat 5, round-2 chat 2, chat 2 of 8 on 13 Nov) and one cheap older film's chats if visible,
split the cost by step: start-up reading, film code reads, pre-flight, critique helpers, pictures, renders waited on,
rework of a repeated fault. Name the 3-5 steps that cost most and whether each ever caught a fault Sam would have
named (the ledger's critique lines, notes tables).

## Job C: proposals for Sam (one message, numbered, Y/N)
Make each step cheap and good: cut or shrink steps that cost much and catch little; keep chats small (one stage
each, on its model); reuse before re-reading; checks that test what Sam actually notes (overlaps, movement,
repeats). Each proposal: what it saves (in % of a week, measured), what it risks, the rule or tool it replaces
(CLAUDE.md: the rulebook never grows). Target: a film in 10-15% again.
