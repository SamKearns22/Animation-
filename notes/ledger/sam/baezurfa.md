# Sam's messages, chat cse_01J1JB7ZDeRUXyAPbaEZurfA (handover.py log)

### 2026-11-18T10:53:52
Milburn came in at 22% of a week in total according to my manual check (71%-93%). 

1.  What did you record as the total usage cost of this film?

2. This was decent but outside of our 15% budget. Explain what would have to change or improve in order to hit this target?

### 2026-11-18T11:02:57
1. It is only worth taking a cost estimation once the whole film's screenplay was provided. It came through in chunks and you shouldn't cost a lone chunk.

2. You keep changing your mind on the handover strategy. Recently, you proposed hanging over at roughly 100 (letting it go longer to finish a job up to 150) in order to save costs on handovers. This appears to have reduced costs successfully so I don't trust your current opinion.

3. You are the one who sets the plan for changing model. Your already existing guidance tells you to assign the best model for the task. Why didn't you follow your own guidance or are you wrong about your assertion here.

4. My understanding is that you've just built a tool map and code finder function in the last round of improvements. Were these used?

5. You built a tool for a shot-by-shot sheet in the last round of improvements. Why did you not use it?

And why do you not already record cost with real app figures?

### 2026-11-18T11:15:05
1. 15% is our goal for all films and what we are working for, which you should be aware of as you should always be aware of statement one when we discuss tools and processes.

3. I follow your advice on model efforts.

4. That is a serious problem. As for the tool map, it sounds like we should have one. 

5. The board check tool is the shot board (rule 11). It is already on the main line, claude/create-claude-md-oe8z4g, so merge that first if your branch is older.

It’s a command in source/rough.py. Run python3 source/rough.py board FILM OUT.jpg. It draws every shot on one sheet, with the real camera, the cast at their marks, and a row of notes under each shot.
The rows come from story/FILM-board.txt. Each shot has a block of camera, lead, focus, next focus, match and choices.
After the sheet reaches me, run python3 source/rough.py sent FILM OUT.jpg --delivered --board. That records it as sent.
The pre-flight refuses to build any movement until a delivered board exists. It also refuses a shot with nobody in it.
For the rules, read rule 11 in guides/film-quality-rules.md. For where it sits in the workflow, read the Plan pack in guides/job-packs.md, under Bite.

The Milburn film’s board is a working example: story/milburn-board.txt and story/milburn-board-sent.txt.

### 2026-11-18T11:49:56
The key thing missing from your proposal is that almost all of the searches did not use the code search tool developed for it, which surely has been our biggest and most damming overspend.

### 2026-11-18T11:50:34
Y

