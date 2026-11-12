# Follow call to action on the sign-off (12 Nov): built. Sam: Y to all; lines 4-15 for the next 12 films, then a new batch

## Brief (Sam, 12 Nov)
- A follow call to action on the sign-off (watchers to the end are the likeliest followers).
- Hook Text style (TikTok Sans Bold, black on white rounded boxes), top left, on a diagonal.
- 1.6 s only, so it must use every proven call-to-action trick. Goal: follows.

## What the research says (short)
- Reading: adults read about 4 words a second (Brysbaert 2019 meta-analysis, ~240 wpm silent); with a 0.15 s pop and
  the beaver competing for the eye, ~1.4 s of reading = **5 words at most, 4 better**.
- Creator advice (TikTok/IG marketers; Hootsuite figure of "30-50% more follows with a clear follow CTA" is quoted
  second-hand, unverified): say **what they get by following**, one action only, verb first.
- Sales levers that fit in 5 words: a clear single command (verb first); the benefit ("more of what you just
  laughed at"); a pointer to the button (directional cue: eyes follow arrows and gaze); humour to lower resistance to
  being sold to (reactance); a likeable mascot asking (liking, mild guilt); consistency with the bio ("Follow to
  'lmao'", "nonsense").
- Rejected: "Follow for part 2" (no part 2: a broken promise costs trust), follower counts (social proof is weak at
  our size), "tomorrow" (we post 3-4 a week, not daily), long benefit lists, all caps (reads as shouting, slower).

## Critique rounds
1. First mock: narrow card wrapped to 3 rows (slow to read), sat on the fire. Fix: 700 px wide, 2 rows max.
2. Placement: the top 310 px is under TikTok's tabs, so "top left" = just below them, over the picture's top-left
   corner and the white above it, never the face. White box on white paper vanished: a soft shadow down-right fixes it.
3. Tilt: 7 degrees **down to the right**, ending in 👉, so the whole card points towards TikTok's + follow button
   (right side, ~45% down). Pops in on the sign-off's first frame (rule 75 pop) and stays to the end.
4. Measurement: followers per 1,000 views is ~1-2 now, i.e. 5-20 follows a film, so one film proves nothing.
   Alternate two lines film by film for 4 weeks (~14 films), compare with the 14 films before, keep the winner.

## Shortlist (mock: `cta-options.jpg`, not on GitHub)
1. "Follow for more nonsense 👉" - benefit + brand voice + pointer. Pick A.
2. "Follow. The beaver is thirsty 👉" - joke + mascot's plea. Pick B.
3. "Follow for next week's news 👉" - series promise; reads serious, not funny. Reserve.

## Build (once Sam says go)
- `finish.py`/`signoff.py`: the card drawn by `hook_text.card` (x_mid 440, width 700, y 400), tilted -7°, shadow,
  laid at (70, 318) from the sign-off's first frame; line chosen per film (`--cta`, default alternates A/B), logged
  in `story/metrics.md` per film. Kittest: card present on every sign-off frame, inside x 60-900 / below y 310.
- Rule: replace rule 52 (see the message to Sam), no new row.

## More options (Sam asked, 12 Nov; 4-9 mocked in `cta-more-options.jpg`, not on GitHub)
4. "Next one's worse. Follow 👉" - curiosity + promise, joke. 5. "Follow if you got that 👉" - flatters the viewer
(in-group). 6. "Follow. It's free 👉" - absurdly obvious, low effort. 7. "Feed the beaver. Follow 👉" - mascot plea.
8. "A crow says follow 👉" - callback to the bio's crow quote. 9. "Follow. We ruin the news 👉" - says what we do.
Text only: 10 "Don't miss the next one 👉" (fear of missing out, no joke); 11 "Follow or the beaver cries 👉";
12 "Follow for weekly chaos 👉"; 13 "One tap. Zero regrets 👉" (no "follow": weaker); 14 "Definitely don't follow 👉"
(reverse psychology: too slow to decode in 1.6 s); 15 "Your mum would follow 👉".
