# Proposal: find out which rules and tools work

Status: open (replay case 4)

## Problem
Sam: "This then is a systemic issue that could apply to every rule, test, kit and process ever written into the
project." We do not know which of the project's rules and tools are followed, or which of them actually help (fewer
notes, fewer faults reaching Sam, lower cost). Decide how to find out, and what to do with what is found.

## Facts
- About 64 rules (guides/film-quality-rules.md plus CLAUDE.md) and about 115 tools and kits (guides/kit-catalogue.md);
  counts unchecked.
- Only a few act on their own, as hooks in .claude/settings.json: the cost watch, the handover log and the ledger
  (check the file); others (pre-flight, checks) run only when a chat runs them.
- The notes-round section of guides/job-packs.md already tells a chat to use page.py; chats 29 and 31 still ran it 0
  times and searched code by hand 25 and 26 times (record: tool-use file).
- Earlier failures named in this chat: cost stops fed chats' own cost figures that were 20-75% too low; the critic
  found 8 faults in a "pillar" rule only after Sam asked for a critique.
- Protest Tiers' ledger holds every chat's real cost; its notes file holds Sam's notes; the handover check can read a
  chat's own record for free (source/handover.py).
- Sam's own messages so far are in the record.

## Record
notes/proposals/replay-record/sam-to-case4.md
notes/proposals/replay-record/tool-use-29-31.md
notes/proposals/replay-record/bills-29-31.md
notes/ledger/protest-tiers.md
notes/protest-tiers.md
CLAUDE.md
guides/film-quality-rules.md
guides/kit-catalogue.md
guides/job-packs.md
source/handover.py
source/ledger.py
.claude/settings.json

## Verdict (the judge, word for word)
<!-- verdict-hash: 137c43b2c87a8d70 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = chat, V3 = helper B. Picked: V3 (helper B). Critiqued: 10 found, 4 fixed, 6 named.

## Leak
yes: mild. The Facts list which hooks already run by themselves and say "the handover check can read a chat's own record for free" and that the ledger and notes file hold real costs and Sam's notes. That points the helpers toward an automatic, record-based measure built on the existing hooks (V1 and V3 both landed there). It does not state the design.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 3 | 4 | 19 |
| V2 | 2 | 2 | 3 | 3 | 4 | 14 |
| V3 | 4 | 4 | 4 | 4 | 4 | 20 |
## Sam test
Q1: Yes. An expert judges agents by their tool records and outcomes, not their own reports, and nudges at the moment of action. The merged pick does both.
Q2: Every chat of Protest Tiers plus the last two films, back-filled, not a sample. Older chats with no saved log need list_events (unchecked how many).
Q3: Root cause named with evidence (ledger "0 notes" over 32 chats; page.py run 0 times against 25/26 hand searches). The Stop hook scores every chat with no chat choosing to; bypass is counted; the nudge fires at the moment. A chat can still "name" a skip at handover, but it is counted on the scorecard.
Q4: Five approaches weighed in V3 (audit, gates, paper red-team, note tracing, register); the register feeds the gates and the note tracing, so it is the best of them.
Q5: It only flags and nudges; nothing is removed without Sam's Y on a "Lost:" line; it must reproduce chats 29 and 31's known counts before switching on. The fewer-notes effect cannot be shown until a film ends (named).
Q6: Facts checked: ledger 0/0/0 over 32 chats, page.py in the pack (job-packs line 32), 0 vs 25/26 counts, --notes at ledger.py line 469, chats 27/30/31 titled Opus but logged Sonnet, 11 saved logs, past tool jobs 6.42/7.01/6.65%. Corrected: 13 of 54 numbered rule rows say "by hand" in their check column (V3 said of 64; V1 said 21). Tool count and cost unchecked.
Q7: Sized by the result: every item, a real back-fill, note tracing. Honest cost stated (8-12% once).
Q8: Permanent hooks and records, reviewed at each film's completion. The 29/31 reproduction is an acceptance check on the build, not a trial.
## Pick
V3
## Why
V3 and V1 share the core (an automatic register read from chat records by the existing Stop hook). V3 wins on safety: it proves the signatures on chats 29 and 31 before Sam's Y, only flags, and gives a fixed decision table. Its weak spot is enforcement: a skip is only flagged at handover, after the hand searching has already cost money. From V1 I took the steering hook at the moment of use (nudge, never block), the "which check should have caught this note" line for every one of Sam's notes, the back-fill of the last two films, and refusing a new rule or tool that has no signature. V2 is a one-off audit (temporary, fails Q8), rests on a wrong fact (it says pre-flight and the handover check run by themselves; .claude/settings.json shows only setup, the cost watch, the handover log and the ledger), counts 29 chats where the ledger has 32, and measures nothing after the audit.
## Faults in the pick
- F1 [fixed] Skips were caught only at handover, after the cost; added V1's nudge at the moment of use.
- F2 [fixed] Notes were "logged against the rule" with no one assigning them; the next chat's handover start now names the check that should have caught each note, or "none exists".
- F3 [fixed] "Lost: nothing" was wrong: hand-typed note counts go, and hand searches in notes rounds are steered away.
- F4 [fixed] "13 of 64 rules by hand" corrected to 13 of 54 numbered rule rows.
- F5 [named] The 95% use bar is a judgement, not drawn from evidence; reviewed after the first film.
- F6 [named] Only 11 saved message logs exist for 32 chats; the back-fill of older chats depends on list_events and may be incomplete.
- F7 [named] Taste rules (poses, staging) leave no command in a record; their use is judged only through check results and Sam's notes.
- F8 [named] Signatures are keyword matches and can misread (the bills record calls its own counts approximate).
- F9 [named] Cost 8-12% and the ~115 tool count are unchecked; past tool jobs cost 6.4-7.0% each, and this one is larger.
- F10 [named] Whether chats 27, 30 and 31 ran on Sonnet or were mislogged is untraced; the register adds a title-versus-record model check.
## Final version
**What.** One register entry per rule and tool (about 54 numbered rules, the CLAUDE.md rows and about 115 tools), each with three signatures read from chat records: **Arose** (the situation came up), **Used** (e.g. page.py ran), **Bypass** (e.g. grep or sed on a film file in a notes round). A new rule or tool without signatures is refused when written.

