# Notes for CRY MINISTER (one file, numbered; mark each done as it is fixed)
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | wolves | - | Side-on open jaws must be see-through (no red fill between the jaws). Front view keeps the dark throat. | done |
| 2 | 12 | wide | Bring the street down to his feet: no empty pavement between him and the shops. | done |
| 3 | most | - | Behind him: half pub, half ZapBets, the wolves feeding in the background. | done |
| 4 | 12 | sky | A charming church spire behind the pub; a drab, functional office block on the right. | done |
| 5 | - | - | More graffiti tags on the boarded-up shop. | done |
| 6 | - | - | A drunk lying face down in a puddle outside the boarded-up shop. | done |
| 7 | - | - | Shoppers passing, now and then glancing at the wolves or the Prime Minister. | done |
| 8 | all | - | The full TikTok screen on every frame (search bar, buttons and counts, account picture, name, description, progress bar), placed so the real app never hides it completely. Replaces the little white caption. | done |
| 9 | 6 | - | Kevlar on her arms too; the wolf chews on it without success. | done |
| 10 | 13-14 | - | Andy's stress level: 4, Haunted. | done |
| 11 | 2+ | - | The attacked man must be a proper character, not a flat blob. | done |
| 12 | 5 | - | Running arms were wrong (crossed on his chest). | done |
| 13 | 5 | - | The net falls on the wolf. | done |
| 14 | 6 | - | The old lady extends her armoured arm; the wolf gnaws on it. | done |
| 15 | all | - | Remove the pub's hanging sign (looked rude). | done |
| 16 | 12 | wide | Andy was huge next to tiny shoppers; graffiti looked like WordArt (hand-drawn mix used; Sam never picked from the 6 styles). | done |
| 17 | 20 | - | Andy's mouth vanished (wrong mouth shape name). | done |
| 18 | all | - | Remove every sound made in code. Film is voice only. | done |
| 19 | shoppers | - | Drawn in the show's usual people style (conference-goer models, changed up). | done |
| 20 | man | - | Man City shirt from Sam's reference photo. | done |
| 21 | 1 | - | Shopper in the nearer lane looked child-sized: nearer lane drawn bigger. | done |
| 22 | all | - | Walkers faced forward while moving sideways: new three-quarter walk (walker.py). | done |
| 23 | 2 | 4.4 s | A wolf overshot the man: the right-hand wolves sweep in from the right. | done |
| 24 | 2 | 7 s | The man at the back stops, frowns and shakes his head. | done |
| 25 | 5 | - | The falling net dipped below the floor: its hem now stops at the ground. | done |
| 26 | 20 | - | Chasers a mix of full and smaller wolves; Andy angry / terrified / panicked, no red eyes (red eyes only in 13-14). | done |
| 27 | 15 | - | More despairing on "I CAN'T stop every wolf attack". | done |
| 28 | all | - | No in-video title (tested on TikTok; title on the cover). | done |
| 29 | 20 | - | His selfie arm ended in a dark block (read as a second phone): the arm now reaches to the lens and leaves the frame bottom left. | done (in code; not yet rendered) |
| 30 | 20 | "here come" | He looked away from the wolves: now glances back over his shoulder at them, then back to us. | done (in code; not yet rendered) |
| 31 | 20 | - | Blank red buildings on the right: now shop fronts, fascia boards, doors, sash windows, drainpipes. | done (in code; not yet rendered) |
| 32 | all | - | Crackles (Sam heard them still after the first fix): the film was turned up 7 dB over the recordings and every loud word squashed by up to 8 dB in milliseconds. Now the loud stretches are eased down gently (over 30 ms, back over 300 ms), at most 3 dB of soft limiting on a few bursts, mastered at -16.8 LUFS (was -14). | done (in code; not yet rendered) |
| 33 | 2 | 6-9.9 s | The man in blue barely reacted: now stops dead, hands on hips, a hard frown at the pack, three slow big head shakes, then walks on. | done (in code; not yet rendered) |
| 34 | shoppers | - | Walkers looked too thin: body squeezed less (0.78 to 0.9), legs thicker. | done (in code; not yet rendered) |
| 35 | 20 | - | Two mouths at once: the gritted teeth were drawn over his talking mouth. Now only when the talking mouth is off; between "Aw fook" shouts, gritted teeth instead of a lopsided smirk. | done (in code; not yet rendered) |
| 36 | 20 | - | Arm higher, holding the phone up for the over-the-shoulder view: it now rises out of the frame on the left above the name and description. | done (in code; not yet rendered) |
| 37 | ZapBets | - | Advertising window: Sam picked option 3, a yellow poster in both windows: FREE £10 BET for new customers*, small print "*18+. Must not be currently being eaten." | done (in code; not yet rendered) |
| 38 | all | after lines 1, 12, 13, 15, 17 | Crackles at line ends. In Sam's recordings too (he checked): the phone's voice clean-up chopped the final "s"/"z"/"k" hiss into bursts (about 12 a second) and a thump, made obvious by the film's extra volume. Now each line's tail keeps its real consonant, then only ever fades (smooth_tail); lines Sam ran together (16-18) stay one unbroken piece; soft 100 ms end fades; the tone matching never brightens above 4 kHz. | done (in code; not yet rendered) |

