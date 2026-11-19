# Proposal: Name what is in the unexplained two thirds of each chat's cost

Status: open

## Problem
Sam's aim is a film within 15% of a week. The tool that splits each chat's cost into kinds of step (searches,
whole-file reads, page tool, routine, renders, pictures) leaves about two thirds of every film's cost as "other",
so nobody can say what most of the money is spent on, or which part could be cut without lowering quality. Even if
every search cost nothing, Milburn would still be far over 15%. The 15 Milburn chats' full records are no longer in
the container; reading them back through the session record is slow and costly.

## Facts
- Units (checked): the ledger's cost column is % of a week, not dollars (notes/ledger/milburn.md: "spent 32.4%").
  Sam's brief wrote it as "$32.40". At WEEK_USD 245 (provisional, .claude/hooks/costwatch.py:26) 32.4% is ~$79.
- Milburn (notes/ledger/milburn.json): 15 chats (11 Opus, 4 Sonnet), 1,281 steps, every row an estimate from the
  transcript (src "estimate"); total 32.4% against an estimate of 24.0%. Sam's own app figure at posting: 22.0%
  (milburn.json "final", src "Sam (app)"). So the transcript estimate ran ~47% above Sam's meter; the kind shares
  are shares of a total that is itself off by about half (cause unchecked: prices, WEEK_USD, or double counting).
- Cost-weighted shares over Milburn (counted from milburn.json kinds x cost): other 66.7%, tool search 16.3%,
  film-file search 8.6%, pictures 5.1%, renders 2.5%, page.py 0.5%, whole-file .py read 0.2%, routine 0.1%.
  Per chat, other runs 58-87%; calls counted as "other" per chat: 2-31.
- How "other" is made (source/stepcost.py, measure(), lines 119-200): each tool result is charged its write plus a
  re-read at every later step; the output that asked for a call is shared among its calls; whatever is left of the
  chat's real cost is added to "other", and calls kind_of() does not name (Edit, Write, Bash running python, tests,
  git, session/GitHub tools, agents) are charged to "other" too. So "other" holds: the context already there before
  step 1 (the app's own instructions and tool list, CLAUDE.md, start-up hook text) re-read at every step; Claude's
  own words and thinking with no call; reminders; and all edits, writes, python runs, tests, git and session calls.
- Prototype split, this chat (19 Nov), a throwaway script in the scratchpad, no tool changed: on
  tests/stepcost-transcript.jsonl (16 steps, $1.31): before-step-1 context 36.8%, tool search 20.9%, edits and
  writes 20.3%, left over 16.8%, python 3.9%. On this chat's own first 13 steps: before-step-1 context 73.6% (83k
  tokens at step 1). Both are short chats; no long film chat has been split this way.
- Earlier split (notes/proposals/startup-reading.md Facts, from notes/cost-diagnosis.md, 13-16 Nov): median Opus
  film chat ~78 actions ending ~220k, ~$5.6: app's own ~80k re-read ~25%, start-up reading ~15%, work history ~25%,
  output ~20%, writes the rest. Startup-reading was adopted 16 Nov (CLAUDE.md condensed); Milburn ran after it.
- Record: ~/.claude/projects holds only this chat's transcript (checked). The ledger stores per chat only steps,
  end history, kind shares and call counts (milburn.json), not the transcript. list_events: two small reads of one
  Milburn chat (session_01J1JB7YBXPnoLsQGLnhHAxi) returned pages with no assistant events; whether its events carry
  per-step token usage is unchecked. Sam's brief: ~10k tokens per 6 steps through list_events, so all 1,281
  Milburn steps is ~2.1M tokens read (at Opus's $8/M write price at least ~$17, ~7% of a week; estimate).
- ledger.py auto (the Stop hook) runs stepcost on every chat at its end (stepcost.py docstring), so any change to
  stepcost measures every new chat from then on at no extra cost.

## Record
notes/ledger/milburn.json
notes/ledger/milburn.md
notes/ledger/protest-tiers.json
source/stepcost.py
source/ledger.py
.claude/hooks/costwatch.py
notes/cost-diagnosis.md
notes/proposals/startup-reading.md
notes/proposals/chat-size-and-model.md
tests/stepcost-transcript.jsonl
