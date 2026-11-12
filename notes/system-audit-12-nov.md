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

### Chat B (Opus, medium, 12 Nov): job 2 (did it cost notes?) and questions 1, 2, 3, 8, 10
Read only: each film's notes table and handovers, the "allowed" lists in each film's code, the critique records and
the rulebook. Nothing changed but this file. This chat cost about 0.7% of a week (audit so far about 1.1%).

**First, two corrections to chat A's list.** (a) "No acting list" is wrong for Ad-Vanced Notice and Islamocommunism:
both have one, in their notes, which had moved to `notes/archive/` when the films were posted (Ad-Vanced's code even
says where). The checker only looks in `notes/FILM.md`, so for every posted film it cries "missing". A false alarm, but
one that teaches us to ignore the checker: chat C should make it look in the archive too. MidTerminal really has none
(it predates the rule). (b) Several of chat A's faults were **told to Sam at the time and he accepted them**: Swindon's
15 s shot (his own note 52: "hold the aerial view 5 s more"), Islamocommunism's 12 s close-up ("chosen"), its three quick
subtitles and its desk-arm and phone-hand faults, MidTerminal's voice/script mismatches (his own takes; he chose the
subtitle wording in notes 46, 49, 50) and its 8.2 s Epstein shot, Ad-Vanced's two long shots (named with animatic 2).
These are not misses.

**Job 2: did the faults cost Sam rounds of notes?** Yes, on three of the five films, and mostly hands and arms.
- **Ad-Vanced Notice: the costliest.** Chat A's biggest group (hand drawn over or inside a body; a line where the arm
  meets the shoulder) is exactly what Sam spent **six notes** on: Vance's arm "punches through the guy's chest" (notes 34
  and 36b, "how do you not see it"), the arm "a separate piece laid over the shoulders" (37c), the shoulder hump (40),
  "a few pixels of non-connection" (41a), plus 14 (join the arms to the shoulders, all films). The hand check now catches
  all of these, and it still finds 27 of them in the finished film: so the check came after the notes, and the film
  went out with more of the same on the ICE officers that Sam never pointed at. Also the pointing finger (37e, 39b) and
  the bent-elbow point chat A found at 26.8 s. **About 8 of Sam's notes, roughly 3 rounds.**
- **Islamocommunism: 3-4 notes.** Chat A: El-Sayed's hand hidden for 7 s at 5-12 s. Sam: "free arm forward, resting on
  the desk" (11), "his hand goes into the table and disappears" (16), "two hands, handset vanished" (19). And the glass
  that "jumped" to the wrong hand (note 9): the touch check had said "not in the scene", which the chat took as
  paperwork. That is the same "could not test" chat A found at 24.8 and 27.4 s. (It was fixed: the tool now says
  COULD NOT TEST, 7 Nov.)
- **Remakes: about 6 notes, all in the checks that were switched off.** The film told the checker "no people" (the
  code says why: its cast is custom-drawn, not the standard kit), so the touch, collision, pop-in and room checks never
  ran. Sam then gave: the wings "don't make accurate contact with the neck" (34) and the wings across Link's chest (37c),
  both touch-check faults; "townsfolk stood in the house walls" (68), a collision/room fault; "the lower-left man appears
  like a wipe, not a run in" (77), a pop-in fault; the tower man's boots poking under his box (76). Bleep and subtitle
  timing (43, 51, 69) match chat A's voice and caption faults.
- **MidTerminal: 1-2 notes.** "The cut comes too soon, Satan speaks under the old subtitle" (36) is a caption-timing
  fault; "a pointing finger whenever anyone points" (33) is near the bent-elbow point chat A found. Sam never mentioned
  the sudden loud jumps at the cuts; nobody asked him.
- **Swindon: none.**
- **In all: about 18-20 of Sam's notes (roughly 6 rounds) were things a check catches today.** Most were in films made
  before the check existed; Remakes' were after, with the check switched off. That is the real cost of a skipped check.

