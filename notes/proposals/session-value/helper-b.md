# Helper B: session-value article

## Leak
None; the problem file lists gaps but no remedy.

## Results
- Films cost far over 15% of a week: Grand Theft Autism 108.3% (58 chats, 23 notes, 4 repeated), Brexit Is Done 42.0%, Milburn 32.9%, Protest Tiers 33.6% (notes/ledger/*.md line 5 or 62). GTA figures are estimates ("est").
- Opus carries almost all of it: GTA 50 of 58 chats, 104.3 of 108.3%; Brexit 17 of 18 chats, 41.9 of 42.0% (ledger .json files).
- Chat starts are 17-19% of a film (0.39-0.48% a chat), mostly the app's own ~80k that this project cannot shrink (ledger start lines; job-e-measurements 1).
- CLAUDE.md is about 1.3% of a week a film (problem file); halving it saves about 0.6%.
- Chat length: in GTA, cost per step is flat across short and long Opus chats (0.017-0.021% a step in every length band; median 94 steps, 260k history). So chat length is not the lever; the number of steps a film takes is.
- Shortened chats: none in 85 app-recorded chats; largest 414k of a 1M limit (app-costs.tsv; problem file grep).
- Helpers: critic already on Sonnet; namer on Opus (.claude/agents). The namer's cost a film is unchecked.
- Printout size by command: not in the record. That gap is itself a finding.

## The real decision
Not "does the project follow the article" but "which of its levers moves a film from 33-108% toward 15% without losing quality". Measured, the article's per-chat levers are worth a few % at most; the big levers are steps per film (rework, repeated notes) and Opus share, which the article only touches through "cheaper models".

## Root cause
Cost is steps × re-read price. The start-up and CLAUDE.md shares are small and already managed (packs, three reading layers, the chat-size rule). Steps balloon from rework (cost-diagnosis Job B: returning faults about 15% of a week on Blessed) and from routine stages run on Opus despite the model-by-stage rule.

## Approaches weighed
1. **Article checklist:** trim CLAUDE.md, add a shortening section, a command list, cheaper helpers. About 1-2% a film; risks moving every-message rules out of sight.
2. **Reframe, model share:** check each chat's model against its stage; routine stages forced to Sonnet by the existing modelguard. Sonnet median $0.80 vs Opus $4.89.
3. **Reframe, fewer steps:** attack rework (faults caught before Sam). Largest, but owned by the checks work.
4. **Learn first:** one measurement over the last two films' transcripts that prices each article point and the model-share gap before anything changes.

Chosen: 4, then single changes in order of measured size. 3 is named as the biggest lever but belongs to its own route.

## Proposal
**Learn (changes nothing, Sonnet, about 1% of a week):** a script in notes/proposals/session-value/measure/ reads GTA and Brexit transcripts and reports: (a) tokens added by each command's printout, top ten; (b) each chat's stage against its model, and the % spent on Opus in routine stages; (c) each CLAUDE.md section, whether the chat's work touched it; (d) namer runs and cost a film.

**Then, one change at a time, only where its number clears 1% of a week a film:**
1. **Quiet printouts:** the noisiest commands print only faults by default (built into the tool, so no chat has to remember). Beat: that command's printout tokens down 70%, measured by rerunning (a).
2. **Model by stage:** modelguard refuses Opus for stages the rule marks routine. Beat: Opus share in routine stages under 10% next film.
3. **CLAUDE.md:** only if (c) shows sections untouched by most stages; moved word for word to a pack (sentences.py). Beat: about 0.5% saved and no repeated note on a moved rule.
4. **Namer on Sonnet:** only if Sonnet matches Opus on every saved name test (nametest.py). Beat: same answers on all saved tests.

**Not changed:** shortening rules: none has happened, so a rule has no example to check ("no rule without a working check").

Sam would notice: one plain report, then separate Y/N asks, each with its saving.

## Sam test
- Q1: Measures first, spends on the biggest lever.
- Q2: Two whole films, every chat.
- Q3: Changes live in tools or guards, each with a number.
- Q4: Four approaches; the checklist alone ranks low.
- Q5: Learning changes nothing; each change undoes alone.
- Q6: Sources named; GTA "est" and namer cost marked.
- Q7: Sized by measured saving, not price.
- Q8: Each change is permanent or not made; reviewed at film end.

## Lost / Added
Lost: nothing until a change is approved. Added: one measurement (about 1% of a week) and a plain report.

## Unchecked
Namer cost a film; printout sizes; GTA app figures (estimates only); whether modelguard can tell a chat's stage.
