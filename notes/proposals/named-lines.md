# Proposal: Checks that are always red or always "named" are noise, so real faults hide among them

Status: open (un-parked 22 Nov, Sam: "Milburn: begin all"; his 19 Nov words below still stand)

## Problem
Before every animatic, pre-flight (the checks run before an animatic) printed 48 lines on Milburn that chats "named"
(listed to Sam as known) instead of fixing, growing to 61; two kit tests (the automatic tests of the shared tools)
stayed failing for the whole film, and two "before Sam approves" tests were stale. A line that is always there is
never read: the real clipping fault (could-not-test) sat among them. Milburn review section 1 items 6 and 7, lesson 2.
Sam (19 Nov): no check is deleted; each old line is fixed, or dropped only under the three-films rule (CLAUDE.md: a
step is removed only if it caught nothing in three films, with Sam's Y on a "Lost:" line).

Merged in (22 Nov, same cause: false lines in the checks): On Milburn, chat 18 removed 60 false lines from pre-flight (the checks run before every animatic) by making the film's
own code hand the checks the cleaned voice takes. The fix lives in that film's code only, so the next film starts with
the same 60 false lines. False lines bury real faults: Milburn's real clipping fault sat among 48 to 61 named lines.
Milburn review lesson 4 and section 1 item 5; Sam put it third in the queue (19 Nov).

## Facts
- notes/archive/milburn.md line 20 (chat 15): 48 quick-check lines, "the same 48 as chat 13 (plan gaps, SHOT CAST
  'never on screen' for want of scene(t), house-style lists missing, two fast captions, the 'fucker' bleep waiting on
  Sam's recording, clipcheck COULD NOT TEST), none new; named to Sam ... not settled (each needs a build)".
- notes/archive/milburn.md line 13 (chat 18): 60 lines left named after 60 false ones were removed: the old 48, 12 more
  "too fast to read" captions, 2 syllable counts.
- Picture checks: 28-31 faults each animatic (HANDS 14-17, LAP 14), "file identical to animatic 1's: not new"
  (milburn.md lines 13, 16, 20).
- Kit tests round_page and facehouse_whole_head failing before and through the film
  (notes/archive/milburn-handovers.md lines 23, 33); `handover.py start` on 19 Nov still prints both as BROKEN, plus
  "cost_faults has no promise in the watcher".
- Chat 11 asked Sam to approve fixing the stale tests; the guard stopped the ask (notes/proposals/unrouted.md,
  2026-11-18 06:11); nothing was fixed.
- CLAUDE.md "Rules are permanent": remove a step only if it caught nothing in three films, with Sam's Y on a Lost line.

- notes/archive/milburn.md line 13 (chat 18): "milburn.py now hands the checks the cleaned takes (`_voice`,
  `_stretches`, `n` per line), which removed 60 false script/mouth lines; 60 lines left named".
- notes/proposals/milburn-review.md section 1 item 5: "Improved the film, not the tool ... only for this film".
- The shared checks: source/preflight.py (unchecked name; search), source/kitchecks.py, source/audit.py.
- The film template new films start from: source/satire_template.py (rule 75 names it).
- How many other check fixes went into film code instead of shared tools across Blessed and Milburn: unchecked.

## Record
notes/archive/milburn.md
notes/archive/milburn-handovers.md
notes/proposals/milburn-review.md
notes/proposals/unrouted.md
source/kittests.py
source/kitchecks.py
source/watcher.py
source/handover.py
CLAUDE.md
source/milburn.py
source/satire_template.py
source/audit.py
source/
guides/kit-catalogue.md
