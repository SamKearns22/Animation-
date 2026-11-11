# The budget job: Remakes at 15% (11 Nov; proposals only, nothing changed yet)

## Where things stand (11 Nov, 21:00 UTC; budget chat 3 handed over at the amber line: (a)-(d) built, (e) a third built)
- **Rules that bite next:** 89 (two hunts, each fault once), 24 (stage-share stop), 85 (helpers counted).
- **Done (each with a kittest, all pushed):** (a) `critique.py`: answer form "## Faults / FAULT P3 [2, 4-6]" (the old
  form still reads), spec needs `"stage"`, a third hunt or third pack per stage refused, `fixed` clears hunt 2,
  CAN'T TELL never blocks, `"glimpse": true`, Build pack line. Measured on the 18 recorded answers: 25% fewer words,
  710 fault lines become 450 (a floor: word-for-word repeats only). (b) `ledger.stage_alarm`: auto stops at a stage's
  share and each half share on; rule 24's check column. (c) `critique.py redo FILM SPEC` (spec adds "draw", "checks"):
  one sheet of changed panels only, fault lines only; not yet used on a film. (d) timed, one-line job, Opus: general-
  purpose 0.19, claude 0.19, Explore 0.15 and Plan 0.15 but read-only (cannot write look.md): none usefully lighter.
  (e) `critique.palette`: ours' main colours against the references (A2, S3), run by redo and pack.
- **Next (Fable, high effort; "Budget job, chat 4"):** 1. time ONE one-line `critic` helper (`.claude/agents/critic.md`,
  Read and Write only; a chat learns its kinds at start, so chat 3 could not): if lighter than 0.19, set
  `critique.HELPER` with the figure beside it. 2. try `palette` on a real film's panels and references (Blessed's
  sets): count false alarms, tune or make it advisory. 3. the rest of (e): the reference tick-list filled by a tool
  (`guides/reference-pack.md`); "big enough at phone size" as a script (the testable part of A1, O3, S1); the trials'
  child body and poses into the kit. P2 (acting reads) cannot be scripted; P6 has handcheck. Then one message to Sam.
