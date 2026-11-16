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
