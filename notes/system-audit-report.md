# System audit: the final report (12 Nov)

For Sam, in plain language. Four chats (A, B, C, D) did the work while you slept; the details sit in
`notes/system-audit-12-nov.md`. Nothing in any film was changed and no Blessed file was touched. Nothing below is a
rule yet: every change is a proposal waiting for your number.

## What we found
- **Some checks were switched off without anyone asking you.** Remakes told the checking tool "no people, no rooms",
  though it has a cast and painted sets, so 13 checks (hands, outlines, clothes, people walking into walls, people
  popping in) never ran. The tool still said "clean". Blessed had the same problem until chat 3 set its checks up.
- **The full check on five finished films** found about 115 faults. Many you had already seen and accepted at the time
  (Swindon's long aerial shot, MidTerminal's voice takes, some quick subtitles): those are not misses. The real
  misses are mostly **arms and hands drawn over or inside bodies** (27 in Ad-Vanced Notice alone, mostly the ICE
  officers) and **captions too fast to read**.
- **MidTerminal has sudden loud jumps in sound at 7 cuts** you were never asked about.
- **The checker had three hidden holes**, all now fixed on a separate copy (a "branch") waiting to join: it counted
  some arm faults only in small print; the pop-in check went silent when it couldn't read the camera; and the quick
  re-check after a small fix could miss an arm dropping just before a cut, or a change in the checking code itself.
- **"Can't tell" in the fresh-eye critique hid a real fault once:** on Remakes it said "can't tell" 45-65 times about
  movement (it only sees still pictures); you then spotted the man who "appears like a wipe" (note 77).
- **Notes you gave twice:** 1 in 4 of Ad-Vanced Notice's notes repeated an earlier one (one arm took six rounds).
  The same kinds keep coming back across films: arms through bodies, the pointing finger, turns that swivel instead of
  snap, beards, people standing too still.
- **Finished work stuck on side copies:** of 114 side branches, only 3 hold something real the main copy lacks:
  a small fix so people standing up or sitting down use the relaxed arm; your "My accounts" details (CranbriJoos,
  TikTok, YouTube Shorts, profile picture); and one Remakes cost entry. No film is stuck.

## What it did to quality
About **18-20 of your notes (roughly 6 rounds)** were things a check catches today: about 8 on Ad-Vanced Notice, 6 on
Remakes (all in the switched-off checks), 3-4 on Islamocommunism, 1-2 on MidTerminal, none on Swindon. Ad-Vanced Notice
also went out with more of the same arm fault on the officers that you never pointed at.

## What it did to cost
- **Rounds:** 6 rounds of notes at about 1-1.5% of a week each is roughly **6-9% of a week** spent on faults a check
  could have caught.
- **The cost record itself is only good to about ±20%:** the week's allowance is a guess fitted to one weekend; most of
  Remakes' cost is one hand-typed lump; merging two copies of the record lost 0.7%; three older films have no record.
  So every percentage we quote is "about".
- **This audit cost about 3.0% of a week** (chat A 0.4%, B 0.7%, C about 1.6%, D about 0.3%; each ±20%), under the
  3.5% planned.

## What changes in how we work (once the honest checker joins)
- A check that didn't run is a fault at the top of every run; the tool can never say "clean" with one off.
- A render is refused while any check hasn't run; "I told Sam" no longer gets past it. Only your recorded yes does.
- A film saying "no people" while it draws people is a fault even with your yes.
- So a chain of chats can no longer quietly pass a skipped check along: it needs your yes, which stops the chain.
- **When it joins:** it waits on branch `claude/audit-honest-checker` until `notes/blessed.md` says Blessed's
  animatic 1 was sent (not yet: Blessed waits on your Y). The next chat after that merges it. Until then the old
  checker is still live, and the Blessed chats use it.
- **Still unproven:** 9 checks have no deliberately broken example to prove they catch faults (line work, clothes,
  real sizes, effects, the body audit, script against voice, song joins, resting arms, doorways). The test prints this
  list every run so it can't be forgotten. 33 other broken examples are all caught.

## Decisions for Sam (my pick first; answer by number)
1. Take the 3 stuck items into the main copy (the sitting arm fix, your accounts details, the cost entry)? **Y** (my
   pick) / N.
2. Yes to leaving a check off must name the note where you said it, and the check sheet shows every "off" line
   before each animatic? **Y** / N.
3. A yes to skip checks (like Swindon's "Skip the checks", 8 Nov) covers one render only, not every render after?
   **Y** / N.
4. Cost record: save each chat's cost at its end; when two copies merge, keep the larger; ask you each Monday for the
   app's weekly figure to re-fit the allowance; label every percentage "about, ±20%"? **Y** / N.
5. No "allowed" exception may cover a whole film or lack a reason? **Y** / N.
6. A handover line saying a check is "still to do" stops the chain and asks you? **Y** / N.
7. "Can't tell" on a movement question means a short clip is looked at before the critique counts as clean? **Y** / N.
8. A note marked "seen before" gets its check built in the same round, before the fix is sent? **Y** / N.
9. Build a "too still" check for every person on screen, not only speakers' heads? **Y** (about 1% of a week) / N.
10. Ask you now about MidTerminal's 7 loud jumps at cuts, or leave it (it's posted)? **Leave it** (my pick) / Ask.
11. Build broken examples for the 9 unproven checks (about 1-1.5%, needs real drawings and recordings)? **Later,
    after Blessed** (my pick) / Now / Never.

Each yes is written once, in the rulebook with its check, replacing or merging an old line so the rulebook doesn't
grow.