- **Needs Sam:** nothing. **Open rule requests:** none.
- **Read:** the MAP of `critique.py`; only the functions touched. Do not read the trial chats' events.
- **For Claude:** chat 3 cost 2.4% (0.7 of it the four timing helpers). `passes` rows now carry `stage`, `hunt`,
  `fixed`; a pass with faults files nothing in "Passed the critique" even after `fixed` (Sam's look replaces hunt 3).

## Corrections after Sam's challenge (11 Nov): these override anything below that disagrees
- **Chats:** the last audit was right; short chats with good handovers stay. My "0.4% to start a chat" was wrong: a
  whole Opus chat on this film cost 0.21%, so a start is about 0.15%, and starts were about 4% of Remakes, not 8%.
  Proposal 5 is now only: fix faults as one list, draw once, look once (fewer steps), and one critique helper per
  stage rather than one per set. "One chat per stage" is withdrawn.
- **Critique:** the record backs Sam. Pass 1 and pass 2 both found many real faults; pass 3 found 31, of which 4 were
  fixed and 6 went to Sam, who passed them. Proposal 2 is now: keep both hunts; the third hunt is replaced by Sam's
  look at the cast sheet; each fault listed once; "can't tell" answers no longer block.
- **Cast sheet:** already done. Proposal 3 is withdrawn; the only change is that the sheet goes to Sam after pass 2,
  in place of a third pass.
- **Forecast now about 20%** (cast 7.5, sets 3.5; the rest as the table). The trial measures the cast figure.

## Trial 1 result (11 Nov): Link rebuilt as a Lead, two critique hunts, batch fixing
- **Cost 2.0% of a week** (two Opus high chats; the helpers' 200k tokens may be on top), against 1.1% planned and
  about 1.9% a character in the real film. **Batch fixing did not make a Lead cheaper.**
- Read-in 0.3 a chat; first drawing 0.7; own look 0.3; hunt 1 0.5; hunt 2 0.2. The first chat went amber (history
  size) at 1.0%.
- Hunt 1: 34 listed, 13 distinct, 8 real. Hunt 2: 37 listed, 15 distinct, 11 real (5 were hunt-1 fixes that had not
  landed, 6 new). **Both hunts earn their place (Sam was right).** About 60% of what a helper lists is repeats.
- Quality (the trial chat's view; Sam has the sheet): the real Link's costume is more polished; the trial has all
  five poses where the real cast file had one. The repeat faults were all poses, not the design.
- **A Lead at this quality costs about 2%.** Forecast for Remakes stays about 20-21%: 15% is not reachable for 9 new
  characters and 3 places. Untested lines: Glimpses (trial 2, `notes/trial_lineup.md`), sets, the notes rounds.

## 1. Where Remakes' 60% went
The early chats were recorded as one lump, so these are rebuilt from the handovers (good to a few points each).

| Stage | Remakes, real | New process | What changes |
|---|---|---|---|
| Plan | 1 | 1.5 | more is asked up front |
| Cast (9 new characters) | about 17 (7 chats) | 6 | tiers, one critique hunt, Sam's early look |
| Sets (3 places) | about 8 (3 chats) | 3 | backdrops judged inside the shot |
| KG's beak rebuilt | 1.5 | 0 | asked at the brief |
| Shots and animatic 1 | about 5 | 3.5 | the acting goes in first time |
| Notes rounds, animatics 2-3, critiques | about 25 | 3.5 | far fewer notes to fix |
| Final | about 2.5 | 0.5 | one render, no re-render |
| **Total** | **about 60** | **18** | |

**Honest answer: Remakes exactly as it ended up lands at about 18%, not 15%** (it was 16.5 before Sam's answer that the animatic stays as clean as Remakes')**.** It had 9 new characters, 3 places
plus a fourth background added later, and 4 action scenes; MidTerminal (11%) had 3 characters and one room. It reaches
about 16% if the three mid-film additions (Saria, the reverse-shot street, the beak) are known at the brief, so
they are built once. The least certain line is the notes rounds (3.5): it assumes the first animatic already acts.

## 2. The five causes
1. **The critique never finished.** Each pass used a fresh helper told to hunt for everything. The cast passes found
   39, then 52, then 31 faults: a fresh eye always finds 30-50. Everything was fixed, including "can't tell" answers,
   and the same fault was often listed under several headings. Sam's one look ("It looks excellent") settled six
   faults that had survived three passes. Two critique fixes were later undone by Sam (notes 65, 70).
2. **Every character got the lead's treatment.** Five line-up characters are on screen for about 3 seconds, small.
   They were drawn in several poses, alone at full size, and critiqued three times.
3. **Polish ate the acting budget.** By the animatic the week was at 75%, so it was made with "holds and cuts, no
   rehearsals". Sam's notes were then the brief's own acting: KG too static (three notes), the gate, the blood, the
   grenade. Stills were over-checked; movement, which Sam notes on most, got nothing.
4. **Too many chats, too many small steps.** About 25 chats. Each new chat costs about 0.4% of a week before it does
   anything, so roughly 8% went on starting chats. Faults were fixed one at a time (fix, draw, look), and every look
   re-reads the whole chat.
5. **The estimate priced drawing, not loops.** 1.1% per character was planned; about 1.9% was spent. Nothing stopped
   the cast stage spending the sets' and the movement's share.

## 3. Proposals (Y/N each; each replaces or merges into an existing rule, so the rulebook does not grow)
1. **Screen-time tiers** (into rule 24's estimate). Every new character and place is a Lead (speaks or has a
   close-up), Support, or Glimpse (under about 4 seconds, or never taller than a third of the frame). A Glimpse gets
   one view and one pose, and is checked only inside its shot at phone size. In Remakes: Leads Link and KG; Support
   Navi and the gunman; Glimpse the five in the line-up.
2. **One hunt, then a check-back** (rewrites rule 89's "two passes, a third if..."). One cold critique per stage
   (cast, sets, animatic). Each fault is listed once and ranked: "Sam would send it back", "he might", "polish".
   Sam, 11 Nov: the animatic must arrive as clean as Remakes' did, so both "would" and "might" faults are fixed
   before sending. Only pure polish and "can't tell" are dropped. The second pass only checks that the fixed faults
   are fixed; it does not hunt again.
3. **Sam sees a rough cast sheet first** (changes the order in the Build pack). Shapes, proportions and colours, no
   detail, before the critique. His notes on taste ("not too chibi", the crests) then cost minutes, not chats.
4. **Movement's share is ring-fenced** (into rule 24). The estimate's movement and acting share cannot be spent by
   the cast or sets. The rehearsal clips of the showstoppers are made straight after the rough cast sheet, before
   detail. Animatic 1 always carries the acting list; "holds and cuts" is never the fallback.
5. **Batch work, fewer chats** (into rule 85 and the "Models and chats" section). One chat per stage, not per critique
   pass. Faults are fixed as one list, drawn once, looked at once on one sheet. One critique helper per stage, not
   one per set.
6. **A hard stop at each stage's share** (tightens rule 24: now it stops a quarter over). At the share, the chat stops
   and sends Sam what exists, with what is left and the cheapest way on.
7. **Estimates in measured units** (into rule 24). A full Opus chat is 3% of a week; a fresh chat is 0.4%. Targets,
   to be replaced by real figures as films are made: Lead 1.2, Support 0.6, Glimpse 0.25, a backdrop 0.7, a
   showstopper move 0.6, a notes round 2.5.

## 4. Who does what
**Sam, at the brief**
1. For each new character: a picture, and up to three must-haves ("a real beak that moves", "carries the sword").
   In Remakes these arrived mid-build and cost about 3%.
2. Say Y or change my tiers (proposal 1).
3. Name the 2-4 showstopper moments.
4. If the estimate is over 15%, choose the full or the trimmed version knowing the figure.

**Sam, during the film**
5. One look at the rough cast sheet; one look at the rehearsal clips.
6. Notes in one batch per animatic where possible (each batch opens a chat).
7. For anything added after "go", I give the price first; Sam says Y or N.

**Claude**
- Tiers, the estimate in measured units, stage shares and the stop.
- Rough sheet, then moves, then detail; one critique hunt per stage, ranked.
- Batch fixing, one chat per stage, the acting in the first animatic.
- The forecast line at every stage end (already built, Job M).

## 5. After both trials (11 Nov): these figures override sections 1-3 where they disagree
**Measured units (% of a week, critique helpers counted):** a Lead through two hunts 3.2 (trial 1); five Glimpses in
one frame through two hunts 3.7, 0.74 each (trial 2; 0.3 of it a 2-hour stop that re-read the chat); a critique helper
0.48 (0.44-0.51), 0.16-0.18 of it start-up; one step of a fixing chat 0.02 (1.35 over 70 steps, 1.22 over 59); a fresh
chat's read-in 0.2-0.3; a Sonnet finishing chat 0.34. The cost watch under-read both trials by 0.9-1.0 (the helpers).

**Savings, stage by stage (Remakes real, then new):**
| Stage | Real | New | The saving and its measured figure |
|---|---|---|---|
| Plan | 1 | 1.5 | none: more is asked at the brief |
| Cast: the line-up five | about 9 | 3.7 | Glimpse tier, measured (trial 2). Needs Sam's yes on the sheet |
| Cast: Link, KG (Leads) | about 5 | 6.4 | none: a Lead at this quality is 3.2, measured (trial 1) |
| Cast: Navi, the gunman (Support) | about 3 | 2.5 | not measured |
| Sets, 3 places | about 8 | 4.5 | 9 critique helpers (4.3) become 2 (1.0): the helper figure is measured, the rest is not |
| KG's beak rebuilt | 1.5 | 0 | asked at the brief |
| Shots and animatic 1 | about 5 | 5 | none: the acting now goes in, so no cheaper (not measured) |
| Notes rounds | about 25 | 5.5 | two rounds at about 2.7 (a fixing chat 1-2, a Sonnet chat 0.34, two helpers 1.0) |
| Final | 2.5 | 0.5 | one Sonnet chat, measured 0.34 |
| **Total** | **about 60** | **about 30** | |
| Two tool changes, if they work | | **about 26** | fewer steps: 70 to about 40 a fixing chat, 0.4-0.5 a pass, 8 passes; each fault listed once: 0.08 a helper, 16 helpers |

**Why the forecast rose from 20:** the helpers (a quarter of every build) were invisible to the cost watch, and a Lead
costs 3.2, not the 1.2 planned. The cost follows the process (two chats and two helpers, 3.2-3.7), not what is drawn.
15% fits a film the size of MidTerminal (3 characters, one room), not Remakes (9 new characters, 3 places).

**Proposals sent to Sam (11 Nov), my pick in brackets:**
1. Tiers in the estimate: Lead, Support, Glimpse (one view, one pose, judged only in its shot at phone size). (Y)
2. Critique: two hunts a stage; Sam's look at the sheet replaces the third; one helper per hunt for the whole stage,
   not one per set; each fault listed once; "can't tell" no longer blocks. (Y)
3. One command that draws, checks and makes the sheet; faults fixed as one list; only the sheet is looked at. (Y)
4. The cost watch and ledger count the helpers, and price Fable as Fable. (Y)
5. Movement's share ring-fenced; rehearsal clips before detail; animatic 1 always carries the acting. (Y)
6. A hard stop at each stage's share (now a quarter over). (Y)
7. Estimates in the measured units above, replaced by real figures film by film. (Y)
8. At the brief: per new character a picture and up to three must-haves; 2-4 showstopper moments named; anything
   added after "go" gets a price first. (Y)
9. No sets trial: the next film's sets are the measurement, under the hard stop. (N to a trial)
10. The trial line-up is good enough at the shot's size, so the Glimpse tier stands. (Y)
11. Accept about 26% for a Remakes-sized film, 15% for a MidTerminal-sized one. Further cuts, both untested:
    (a) a Lead's poses judged in the rehearsal clips, not on a pose sheet; (b) the second hunt on Sonnet (0.2 a
    helper cheaper). (Y to the target; N to a and b until a film has shown the 26)

## For Claude
Sources: `notes/archive/remakes-handovers.md`, `notes/ledger/remakes*.json`, `notes/job-e-measurements.md`,
`.claude/hooks/costwatch.py` (prices). Start-up cost: about 90k tokens written at the 1-hour cache price plus 40-55k
of reading. Tools the proposals touch: `critique.py` (ranking, one listing per fault, `status` no longer blocked by
CAN'T TELL, check-back pass), `ledger.py estimate --stages` (tiers, hard stop), `guides/job-packs.md` Build order.
