# Blessed: old handovers

## Build chat 1 (11 Nov)
- **Rules that bite next:** 49 (likeness check 60%+ before the cast sheet), 41 (every arm ends in a hand; one outline shoulder to arm), 89 (critique: Brand alone beside his photos, two passes).
- **Done (11 Nov, build chat 1, Opus high):** Brand's likeness pack filed, `references/blessed/likeness/` (b01-b03 straight-on, not smiling: Courthouse News, Guardian, BBC; b04 talking; b05 smiling; b06, b07, b09 sunglasses; b08 topknot sketch); his face card `brand-card.jpg`/`.json`. Card: close-set eyes (84th), long narrow face (77th), narrow forehead (76th), wide nose (73rd); "short nose" is unsure (photos disagree; by eye his nose is long and straight: trust the eye). It missed his beard: by eye a full beard, dark at the moustache, grey-white at the chin and jaw; long dark-brown curls past the shoulders, grey streaks, high hairline.
- **Spent against the estimate:** plan about 1%; build chat 1 about 1% (pack only; amber on reading).
- **Next:** build chat 2 (Opus, high effort): build Brand in `source/blessed_cast.py` copying `ad_vanced_notice_cast.py`'s Vance pattern (P4 MEASURED from `brand-card.json`, beard by hand like `scrub_beard`, turnhead register); `likeness.py check` 60%+; then judge, officer, newsreader; cast sheet to Sam.
- **Needs Sam:** nothing until the cast sheet.
- **Read:** `guides/job-packs.md` Build; this file; `source/ad_vanced_notice_cast.py` lines 1-78, 229-300, 376-416, 750-871 only.
- **Lost / Added:** none yet.
- **Open rule requests:** none.
- **For Claude:** sources that worked 11 Nov: Courthouse News (www.), Guardian (i.guim.co.uk, `s=none&width=1400`), BBC (ichef), Sky (e3.365dm.com), AP via WJTV; upload.wikimedia.org thumbs (429 after ~5); commons pages via firecrawl_scrape. Refused: AP/People/NYT/Independent/NPR/SCMP. Police interview stills are straight-on but small.



## Build chat 2 (cast), 11 Nov
- **Rules that bite next:** 89 (fresh-eye critique once the film draws frames), 41 (arms end in hands), 74 (acting list before animatic 1).
- **Done (11 Nov, build chat 2, Opus high):** the cast in `source/blessed_cast.py` (Vance pattern). Brand: measured face, beard, long curls, topknot, aviators (on / lowered), 10 moods, three looks (trial, stand/dock, prison), turned heads. Likeness 64% on b01 (pass) after Sam's notes 1-2 (bigger head, short chin and beard; b10 is the usual reference). Sam's six recordings filed (note 3). Judge (invented, wig front only), prison officer, newsreader. Two by-eye critique passes: fixed the judge's missing wig, the officer's lab-coat look, the topknot cone, the lowered shades, the turned hair's spikes and the strip across his face. Cast sheet, faces sheet, likeness sheet in `notes/sheets/blessed-*.jpg`, sent to Sam.
- **Spent against the estimate:** plan ~1%; cast stage 2.41% of 4% planned (ledger: lands at 11.4%).
- **Next:** build chat 3 (Opus, high effort), opened by build chat 2 on Sam's Y: the sets (court outside, courtroom x2, prison cell + phone, van, TV room, BBC-style studio, gates), then `source/blessed.py` from `satire_template.py`.
- **Needs Sam:** nothing until the sets sheet (Sam: Y to the cast, 11 Nov).
- **Read:** `guides/job-packs.md` Build; this file; `source/blessed_cast.py` MAP only.
- **Lost / Added:** Lost: prayer beads on his chest (read as dots; can go in his hand). Added: none.
- **Open rule requests:** none.
- **For Claude:** `critique.py pack` needs film frames (`blessed.py` not built), so rule 89's fresh-eye helper was not run on the cast; run it on the first set/shot frames. Likeness: `P4.TUNE['brand']` was tuned against b01+b03; the dark moustache and the long beard tip carry the chin and nose measures (slimming them dropped b03 to 44%). Judge side/back views are bald (wig is front only: he is only seen front-on at the bench). Turned long hair: `_turned_long` (screen units).