**Question 1: "allowed" lists.** They are **not growing**: each film has 4-17 entries (Prepper 17, Patriots 3 about 26
counting its turned-view list, Ad-Vanced 16, Remakes 11, Blessed 10, MidTerminal 8, Islamocommunism and Swindon 4-5),
and the newer films have fewer. Almost every entry gives a reason and many say "looked at full size, date". Three
weak spots: (1) some cover **the whole film** (Ad-Vanced: officers may touch the man and each other "0 to 99 s"; the
driver's fist "to the end"), so a new fault in that window would pass unseen; (2) a few have no reason at all
(Islamocommunism's two contacts, Poker-mon's two line exceptions); (3) the biggest "allowance" is not a list at all but
**a film saying it has no people or no rooms** (Remakes), which switches off whole checks with one word and no question
to Sam. Rule 59 now covers (3); chat C's honest checker should list every switched-off check at the top.

**Question 2: problems passed along.** Old films almost never wrote "still to do" and carried it on (a handful of
"held" notes, all done before the final). The one real case is **Blessed**: the missing checks (set feet, collision
scenes, line subjects) were written as "still to do" from 11 Nov 22:33 and passed through at least four handovers and
about 7 hours before chat 2 stopped on them at 05:50 (which is how this audit began). Remakes carried "watch and listen
to the animatic before sending" (note 40) as "part done" for a day. Patriots 3 carried "reference photos still
missing" for two handovers. So the habit is new and rare, but when it happens nothing stops it: the handover just copies
the line forward.

**Question 3: the fresh-eye critique's "can't tell".** **Yes, once clearly.** On Remakes round 3 the critique answered
"can't tell" 45 and 65 times, nearly all on the movement lines (M1 "nothing pops in or jumps", M2 "moves take a natural
time"), because it was shown still strips, not moving pictures. Sam then gave note 77, "the man appears like a wipe,
not a run in": an M1 fault, the very line it couldn't tell. It may also have hidden note 70 (the kneeling man tipping
up). The critique did see the dangling boot (note 76) as a fault, but the fix was judged on a sheet where the tower
was too small. Blessed's first pass had 18 "can't tell". The trial on 11 Nov treated "can't tell" as "act only if a look
shows a real fault": when movement can't be judged from stills, that means it is never acted on. Fix to propose: a
"can't tell" on a movement line needs a short clip looked at before the critique counts as clean.

**Question 8: rules checked only by hand.** 16 of about 90 rules: 11 (composition sheet), 28 (catalogue updated), 30
(seen-before mark), 32 (falling pieces), 47 (splicing small fixes), 59/67 parts, 72 (no arm behind wings or cape; turns
snap: critique only), 77 (Sam confirms beard), 86 (tool estimates), 87, 88, S4 (joins at 24 fps), and most of the
"working with Sam" rules. The ones that **keep turning up in Sam's notes:**
- **Rule 72's "a turn snaps"**: Sam on Ad-Vanced (41b), again on Remakes (67, 74: "why it came back: it was only ever a
  film note"). Critique only, no tool.
- **Rule 30, "seen before" means a check is missing, add it**: by hand, and Ad-Vanced shows it not working (below).
- **Rule 76/77, check every reference, beards**: Islamocommunism's beard took 3 rounds, Ad-Vanced's 4 (notes 1, 4, 6, 7).
  The beard tool came after; Sam's confirm step is still by hand.
- **Rule 32, falling pieces**: Ad-Vanced debris (29), Prepper's crossbow "flat 2D line in mid-air" (50).
- **"Too still"** (no head, eye or arm movement) is checked by a tool only for speakers' heads; Sam's notes on stillness
  come up on almost every film (Ad-Vanced 42f, MidTerminal 35 and 40, Islamocommunism 15, Remakes 44, 54, 57).

**Question 10: notes Sam gave twice.** The "seen before" mark is used properly only from Ad-Vanced Notice (7 Nov) on.
- **Ad-Vanced Notice: 19 of about 72 notes were seen before (1 in 4).** Six rounds on one arm over the driver (32, 34,
  36b, 37c, 40, 41a), five on the man on the ground's arms (55-59a), four on the beard (1, 4, 6, 7), three on the
  driver's neck (36c, 37a, 38), two on the pointing finger (37e, 39b), elbows (16, 17, 18).
- **Remakes: 4 marked seen before**, two of them Sam changing his mind (fair), two real (the turn snap; the gunman).
- **Earlier films:** MidTerminal 1 (the skull, note 30 "repeat of 27/28"), Patriots 4 2 ("REPEAT" notes 18, 33),
  Islamocommunism 1 (beard round 3, which became rule 76).
- **Across films, the same kinds come back:** arms and hands through or over bodies (Ad-Vanced, Islamocommunism,
  Remakes), the pointing finger (MidTerminal 33, then Ad-Vanced 37e and 39b, then rule 41), turns that swivel instead of
  snap (Ad-Vanced, Remakes), beards (Islamocommunism, Ad-Vanced), people too still (five films).
- **Why:** the fix was judged by what was meant, not against Sam's picture at full size (Ad-Vanced 36b says so in its
  own words), and the check that would have caught it was added only after the second or third note.

