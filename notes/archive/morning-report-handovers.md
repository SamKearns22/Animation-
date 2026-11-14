
## Critic bench, next steps (Sam, 14 Nov: N to Sonnet for now; "know definitively"; acting must be covered)
Where things stand (critic bench, chat 3 onward):
- **Rules that bite next:** 89 (critique), 13/83 (set checks), 30. CLAUDE.md: before suggesting or building a check, find the closest rule; an edit beats a new check.
- **Done:** Remakes test scored; close-ups in every pack; overnight work billed apart (ledger).
- **Next (Opus, high effort, chat 3):** (1) Acting key: from Sam's face and body notes on Blessed and Remakes (e.g. Remakes 31/58 doubtful look, 53 terrified, 62 tipping to aim, 54/57 KG's moods), scored apart from the checklist faults. (2) Repeat test: Sonnet chat runs each critic 3 times on both films with close-ups, reports the spread, checklist score and acting score; rule: switch to Sonnet only if it matches Opus on both across all runs, else split (Sonnet checklist, Opus acting). Stop at 2.5% of a week.
- **Place checks (edits, found 14 Nov):** townsfolk in walls = rule 13 / `setcheck.moving_faults` and rule 5 already exist; Remakes' town street has no SET_FEET, so give it SET_FEET (data, no new tool). Banner in one shot = checklist S6 already says "one frame per shot of the set, side by side" but `critique.py pack` never builds that sheet: edit pack to build it per set. Hazed near flower box: nothing in the rulebook; closest rule 83 and `critique.py where`: add one small draw-order check (near things drawn after the haze).
- **Needs Sam:** Y/N on the wording below (open rule request).
- **Open rule request:** CLAUDE.md "Before suggesting anything" line: add "or building": "Before suggesting or building anything (rule, tool, check or idea), search the rulebook and kit catalogue; if an existing rule or tool needs only an edit, edit it; each names the closest one and what is new."
- **Read:** `guides/job-packs.md` tool jobs; source/critbench.py MAP; source/critique.py closeups.
- **For Claude:** bench files source/bench/remakes-a3*.json (code at 98cc08d); `critbench.py make CASE`, agent line it prints, `score`.

