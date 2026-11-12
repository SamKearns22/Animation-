# The system audit (started 12 Nov)

Written in plain language for Sam. Kept separate from any film: it has its own budget, not Blessed's.

## Why we're doing this
While getting Blessed ready, we found that several of the automatic checks that are meant to catch mistakes had
never been switched on for that film. Nobody asked Sam about it. Each chat wrote "still missing" in its notes and
passed it on to the next one. The checking tool still said "clean", because it only lists missed checks in small
print. Two earlier audits didn't notice. Like a car with some warning lights quietly unplugged, everything looked
fine on the dashboard.

## What we've changed already
- **A new line in the rulebook (rule 59):** no check can be left off, left half-built or put off until later without
  Sam saying yes. A check that hasn't been set up counts as a mistake that must be fixed before the first animatic.

## The quick look at the last five films (12 Nov)
This was the fast version of the checks, which reads the script and the plan but doesn't look at the pictures. So it
shows what was missing, not whether the films looked wrong.

- **Remakes:** told the checker it had no people and no rooms, so the checks for rooms, hands, outlines, clothes and
  who is in each shot didn't run. It does have a cast and painted sets, so this was probably wrong. The checks for
  people walking into things or popping in and out didn't run either.
- **Elder Scrolls: Swindon:** told the checker it had no rooms and no voices, so those checks didn't run. This one is
  probably right for that kind of film. One shot is 15 seconds long; the limit is 8.
- **Ad-Vanced Notice, Islamocommunism, MidTerminal:** none has an "acting list", the plan of what each person does
  on each line. The rulebook asks for one because it cuts down rounds of notes.
- **Islamocommunism** also: one shot has no camera written into the plan, and two places in a drawing have a missing
  outline.
- **Shots over 8 seconds:** Swindon (15 s), Islamocommunism (12 s), Ad-Vanced Notice (9 s), MidTerminal (8.2 s). We
  don't yet know if these were agreed with Sam.

## The jobs still to do (Sam said yes to all, 12 Nov)
1. **The full check on each of the five films.** This time it looks at every picture. It runs one film at a time,
   about 9 minutes each, and reports only. (Sonnet)
2. **Did it cost us notes?** For each mistake the full check finds, look through Sam's old notes on that film. If Sam
   pointed it out himself later, that's a round of notes the checks should have saved. (Opus, medium effort)
3. **Make the checker honest.** Change the checking tool so it can never say "clean" while any check was skipped,
   never set up, or switched off. Each skipped check becomes a mistake listed at the top. The tool also checks that
   what a film says it contains (people, rooms, voices, props) matches what it really draws. (Opus, high effort)
4. **The ten wider questions** (Sam: all yes):
   1. **"Allowed" lists:** films keep lists of mistakes marked "meant to be like that". Do they keep growing, and
      does each one still have a good reason?
   2. **Problems passed along:** how many "not fixed yet" items does each film carry from chat to chat, and for how
      long?
   3. **The fresh-eye critique:** it lets "can't tell" through. Has that ever hidden something Sam later noticed?
   4. **Checks that can't fail:** give each check a deliberately broken example and make sure it actually catches it.
   5. **The shortcut re-check:** after a small fix, the checker only re-checks the pictures that changed. Make sure
      it never misses one.
   6. **The cost record:** it was once corrected by hand. Are the cost numbers we plan budgets with correct?
   7. **Lost work:** there are over 120 side branches (separate copies of the work). Check that no finished work is
      stuck on one and never reached the main copy.
   8. **Rules checked by hand:** which rules have no automatic check, and which of those keep turning up in Sam's
      notes?
   9. **Chats starting chats:** make sure a chain of chats can't carry a skipped check forward with no one looking.
   10. **Notes that come back:** count the notes Sam had to give twice, across past films. They show which mistakes
       the system keeps letting through.

## Order and cost
Blessed comes first (its own budget). Then this job: jobs 1 and 2, then 3, then 4. Rough guess for the whole job:
about 3.5% of a week (the checking runs on Sonnet about 1%, reading old notes on Opus about 1%, fixing the checker on
Opus about 1.5%). It's a guess; the first chat measures it and says if it's heading higher.

## Where things stand
- **Sam (12 Nov, before sleeping): start now and see it through to the end, as long as it doesn't get in Blessed's way.
  It must end with a plain-language report on what this means for quality, cost and how we work.**
- **Keeping out of Blessed's way:** jobs 1, 2 and 4 only read and report, and each runs in its own chat (its own
  computer). Job 3 changes the checking tool that Blessed's chat is using right now, so it is built on its own branch,
  `claude/audit-honest-checker`, and only joins the main line AFTER notes/blessed.md says animatic 1 was sent (if not
  yet, it waits and says so in the report). Nothing in this job edits Blessed's files.