**For chat D (proposals, none written):** (1) the checker reads archived notes, so posted films stop failing "no acting
list"; (2) no "allowed" entry may cover a whole film or have no reason; (3) a handover line saying "still to do" for a
check stops the chain and asks Sam (rule 59's check for chains, which is chat C's question 9); (4) "can't tell" on a
movement line means a clip is looked at before the critique is clean; (5) a "seen before" note gets its check built in
the same round, before the fix is sent (rule 30 made a check, not a by-hand promise); (6) a "too still" check for every
person on screen, not only speakers' heads.

### Chat C (Opus, high, 12 Nov): job 3 (the honest checker) and questions 4, 5, 9
Built on its own branch, `claude/audit-honest-checker`. **It has NOT joined the main line:** notes/blessed.md does not
yet say animatic 1 was sent (Blessed is waiting on Sam's Y to fix its 17 faults), so the new checker waits, as planned.
The first chat after animatic 1 is sent merges that branch (one command; nothing in it touches Blessed's files). This
chat cost about 1.6% of a week (audit so far about 2.7%). Nothing in the five films was changed.

**Job 3: the honest checker. Done, with its test.** What changes when it joins:
- **Every check that does not run is a fault, listed first** ("NOT RUN: ..."), whether the film's list of what it
  contains left it out, it was never set up, or it was switched off. The summary can no longer say "clean" while any
  check is off. The only way to leave one off is a line in the film's code recording **Sam's yes with a date**; even
  then it is printed at the top of every run, and the word "clean" is replaced by "no faults found, but N checks did
  not run (Sam's yes)".
- **The render refuses** while any check has not run, and "every fault was named to Sam" no longer gets past it:
  only setting the check up, or Sam's recorded yes, does.
- **It checks what a film says it contains against what it really has:** a film that says "no people" but names a
  cast for its shots, lists famous faces, or has people drawn on screen is a fault; the same for rooms (a sets file
  or rooms in its plan), voices (script lines), props and effects. Sam's yes does not excuse this one.
- **The quick run on the six films:** Remakes now shows **13 checks that never ran**, and the two false claims ("no
  people" though its shots name a cast; "no rooms" though it draws sets). Swindon 6 (rooms, voices and captions left
  out, probably right for that film but now needing Sam's yes; famous faces never set up). Ad-Vanced Notice and
  MidTerminal 2, Islamocommunism 2 (all three: the new "people walking through the set" check and the famous-faces
  list were never set up). **Blessed: none** (chat 3 set them all up).
- **Chat B's "no acting list" false alarm, corrected diagnosis:** the checker did already look in the archive. The real
  cause was the heading: those two films' lists are under "## Acting (rule 74 ...)", and the checker only knew "acting
  list". It now reads any "Acting" section, in the notes and the archive. Ad-Vanced and Islamocommunism now pass;
  MidTerminal still (rightly) has none.
- **A second hidden hole, found while testing:** in the "list every fault" mode chat A used, **arm faults that would
  stop a normal run were only written in the small print and not counted.** They now count (MidTerminal: 23 faults,
  not 20: 2 checks never run, 1 arm). So chat A's totals were a little low.
- **A third:** the collision test's **pop-in check went silent** when it could not read a film's camera (nothing
  counted as "inside the frame", so nothing could ever pop). It now says "COULD NOT TEST pop-ins" instead.

**Question 4: checks that can't fail.** A new test file feeds each check a deliberately broken film. **All 33 broken
films are caught** (overlapping rooms, a missing reference, the Hook Text over a face, a missing cast member, a 9.5 s
shot, a blank brief row, no composition sheet, no acting list, a still-headed speaker, people standing in each other,
someone popping in, a head teleporting, a drawing-order flip, a bullet hole in mid-air, a door with no angles, and the
honest-checker cases). One check **failed** its first broken example: the pop-in test with an unreadable camera (above;
now fixed). 15 more checks were already proven by the older test file (hands, held props, facing, poses, copies, cut
rests, famous faces, eyes, subtitles, bleeps, the Hook Text plan, figures moving in the set, the render lock). **9 checks
still have no broken example**, because breaking them needs real drawings or recordings: line work, clothes, real
sizes, the effects checks, the body audit (in pieces, frozen), script against voice, song joins, resting arms, and
doorways showing the space beyond. The test prints this list every run so it can't be forgotten.

**Question 5: the shortcut re-check.** It can miss, in two ways, both fixed on the branch:
1. **A change to check code it didn't know about.** It only trusts an old clean run if the check code is unchanged,
   but it watched a fixed list of 23 files, and several checking files were missing from it (the turned-heads check,
   the set check, the pose gallery and others). It now records every shared file it actually used, and any change to
   any of them forces the full check.
2. **An arm dropping to rest just before a cut.** That check needs the second before the drop, but the shortcut only
   redrew a quarter-second round each changed picture, so if a fix changed only the last frames of a shot, the drop
   went unseen. It now also redraws the last 1.5 s of any shot that holds a changed picture.
Checked and fine: everything else either redraws whole bodies or works frame by frame; the fingerprints are exact (any
one-pixel change counts); a run that found any fault, a changed allowed-list, a changed length or speed all force the
full check. One harmless quirk: on a shortcut run the famous-face size check can raise a false alarm (never a miss).

**Question 9: can a chain of chats carry a skipped check forward with no one looking?** **Today, yes; once the honest
checker joins, mostly no.** Why yes today: the old checker printed skipped checks in one small line, said "clean", and
a render needed only "every fault named to Sam", which a chat says itself. That is exactly how Blessed's checks went
"still missing" through four handovers. Once the branch joins: a skipped check is a fault at the top of every run, the
render refuses it even "named", and the pass stamp is never shared between chats (each chat must run the check again
itself), so it cannot be inherited. The chain rule (anything needing Sam's yes stops the chain) then stops it, since
leaving a check off needs his yes. **Three holes remain (proposals for chat D, none written):**
1. A chat could write "Sam, 12 Nov: yes" into the film's code itself. Proposal: each "off with Sam's yes" line names
   the note or message number where he said it, the checker looks for that line in the film's notes, and the check
   sheet shows every "off" line to Sam before each animatic.
2. **Swindon has a "--no-lock" switch** in its code (Sam, 8 Nov: "Skip the checks"), which renders with no checks at
   all; any later chat on that film can use it. Proposal: such a yes covers one render, not every render after it.
3. Until the branch joins, the old checker is live; the Blessed chats are running on it now.

### Chat D (Opus, medium, 12 Nov): the final report
Written: `notes/system-audit-report.md` (findings, quality, cost, how we work, 11 numbered decisions). This chat about
0.3%; the audit in all about 3.0% of a week (±20%), under the 3.5% planned. Open: Sam's numbers 1-11; the honest
checker merges after Blessed's animatic 1 is sent.

## Sam's answers to the report (12 Nov): Y to all 1-11; 10 = leave it; 11 = NOW, not after Blessed
Done in chat D: (1) the accounts details are in CLAUDE.md; the lost Remakes cost (1.03 to 1.73) is back in its ledger;
the sitting arm fix is on `claude/audit-honest-checker` (it changes the figure kit, so it joins with the checker, after
Blessed's animatic 1). (10) left alone.
**The build job (chat E, Opus high, ALL on branch `claude/audit-honest-checker`, nothing on the main line, no Blessed
file touched; about 3-4% of a week; stop and push-notify Sam past 4.5%):** write each yes as a rule WITH its check,
merging or replacing an old rule so the rulebook does not grow:
- [ ] 2 every "off with Sam's yes" line names the note/message where he said it; the checker finds that line in the
      film's notes; the check sheet lists every "off" line before each animatic.
- [ ] 3 a yes to skip checks covers one render only (Swindon's --no-lock becomes one-use).
- [ ] 4 cost record: each chat's cost saved at its end whatever it moved; merging two ledgers keeps the larger; a
      Monday question to Sam for the app's weekly figure, re-fit the allowance; percentages labelled "about, ±20%".
- [ ] 5 no "allowed" entry may cover a whole film or lack a reason (a check).
- [ ] 6 a handover line saying a check is "still to do" stops the chain and asks Sam.
- [ ] 7 a "can't tell" on a movement line needs a short clip looked at before the critique is clean.
- [ ] 8 a "seen before" note gets its check built in the same round, before the fix is sent.
- [ ] 9 a "too still" check for every person on screen (not only speakers' heads).
- [ ] 11 broken examples for the 9 unproven checks (line work, clothes, real sizes, effects, the body audit, script
      against voice, song joins, resting arms, doorways).
Then run the kit tests and the quick check on the six films (report only), write results here, and hand over.
