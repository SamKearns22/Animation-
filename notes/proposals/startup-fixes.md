# Proposal: Startup fixes: the three measured start-up savings

Status: open

## Problem
Every chat reads the same text before it works, and pays for it again on every later step and in every new chat.
Sam chose (16 Nov, "proceed" on the startup-reading verdict, option 1) to measure first and then change one thing at a
time, each with its own yes and its own number. The measuring chat (chat 2) has now counted what five real chats read
at start-up and ranked it. Three items remain worth changing: the branch listing at the start of each chat, the film
notes read at the start, and CLAUDE.md itself. For each one, the job now is the safest way to make it cheaper that
keeps every rule, never lets a chat miss newer work on another branch or an open note of Sam's, and can be undone on
its own. CLAUDE.md is the riskiest: its rules were mostly written after something went wrong, so wording cut too far
may let an old fault return. Chat length, the app's own 72k and the number of chats are other jobs (Sam, 16 Nov).

## Facts
- The measured table: notes/proposals/startup-reading/learn.md (chat 2, Sonnet, 16 Nov). Sample of 5 of 9 readable
  Protest Tiers chats (0, 1, 4, 5, 7); Elder Swindon none readable. Tokens = characters / 2.35.
- Every chat starts at ~79.5k tokens before its first step; ~72k is the app's own. Repo-controlled start-up is
  ~13.5k a chat, ~4% of a week a film (32 chats). 1% of a week ~ $2.45; a 1k-token piece read at start costs ~$0.023 a
  chat on Opus (write once plus ~78 re-reads), $0.74 a film.
- Ranked (learn.md): CLAUDE.md 5,470 tokens a chat (1.6% a film); film notes read at start 3.6k mean (2.7k, 2.8k, 4.0k,
  4.9k; read in slices by sed/grep, one planning chat read the whole file) 1.1%; branch listing/checks 2.0k mean (1.2k,
  1.0k, 1.2k, 3.9k, ~2.6k) 0.6%; pack 0.5k 0.14%; handover.py/hook printouts ~0. The earlier verdict's notes cap was
  built on an assumed 10-13k of notes a chat; measured is 3.6k, so learn.md replaces it with a start-up printout idea
  worth ~2.5k a chat (~0.7%). The pack printout was dropped (chats read 0-1k of the pack).
- Branches (counted today, chat 3, 16 Nov): `git branch -r` lists 254 branches, 9,242 characters (~3.9k tokens).
  135 of them hold commits not on the main line, most 4+ days old, several showing ~1,500 commits (histories that were
  rewritten, not new work). Branches with a commit not on the main line from the last 1 / 2 / 3 days: 7 / 11 / 26.
  Of the 135, the ones touching CLAUDE.md, the hooks, handover.py or the proposal tool are all 4-5 days old.
- CLAUDE.md "Making the films": "At the start, list every branch (`git fetch --all; git branch -r`) and merge any newer
  work on the film or tool before building." The SessionStart hook (.claude/hooks/setup.sh) already fetches the main
  line and prints 3 lines when the copy is stale; it does not look at other branches.
- Film notes: "Where things stand" is 3,362 characters (~1.4k tokens) in notes/protest-tiers.md (lines 3-17), 1,438
  in notes/elder-swindon.md. The whole files: protest-tiers 4,531 words / 25,037 characters (~10.7k tokens),
  elder-swindon 5,965 words (both over the 4,000-word rule). handover.py `start --film NAME` today prints only faults
  and one line on how to look at code (source/handover.py, main()).
- CLAUDE.md (counted today): 12,857 characters, 129 non-empty lines, ~5.5k tokens; 10 dated tags like "(Sam, 13 Nov;
  was 8 in a row)", 3 "replaces/was" histories; rarely used sections (My accounts, TikTok finish command, reference
  photo search order). The rulebook guides/film-quality-rules.md has a last table listing the CLAUDE.md rules.
- The earlier verdict's guards for CLAUDE.md (startup-reading.md, "Final version", change 3): a check listing every
  rule sentence before and after (any missing refuses); a fresh helper answers 10 past situations with old and new
  CLAUDE.md and must match. Beat: ~5.5k to under 3.5k tokens, no rule lost.
