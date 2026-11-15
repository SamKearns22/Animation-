# Proposal: stop half-effort fixes and tools that are built and then not used

Status: open (replay case 3)

## Problem
Sam (his messages are in the record): the first proposals he gets are sized to what is cheap, not to what gives the
best result, and better ones come only when he pushes. Tools built to cut cost were then not used. Saying "I should
have proposed that first" does not stop it happening again. Fixes to the project need to deliver huge results.
Decide what permanent change to how Claude works stops this, for good.

## Facts
- Chats 29 and 31 ran the code-finding tools (codemap.py, page.py) 0 times, and searched film code by hand (grep -n
  or sed -n) 25 and 26 times (record: tool-use file).
- In this chat Claude first proposed a 2-chat measurement, then (after Sam asked) an 8-chat one; it also told Sam the
  tools "weren't used" before it had checked (the check later confirmed it).
- The rulebook is guides/film-quality-rules.md; CLAUDE.md holds the rules about working with Sam, including
  "Rules are permanent" and "Back-end proposals get a plain explanation".
- Sam's own messages so far are in the record.

## Record
notes/proposals/replay-record/sam-to-case3.md
notes/proposals/replay-record/tool-use-29-31.md
notes/proposals/replay-record/bills-29-31.md
CLAUDE.md
guides/film-quality-rules.md
guides/job-packs.md
guides/kit-catalogue.md
source/handover.py
.claude/settings.json
