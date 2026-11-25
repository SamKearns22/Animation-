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

## Verdict (the judge, word for word)
<!-- verdict-hash: ff5b8a5b189f9738 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = helper A, V3 = chat. Picked: V1 (helper B). Critiqued: 7 found, 3 fixed, 4 named.

## Leak
none (the problem lists the article's points and marks gaps "unchecked"; it names no remedy. Its framing by the article's five points narrows the question, but every version reframed it.)
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 3 | 3 | 4 | 5 | 19 |
| V2 | 3 | 3 | 3 | 4 | 5 | 18 |
| V3 | 2 | 2 | 3 | 2 | 4 | 13 |
## Sam test
Q1: Yes, once fixed: an expert ranks the article's points by measured share of a film before changing anything, and reads the cost split the project already records (each GTA and Brexit chat is split by where its money went) instead of measuring it again.
Q2: The unit is the whole film. GTA (52 chats split) and Brexit (15 chats split) are the two latest films and already measured; they are the right evidence. Weak spot: GTA's figures are transcript estimates, not the app's own (named).
Q3: Root cause shown: cost is steps x re-read price (cost per step flat at about $0.020-0.022 across GTA chat lengths, re-checked), so per-chat trims are small; the record's dearest blocks are start-up (~21%), Claude's own writing (~40%), search printouts (~13%), messages and reminders (~9-13%). Each change lives in a tool or guard with a number to beat, not in prose a chat must choose to read.
Q4: Four approaches weighed (article checklist, model share, fewer steps, learn first); the checklist is shown to be worth 1-2% at most and the biggest lever (repeated faults) is pointed to its own route.
Q5: The learning changes nothing; each later change is its own yes and undoes alone. Nothing moves out of the instructions every chat reads.
Q6: Figures re-checked against the ledgers, app-costs.tsv, stepcost/dearest output and modelguard; unchecked items listed.
Q7: Sized by the result: only a change whose measured share clears 1% of a week a film is offered; no cheap cut to the rules Sam relies on.
Q8: Each change is made properly or not at all and is reviewed at film end; no trial.
## Pick
V1
## Why
V1 is the only version that names the real lever behind 33-108% films (steps per film and the dearer model's share) and keeps every change gated by its own measured size; its figures check out (GTA 50 of 58 chats on Opus, Brexit 17 of 18, flat cost per step). V2 is close but measures Milburn and Protest Tiers, whose ledger rows have no cost split, so it would re-measure from scratch, and its ceiling on the instructions file would squeeze the place Sam's working-with-me rules must be written. V3 acts before measuring (moves chain rules out of the file every chat reads, adds a shortening section no saved example can test, and a command list a chat must choose to read).
What every version missed: the ledger already splits each GTA and Brexit chat's cost by origin (stepcost/dearest), and Sam already approved (22 Nov, dearest-grand-theft-autism-1 Option 2) a measure of the start-up block plus a check for searches made one at a time. So the learn step shrinks to the parts not yet split, and the CLAUDE.md point joins that approved build instead of opening a second one.
Taken from V2: the plain ranked table answering Sam point by point; "no shortening section" with its reason; the correct film figures.
## Faults in the pick
- F1 [fixed] V1's measure (a) says printout sizes are "not in the record"; the ledger already splits search printouts (~13% of GTA, ~12% of Brexit), pictures (~5%) and other printouts (~2%). Learn now reads that and splits only search printouts by command.
- F2 [fixed] Overlap with the approved start-up measure (22 Nov): the CLAUDE.md point is folded into it; V1's measure (c) (did a chat "touch" a section) is dropped, since rules on messages to Sam apply in every chat and cannot be shown unused that way.
- F3 [fixed] Protest Tiers is 34.48%, not 33.6%.
- F4 [named] Model by stage: 38 of GTA's 50 Opus chats are labelled stage "auto", so the stage cannot yet be read from the ledger; and modelguard already refuses routine commands on Opus. Change 2 is offered only if the stages can be labelled from each chat's handover Next line.
- F5 [named] GTA figures are transcript estimates (no app rows).
- F6 [named] "messages and reminders" (9-13%) includes Sam's own messages, which are never cut; the hooks' share is unknown until split.
- F7 [named] Namer runs a film are uncounted; switching it may save little.
## Final version
**Answer Sam now, from the record (no new job):** a plain table, one line per article point: done already (stage packs and three reading layers = "load only when used"; long chats governed by the cost watch and chat-size rule), not needed (no chat ever shortened: largest 414k of 1M, 85 records), or measured gap.

**Learn (changes nothing; Sonnet; about 0.5% of a week, unchecked):** from GTA and Brexit transcripts and their ledger split: (a) search printouts by command, top ten; (b) "messages and reminders" split into hook printouts, app reminders and Sam's messages; (c) each Opus chat's stage, read from its handover Next line, and the share spent on routine stages; (d) the saved name tests rerun with the namer on Sonnet. The CLAUDE.md share is taken from the approved start-up measure, not measured again.

**Then one yes each, only where the number clears 1% of a week a film:**
1. Quiet by default: the noisiest commands, and any hook that prints every step, print only faults (built into the tool). Beat: their tokens down 70% on the next film, same measure.
2. Model by stage: modelguard extended from routine commands to routine stages, only if (c) can label stages. Beat: Opus share in routine stages under 10%.
3. Namer on Sonnet only if it matches Opus on every saved test.
4. CLAUDE.md: decided inside the approved start-up route, word for word only (sentences.py).
Not changed: a shortening section (nothing to check it against). Repeated faults, the biggest lever (~15% of a week on Blessed), stay with their own route.
## For Sam
### Option 1: Answer from what we already measure, then fix only what is big
Problem: You asked if we follow the article's advice on saving money in long chats. Most of it we already do in another form; the rest is small or unmeasured, and our films cost 24% to 108% of a week.
1. I send you a short table: each point of the article, marked done already, not needed, or a measured gap.
2. A cheap chat reads the cost records we already keep for the last two films and splits the few parts not yet split: which printouts are biggest, how much the small automatic checks that run on every step add, and how much dearer-model time goes on routine work.
3. For each gap worth at least 1% of a week a film, you get one Y or N with its saving.
Why: The rules file every chat reads costs about 1.3% of a week a film; the big costs are elsewhere (start-up about a fifth of a film, Claude's own writing about two fifths, search printouts about an eighth).
You'd notice: one table now, then a few Y or N questions; films look the same.
Other option: cap the size of the rules file and measure two older films from scratch.
Lost: nothing until you say yes to a change.
Added: one small measuring chat, about half of 1% of a week (estimate).
### Option 2: Cap the rules file and measure two older films
Problem: The same question; this option also stops the rules file every chat reads from growing, since it grew by a third in nine days.
1. I send you the same table.
2. A chat measures two older films' chats from scratch: printouts, chat length against cost, helpers, and the naming helper on the cheaper model.
3. The end-of-chat check refuses to hand over if the rules file grows past today's size; room is made by moving text word for word to the rulebook.
Why: It stops a slow growth that every chat pays for.
You'd notice: the same table, up to three Y or N questions, and new rules for how we work with you moving to the rulebook more often.
Other option: Option 1.
Lost: room in the rules file for new rules about working with you.
Added: a measuring chat of about 1 to 1.5% of a week, and a size limit.
