# Learn job: split the costs not yet measured (Sam's Y, 26 Nov, slim Option 1)

Model: Sonnet. Changes nothing in tools, rules or films. Budget: about 0.5% of a week (estimate); stop and say so at 1%.

Sam's words: "A chat on the cheaper model (Sonnet) uses the cost records of the last two films to split out the parts
not yet measured: which printouts are biggest, what the small automatic checks that run on every step add, and how
much time on the dearer model (Opus) goes on routine work. For each gap worth at least 1% of a week per film, you get
one Y or N with its saving." Lost: nothing until Sam says yes. Added: this one measuring chat.

Films: Grand Theft Autism and Brexit Is Done (notes/ledger/grand-theft-autism.json, brexit-is-done.json; their
existing stepcost/dearest split already gives search printouts ~13%/~12%, pictures ~5%, other printouts ~2%).

Measure (read the ledger first; list_events on the films' chats only for what the ledger lacks, sampled, not all):
- (a) Search/command printouts by command: top ten by tokens, % of a week per film each.
- (b) "Messages and reminders" (9-13%) split into: hook printouts (costwatch, finderwarn, humancheck, sendgate,
  modelguard, ledger; .claude/settings.json), app reminders, Sam's own messages (never cut).
- (c) Each Opus chat's stage from its handover Next line; share of Opus cost on routine stages (checks, check sheet,
  animatic, filing, final render, sending, saving), and what it would have cost on Sonnet.
Not measured: the namer (dropped by Sam), CLAUDE.md (inside the approved start-up measure, 22 Nov).

Output: one plain table in this folder (results.md): gap, % of a week per film, how sure. Then, to Sam, in plain words,
one numbered Y/N per gap at 1% of a week a film or more, each with its saving and a Lost:/Added: line; changes that are
rules or tools go through the proposal route (source/propose.py) only after his Y. Gaps under 1%: one line, no question.
