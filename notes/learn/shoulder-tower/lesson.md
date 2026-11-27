# The shoulder tower (Patriot 5, shot 4): what the photos show (27 Nov)

Sam (27 Nov): "This is the hardest thing in this film to pull off so you will have to learn this pose. It has been used
in animation plenty." Photos: references/patriots-5/tower/ (Openverse thumbnails; Flickr and Wikimedia refused full
size downloads, 403 and 429).

## A reference is a checklist
| photo | what it shows |
|---|---|
| 01 two stacked, side-on, at a lamp post | the closest to our camera: the top man's thighs over the lower man's shoulders, shins down his chest, the lower man's hands round the shins; the top man holds the post; the lower man's knees a little bent |
| 02 three stacked, front (pool) | each sitter's thighs either side of the neck below, calves hanging in front, the lower person's hands gripping the calves/knees; the top person's arms free |
| 03 three stacked, front, standing | each sitter's hands on the head or shoulders below; heads in one column; the stack only a little narrower going up |
| 04 one on shoulders, three-quarter | the lower man's stance wide, knees bent, back upright; the sitter's lower legs clamped against his chest by his hands; the sitter's arms out for balance |
| 05 two stacked from behind (festival) | arms out wide on the top man as he balances |
| 06 one on shoulders, front, arms up | the base's hands hold the sitter's shins at his own chest |

## How it works (the rules to draw it by)
- Each sitter's seat is on the shoulders of the man below; his thighs straddle that man's neck, his shins hang down that
  man's chest, his feet about at the lower man's belly; the lower man's hands grip the shins (except the base, whose
  hands are free or on his knees, and anyone who needs a hand free).
- Height: a sitter adds about his seated shoulder height (about 0.6 m for a grown man) per tier. Base shoulders about
  1.45 m; eight men: the top man's shoulders about 5.65 m, his head top about 6 m: a first-floor cell window outside.
- Balance: the whole stack's weight must stay over the base man's feet. A sway is the column pivoting about the base's
  feet, every tier following a little later and further than the one below (overlapping action), with the upper men
  throwing their arms out to balance (photos 04, 05) and the base stepping or bending his knees to catch it.
- Weight shows: the base's knees bent and stance wide; every man's back upright; heads in one column.
- Side-on (shot 4) is the view the drawing can carry: legs in front of chests, thighs over shoulders read clearly.

## Still to learn (the practice clip answers these)
- How far it may sway before it reads as falling (a test of 3 sizes).
- Nick's head "up the Patriot's arse": the Patriot sits on Nick's shoulders; Nick's head is right under him, tipped
  forward; the Patriot shifts his seat on "arse".

## What chat 2 learned (27 Nov; code `source/shoulder_tower.py`, clip `tower-practice-v1.mp4`, joins `joins-27nov.jpg`)
- **Drawn by layers.** Each man is drawn as three layers (body with head and far leg; near leg; near arm), split by
  renders in flat key colours (a near leg over the far leg, or a sleeve over a jacket of the same colour, otherwise left
  only outlines). Order: bodies from the top man down (each lower head over the seat above), then every near leg (over
  the neck below), then every near arm (the hand over the shin). Each man's layers turn about his pivot for the sway.
- **Our big heads change the seat.** Sam's note "there are clipping errors": with the seat just behind the neck, each
  head sat 54-92% inside the body above (`note-clipping-27nov.png`). Fix: the sitter sits behind the head below
  (`column_seat()`), every man leans 18 degrees so his neck comes forward over his own hips (the column stays straight
  over the base's feet), and each lower head bows 25 degrees under the seat ("Nick's head is up my arse", literally).
- **Feet at the belly stood on the head two below.** The shins now wrap round the sides of the chest with the feet
  tucked under the lower man's arm (a cheerleader's shoulder sit); the lower man holds the shin near the ankle (closer
  folds the elbow past the rig's 25-degree limit).
- **A bowed head takes its neck with it.** Sam's note "the neck is separated from the head"
  (`note-neck-separated-27nov.png`): the neck stayed upright while the head tipped. Shared fix: `j['bent_neck']` in
  views (opt-in; posted films keep their frames). Check `views.bent_neck_fault`, kittest `bent_neck_joined`.
- **Checks built:** the tower's clipping check (a head inside the body above; any shoe on or touching another man's
  head; anything through the wall), kittest `tower_clipping`; the joins check (`faults`: legs not stretched, base on
  the ground, the stack's weight over the base's feet).
- **Draw time:** 15 min for 4 s the first way (every man drawn six times a picture). Now each man's drawings are
  reused while only the sway turns them, frames split over 4 processors: 78 s.
- **Sway:** 0.011 rad at the base, growing 22% a tier, each tier 0.07 s later: the top man moves 0.23 m in all.

## Still open
- Sam (27 Nov, on v1): "I don't like the hand thrusting the lower characters are doing." The two middle men
  (BALANCE_ARMS) throw the near hand out at each end of the sway. Plan: take it out (both hands stay on the shins;
  the sway reads from the column and the top man's free arm). Lost: the arms-out balance from photos 04-05.
- The top man's head is near, not in, the window (the wall is set clear of every knee and hat brim through the sway):
  the film's shot will need his face at the bars.
- Peaked caps are left out: a bowed head turned the cap into a black blob (the film's men wear balaclavas).
- The feet check did not flag a shoe that looked close to a head in an enlarged crop; at 1:1 there was a gap.
