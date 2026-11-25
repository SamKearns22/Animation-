# Proposal: Anthropic's session-value article against how this project runs

Status: open

## Problem
Sam asked (25 Nov) whether the project follows the advice in Anthropic's article "Maximizing the value of your
Claude Code sessions" (claude.com/resources/articles/maximizing-the-value-of-your-claude-code-sessions, 14 Aug 2026).
The article's points that touch this project: keep CLAUDE.md to specific instructions and move workflow-specific
ones into material that loads only when used; give the summary that shortens a long chat instructions on what must
survive; list the few daily commands with their quiet settings; long chats cost more because each step re-reads all
earlier ones; use cheaper models for helpers where they do as well. Some of these may already be done here in
another form, some may cost more than they save, and some may risk quality (Statement One: quality is never cut;
every film within 15% of a week). Sam needs to know which points are real gaps worth changing, what each would
save or protect in measured terms, and what each could lose.

## Facts
- CLAUDE.md is 16,023 characters, 2,791 words, about 6,800 tokens at this project's measured 2.35 characters a token
  (notes/job-e-measurements.md section 1; it was about 5k tokens on 16 Nov). The app loads it into every chat and
  every helper. Words by section: Statement One 57, Statement Two 50, Fix the drawing 145, Seeing like Sam 305,
  Working with me 136, Messages to me 279, Files 70, Asking me before you go on 425, Rules are permanent 347,
  Models and chats 325, Fresh chats and the handover 219, Reading little 130, Making the films 218 (counted 25 Nov).
- Cost of CLAUDE.md, worked from the cost watch's prices (.claude/hooks/costwatch.py: Opus re-read $0.18/M, write
  $8/M; WEEK_USD 366): written once per chat about $0.054, re-read on each of a median ~78 steps about $0.095,
  together about $0.15 a chat = about 0.04% of a week. At ~32 chats a film (notes/proposals/startup-reading.md
  Problem) about 1.3% of a week a film; helpers that load it add more (unchecked how many per film).
- A fresh chat is about 80k tokens before any reading, of which the app's own part (system prompt, tool definitions,
  connectors) is about 75k and is not controlled by this project (notes/job-e-measurements.md section 1). A film
  round then reads 40-55k more of guides and notes (same file). Re-reading is most of the cost
  (notes/cost-diagnosis.md, Job B: app's own 80k re-read ~25% of a median chat, start-up reading ~15%, work
  history ~25%, output ~20%).
- Real chat records (notes/ledger/app-costs.tsv, 85 chats): Opus 63 chats, median $4.89, median history at the end
  218k tokens; Sonnet 19 chats, median $0.80, median history 118k. Largest 414k (Blessed chat 5, $27.73: bundled
  stages, a model switch re-paid 364k). Only 1 chat passed 400k. Context limit 1M; no chat record or log in
  notes/logs mentions a shortened (compacted) chat (grep, 25 Nov).
- Each step at 215k costs about 4.7 cents before doing anything; at 400k about 9 cents (notes/cost-diagnosis.md).
  A model switch mid-chat rewrites the whole history at the write price (same file).
- Earlier routes on the same ground: startup-reading (adopted 16 Nov: condensed start-up reading, packs per stage in
  guides/job-packs.md, three reading layers); claude-md-duplicates (Half A: five doubled rules merged). Text may leave
  CLAUDE.md only word for word to the rulebook or a pack (source/sentences.py, Sam's Y 16 Nov).
- The project already has per-stage reading: guides/job-packs.md (1,124 words) names one pack per stage; the
  rulebook guides/film-quality-rules.md is 8,304 words and is read only by named rule. No .claude/skills folder.
- CLAUDE.md has no section saying what must survive if a chat is shortened. Things that must not be lost
  mid-chat: Sam's locked shots, open notes, the brief checklist, the "Override" scope (CLAUDE.md, Asking me...).
- CLAUDE.md names commands in passing (finish.py, handover.py start/end, `final OUT --small --span`,
  branches.py scan, propose.py) but has no short list of the daily commands with their quiet or short-print flags;
  rule 19 asks for long printouts filtered to the faults (named in CLAUDE.md, Reading little).
- Chat size rule (CLAUDE.md, Models and chats): aim about 100 steps, up to 150, none under about 40 except two
  named cases. A fresh chat costs its 80k start plus a pack read (40-55k) plus the handover check; unchecked
  which chat length gives the lowest cost per finished stage.
- Helpers (.claude/agents): critic runs on Sonnet; namer on Opus. Proposal helpers A and B and the judge run on
  Opus (source/propose.py). The route itself costs about 1.3% of a week a run (notes/proposals/install-route.md).
  Whether the namer does as well on a cheaper model is unchecked (earlier name tests are saved by
  source/nametest.py).
- Hooks run on every step (.claude/settings.json): UserPromptSubmit costwatch; PostToolUse costwatch and
  finderwarn; PreToolUse humancheck sendgate and modelguard; Stop ledger auto. What they add to the chat per step
  (printed text) is unchecked.
- Rules: no rule without a working check (CLAUDE.md, Rules are permanent); every fix for all films; Sam reads only
  plain words on an iPhone.

## Record
notes/job-e-measurements.md
notes/cost-diagnosis.md
notes/ledger/app-costs.tsv
notes/proposals/startup-reading.md
notes/proposals/claude-md-duplicates.md
notes/proposals/install-route.md
CLAUDE.md
guides/job-packs.md
.claude/settings.json
.claude/hooks/costwatch.py
.claude/agents
source/sentences.py
source/nametest.py
