# The system audit (started 12 Nov)

Written in plain language for Sam. Kept separate from any film: it has its own budget, not Blessed's.

## Why we're doing this
While getting Blessed ready, we found that several of the automatic checks that are meant to catch mistakes had
never been switched on for that film. Nobody asked Sam about it. Each chat wrote "still missing" in its notes and
passed it on to the next one. The checking tool still said "clean", because it only lists missed checks in small
print. Two earlier audits didn't notice. Like a car with some warning lights quietly unplugged, everything looked
fine on the dashboard.

## What we've changed already
- **A new line in the rulebook (rule 59):** no check can be left off, left half-built or put off until later without
  Sam saying yes. A check that hasn't been set up counts as a mistake that must be fixed before the first animatic.

## The quick look at the last five films (12 Nov)
This was the fast version of the checks, which reads the script and the plan but doesn't look at the pictures. So it
shows what was missing, not whether the films looked wrong.

- **Remakes:** told the checker it had no people and no rooms, so the checks for rooms, hands, outlines, clothes and
  who is in each shot didn't run. It does have a cast and painted sets, so this was probably wrong. The checks for
  people walking into things or popping in and out didn't run either.
- **Elder Scrolls: Swindon:** told the checker it had no rooms and no voices, so those checks didn't run. This one is
  probably right for that kind of film. One shot is 15 seconds long; the limit is 8.
- **Ad-Vanced Notice, Islamocommunism, MidTerminal:** none has an "acting list", the plan of what each person does
  on each line. The rulebook asks for one because it cuts down rounds of notes.
- **Islamocommunism** also: one shot has no camera written into the plan, and two places in a drawing have a missing
  outline.
- **Shots over 8 seconds:** Swindon (15 s), Islamocommunism (12 s), Ad-Vanced Notice (9 s), MidTerminal (8.2 s). We
  don't yet know if these were agreed with Sam.

## The jobs still to do (Sam said yes to all, 12 Nov)
1. **The full check on each of the five films.** This time it looks at every picture. It runs one film at a time,
   about 9 minutes each, and reports only. (Sonnet)
2. **Did it cost us notes?** For each mistake the full check finds, look through Sam's old notes on that film. If Sam
   pointed it out himself later, that's a round of notes the checks should have saved. (Opus, medium effort)
3. **Make the checker honest.** Change the checking tool so it can never say "clean" while any check was skipped,
   never set up, or switched off. Each skipped check becomes a mistake listed at the top. The tool also checks that
   what a film says it contains (people, rooms, voices, props) matches what it really draws. (Opus, high effort)
4. **The ten wider questions** (Sam: all yes):
   1. **"Allowed" lists:** films keep lists of mistakes marked "meant to be like that". Do they keep growing, and
      does each one still have a good reason?
   2. **Problems passed along:** how many "not fixed yet" items does each film carry from chat to chat, and for how
      long?
   3. **The fresh-eye critique:** it lets "can't tell" through. Has that ever hidden something Sam later noticed?
   4. **Checks that can't fail:** give each check a deliberately broken example and make sure it actually catches it.
   5. **The shortcut re-check:** after a small fix, the checker only re-checks the pictures that changed. Make sure
      it never misses one.
   6. **The cost record:** it was once corrected by hand. Are the cost numbers we plan budgets with correct?
   7. **Lost work:** there are over 120 side branches (separate copies of the work). Check that no finished work is
      stuck on one and never reached the main copy.
   8. **Rules checked by hand:** which rules have no automatic check, and which of those keep turning up in Sam's
      notes?
   9. **Chats starting chats:** make sure a chain of chats can't carry a skipped check forward with no one looking.
   10. **Notes that come back:** count the notes Sam had to give twice, across past films. They show which mistakes
       the system keeps letting through.

## Order and cost
Blessed comes first (its own budget). Then this job: jobs 1 and 2, then 3, then 4. Rough guess for the whole job:
about 3.5% of a week (the checking runs on Sonnet about 1%, reading old notes on Opus about 1%, fixing the checker on
Opus about 1.5%). It's a guess; the first chat measures it and says if it's heading higher.

## Where things stand
- **Sam (12 Nov, before sleeping): start now and see it through to the end, as long as it doesn't get in Blessed's way.
  It must end with a plain-language report on what this means for quality, cost and how we work.**
- **Keeping out of Blessed's way:** jobs 1, 2 and 4 only read and report, and each runs in its own chat (its own
  computer). Job 3 changes the checking tool that Blessed's chat is using right now, so it is built on its own branch,
  `claude/audit-honest-checker`, and only joins the main line AFTER notes/blessed.md says animatic 1 was sent (if not
  yet, it waits and says so in the report). Nothing in this job edits Blessed's files.
- **The chain (chain rule, CLAUDE.md "Models and chats"; each chat opens the next):**
  - **Chat A, Sonnet, medium:** job 1, the full check on the five films; writes the results per film below. Also
    gathers the facts for questions 6 (cost record) and 7 (lost work on side branches).
  - **Chat B, Opus, medium:** job 2 (did it cost notes?), and questions 1, 2, 3, 8 and 10 (reading lists and old notes).
  - **Chat C, Opus, high:** job 3 (make the checker honest, with its test), and questions 4, 5 and 9 (testing the checks).
  - **Chat D, Opus, medium:** the final report, `notes/system-audit-report.md`, in plain language: what we found, what
    it did to quality, what it did to cost, what changes in how we work, and anything Sam needs to decide (numbered,
    pick first). Sent in the chat, with a push notification.
- **Rules for the chain:** report only; fix nothing in the five films. Any new rule is PROPOSED in the report, never
  written (except the rule 59 wording Sam already said yes to). Stop and push-notify if the job passes about 5% of a
  week. Write every finding here, in plain words, as you go.
- **Results:** (each chat adds its findings below)