- Sam's standing aims (CLAUDE.md "Rules are permanent"): high quality, fewer notes and faults, a film within 15% of a
  week; never trim the film or the joke; each change its own yes with a "Lost:" / "Added:" line.
- Cost of this route itself: two Opus helpers and one Opus judge, roughly 1-2% of a week; the honest ceiling of all
  three savings together is ~1.8% of a week a film (learn.md point 6), so the savings repay the route after one film.

## Record
notes/proposals/startup-reading/learn.md
notes/proposals/startup-reading.md
notes/proposals/startup-reading/chat.md
CLAUDE.md
.claude/hooks/setup.sh
source/handover.py
guides/job-packs.md
guides/film-quality-rules.md
notes/protest-tiers.md
notes/elder-swindon.md
notes/ledger/protest-tiers.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 94e3eea2f712120f -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V2 (helper B). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the Facts carry remedies, not only facts: learn.md's "start-up printout idea worth ~2.5k a chat", the earlier verdict's CLAUDE.md guards (sentence check, 10-situation helper) and its "under 3.5k tokens" beat, and the "~1,500 commits = rewritten histories" reading of the branches. V3 builds on all of them; V1 and V2 set them aside. The "rewritten histories" reading is also wrong (see Why).
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 3 | 3 | 4 | 18 |
| V2 | 5 | 4 | 4 | 4 | 4 | 21 |
| V3 | 2 | 2 | 4 | 2 | 4 | 14 |
## Sam test
Q1: Yes. An expert stops the mess where it starts (each chat's cost row being saved onto its own side branch) and gets the start-up tools to print what matters. They don't just shorten a list or the wording. The final version adds what V2 left out: a row-only push, and a filter that still works on the half-copied history a cloud chat gets.
Q2: The branch evidence covers all 254 branches (I checked it today: 24 of the 27 from the last 3 days hold only cost rows, and 3 hold real work). The notes and CLAUDE.md figures still come from 5 chats of one film. That is named, and the beat for each change is measured on the next film.
Q3: The root cause is in the code: ledger.py lines 207-209 push to `claude/chat-XXXX` "which the next chat's branch scan merges", and nobody does that scan in full. I checked 9 branches: 7 of them have cost rows that are missing from the main line. The start hook and `handover.py end` run in every chat, so nothing depends on a chat choosing to follow a rule. It worked if the next film ends with 0 missing rows and 0 unmerged real work, and if the start-up reading goes down.
Q4: Yes. Four approaches were weighed (wording only, fixing the source, a one-off branch delete, and learning first). Fixing the source is the best of them.
Q5: Four separate yeses, each undone on its own. No rule wording changes. The one-off row merge matches rows by chat ID (`sid`), so it never counts a chat twice.
Q6: The facts I relied on are checked: ledger.py lines, the setup.sh behaviour, the shallow copy, the branch census, the lost rows, job-packs line 32 and the 8 Nov duplicate build. Build costs and the size of the open notes are marked unchecked.
Q7: It is sized by the result, which is complete cost totals and no missed work, as well as fewer tokens. Its honest cost is about 2-3% of a week once. It saves about 1.2% a film.
Q8: Every change is permanent and is reviewed at the end-of-film review. The CLAUDE.md map is a read-only step that comes before its change; it is not a trial.
## Pick
V2
## Why
V2 is the only version that found the real loss: the automatic cost rows never reach the main line. The 24 bookkeeping branches are a side effect of that loss. Stopping it at the source makes the branch listing short for good. V1 found the same cause but treats the symptom: its start hook would merge bookkeeping branches in every chat, which means writes on every start. V1 also puts a census first that costs more than the notes change it gates. V3 misses the cause altogether. Its 8-line cap with a "last 2 days" window would today be filled by about 24 bookkeeping branches, so it could hide the 2-3 that hold real work. That is the exact fault the branch rule exists to stop. The problem file also misreads the branches: this copy is shallow (main-line history starts 11 Nov 17:35). 70 of the 79 branches more than 1,000 commits ahead were last changed before that date, so "rewritten histories" is mostly an artefact of the cut-off history.
Taken from V1: the shallow-copy finding, used for the filter (F2), and the `end` refusal while a listed branch is neither merged nor named. Taken from V3: the 10-situation check, but only for later rewording. Moving text word for word needs only the sentence check.
## Faults in the pick
- F1 [fixed] V2's ledger push sends the chat's whole HEAD to the main line, which would publish half-done work mid-chat. Fixed: the row goes in as its own commit on top of the newest main line, holding only the ledger files, with fetch and retry.
- F2 [fixed] V2's filter compares files with the main line, but in a shallow copy an old branch differs everywhere. Fixed: the filter uses each branch's own commits since a date and the files those commits touch, outside `notes/ledger/`.
- F3 [fixed] The one-off merge could count a chat twice, because app-imported rows hold the same chats under other IDs. Fixed: rows are matched on `sid`, across all branches, not only recent ones.
- F4 [named] The notes and CLAUDE.md savings come from 5 chats of one film (characters / 2.35), not from measured chats.
- F5 [named] Build costs are estimates (unchecked).
- F6 [named] Three stranded items need Sam's call: the slurp profile picture, the Blessed WIP and the 12 Nov audit branch.
## Final version
Four changes, asked as four numbered Y/Ns, in this order. Each is undone on its own.
1. **Cost rows reach the main line.** ledger.py writes each row as its own commit on top of the newest main line (fetch, commit only the ledger files, push, retry up to 3 times). It never pushes the chat's own HEAD. A one-off merge brings in the missing rows from every branch, matched on `sid` so no chat is counted twice. `ledger.py audit` reports missing rows. Beat: 0 missing at film end (today 7 of the 9 checked).
2. **Branch printout by the start hook.** setup.sh fetches the branch tips. It prints one line per branch that has commits from the last 7 days touching files outside `notes/ledger/`, with the age, the files and a count. It is filtered by each branch's own commits, so it works on a shallow copy. CLAUDE.md: "merge or name every branch the start lists" (the rule is unchanged). `handover.py end` re-scans with no filter and refuses while a listed branch is neither merged nor named in the notes. Beat: under 0.2k tokens a chat (from 2.0k), and zero real work missed. The first run lists the 3 stranded items for Sam.
3. **Notes printout.** `handover.py start --film` prints "Where things stand" and the unticked notes. carried() still checks the whole file. Beat: notes under 2.5k a chat (from 3.6k), and no rise in repeated notes or dropped asks next film.
4. **CLAUDE.md.** First a read-only Sonnet chat maps each sentence to its rule, its source fault and its date. Then text moves word for word: the dated tags go to the rulebook's last table, and My accounts, the photo search order and the TikTok command go to their packs, each leaving a one-line pointer. A check refuses the change if any old sentence is not found word for word. Beat: under 4.8k tokens, no sentence lost. Rewording is a later, separate proposal, and only where the map shows a duplicate, with the 10-situation test.
Saving: about 1.2% of a week a film, plus complete cost totals. Cost: about 2-3% of a week once (unchecked). Reviewed at film end.
## For Sam
### Option 1: Fix the cause, then trim
Each chat's cost record is saved on a side branch and mostly never brought back (7 of 9 checked are missing). That is why the list of branches each chat reads at the start is 254 long. This option sends cost records straight to the main copy, then has the start-up tool print only the few branches holding real work. Then each chat gets a short printout of the film's open notes and status. Last, rarely used parts of CLAUDE.md move word for word into the guides that use them. Four separate yeses. You'd notice complete cost totals and one question about 3 stranded items (the slurp picture, the Blessed draft, the audit branch).
Lost: the full branch list at start (one command away), and dates and rare sections in the always-read file (kept in the rulebook and guides).
Added: a cost-saving fix, a short branch printout with an end check, a notes printout, a word-for-word check, and one mapping chat.
### Option 2: Count first, then change
A cheaper first step: one chat counts every branch on a full copy and records which notes lines and rules chats actually use. Then the start-up tool tidies the bookkeeping branches each time a chat starts, and the notes and CLAUDE.md changes go ahead only if the count shows they're worth it. Safer on paper, but it costs a counting chat and leaves the cost records leaking until the tidy-up runs.
Lost: the full branch list at start, and about 0.5k of non-rule text in the always-read file.
Added: a counting chat, an automatic tidy-up at every start, and an end check.