**How it runs, with no chat choosing to.**
- The existing Stop hook (`ledger.py auto`) scores every chat from its record, not its claims, at no chat cost.
- Every check's FAULT lines (already saved by `ledger.record`) are tallied per check.
- Notes and repeats are counted from `handover.py log`'s saved messages, not typed `--notes`.
- `handover.py start` makes the next chat name, for each of Sam's notes, the check that should have caught it, or "none exists"; stored as a miss.
- A new PreToolUse hook nudges at the moment of a known bypass ("use page.py FILM find"); it never blocks.
- `handover.py end` flags each "arose, not used" as a fault, fixed or named before handover.

**Shown first.** Before Sam's Y, the signatures must reproduce chats 29 and 31's known counts (page.py 0; hand searches 25 and 26). Then back-fill Protest Tiers and the last two films for a real baseline.

**At each film's completion**, a fresh Sonnet helper applies a fixed table to a one-page scorecard (arose / used / caught / missed):
- Used under 95% where it arose: gate it or rewrite it.
- Missed a note: improve that check first.
- Caught nothing and missed nothing in three films: a removal proposal with "Lost:" for Sam's Y.

**Number to beat.** Use where arisen at least 95%; notes per round, repeated notes and notes a named check should have caught all falling against the back-filled baseline; real cost per film from app figures.

**Cost.** About 8-12% of a week once (build, about 180 signatures, back-fill, review); unchecked. Then about 0% per chat and about 1% per film.

**Lost:** hand-typed note counts; hand searches of film code in notes rounds (steered to page.py).
**Added:** the register, the scoring, the nudge hook, the note-to-check line, "skipped" handover faults, the scorecard.
## For Sam
### Option 1: An automatic scorecard, with nudges
Every chat is scored by itself, from what it actually did, not what it says: which rules came up, which were followed, which were skipped. Each of your notes is traced to the check that should have caught it. When a chat starts to skip a tool, it gets a nudge right then. It is tested on two past chats before it is switched on. At the end of each film you get one page showing which rules work, and any removal comes to you as a Y/N with the numbers. About 8-12% of a week, once.
Lost: chats typing their own note counts; chats searching film code by hand during notes rounds.
Added: a scorecard per film, nudges at the moment a tool is skipped, every note traced to the check that missed it.
### Option 2: The same scorecard, enforced harder, not tested first
The same automatic scorecard and note tracing, but switched on straight away without first proving it on past chats, and with stricter tools that refuse more. You would see results sooner, but you would be trusting it before it has been shown to work, and a too-strict tool could get in the way of real work. Similar cost.
Lost: chats typing their own note counts; hand searches of film code in notes rounds.
Added: a scorecard per film, stricter automatic tools, every note traced to the check that missed it.
