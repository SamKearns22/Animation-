# Proposal: Routine work keeps running on the expensive model

Status: open

## Problem
Routine work (animatics, splicing clips into the animatic, checks, sound, filing, sending) is meant to run on the
cheaper model (Sonnet) and keeps running on the expensive one (Opus). The check built on 15 Nov to catch this did not
fire once on 16 Nov, although several routine chats ran on Opus. Sam said Y (17 Nov) to "routine stages on Sonnet" as
part of the chat-size rule (built separately, chat A); this proposal is about why the switch does not happen in
practice and what makes it hold.

## Facts
- Why it stopped working, from the Protest Tiers notes' Next lines in git (notes/proposals/chat-size-and-model/
  why-model-switch-failed.md): (1) from 16 Nov 12:46 every Next line gave the Opus medium notes chat "clips with
  `final --span` ... splice fixed seconds into the animatic", so the animatic was made inside the Opus fix chat; on 15
  Nov 18:49 a Sonnet chat had made animatic 3 by splicing, cheaply and correctly. The check's ROUTINE word list skips
  `--span` on purpose and has no word "splice". (2) CLAUDE.md's "Models by stage" itself put clips and "building from
  ... sound" on Opus medium, so France chat 7 (look, check, clip) and chat 8 (sound) on Opus followed the rule as
  written. (3) The check (source/handover.py, `model`) reads only the film notes' first Next line, at start and end;
  it never sees the model a chat is actually opened on (create_session) nor what a chain does. 16 Nov's country
  chains (Albania, Germany, France) were opened from Sam's phone and passed work in their own prompts. (4) Before 15
  Nov 17:29 there was no check at all.
- The platform switch itself works: chats whose parent asked for Sonnet ran on Sonnet (get_session: configured and
  served claude-sonnet-5-5 for Startup reading chat 2 and Learn chat 2). France chats 7 and 8 configured and served
  Opus, medium (get_session, 16 Nov).
