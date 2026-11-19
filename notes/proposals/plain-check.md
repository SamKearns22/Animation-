# Proposal: The plain-language rule has no check, so system-change asks reach Sam unexplained

Status: open

## Problem
CLAUDE.md's rule "Back-end proposals are explained plainly" says every proposal Sam can't see (a check, a tool, a
rule, a change to how films are built) reaches him as: the problem in one or two plain sentences, numbered steps,
why, what he'd notice, the other option, one Lost/Added line each, no code names, every technical word explained where
it appears. Nothing enforces it. In the Milburn end-of-film review chat (19 Nov) the lessons went to Sam as one-line
summaries full of unexplained words, and Sam said he is struggling to follow the chats. Sam (19 Nov): "A rule should
function. If it doesn't function, you built it wrong." He asked for this first ("fix now"). The decision: what makes
every message that asks Sam to approve a system change follow the rule, in every chat, without Sam checking it.

## Facts
- The rule's text: CLAUDE.md lines 16-19 (section "Messages to me"). Its row in the rulebook's last table
  (guides/film-quality-rules.md, "Dates moved from CLAUDE.md") names no check.
- The only check on Sam-bound asks is the Stop hook `source/propose.py hook` (a script the chat app runs each time a
  chat finishes a reply; it can send the reply back once with a reason). It looks at lines that ask Sam to approve
  something (`questions`, `is_change`) and requires only: a judged proposal file named in the reply (a verdict with a
  valid hash) and the "Critiqued: N found, N fixed, N named" line. It reads nothing about the message's shape or words
  (source/propose.py lines ~361-490).
- The hook blocks at most once per reply: on the second try (`stop_hook_active`) it lets the reply through and logs it
  to notes/proposals/unrouted.md, which `handover.py end` flags. 8 such let-throughs are logged 19 Nov alone
  (notes/proposals/unrouted.md, last 8 lines).
- The test case that must fail: notes/proposals/milburn-review.md section 3 ("Lessons, each proposal-ready"): 10
  lessons, each one paragraph of "Problem / Steps (a)(b)(c) / Added / Lost / Other option". None has "why" or "what
  you'd notice"; steps are lettered inline, not numbered lines; unexplained words include guard, pre-flight, kit,
  ledger, named lines, kittest, Stop hook-style names, "3/4-parts rule", "milburn.py", "chain depth", "0.14 brow cap".
  The review chat's own record (session_01J1JB7ZUimqTBbLiqdPxYKr) shows these went to Sam (the earlier events are
  past the 100 the chat record returns at once; unchecked word for word).
- The route's own output for Sam does not follow the rule either: guides/proposal-route/judge.md's "For Sam" shape is
  "Option N: short name / plain English, 3-6 lines / Lost / Added", and `propose.py show` prints it as is. Example,
  `propose.py show front-on-focus` (19 Nov): each option is one paragraph, no numbered steps, no "what you'd notice",
  words like "the BoJack way", "house head", "planning step", "best tool" unexplained.
- What Sam is sent is also routine (animatics, clips, notes): those are not covered by this rule and must not be slowed.
- Earlier guard fixes: notes/proposals/guard-holes.md (15 Nov) widened what counts as a change ask; kittest
  `proposal_route_hook` in source/kittests.py tests the hook (asks blocked, routine passes).
- No list exists of which words in this project count as "technical" for Sam (unchecked; searched guides/ for
  "glossary": none found).
- Sam uses only an iPhone and does not code (CLAUDE.md "Working with me").

## Record
CLAUDE.md
source/propose.py
guides/proposal-route/judge.md
notes/proposals/milburn-review.md
notes/proposals/unrouted.md
notes/proposals/guard-holes.md
source/kittests.py
guides/film-quality-rules.md
