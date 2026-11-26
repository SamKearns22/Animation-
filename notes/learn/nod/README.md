Kind: practice

# A nod, learnt (Open Wounds chat 39, Sam's note 26, 26 Nov: "It's not a nod, it's a head-bob.")

**Why nobody saw it:** the move-size check and HEAD_MIN measure how far and how fast the eyes travel, never how
the head moves. The kit's nod (views.Rolled, `dy = nod x 5`, eyes 'down') slid the whole head down and up: a bob.

**Reference:** `ref/nodding-gesture.gif` (Wikimedia Commons "Nodding gesture", public domain, a 16-frame line
drawing of a nod side-on), laid out in `ref/nodding-frames.jpg`. Fetched with `source/wikifetch.py`, the project's
earlier Wikimedia fix (Ad-vanced Notice: a client name and ~6 s between requests) made a shared tool, plus
thumbnail sizes only (the full file got 429 "use thumbnail images").

**What a nod is (from the reference):**
1. The head turns about a point just below and behind the ear (the top of the neck). The neck and collar do not move.
2. The chin goes down AND in, toward the collar; the nose tips down; the forehead comes forward.
3. The ear and the back of the skull barely move; the crown moves about a third as far as the face.
4. About 10-15 degrees for a conversational nod; down quicker than up (HEAD_MIN already eases both).

**How the kit draws it now (views.Pitched, prevention: a nod can only be drawn as a turn):** every mark on the
head gets a depth from a head-shaped ellipsoid (the face nearest us, the outline at the edge, the jaw fuller so the
chin tucks), is turned in 3D about the ear point and seen straight on again. Front: the eyes, nose and mouth slide
down inside the outline and the lower face shortens, the chin tucks over the collar, the crown nearly still.
Side-on: the reference's turn. Three-quarter: the mix. The face's real size is measured from its own skin shape
(views.face_box): house heads are ~1.5x the kit's hw/hh and higher; the first try used the kit's numbers and
pivoted far below May's ear, so side-on she still slid down (seen in this practice clip, fixed before Sam saw it).

**Practice:** `practice.py` (grey heads, old bob above the new nod, front / three-quarter / side).
