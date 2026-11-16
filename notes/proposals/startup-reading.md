# Proposal: Startup reading: condense what every chat reads before it works

Status: adopted (2026-11-16)

## Problem
Every chat reads a fixed set of text before it does any work: CLAUDE.md (loaded by the app itself), the stage's pack
in guides/job-packs.md and the sections it names, the film's notes, and printouts the start-up steps make (the
branch listing, hook output). Everything read early is paid for again, at the re-read price, on every later action
of that chat (~78 actions in a median Opus film chat), and again in every new chat (~32 chats a film). Sam was told
(16 Nov) that start-up reading is one of the largest costs and asked for the CLAUDE.md, rules, kits, processes and
guides to be analysed for where the text can be condensed and made cheaper to read, without losing any rule and
without the quality of films or the number of Sam's notes getting worse. Rules were mostly written after something
went wrong; wording that is cut too far may let an old fault return. Chat length, handovers and chat count are a
separate job (Sam, 16 Nov) and are out of scope here.

## Facts
- Prices (notes/cost-diagnosis.md, Job B, fitted to the app's real costs): Opus re-read $0.22/M tokens, write $6.0/M,
  output $19.8/M; Sonnet $0.106 / $3.94 / $8.2. Median Opus film chat ~78 actions ending ~220k, ~$5.6: app's own ~80k
  re-read ~25%, start-up reading ~15%, work history ~25%, output ~20%, writes the rest. 1% of a week ~ $2.45
  (notes/proposals/learn/protest-tiers-costs.md: chat 1, 1.53% = $3.752).
- Near-empty chats end at ~90-100k history (protest-tiers-costs.md chats 0, 5, 7: 89.7k, 99.7k, 97.0k), so the fixed
  footprint before work is ~90k, most of it the app's own (tool definitions, system prompt), not the repo's text.
- CLAUDE.md (16 Nov, counted): 139 lines, 2,192 words, 12,857 characters (~3.2k tokens); loaded into every chat and
  every helper that loads project instructions. 10 dated tags like "(Sam, 13 Nov; was 8 in a row)", 3 "replaces/was"
  histories. Longest line 183 characters. Some parts are used rarely (My accounts; YouTube; Yuletide pointer is in
  job-packs).
- Start-up step "list every branch (git fetch --all; git branch -r)" (CLAUDE.md, Making the films): 252 remote
  branches today, 9,171 characters (~2.5k tokens) printed into every chat. The SessionStart hook
  (.claude/hooks/setup.sh) already checks whether the copy is the newest main line and prints 3 lines if not.
- guides/job-packs.md: 707 words (4,558 chars), read at the start of every film chat. Stage reading it names
  (words, counted by section 16 Nov): Plan ~2,600 (preflight 1-2: 385; satire Start 526 + Getting it right 587 +
  Acting list 225; tiktok Hook Text 156; plus notes template); Build ~5,300 (figure-rig 2,3,4,5c: 1,659; satire
  Movement 862 + One set 646; critique-checklist A-M ~2,100; pose-gallery rows); Notes round: the film's notes only;
  Checks/animatic ~1,670 (satire Before every render 414, Render 320, If a check fails 563; preflight 3: 376);
  Final ~1,000 (tiktok The video file 337, Sign-off 359, Posting 215; preflight 5: 73).
- Whole guides (words): film-quality-rules 6,769; kit-catalogue 6,822; satire 6,566; best-practice 5,966;
  figure-rig 3,514; critique-checklist 2,580 (of which "Came from", for Claude only, 468); pose-gallery 2,372;
  tiktok-design 2,069; reference-pack 1,717; preflight 1,103. Packs say these are never read end to end.
- Film notes: rule says under 4,000 words; notes/elder-swindon.md is 5,965, notes/protest-tiers.md 4,531.
- handover.py start/end printouts: ~60 words (small). costwatch hook prints nothing at low cost.
- Rough money (derived, unchecked against a real chat): each 1k tokens read at the start of an Opus chat costs ~$0.006
  to write + 78 x $0.00022 = ~$0.023 per chat, ~$0.74 per 32-chat film (~0.3% of a week). CLAUDE.md alone ~1% of a
  week per film; the branch listing ~0.8%; a Build pack ~2-3% across the build chats.
- Earlier finding (notes/proposal-route.md case 3): naming a tool in a pack already failed once (page.py run 0 times
  in chats 29 and 31), so shorter text must not drop the instructions that get tools used.

## Record
CLAUDE.md
guides/job-packs.md
guides/film-quality-rules.md
guides/satire.md
guides/preflight.md
guides/tiktok-design.md
guides/figure-rig.md
guides/critique-checklist.md
guides/kit-catalogue.md
guides/pose-gallery.md
notes/cost-diagnosis.md
notes/proposals/learn/protest-tiers-costs.md
.claude/hooks/setup.sh
source/handover.py

## Verdict (the judge, word for word)
<!-- verdict-hash: 47680503f048afd4 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = helper A, V3 = chat. Picked: V2 (helper A). Critiqued: 7 found, 4 fixed, 3 named.

## Leak
yes: the title and ask ("condense what every chat reads", "where the text can be condensed") name the remedy as rewording, and the Facts single out the branch listing, CLAUDE.md's dated tags and the over-cap notes, pointing helpers at those three levers. It also prints token figures at 4 characters a token, which the project's own measurement (notes/job-e-measurements.md: 2.35 characters a token) shows are about 40% too low.

## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 3 | 4 | 5 | 20 |
| V2 | 4 | 4 | 4 | 4 | 4 | 20 |
| V3 | 3 | 2 | 3 | 2 | 3 | 13 |

## Sam test
Q1: Yes. An expert measures what enters each chat by source, then removes non-rule text by tools and checks, leaving rule wording alone unless a measured item is still large.
Q2: Scope is every readable chat of the last two films. Gap named: Protest Tiers chats 9-32 cannot be opened, so the table covers chats 0-8 plus whatever Elder Swindon chats are readable; the learn chat says how many chats it covered.
Q3: Root cause (text only grows; the one size limit is unchecked; reading left to chat choice) shown with evidence (notes 5,965 and 4,531 words against 4,000; handover.py has no word check; 252 branches printed). Each change is a refusal or a tool, not text to follow. Known to work by start-up tokens per chat and notes/repeat faults at film end.
Q4: Four approaches weighed (rewrite, tool-chosen reading, layering, learn-first); rewrite kept only as a last step for a measured big item.
Q5: Learning changes nothing; each change is its own yes and undone alone. Guarded against rule loss by a sentence-by-sentence check and a situations test. Weak spot named: change 4 (pack printout) could raise tokens; it now runs only if the table shows chats read beyond their pack.
Q6: Token counts corrected to the measured 2.35 characters a token; money derived and marked unchecked; the film total (33.55% ledger line vs 53.6% spent) flagged as unresolved.
Q7: Sized by measured result; the cheap trap (trimming rule wording, V3) refused. Honest cost: learn ~1-1.5% of a week, each change ~0.5-1%; payback about 2 films at ~2-4% a film (unchecked).
Q8: Each change permanent, reviewed when Sam declares the film complete; no trial.

## Pick
V2

## Why
V2 and V1 share the right shape: learn first, then one tool-enforced change per yes. V2 wins on facts: it alone corrects the token figures using the project's measured rate (checked: job-e-measurements.md line 13), which nearly doubles every saving and makes the film notes (~10-13k tokens) the biggest repo-controlled item, ahead of CLAUDE.md. V1 rests on the problem's undercounted figures, but has two better parts taken here: the notes check refuses and names sections to archive instead of moving them itself (nothing of Sam's moved without a chat looking), and the rule-sentence guard (every rule sentence before and after; any missing one refuses). V1 also catches the ledger mismatch (checked: notes/ledger/protest-tiers.md line 64, 33.55% vs 53.6% spent), which the learn step now settles. From V3: the situations test (a fresh helper with only the new CLAUDE.md answers 10 past situations the same way as the old). V3 itself bundles a full rewrite, pack trimming and branch deletion into one yes, before any measurement, and trims rule wording: the trap the problem warns about.

## Faults in the pick
- F1 [fixed] Notes check moved finished items itself; now it refuses and names sections to move (from V1).
- F2 [fixed] Rule-loss guard was a placement kittest only; now also a sentence-by-sentence guard and the 10-situations test.
- F3 [fixed] Change 4 (pack printout) could add tokens; now only if the table shows chats read more than their pack.
- F4 [fixed] Film-total mismatch (33.55% vs 53.6%) not handled; learn step now settles it.
- F5 [named] Learn table can cover only readable chats (Protest Tiers 0-8, Elder Swindon unknown); the rest is estimated.
- F6 [named] Savings are derived, not measured; build cost (~3-5% of a week across learn and changes) pays back over about two films if the estimates hold.
- F7 [named] Dated tags tell chats which version of a rule wins; moving them is safe only where the old wording is already gone. The guard checks this rule by rule.

## Final version
**Learn (changes nothing).** One Sonnet chat reads the start of every readable chat of Elder Swindon and Protest Tiers (list_events), and records per chat each start-up item (CLAUDE.md, pack, named sections, film notes, branch listing, hook and handover printouts) in tokens at 2.35 characters a token, plus history size when work begins. It settles the 33.55% vs 53.6% film total. Output: a ranked table with, per item, the number a change must beat, and how many chats it covered. Cost ~1-1.5% of a week.

**Then one change at a time, each its own yes, in the table's order (expected):**
1. **Notes cap enforced:** handover.py end refuses a handover while the film's notes exceed 4,000 words and names the finished sections to move to notes/archive/. Beat: notes under ~9.6k tokens in every chat of the next film; no note lost.
2. **Branch step by tool:** the start check prints only branches with commits not on the main line; CLAUDE.md's "list every branch" points to it, the merge rule unchanged. Beat: under 200 tokens, zero missed newer work (checked against the full list at film end).
3. **CLAUDE.md layered:** dated histories to the rulebook's last table / notes/archive/; rarely used sections moved to the pack that uses them, a one-line pointer left. Guards: a check listing every rule sentence before and after (any missing refuses); a fresh helper answers 10 past situations with old and new CLAUDE.md and must match. Beat: ~5.5k to under 3.5k tokens, no rule lost.
4. **Pack printout by handover.py start**, only if the table shows chats read beyond their pack. Beat: start-up tokens per chat down a third.

Each change: ~0.5-1% of a week. At the film's end review, each is held to start-up tokens per chat and Sam's notes plus repeat faults, which must not rise against the last two films.

## For Sam
### Option 1: Measure first, then fix by tools one at a time
A cheap chat first counts exactly what each past chat read before working, piece by piece, and ranks the pieces by cost. Then, one yes each: a check that stops a film's notes growing past their size limit (both last films broke it), a short list of only the branches (saved copies of work) that hold new work instead of all 252, and CLAUDE.md slimmed by moving old dates and rarely used parts elsewhere, with a check that no rule sentence goes missing. You would notice nothing in the films; chats cost a little less, and each step comes with its number.
Lost: the full branch list and dated histories in every chat (kept in the archive).
Added: one measuring chat; a notes-size check; a short branch list; a no-rule-lost check; up to four separate questions.

### Option 2: Same fixes now, without measuring
Build the notes-size check, the short branch list and the slimmer CLAUDE.md straight away, skipping the measuring chat. Faster to start, but the order and size of each fix are guesses, and the figures in the problem were about 40% too low, so guesses can miss.
Lost: the measuring chat's ranked table and its proof of what each fix saved.
Added: the same three tools, sooner, as separate questions.
