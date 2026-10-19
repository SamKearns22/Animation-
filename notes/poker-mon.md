# Notes for Poker Mon (one file, numbered; mark each done as it is fixed)

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word) | done? |
|---|------|------|
| 1 | "A high class and stakes poker game. They are, in fact, playing Poker Mon Cards" | |
| 2 | "The first player lays out his hand confidently. All Queens." | |
| 3 | First player says: "Four of a kind." | |
| 4 | "We 180 to the second player, who inspects their hand." | |
| 5 | Second player says: "Dragonite, use hyper beam." | |
| 6 | "The shot expands, showing that a Dragonite stands next to him in a bow tie." | |
| 7 | "The Dragonite prepares hyper beam." | |
| 8 | "We see the first player slowly lit by glowing light." | |
| 9 | "We see the scene from above at an angle, à la The Salt." | |
| 10 | "Dragonite fires the huge blast ray, hyper beam, throwing the other players and everything in the room far back off camera, à la the Salt." | |
| 11 | The joke: poker, but Pokemon cards; instead of losing, player two uses a powerful Pokemon move and destroys the game and the other players in comical explosive fashion. | |
| 12 | "Use the Pokemon brand detailing on the cards and infuse them with the standard detailing of poker cards and chips." | |
| 13 | "We never use the word Poke'mon, just Poker Mon." (on screen, in subtitles, in the Hook Text, anywhere) | |
| 14 | Use the real Pokemon imagery (Sam, 19 Oct: go ahead, no monetisation for now). | |

## References as checklists (guides/satire.md): what each photo shows, and whether ours matches (compare.py sheet)
All in `references/poker-mon/`.
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|------|------|
| queens-1..3 | Four Queens (spades, clubs, diamonds, hearts). White card, rounded corners, thin blue frame round the picture. "Q" + suit top-left, same upside down bottom-right; one big suit pip beside the queen. Mirrored double-ended portrait. Colours only red, royal blue, mustard yellow, black, white; flat bold patterns, heavy outlines. Queens three-quarter/side-on, crown, hood or veil, stiff patterned robes; most hold a flower, spades a sceptre. Spades/clubs black, hearts/diamonds red. queens-2: fanned in a real hand. | |
| card-back-1..2 | Deep blue with a lighter swirl spinning out from the centre. Poke Ball just right of centre, slight tilt: red top, white bottom, black band, white button; soft shine. Chunky yellow logo with blue outline across the top, the same upside down across the bottom (ours reads POKER MON). Plain dark blue border. | |
| dragonite-1..3 | Pear-shaped: small head, wide round belly, short stubby legs. Orange skin, cream belly with horizontal stripes, teal wing skin, white claws. Rounded snout, big friendly dark eyes, gentle smile; two thin antennae curling back from the forehead, small horn between. Small bat-like wings on the shoulders. Short arms (circle hands in our style; claws kept on the feet). Long tail, thick at the base, tapering, curled behind. Easy-going, slightly dopey (dragonite-3 is the main guide). | |
| hyper-beam-1..4 | Charge: head thrown back, mouth wide, a white ball of light grows in the mouth; eyes narrow, determined. Fire: head snaps forward and down, a thick straight beam from the mouth, white-hot core fading to yellow then orange at the edges, sparks and embers around it; wings spread, arms out, legs braced against recoil; explosion, rocks and dust where it lands. Beam colour: yellow-white (3 of 4 refs). Comic lettering "HYPERBEAM!" (not used unless Sam asks). | |
| casino-royale-1..4 | Warm golden room: cream walls, gold trim, crystal chandeliers, pale lampshades hung low over the table; cream padded armchairs; onlookers and guards in black suits behind. Big oval green felt table, thin yellow line, dark padded leather rail; dealer standing mid long side; chip stacks red, blue, white, a few green; cards face down. Players in black tuxedos and bow ties. Bond: white shirt, black bow tie, short fair hair, hands clasped in front of his mouth, steady stare. Le Chiffre: black suit and black shirt, dark slicked-back hair, scar by one eye, pushes chips with both hands. A player in a black shirt covered in playing-card patterns. Shots: wide of the table; over-the-shoulder close-up of Bond. | |

## Notes
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 |      |      |      | open   |

Decisions made (kept so a long session or a new session never has to rediscover them):
- 19 Oct: Sam chose to use the real Pokemon characters and imagery (parody, no money involved). The word Pokemon is
  never used: the cards, logo and chips say POKER MON.
- Format: TikTok vertical (1080 x 1920), Satire style, `source/poker_mon.py` from `source/satire_template.py`; no title;
  ends with the CranbriJoos sign-off via finish.py. Motion-led film: after the cast sheet, go to a quick animatic early.
- Draft shot plan (waiting on Sam's answers), about 14 s plus the 2 s sign-off:
  1. Player 1 across the table, mid shot: lays his hand face up on the felt, confident. "Four of a kind."
  2. Close insert: the four Queens on the felt, readable (staging choice, to be confirmed).
  3. 180 to player 2, close: inspects his cards. "Dragonite, use hyper beam."
  4. The shot widens: a Dragonite in a bow tie stands beside his chair; it throws its head back, light grows in its mouth.
  5. Player 1 close: slowly lit by the glow (flat bands of light creeping over him; no soft glow, house style).
  6. High angled view from above: the beam fires across the table; players, dealer, chips, cards and chairs blown far
     back and out of shot.
- Reuse: people from `views.py`/`moves.py` (sitting, gestures, things held; taking a blow and falling in stages for the
  blast); props under gravity for the cards, chips and chairs; the room on `stage.py`. New builds: Dragonite, the
  Hyper Beam, the card faces and backs, Poke Ball chips, the casino room.
