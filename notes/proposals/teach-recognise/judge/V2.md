# Helper B: how to stop broken drawings reaching Sam

## Leak
The problem file hints at answers (shape measures, "phone size", lesson 22); so does the film notes' v7 note 10. I
opened chat.md by mistake while listing the folder; nothing below rests on it.

## Results
- Shot 4: 7 versions, about 12 chats (problem file) at 1.1-3.3% each (ledger): roughly 20-25% of a week (unchecked).
  Film forecast 93.4% (notes/ledger/grand-theft-autism.md).
- Sam's notes: v4 16 notes, 8 of them broken bodies (case study s.7, cause A); v7 10 notes, 3 repeats, 4 about the
  drawn body (case study s.15).
- **Every one of the film's 34 critique panels had close-ups switched off** (`"closeups": false` in all eight specs,
  source/data/critique-src/grand-theft-autism/). Rule 89 requires a close-up of every person (it took the critic from
  4 to 7 of 12 on Blessed). The pack only warns (critique.py line 492); turning close-ups off silences it.
- The critic saw the frame: round 22's crash panel (v8-crash.jpg, 540 px, shown at 270 px) holds the same L-shaped
  arm with the thumb-stub. It asked twice for what it needed: round 21 "a close full-size crop of Jason's arm at the
  shoulder would show it"; round 22 "a full-size crop of the hand and the head would show it" (ledger round-21/22).
  CAN'T TELL never blocks (rule 89), so the clip went.
- Up close it can see them: on v4 a cold critic named "a stubby tube arm with no clear shoulder join", 2 of 8 body
  notes caught, 3 half (big-body-moves/learn.md). Checklist line P3 already says "no rubber or broken arm".
- Gap: how many of Sam's ~25 pictured faults the critic finds at full size is unmeasured.

## The real decision
Not "teach Claude to see" but: why does the whole chain let a broken frame reach Sam? The eye exists, asked for the
picture, was refused it, and its doubt never stops a send.

## Root cause
1. The flat figure is drawn into views where it breaks; the bone rebuild left drawn thickness alone (1.26-1.37x, problem file).
2. Machine checks test bones; lesson 17 (20 Nov, "test the drawn picture") was never built.
3. The one picture-reading check was starved by an opt-out and ungated by CAN'T TELL. Earlier fixes added point checks, not picture checks.

## Approaches weighed
1. Teach by example: Sam's labelled pictures in every pack. Unmeasured.
2. Reframe, enforce the eye: close-ups cannot be switched off; a CAN'T TELL asking for a crop gets it and a fresh look before sending.
3. Prevent at source: score cameras for views that break flat drawings.
4. Measure drawn shapes in code (limb thickness to length, shoulder join, hand contact).
5. Learn first: a bench of Sam's pictures, measured.
Chosen: 5, then 2, then 4 or 1 or 3 only where the bench shows a gap.

## Proposal
**Learn (changes nothing; about 2% of a week: Opus medium, three Sonnet helpers at 0.5%).** Add Sam's ~25 pictured
faults, each with its full frame and a clean frame of the same shot, to the critic bench for good. Run it three ways:
as run here; with close-ups; with close-ups plus three labelled examples. Count catches and false alarms per kind.
**Change 1 (own Y): enforce the eye.** The pack refuses close-ups off on any person panel and refuses a picture panel
without people boxes; a CAN'T TELL that names a crop builds that crop and re-asks one helper; pre-flight refuses a
send until it is answered or named on a "Checks:" line. To beat: the bench's close-up score, and Sam's
body notes per clip next film below shot 4's (8, then 4).
**Change 2 (own Y, only for a kind the bench shows close-ups still miss):** the measure or the examples that close it,
each with its own bench number.
Each judged at film end. Cost after: about 0.5% a film (unchecked), against ~20% here.
Sam would notice: fewer broken bodies; a "Checks:" line when the critic could not tell.

## Sam test
Q1: an expert measures and enforces the existing eye before building a new one.
Q2: all of Sam's pictures, not one frame.
Q3: refusal in code; success counted on the bench and in Sam's notes.
Q4: five different approaches weighed.
Q5: removes nothing Sam sees; each undone alone.
Q6: sources named; estimates marked.
Q7: sized by catching Sam's faults, not by price; the bench is kept.
Q8: permanent; reviewed at film end.

## Lost / Added
Lost: a chat's option to turn person close-ups off.
Added: a permanent bench of Sam's pictures; larger critique packs; a send held while the critic cannot tell.

## Unchecked
Cost figures; that the "v8" specs are Sam's v7 clip and his crop the crash panel's instant (same pose seen).