- **The chain (chain rule, CLAUDE.md "Models and chats"; each chat opens the next):**
  - **Chat A, Sonnet, medium:** job 1, the full check on the five films; writes the results per film below. Also
    gathers the facts for questions 6 (cost record) and 7 (lost work on side branches).
  - **Chat B, Opus, medium:** job 2 (did it cost notes?), and questions 1, 2, 3, 8 and 10 (reading lists and old notes).
  - **Chat C, Opus, high:** job 3 (make the checker honest, with its test), and questions 4, 5 and 9 (testing the checks).
  - **Chat D, Opus, medium:** the final report, `notes/system-audit-report.md`, in plain language: what we found, what
    it did to quality, what it did to cost, what changes in how we work, and anything Sam needs to decide (numbered,
    pick first). Sent in the chat, with a push notification.
- **Rules for the chain:** report only; fix nothing in the five films. Any new rule is PROPOSED in the report, never
  written (except the rule 59 wording Sam already said yes to). Stop and push-notify if the job passes about 5% of a
  week. Write every finding here, in plain words, as you go.
- **Results:** (each chat adds its findings below)

### Chat A (Sonnet, medium, 12 Nov): job 1, the full check on the five films, and the facts for questions 6 and 7
**How it was run:** `preflight.py FILM OUT --audit` (the full version: it draws every third frame and checks the hands
on every frame; `--audit` lists every fault instead of stopping at the first, and leaves no pass stamp, so nothing in the
repo changed). One film at a time, results in the scratchpad. Times: Remakes 2 min, Swindon 13 min, Ad-Vanced Notice
5 min, Islamocommunism 6 min, MidTerminal 2.5 min (about 29 min in all, faster than the 9 minutes each we planned for
the small ones, slower for Swindon). This chat's whole cost so far is about 0.4% of a week. No film file was changed.
**Note:** a fresh chat has none of the tools installed until `.claude/hooks/setup.sh` runs; the first try failed on a
missing library until it did. Also the clone was "shallow" (cut-down history), which made the side-branch counts
useless until it was fetched in full. Both are things a later chat needs to know.

**Remakes (17 faults).**
- The checker was told the film has no people and no rooms. So its checks for hands, outlines, clothes, facing, who is
  in each shot and the room plan **did not run at all**, though the film has a cast and painted sets. Still skipped.
- Collision and pop-in tests did not run either ("no scene(t)"). So again nobody has checked people walking into things.
- Found anyway: 8 times in the shot at 26-29 s, Malon and Saria "could not be drawn" turned 30 degrees (no turned view
  built); 5 faults where the recorded voice and the script disagree (line 4 Link is 1 word in 0.7 s; lines 5, 11, 13: the
  voice says more words than the script; one swear caption comes up 1.45 s before it is said); 3 captions go by too
  fast to read; an arm squashed to under half its length at 26.5 s.
- 5 other warnings: file is 1,693 lines (rule 61); no "rehearsal clips" line in the notes.

**Elder Scrolls: Swindon (1 fault).** The only fault: shot 6 (the roundabout) runs 15.2 s, limit 8. Told it has no rooms and no
voices, which is probably right for this film. Also no "famous faces" list, no rehearsal-clips line, file is 2,404 lines.
Cleanest of the five; whether the 15 s shot was agreed with Sam we can't tell from the tool.

**Ad-Vanced Notice (32 faults).** 27 are arms and hands: at 11-13 s on the cliff JD Vance's hand is drawn over his body
though it should be behind it (and once inside it); the driver's arm has a line where it meets the body; at 26.8 s Vance
points with a bent elbow so the finger aims at nothing; and 20 more of the same in the street and ending shots, mostly
ICE officers 1-3 with a line at the shoulder join, and officer 2 with a hand inside his own body three times. Also: 3
shots over the limit (cliff 11.3 s, gas 9.3 s, street 9.3 s), 2 captions too fast. Warnings: no acting list, Vance and
the "ground" voice have no head movement, no rehearsal-clips line, no MAP, 1,042 lines. The squashed-arm and folded-elbow
"allowed" lists show 111 + 31 uses of "elbow folded back across the body" in the street and ending.