Decisions made (kept so a long session or a new session never has to rediscover them):
- Brief: `prompts/cry-minister.md`. Code: `source/cryminister.py` (film), `source/wolf.py` (the dire wolves, reusable).
- Sam's answers (8 Oct): one take per line, recorded indoors; TikTok look only hinted (handheld drift, parody handle
  @TheTikTokPM, one short on-screen caption of his, no fake buttons, no real logos: later changed by Sam to the full
  made-up TikTok screen, note 8); gore = flat red cartoon blood, the man
  hidden under the pack, meat flung up; the same five wolves chase him at the end; full script kept (film is about 63 s);
  shot 4 is an instant pop to 60%; title CRY MINISTER on two lines, held 2.5 s.
- Captions copy Andy's own TikTok captions: TikTok Sans Bold (free font, `source/fonts/TikTokSans-Bold.woff`), white,
  soft dark shadow, at most 3 words / 18 letters at a time, each chunk shown as it is said, sitting just under his chin.
- Recordings (`source/audio/cry-*.m4a`): files named after first words. `cry-4-6` holds lines 4-6 (cut at 2.72 and 5.42 s,
  Sam's pauses); `cry-16-18` holds lines 16-18 run together (cut at 2.235 and 2.67 s, the quietest moments between the
  words, found with the PocketSphinx speech recogniser). Voices: hum and hiss out, takes matched in tone (each nudged
  towards the average, at most 4 dB), every line at the same loudness (lines from one file keep their balance).
- Andy films himself (phone framing with small held shifts), talks into the lens. Street plane framed per shot (hard cuts).
- High street, left to right: Cash 4 Gold, The Goose and Cranberry (Tudor pub), ZapBets (behind Andy), the boarded-up shop
  (TO LET, faded sign), Nails & Vapes. The kill happens in front of the pub and stays (blood pool, landed meat) for every
  later shot of it (2, 12, 17).
- Shot 5: one-point view down the alley; the man runs at us, ducks under the council WOLF NET and veers out of frame; the
  wolf leaps at him and is tangled; the net stays sagged round it.
- Shot 6: the armour and the biting wolf appear on "wolfproof"; the wolf stands on the pavement, jaws on her forearm guard.
- Shot 20: selfie over his shoulder, wolves bounding up the street behind him, gaining; the lead wolf leaps at the lens on
  the last half second, hard cut to black.
- Sam said "Go" (8 Oct) without answering the rest, so the recommended answers were taken: I make the wolf sounds in code
  (crunching, tearing, growls, a yappy growl after the pop, paws, his running feet, the net), the lead wolf leaps at the
  lens on the last half second, line 1 kept as recorded. The description reads "Tough on wolves. Tough on the causes of
  wolves." (Sam may change it: `DESCRIPTION`).
- Effects dip 10 dB under every stretch of speech (the voice stays at least 6 dB above everything: checked).
- Captions: chunks close at a full stop, or once on screen about 0.75 s; a stray last word joins the one before.
