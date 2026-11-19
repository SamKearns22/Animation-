# Proposal: scheduled-jobs-attach

Status: open

## Problem
On 19 Nov at 17:01 four timed jobs Sam queued fired and every one opened with no project attached, so none could work. The chat that queued them reported them as queued without anything checking they could run.

## Facts
- The four jobs (trig_0142kNie.., trig_018Pueb.., trig_01TwQ8fJ.., trig_01SVHnkT..) have last_run SUCCEEDED at 17:01 with no source repository in their record (list_triggers include_completed, 19 Nov).
- create_trigger has no repository or source field; create_session does (source_url, revision). Sessions made with create_session at 17:15-17:17 show the repository attached (get_session).
- The failure was seen only when Sam read it at 17:14 (notes/ledger/sam/7r62524n.md).
- Earlier timed reminders (Nov 11-18) bound to an existing session (persistent_session_id) ran fine.
- CLAUDE.md says a chat opening the next chat uses create_session with the project attached.

## Record
notes/ledger/sam/h3akq5qv.md
notes/ledger/sam/7r62524n.md
story/status.md
