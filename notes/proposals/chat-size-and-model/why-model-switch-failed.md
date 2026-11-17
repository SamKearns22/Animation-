# Why the routine-work model switch stopped working (17 Nov, from the Protest Tiers notes' Next lines in git)
1. Splice moved the animatic into the Opus round. 15 Nov 18:49, chat 31 (Sonnet) made animatic 3 by splicing fixed
   clips into animatic 2 (216014a8): cheap and right. From 16 Nov 12:46 every Next line gives the Opus medium notes
   chat "clips with `final --span` ... splice fixed seconds into animations/drafts/protest-tiers-animatic.mp4", so
   the animatic is now made inside the Opus fix chat. handover.py ROUTINE skips `--span` on purpose and has no word
   "splice", so model_faults never fired.
2. The rule itself puts clips and "building from ... sound" on Opus medium (CLAUDE.md Models by stage), so France
   chat 7 (look, check, clip) and chat 8 (sound) on Opus were by the rule as written; the check followed the rule.
3. The check reads only the film notes' first Next line, at start and end. It never sees the model a chat is
   actually opened on (create_session), nor what a chain does. 16 Nov's country chains (Albania, Germany, France)
   were opened from Sam's phone/web and passed work in their own prompts; the notes said "Opus medium" for all.
4. Before 15 Nov 17:29 (e2db044b) there was no check at all (Blessed, Remakes: stages bundled in Opus chats).
