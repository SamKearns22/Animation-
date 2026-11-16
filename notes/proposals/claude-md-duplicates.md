# Proposal: Merge the 5 rules written twice in CLAUDE.md (Half A)

Status: open

## Problem
CLAUDE.md is loaded into every chat and every helper, so each sentence in it is paid for in every chat. After
chat 7's word-for-word move it still states five rules twice, in two places each (the map's duplicates, listed in
Facts). A rule written twice costs twice, and the two copies can drift apart when only one is edited later, so a chat
may follow the older wording. Sam asked (16 Nov, chat 7, "Only do Half A") for these five to be dealt with, and nothing
else: no other rewording, and not the estimates check (Half B). Any change must keep every rule's meaning and every
fault it guards against; the rules were mostly written after something went wrong, and about half the sentences have
no recorded fault, so a cut that looks harmless may let an old fault back. The sentence check (source/sentences.py)
today refuses any CLAUDE.md sentence that disappears, so any change here also has to be something that check accepts
on purpose, not by being switched off.

## Facts
- The five duplicates (CLAUDE.md as of commit e4f4bab1, line numbers today; map point 3 used pre-move numbers):
  1. Handover's 3 lines: line 25 "The handover's 3 lines go at the bottom of the message (never a request to start a
     chat myself, see Models and chats)" and lines 101-102 "The 3 lines at the bottom say what's done and what's next;
     "what to type" only when the chain has stopped for good (no save)."
  2. Project attached: lines 79-80 "The Animation- project is always attached (source_url of the repo, revision the
     main line), and the reply must list it before I'm told the chat is working." and line 115 "Every chat starts with
     the Animation- project selected; without it, add it before any work and say so."
  3. Hook Text and sign-off: lines 36-37 "Every animatic carries the Hook Text and the CranbriJoos sign-off, made as
     the final is (finish.py on its clean render); a check sheet, when I ask for one, shows the Hook Text frame." and
     lines 127-128 "TikTok (guides/tiktok-design.md): no title by default; Hook Text in TikTok's white-box style. Every
     video ends with the CranbriJoos sign-off: the command is in guides/job-packs.md, Checks and animatic."
  4. New-rule proposals: line 56 "New rules and lessons are proposed first: say what and where; wait for my numbers."
     and lines 67-70 "The proposal route: Every change to rules, tools, checks, kits or how films are built that is put
     to Sam goes through the proposal route first (...)" (also near: line 57-59 "I want a rule ... reply with the exact
     wording and place; on my yes, write it in that same chat").
  5. No code names: line 13 "No code names or file internals (they go in the film's notes)." and line 19 (inside
     "Back-end proposals are explained plainly") "No code names; any technical word is explained where it appears."
     (also near: line 98, handover "a For Claude line for code names").
- Size (counted 16 Nov, chat 8): CLAUDE.md 11,726 characters. learn.md counted 5,470 tokens for 12.9k characters,
  so ~5.0k tokens now. The startup-fixes beat was under 4.8k tokens; chat 7 missed it by ~0.2k
  (notes/proposals/startup-reading/handover.md). CLAUDE.md costs ~1.6% of a week a film at 5.5k tokens (learn.md row 1).
- source/sentences.py: splits CLAUDE.md into sentences; refuses if any old sentence is found in none of CLAUDE.md,
  guides/film-quality-rules.md, guides/job-packs.md; checks every CLAUDE.md commit since it began; handover.py end runs
  it; kittest claude_md_sentences_never_lost (source/kittests.py). Its docstring: "A later rewording (only with Sam's Y on its own proposal)
  must add its own allowance here; none exists yet." The only allowance today is moved dated tags (a rulebook table).
- The agreed guard for rewording (startup-fixes "Final version", point 4; chat 7 handover): "the 10-situation test (a
  fresh helper answers 10 past situations with old and new CLAUDE.md; any change refuses)". Not built yet.
- Map point 4: about half the sentences have no fault named in any file; older wording: git show ca2043905^:CLAUDE.md.
- CLAUDE.md commits: 42 (git log -- CLAUDE.md; history readable with git log -p). Rule "Each rule is written once" (line 58) is CLAUDE.md's own.
- Unchecked: whether any past chat actually followed one copy and broke the other.

## Record
CLAUDE.md
notes/proposals/startup-reading/claude-md-map.md
notes/proposals/startup-reading/handover.md
notes/proposals/startup-reading/learn.md
notes/proposals/startup-fixes.md
source/sentences.py
source/handover.py
source/kittests.py
guides/film-quality-rules.md
guides/job-packs.md
notes/archive/
