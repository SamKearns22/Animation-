## Leak
yes: the Facts single out the code-finding tools (the code MAP and `source/page.py`) and flag "whether chats 29 and 31 used them: unchecked", and the record offers only two chats' step bills. Together they steer a helper toward "make code look-up cheaper inside one chat". The wording "decide what change to make" also invites one change picked before the whole film has been measured.

## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 5 | 21 |
| V2 | 2 | 1 | 2 | 4 | 5 | 14 |
| V3 | 5 | 5 | 4 | 3 | 5 | 22 |

## Sam test
Q1: Yes. An agent-workflow expert would measure the unit that sets the bill (chats per film, and why each chat was needed) before tuning steps inside a chat. That is the pick. They would also have the record keep itself filled in from now on, which the pick does.
Q2: The evidence is every chat of the last three films (Protest Tiers 32, Blessed 24, Remakes 19: 75 in all, from the ledgers) at the app's real cost, not two keyword-counted chats. The metered within-chat split comes from the existing step meter (`costbreak.py`), so the numbers are not guesses.
Q3: Root cause, with evidence: moves cost 25.3% of 51.27% (ledger stage table), against 7.5% planned, and the chat titles name fixes (pre-flight crash, pre-flight faults, black frames). This is strongly suggested, not yet measured, because the ledger records "0 rounds, 0 notes" for every film. The cause line is enforced by the handover check, which already runs in every chat. A chat could still tag every chat "first build", so the check proposes the cause from the chat's own events and the chat must give a reason to change it (fixed). We know it worked if the next film has fewer chats and less spend than 32 chats and 51.27%.
Q4: Four approaches were weighed: cheaper steps, fewer chats, measure first, and tool-job spending. The measure-first approach is the only one aimed at the 3.4-times gap rather than at a lever chosen in advance.
Q5: The measuring step changes nothing. The cause line is a separate yes and can be removed on its own. The fix itself waits for the table and has its own yes, so Sam is not asked to trust anything unproven.
Q6: Every figure was checked against the ledgers, bills and tool-use count during this judging. Marked unchecked: the 3% and 1% cost estimates, whether the older cloud chats can all be read, the tool-job period, and why "After the film" says 33.55% when the spend is 51.27%.
Q7: It is sized by the result (the 3.4-times gap), not by its price, and its honest cost is stated. The cheap trap is V2, a look-up tweak worth about 0.3% a chat, and the pick rejects it.
Q8: Nothing is a trial. The measuring is done once, properly. The cause line is permanent. Each fix is permanent and is reviewed against the ledger when Sam declares the next film complete.

## Pick
V3

## Why
V2 answers the problem's wording. It makes code look-up cheaper on the evidence of two chats, about 30% of a ~2.4% chat, while the film overran by about 36 points. It is the cheap version that falls short, and it asks for a build before anything is measured. V1 and V3 both see the real decision: why a film takes 19-32 chats when 15% buys about 9. V3 wins on scope. It covers three films and puts a cause and the real app cost on each chat, which is the unit that sets the result. It also makes the missing record (cause, notes, rounds) permanent, so no future film is judged blind again. V1's per-step meter answers "which kind of step costs most" well, but it is weaker on "why did this chat exist at all".
Taken from V1: run the existing step meter (`costbreak.py`) on the same chats for the metered within-chat split, instead of hand estimates. Also from V1: a fixed number to beat for each possible fix (start-up reads 11-19 down to 3; fix chats per stage about 4 down to 0-1), and the comparison film. Added by the judge: the cause line is proposed from the chat's own events, so it cannot be filled in on paper. Also added: the cause line goes to Sam as its own numbered yes, not bundled with the measuring.

## Faults in the pick
- F1 [fixed] V3 bundled a permanent handover change with the measuring under one yes. Now they are two numbered questions.
- F2 [fixed] A cause typed in by the chat could be filled in lazily. The check now proposes the cause from the chat's own record (a failed check or render before an edit = own fault; Sam's note in the chat = notes), and an override needs a reason.
- F3 [fixed] V3's within-chat shares were estimates. They are now metered with the existing step meter.
- F4 [named] The measuring cost (about 3% of a week) is an estimate. If the older chats must be paged through one by one, it could double, and the measuring chat says so before it goes past 3%.
- F5 [named] The 33.55% vs 51.27% mismatch and the model labels in the ledger ("sonnet" on chats titled Opus) are unexplained. The measuring chat reports them; it does not fix them.
- F6 [named] Tool-job spending (morning report 28.05% alone) is in the table but not yet ranked. The period it covers is unchecked.

## Final version
**Problem in one line:** cost per chat is steady ($3-8, about 1.6% of a week). What breaks the 15% aim is the number of chats: Protest Tiers 32 (51.27%), Blessed 24 (62.21%), Remakes 19 (35.96%). At 1.6% a chat, 15% buys about 9 chats. Moves alone cost 25.3% of Protest Tiers against 7.5% planned, across chats named after fixes.

**Yes 1: measure (changes nothing).** One Opus-high helper chat reads the 75 chats of Protest Tiers, Blessed and Remakes through the earlier-chat reader. It reads each chat's title, first messages and ending, plus the steps around any failed check or render. Each chat gets one cause: first build; fixing Claude's own fault (naming the check that missed it); Sam's notes; tool repair; start-up/handover only; or waiting on renders. Each chat is matched to its real app cost from the ledger. The existing step meter is run on the same chats for the metered split inside them. Output: one table of % of a week per cause, per stage, per film, plus tool jobs by date. Cost: about 3% of a week, once, filed under tool work. It stops and reports if it goes past that.

**Yes 2: keep the record (permanent).** The handover check refuses to finish until the chat's cause line is filled in. It proposes the cause from the chat's own events, and changing it needs a reason. The ledger records the cause line together with notes and rounds. Cost: about 1% of a week. Number to beat: every future chat has a cause, against none today. Removable on its own.

**Then: one fix, on its own yes, after the table.** The biggest cause gets the fix, with its number to beat:
- Own-fault rework is biggest: the check that missed each fault is improved so the fault is caught inside the chat that made it, for example crash and black-frame checks after every moves edit, with the handover refused while one fails. To beat: fix chats per stage from about 4 to 0-1.
- Start-up is biggest: the start check prints the pack's sections itself. To beat: start-up reads from 11-19 to 3 or fewer.
- Code look-up is biggest: a hook routes film-code searches through the page tool. To beat: look-up share down from about 30% of a chat.

Every fix is measured on the next film against 32 chats and 51.27%, and reviewed when Sam declares that film complete.

## For Sam
### Option 1: Find out why films take so many chats, then fix the biggest reason
Each chat costs about the same. The trouble is that a film takes 19-32 chats when the budget allows about 9, and half of Protest Tiers went on re-doing the movement. One chat (about 3% of a week) goes through all 75 chats of the last three films and says why each one happened and what it really cost. From then on, every chat records its reason at handover. Then you get one fix aimed at the biggest reason, with a number it must beat on the next film.
Lost: nothing (about 3% of a week for the one-off check, and 1% to set up the reason line).
Added: a one-page picture of where the money went, a reason recorded for every chat, and then one fix at a time, each on your yes.

### Option 2: Measure where each step's cost goes, then fix the biggest step
The existing cost meter is improved so it can tell start-up and fixing Claude's own mistakes apart from building. It is run on all 32 Protest Tiers chats and on Remakes. The biggest kind of step gets one fix (most likely catching movement faults while they are made), with a number to beat.
Lost: nothing (about 1-1.5% of a week).
Added: a cost table in every film's ledger, then one fix per yes. It is weaker at showing why a chat had to exist at all.
