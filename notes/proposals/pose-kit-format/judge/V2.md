# Chat 11's own idea (rewritten after Sam's note, before the helpers)

The format is two layers, always in this order:
1. BODY: every pose starts from the measured full body (solid_seat mode 'body'; MakeHuman by the person's spec),
   posed only by joint targets on the kit's own skeleton and camera. No hand-drawn limb outlines, no guessed tubes;
   a pose that needs a shape changes the joints, never the outline.
2. CLOTHES: drawn separately on top. The person's posted outfit is kept exactly (never redrawn on the body); the body
   shows only where the outfit ends (below the hem), and every garment below it is its own layer on the body
   (trousers shell, seat, shoes, lap opening). Each layer edge gets a picture check, proved red on Sam's saved frame.
3. A new pose = a pose spec (joint targets + any layer flag), a 4-view sheet of one test person, checks on every tile,
   locked poses fingerprinted. A new person = the same body built from their spec, their posted outfit on top.
4. Stop rule: if a fault is in the body, fix the joints; if at a layer edge, fix that layer; two rounds without
   improvement stops (rule 87). Outline patching is refused.
Lost: nothing. Added: one guide page (guides/pose-kit-format.md, named in job-packs.md "Film types"/kit jobs), a
starter pose-sheet script, Kemi/Blair as the first proof.
