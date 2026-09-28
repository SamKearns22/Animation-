# Horror shot: 'Merry Chr' (the spare room)

(The director's brief, then the notes we work from.)

> A scene the viewer has only a moment to absorb, when the music is at its most insane and distorted.
>
> **Camera:** still, in the centre of the room's doorway, staring in at head height, as if transfixed.
>
> **Location:** a historic vaulted spare room in the family's early 18th century American home (wealth and
> prestige; think the Home Alone house with 18th century detailing blended with contemporary design). A large
> double bed against the left wall; a dresser, desk and window on the right; at the back right an open doorway
> to an en-suite. Varnished hardwood floor, a rug at the centre. Everything incredibly clean, except where the
> events have touched it.
>
> **Scene:** the room has been trashed in a mad, pointless explosion of domestic destruction: glass, shredded
> bedsheets and 'coming home for Christmas' luggage strewn across the floor. On the bed - where the eye goes
> first - a huge, poorly wrapped Christmas present, soiled with dark liquid and worse, the rough length of a
> person, parts pushing against the paper from inside; the sheets under it sodden and dark. Is that a
> chopped-up body wrapped in Christmas paper and ribbon?
>
> The back wall is largely bare. 'Merry Chr' is scrawled on it in fresh, dripping gore, wildly. At the r, a man
> in his early fifties, in a simple shirt and dark blue trousers, kneels towards the wall, robotically slamming
> his head, with controlled force, against the r. Thud... thud. He wrote the words with his forehead's blood and
> can now only hit the r. He stays on his knees as we stare.
>
> **Look:** as always, only certain colours show: Christmas decorations, strewn Christmas clothing, the bright
> red blood of the message and the growing mess round the r, and the dark gore seeping from under the present.

## How it is built
- Recipe: `source/shots/h1_merry_chr.py`. Set: `source/spare_room.py`. What happened there (present, stains,
  writing, wreckage): `source/merry_chr.py`. The man: `source/man.py` (MakeHuman, about 52, kneeling).
- The room: a guest room up under the roof - white plaster vault with the old oak tie beams and ridge beam
  exposed, a lantern hanging from the ridge, panelled walls to dado height, oak floorboards, a Persian rug.
  Mahogany bed with a tall arched headboard against the left wall; chest of drawers with a smashed gilt
  mirror, a shuttered sash window with a wreath, a writing desk (its chair knocked over) on the right; a
  bright white contemporary en-suite through the doorway at the back right.
- Colour (coloured pencil over graphite): the present's green star paper and gold ribbon; the red Christmas
  jumper, Santa hat and small presents spilled from the suitcase; the wreath; the fairy lights; bright blood on
  the wall; near-black red gore on and under the present. Everything else graphite.
- The writing is worked out stroke by stroke: forehead-wide smears that thin and break into streaks as the
  blood runs out along each stroke, drips from the heavy parts, 'Merry' big and energetic, 'Chr' smaller,
  lower and wilder; round the last r a blotch, spatter flung outwards and heavy runs down to the floor.
- Checks (`checks.py`): his knees rest on the floor, it is his forehead (not his nose) that meets the wall,
  and it touches it (0-6 mm), his sleeves cover his forearms.

## Still open (for the animated version)
- The head strikes: pull back ~6 cm and strike, on a slow, mechanical rhythm locked to the THUDs; a tiny
  recoil in the shoulders; nothing else in the room moves.
- **Director's decision (animation session):** the blood does NOT grow. He is weak, mostly dead, drained
  against this wall - there is no more blood to give. The wall stays exactly as in the still; he strikes the
  same wet spot (the middle of the blotch at the r) every time. A drained man: the small end of the
  pull-back, a dull recoil.
- **Director's decision:** no THUDs on the strikes. Seeing him do it is chilling enough; the score (at its
  most distorted) does the work alone.
- Hold length: the brief says the viewer has only a moment - probably 0.75-1.5 s in the cut.
