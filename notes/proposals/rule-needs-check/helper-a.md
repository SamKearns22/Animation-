# Helper A: rules that have no working check

## Leak
The problem file names a solution: Sam's Y to item 12 (no rule without a check, an audit, a gate, a known-bad test). The record also lists the chat's own version (chat.md), which repeats it. I treat item 12 as Sam's aim, not as the method.

## Results
- Rulebook: 89 table rows, 20 say "by hand" (re-counted with grep, guides/film-quality-rules.md).
- "By hand" means "ticked on the check sheet before every animatic" (rulebook line 8). But CLAUDE.md says "No check sheet before an animatic unless I ask". So by default the 20 by-hand rows have **no moment when anyone does them**.
- Three CLAUDE.md sections dated 21 Nov (Be honest, Fix the drawing, Seeing like Sam) have no row in the rulebook's Working-with-Sam table. Their "Locked by Sam" line is checked nowhere: grep of source/ and guides/ finds nothing.
- Some named checks were not working. check-repairs (notes/check-repairs.md, 21-22 Nov) found: the model guard was named but never switched on since 17 Nov; there was no check for notes size, handover length or push messages; 11 kit tests were failing. On Milburn, clipcheck printed COULD NOT TEST, and the name card reached Sam twice (could-not-test.md).
- Cost of faults reaching Sam: Milburn got 33 notes and 4 repeats, and cost 22% of a week against the 15% aim (milburn-review.md). GTA spent 75.49% of a week against a 53.2% estimate (ledger grand-theft-autism.md). Its ledger shows 3 notes, which is probably an undercount (unchecked).
- Gap: nobody has matched Sam's notes to the rule each one broke. So the record cannot yet say which failure costs most: a rule with no check, a check that was never switched on, or a check that ran and missed. That gap is a finding.

## The real decision
The decision is not "write a check for each rule". It is: **how does the system know, at the start of every chat, that each of Sam's rules has a check that exists, is switched on, and catches the fault it is there for**, so that a gap shows before Sam meets it. The unit is the whole rule set, across every film. A bigger lever than any one check already exists. The watcher lists every tool's promise and its proof, and prints any tool with none at every chat start. Rules are simply not in it.

## Root cause
1. The rulebook's Check column is free text that nothing reads. A rule can name a check that is missing, switched off, or failing, and nothing notices.
2. "By hand" points to a check sheet that is not made by default.
3. A check is proven only by calling it directly, never by a known fault it must catch inside a real film (check-repairs, root causes 1-3).
4. New rules written in CLAUDE.md skip the rulebook table, so they never get a row or a check.

Earlier fixes failed because each one patched a single check after Sam saw its fault (plain-check, could-not-test). None closed the general gap.

## Approaches weighed
A. **Sweep:** audit every rule, gate new ones, build a known-bad test for each. This is complete, but the order is a guess and it spends most on rules that have never failed.
B. **Reframe, rules as promises:** each rule row becomes a watcher promise whose proof must lead to a live check or a kit test that passes. Unproven rows print at every start, as unlisted tools do now.
C. **Notes-led:** each of Sam's notes is mapped to the rule it broke. A check counts as proven only when it catches that note's real bad frame.
D. **Learn-first:** do the mapping before anything is built, and let it set the order.
E. **A judge for by-hand rules:** a fresh-eye judge (a separate chat that did not make the work) checks the by-hand rules against the chat's output.

Chosen: D first, then B, then C, then E, each as its own change.

## Proposal
**Learn first (changes nothing):** a table of every rulebook row and every CLAUDE.md rule, with its check and that check's state: live, switched off, failing, by hand, or none. Against it, every Milburn and GTA note and every check-repairs finding, each marked as "no check", "check not running" or "check missed". The table is ranked by notes and cost, and its counts are the numbers each change below must beat.

**Then, one change at a time, each with its own yes:**
1. **Rules as promises.** The watcher reads the rulebook and the CLAUDE.md sections. Any rule whose proof is missing, switched off or failing prints at every chat start and at every reply end. A new rule with no proof is flagged the moment it is written, so this change is the gate. To beat: zero unproven rules at the next film's first chat, against today's count from the learning table.
2. **A known-bad test from Sam's own notes,** in the learning table's order. Each check gets a kit test that must fail on the real bad version Sam saw. A check that cannot catch its example is marked broken. To beat: fewer of the next film's notes that a check should have caught (Milburn's figure from the table).
3. **By-hand rules get a moment and a judge.** At the handover check, a fresh-eye judge answers each by-hand rule against the chat's output, giving the evidence. To beat: fewer by-hand breaks reaching Sam.

Cost (unchecked estimates): learning 1.5%; change 1 2%; change 2 about 0.4% per check, so about 4% for the top ten; change 3 1.5%. All of this is back-end work, done once and not counted against a film. After that, each film adds near zero, because the watcher already runs in every chat.

What Sam would notice: one ranked list first. Then fewer notes on faults that a check should have caught.

## Sam test
Q1 Expert: an expert proves each control (each check) on the bad case it is for, and uses the monitor that already exists.
Q2 Best result: the evidence covers both films, every rule and every note, not just one rule.
Q3 Comprehensive: the watcher runs in every chat, and a check counts only when it catches a real bad version.
Q4 Most intelligent: five different approaches were weighed, and the order comes from the evidence.
Q5 Risk: learning changes nothing, and each change can be undone on its own.
Q6 Checked: every source is named, and the estimates are marked unchecked.
Q7 Not cheap: every rule is covered and the tests are Sam's real faults, so it is not a cheap version.
Q8 Nothing temporary: each change is permanent and is reviewed at the end of the film.

## Lost / Added
Lost: about 9% of a week of back-end time. Lost: some start-up lines are louder until every gap is closed. Added: no rule can sit there without a check that is proven to work.

## Unchecked
The cost estimates. GTA's true note count. How many existing checks have ever been tested on a known-bad example.
