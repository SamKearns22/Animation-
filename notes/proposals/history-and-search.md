# Proposal: Every step re-reads the whole chat, and a third of a film chat's steps are spent finding code by hand

Status: open

## Problem
Sam's aim (15 Nov): cut the cost of every stage of production as far as possible without harming quality. Most of
a film chat's money is not the work itself: every step (even an `ls`) re-reads the whole chat so far, so a chat's
cost grows with how long it runs and how much it pulls into its history, and film chats routinely end at 200-300k
tokens of history. A large share of those steps, and of what they pull in, is finding code by hand (greps, sed
ranges, whole-file reads) in film files and tools. The code finder Sam said yes to on 15 Nov, and the line telling
round chats to use it, have not changed that: in the chats that could be checked it was run 0 times. Quality must not
fall, every film is new (no content reuse), and Sam cannot code, so anything that only works if a chat remembers to
do it has already been shown to fail. The question is which change, to which rule, tool, check or way of running
chats, would cut this cost the most at the lowest risk.

## Facts
- Where an Opus chat's money goes (notes/cost-diagnosis.md "Job A results", 13 Nov; 36 Opus chats, $176, prices fitted
  to the app's figures): re-reading history 49%, writing new history 27%, output 22%. 26 of 36 ended at 200k+
  history and cost $158 of the $176; the 10 under 200k cost $18.
- Per action (notes/cost-diagnosis.md "Job B results"): each action re-reads the whole history; at 215k about 4.7
  cents before it does anything, at 400k about 9 cents. A median Opus film chat is ~78 actions ending ~220k, ~$5.6:
  the app's own ~80k re-read on every action ~25%; start-up reading ~15%; work history (code reads, printouts,
  pictures; 0.5-1.6k per action) ~25%; output ~20%; writes the rest. Most actions add under 2k but pay the full re-read.
- A model change or a long pause inside a chat re-pays the whole history at the write price (cost-diagnosis Job B:
  a switch to Sonnet at 364k cost $1.43; one fallback action at 414k $4.37; costwatch.py: after an hour idle).
- Code searching (notes/proposals/learn/code-search-count.md, counted from 7 chats' own records): 169 of 564 steps
  (30%) were hand code searches (Grep, Read of source/*.py, grep/sed/awk/head on .py), 16-36% per chat; page.py run 0
  times. Six were Blessed chats of 12-13 Nov (before page.py existed: the baseline). The one readable chat after
  page.py was built (Protest Tiers cast chat 5, 14 Nov evening, 2.59% of a week) searched by hand 18 times of 58
  steps, page.py 0. Protest Tiers chats 29 and 31 (15 Nov, other account, unchecked here): 0 runs, 25 and 26 hand
  searches (notes/proposal-route.md). Share of COST (not steps) spent on searching: unchecked.
- What exists now: source/page.py (`FILM show "note words"`: the note's words -> ~40 numbered lines of the functions
  it touches; `find`; a page of every def per film file, about a tenth of the code's words, Blessed 6.7k tokens vs
  ~60k). Rule 61 (guides/film-quality-rules.md) and guides/job-packs.md "Notes round" name it as the one look per
  note ("no greps or sed ranges on film files first"); `handover.py start` prints the same line. None of these
  enforces it; nothing records whether it was used. Whether `show` was used by any chat since Sam's Y on 15 Nov:
  unchecked (those chats are on the other account). Shared tools (source/*.py, not film files) have MAPs in their
  headers (rule 61 is about film files); whether page.py covers tools: it does not (it globs source/FILM*.py).
- Chat sizes: Protest Tiers chats 0-8 ended at 90-300k history (notes/proposals/learn/protest-tiers-costs.md);
  chats 9-32 unchecked. Opus film chats cost 1.3-3.2% of a week each; per-chat cost did not fall after the 13 Nov
  fixes; Protest Tiers took 33 chats, 53.6% against ~20% planned.
- Cost watch (.claude/hooks/costwatch.py, rule 85): amber at 200k history or 3% of a week, red at 300k or 5%; amber
  = finish the step and hand over, red = hand over at once. It acts only at those lines; below them nothing limits
  what a step pulls into history.
- Start-up reading (measured now, characters/4): CLAUDE.md ~3.2k tokens (loaded in every chat), guides/job-packs.md
  ~1.1k, the rulebook ~9.6k (looked up by section). The handover (15 lines) and a film's notes (under 4,000 words)
  are read at start. A new chat in this chain begins at ~80k before its first action (the app's own share).
- Hooks in force (.claude/settings.json): SessionStart setup.sh; UserPromptSubmit and PostToolUse costwatch.py;
  UserPromptSubmit handover.py log; Stop ledger.py auto and propose.py hook. No hook looks at what a tool call reads.
- Earlier attempts that did not land: naming page.py in the job pack (chats 29/31 still searched by hand); the 13 Nov
  "Never again" ideas in cost-diagnosis.md (real-money ledger, budget stop: in force; per-chat cost did not fall).
- LIMIT: chats 9-32 of Protest Tiers (session ids 01Gzna...) cannot be opened from this account.

## Record
notes/cost-diagnosis.md
notes/proposals/learn/code-search-count.md
notes/proposals/learn/protest-tiers-costs.md
notes/proposal-route.md
notes/ledger/protest-tiers.json
notes/ledger/blessed.json
source/page.py
source/handover.py
.claude/hooks/costwatch.py
.claude/settings.json
guides/job-packs.md
guides/film-quality-rules.md
CLAUDE.md