**Islamocommunism (42 faults, the most).** Hands 8 (El-Sayed's hand is hidden for 7 s at 5-12 s; hands over a body part
at 15 s; AOC's hand over/behind/inside her body); 5 voice-and-script faults (subtitles come up 0.8-1.3 s late); 8 caption
faults (the longest caption is 10 words and flashes for 2.5 s); the room checks found 4 things: the Oval Office reference
photos `oval-1-desk-gold.jpg` and `oval-3-both-ends.jpg` are **missing from the references folder**, and the Oval Office
lists 7 things that make it recognisable and the White House 6 (rule: 8-10); one shot ("ext") has no camera in the plan;
2 checks "could not test" (the glass hand-over at 24.8 s and 27.4 s: the checker checked nothing there; this is the
tool saying so honestly); two figures drawn from one copy (El-Sayed twice, AOC twice: "same build, hair, clothes"); at
57-71 s AOC's glass is drawn over her back when she turns away; arms drop back to rest in the last 0.4 s before 2 cuts;
four 2.5 s stretches where a person does not move at all (19, 23, 60 s); edges with no outline on AOC; one shot 12.2 s.
Warnings: no acting list, no head movement for either speaker, no rehearsal clips line, no MAP, 1,015 lines.

**MidTerminal (20 faults).** 6 voice-and-script (Epstein line 9 is 11 script words but the voice says about 22: the take
and script don't match; line 7 and line 2, 10: words in one but not the other); 8 captions too fast or too long; hands 2
(Trump points with a bent elbow, finger aims off); 2 arms dropping back before a cut; Epstein twice from one copy; one
shot 8.2 s. 8 questions for Sam about sudden loud sound after silence at the cuts at 7, 12, 16.7, 27.9, 34, 39.5 and 53 s
(the sound jumps up 24 dB and 41 dB at two of them) and 2.8 s of dead silence; none has been asked. Warnings: no acting
list, three speakers with no head movement, no rehearsal clips line, no MAP.

**What the five have in common (for chat B and D):** all five say "no rehearsal clips line" (Remakes' skipped checks hid the rest); the four
that were checked on people and sets have no famous-faces list; three have no acting list; three have no MAP.
Hands are the biggest group of faults (37 of the 112 over the five films); 21 are captions too fast or too long.
"Could not test" was only printed by Islamocommunism's audit; for Remakes the checker said nothing about the skipped
checks being a problem. Each film's full list is in the scratchpad (`/tmp/claude-0/.../scratchpad/FILM/`), not kept in the
repo because they are test output.

**Question 6, the cost record: is it right?** Not reliable enough to plan a week with, by about 10-25%. What I found:
1. **The yardstick is a guess.** The cost watch turns tokens into dollars with prices "fitted to this account's chat
   records" and a week's allowance of $290, fitted to one weekend (7-9 Nov, "about $260 = 90%"). Its own comment says
   "good to about ±20%". It prices Sonnet, Opus and Fable all against the same $290, though the app may count them
   separately. So all percentages are ±20% to start with.
2. **The Remakes total is mostly a hand-typed lump.** Of Remakes' 48.85%, 43.0 is one line, "before": Sam's own figure
   from the app (45% on 11 Nov) with one chat taken off. The 7 automatic rows add up to only 5.85. So we know Remakes cost
   about 45-49%, not how it split across chats. The 60% in the budget job's table was "rebuilt from handovers, good to a
   few points each".
3. **The record can drop cost.** On the main line the Remakes chat `e5459ba8` is 1.03%; on the side branch
   `remakes-budget-optimization-pf1aj7` it is 1.73%. The 0.7 got lost when two copies of the file were merged on 12 Nov
   ("this chat's latest cost kept"). The chat's later cost was written only on the side branch.
4. **Small gaps by design.** The automatic record only rewrites a chat when its cost has moved by 0.25%, so each chat's
   last row can be up to 0.25% too low (a dozen chats: up to about 3 points).
5. **Missing records.** Ad-Vanced Notice, Islamocommunism and MidTerminal have no cost file at all (they predate it);
   Elder Scrolls: Swindon has one row of 0.18%, for a film that took many chats. Helpers' costs are counted only if
   their record sits in the chat's folder; the Link trial counted 2.0% against 1.12% in the ledger (two chats against one,
   helpers possibly on top).
6. Opus 5, Sonnet 5 and Fable 5 prices were "fitted" in Nov 2026; a price change would shift every figure silently.
**Fix to propose (chat D):** save each chat's cost at its end whatever it moved; when two ledgers are merged take the larger;
ask Sam for the app's weekly figure every Monday and re-fit the $290; label the percentages "about, ±20%".

**Question 7, finished work stuck on side branches.** There are 114 side branches besides the main line. After fetching full history, only **4
hold anything the main line lacks**; the other 110 are fully merged. The 4:
1. `inspiring-heisenberg-0vvyan` (8 Nov): a fix in the sitting kit so people standing up or sitting down use the new
   relaxed arm. **Not on the main line**: `source/sitting.py` still has the old arm at line 720. Small (12 lines). This
   is real work stuck.
2. `youtube-shorts-transfer-oa9q5q` (26 Oct): a "My accounts" section for CLAUDE.md (the CranbriJoos name, the TikTok
   address, YouTube Shorts as second platform, the profile picture to use). **Not on the main line.** Small but it is
   Sam's own information.
3. `remakes-budget-optimization-pf1aj7` (11 Nov): the 1.73% cost row above. Stuck.
4. `flying-whales-rig-build-d380r1` (1 Nov): an early version of the Jackdaw rig and its handover. The main line holds a
   later, bigger version of the same files (and the finished Flying Whales films), so this is superseded, not lost.
Nothing finished (no film or animation) is stuck. Nothing has been merged: this audit reports only; chat D should ask
Sam whether to take items 1-3 into the main line.