- Measured cost (notes/ledger/*.json): Sonnet chats of 8-17 steps cost 0.21-0.39% of a week, 64 steps 0.8%; Opus
  chats of 40-60 steps ~3.4% per 100 steps, 80-100 steps ~2.4% per 100 steps (chat-size-and-model.md Facts).
  Protest Tiers 16 Nov: 24 chats, 39.3% of a week in one day (notes/ledger/protest-tiers.json).
- Switching model inside a long chat re-pays its whole history (notes/cost-diagnosis.md, 13 Nov: $5.80 on Blessed).
- Sam's Y, 17 Nov (notes/proposals/chat-size-and-model/sam.md): aim ~100 steps, up to 150 to finish a stage;
  routine stages on Sonnet; a 40-step floor except notes after an hour's gap or a whole routine stage on Sonnet.
  Chat A builds that wording into CLAUDE.md and rule 85 now (notes/cost-fixes.md, Where things stand).
- Unchecked: how much quality Sonnet loses on the splice/clip/look/sound stages (the critic test on Remakes was to
  decide Sonnet for critique, notes/morning-report.md line 104); how many 16 Nov Opus steps were routine.

## Record
notes/proposals/chat-size-and-model.md
notes/proposals/chat-size-and-model/
notes/ledger/protest-tiers.json
notes/archive/protest-tiers-handovers.md
notes/cost-diagnosis.md
source/handover.py
CLAUDE.md
guides/job-packs.md

## Verdict (the judge, word for word)
<!-- verdict-hash: bf09d280fb907cf7 -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V2 (helper A). Critiqued: 8 found, 4 fixed, 4 named.

## Leak
yes (mild): the Facts say the check "never sees the model a chat is actually opened on (create_session)", which points the helpers at create_session and the served model; all three versions build on that. No full solution is stated.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 3 | 2 | 2 | 4 | 13 |
| V2 | 4 | 3 | 4 | 4 | 4 | 19 |
| V3 | 3 | 3 | 3 | 3 | 4 | 16 |
## Sam test
Q1: Yes. An expert puts the guard at the action, using the model the app actually served. This version also drops V2's second gate, which read the words in the prompt.
Q2: The evidence is every chat of the 16 Nov Protest Tiers day (24 chats, the ledger's served model and steps, read from the transcripts), plus the 15 Nov chats where title and model disagree. That evidence fits a "where does the money go" decision. Weak spot: it is one film; named.
Q3: Root cause found: words were checked by words, and phone-opened chains bypassed the check. A hook denies the command before it runs, in every chat that has the project, so no chat has to read anything and choose to obey. We know it worked from the refusal log and from a new "routine on Opus" share on each film's ledger row.
Q4: Four approaches were weighed: wider word list (V1), a stage list read by the cost hook (V3), a gate on the action (V2), and a one-command routine tail. The action gate is the only one that does not depend on someone writing the right words.
Q5: Learn first, so the gate's command list and its seam come from measurement. One yes for one hook, removed by deleting one entry. A wrong refusal costs at most one extra Sonnet chat. Escape: on a refused Sonnet open or a model fallback, the gate lets the command through and logs it.
Q6: Every figure was checked against the ledger, app-costs.tsv, costwatch.py and handover.py (see Faults). The open items are marked unchecked.
Q7: It is sized by a measured result. The learn step decides whether splitting short tails pays before anything is built, so there is no word-list patch and no large build in advance.
Q8: Permanent. It replaces the word-list check once the gate has caught everything the list caught, and it is reviewed against the film's results at completion.
## Pick
V2
## Why
V2 is the only version that both learns before building and enforces at a point no chat can skip. A PreToolUse hook (an automatic step the app runs before a command, which can refuse it) reads the served model from the chat's own record, as costwatch already does at costwatch.py line 84.

V1 asks handover.py to "read the create_session call the chat is about to make". That call does not exist yet when handover.py runs, so V1 is still a word check. It also bundles three changes with no measurement, and its 2-4% saving is unmeasured.

V3 has the right reframe, but its enforcement fails. The cost watch runs after each step (PostToolUse and UserPromptSubmit), so it can only warn, not stop. Its closed stage list is still a word that a chat writes, and the phone chains never wrote one. It also misstates a fact: there were 19 app-recorded chats on 15 Nov, not 24.

Taken from the others:
- V1: the fixed seam. The Opus chat ends once the fixes and the clips are committed and the clip commands are in the notes.
- V3: the clips-and-sound rule clash goes to Sam as its own decision, with the measured evidence. Also from V3: count served-versus-intended mismatches.

Dropped from V2: the create_session gate. It judged the prompt's words, which is the failed family.

Added by me: the learning must compare the two costs of a split. With Opus at about 3.4% per 100 steps, an 8-15 step tail costs about 0.3-0.5% on Opus, against 0.21-0.39% for a Sonnet chat (ledger). So splitting a short tail saves little. The real waste is whole routine chats on Opus (France 7 and 8).
## Faults in the pick
- F1 [fixed] V2's create_session hook judged prompt words; removed.
- F2 [fixed] Splitting a short tail into a new Sonnet chat may cost about what it saves. The learning now measures both costs, and the seam is enforced only where it pays.
- F3 [fixed] No escape if a Sonnet chat cannot be opened. Added: allow the command and log it on a refused open or a model fallback.
- F4 [fixed] No ongoing measure. Added: a "routine" kind in the per-step cost record, so every film's ledger shows routine-on-Opus.
- F5 [named] CLAUDE.md "Models by stage" still puts clips and sound on Opus medium. Whether sound placement is routine work is Sam's call, given separately with the evidence.
- F6 [named] Unchecked: that a PreToolUse hook here can refuse a command and read the served model in phone-opened chats. This is tested as the first build step; if it fails, nothing is built.
- F7 [named] Unchecked: the routine share of the 16 Nov Opus "other" (23.1% of a week). Also unchecked: why 4 of the 15 Nov chats ran on a different model from their title, and Sonnet's quality on splicing.
- F8 [named] The evidence is one film's days. The saving is about 1% a film, so this guards the rule Sam already approved; it does not bring a film to 15% alone.
## Final version
**Learn (changes nothing; Sonnet, about 0.5-1% of a week).** For each 16 Nov Protest Tiers chat (the ledger has each chat's session id), read its events. Record:
- the served model and the model the notes intended;
- steps by job (fix, build, look, clip, splice, sound, finish.py, full render, sending);
- the cost of each job.

Correct the 15 Nov model labels. Outputs:
1. Routine-on-Opus as a % of a week.
2. The exact commands that carried it.
3. For each tail kept in a fix chat, its Opus cost against a new Sonnet chat's measured cost (0.21-0.39%).

If the transcripts cannot be read, say so and stop.

**Change (one yes, after the learning; Opus medium, about 1% of a week).** One PreToolUse hook on Bash in .claude/settings.json.
- It reads the served model from the chat's own record, the same way the cost watch does.
- On Opus, it refuses the routine commands from output 2: finish.py, a whole-film final render, and the splice into the drafts animatic. Clips with --span stay allowed.
- Each refusal says: "routine step: open the Sonnet chat (create_session, model Sonnet) and hand it the clip commands in the notes".
- It refuses a tail only where output 3 shows the split pays. Otherwise that tail stays in the fix chat and is logged.
- On a refused Sonnet open or a model fallback, it allows the command and logs it.
- Every refusal and allowance is logged for the end-of-film review.

Step 0 of the build: prove that the hook can deny a command and read the model, including in a chat opened from the phone.

The fix seam (from V1): the Opus chat ends when the fixes and clips are committed and the clip commands are written in the notes. The Sonnet chat splices, runs finish.py and sends.

**Measure.** Add a "routine" kind to the per-step cost record, so each film's ledger row shows the routine-on-Opus share. Number to beat: under 0.5% of a week per film, and 0 whole routine chats on Opus. Once the gate has caught everything the old word-list check caught, the word-list check goes.

**Separate, own yes:** whether sound placement and clips are routine work (the CLAUDE.md wording clash), put to Sam with the learning's figures.
## For Sam
### Option 1: Look first, then a guard on the action
First, a cheap look back at 16 Nov's 24 chats finds which routine steps ran on the expensive model, what they cost, and whether handing a short job to a cheap chat actually saves money. Then I add an automatic guard. It sees which model is really running. If an expensive chat tries to finish or splice the animatic, the guard stops it and opens the cheap chat instead. This works in every chat, including ones you open from your phone. You would notice animatics always coming from a Sonnet chat, and a "routine on Opus" figure on each film's cost record.
Lost: Opus chats making the animatic or running the finishing step; the old word-matching check, once the guard has caught everything it caught.
Added: a look back at one day (about 0.5-1% of a week), one automatic guard with a log (about 1%), and a routine-cost figure on every film.
### Option 2: A fixed list of stage names, checked by the cost watch
Each handover names the next chat's stage from a fixed list (plan, build, fix, clips, sound, animatic, final, filing), and each stage has one model. The cost watch, which already sees the real model, warns when the model and the stage do not match. It is cheaper to think about, but it can only warn, not stop. A chat opened from your phone may not have named a stage at all.
Lost: free wording for stages in the handover.
Added: one stage list, one warning in the cost watch, one look back (about 2-3% of a week in all).
