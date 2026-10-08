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
