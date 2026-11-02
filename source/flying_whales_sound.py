#!/usr/bin/env python3
"""Flying Whales: the sound effects (Sam's own sounds, 2 Nov: source/audio/flying-whales-sfx/), placed on the film's
events. No music (Sam, 2 Nov: "We may not need the score"). The voice is flying_whales.LINES; this is the rest.

    python3 source/flying_whales_sound.py            the cue list (what plays when, film seconds)

Each sound is set to its own loudness (LUFS) first, so the levels below are the mix, whatever the file came in at.
Sam's grades: 'minor' and 'major' splashes and explosions for smaller and bigger impacts.
"""
import functools
import os
import sys

import numpy as np
from scipy.signal import butter, resample_poly, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import filmkit                                        # noqa: E402
import mossad_audio as MA                             # noqa: E402
from burnham_film import load, SR                     # noqa: E402
import flying_whales_opener as O                      # noqa: E402
import flying_whales_paths as PATHS                   # noqa: E402
import flying_whales_wreck as WR                      # noqa: E402

SFX = os.path.join(HERE, 'audio', 'flying-whales-sfx')
CUT = O.CUT
BLOW_AFTER = 0.9                                      # as flying_whales.BLOW_AFTER: each whale puffs 0.9 s out of the sea
# the three cleanest puffs in Sam's blowhole recording (s): Sam, 2 Nov: "isolate blowhole noises"
PUFFS = [(11.12, 12.42), (21.04, 22.12), (4.58, 5.84)]


@functools.lru_cache(None)
def clip(name, lufs, a=None, b=None, low=None, rate=1.0):
    """A sound: cut to a-b s (short fades), pitched by rate (below 1: lower and slower), muffled above `low` Hz,
    set to `lufs`."""
    x = load(os.path.join(SFX, name + '.mp3'))
    if a is not None:
        x = x[int(a * SR):int(b * SR) if b else None].copy()
    k = int(0.02 * SR)
    x[:k] *= np.linspace(0, 1, k)
    x[-k * 4:] *= np.linspace(1, 0, k * 4)
    if rate != 1.0:
        up, down = 100, int(round(100 * rate))
        x = resample_poly(x, up, down)
    if low:
        x = sosfilt(butter(4, low, 'low', fs=SR, output='sos'), x)
    return x * 10 ** ((lufs - MA.lufs(x)) / 20)


# ---- the piano (Sam, 2 Nov: "gentle nature piano music appropriate for the first scene. No music in second.")
# D major, soft broken chords that turn with Attenborough's phrases, a sparse tune on top; on "imagined" the
# arpeggio climbs the keyboard with the whales racing for the surface, and it is gone with the cut.
# (film s, bass note, the chord's broken-chord notes, the tune's notes as (s, note))
PIANO = [
    (0.0, 'D2', ['A2', 'D3', 'F#3', 'A3', 'E4', 'A3'], [(0.6, 'F#5'), (1.5, 'E5'), (1.8, 'A4')]),     # "This series,"
    (2.3, 'B1', ['F#2', 'B2', 'D3', 'F#3', 'C#4', 'F#3'], [(2.4, 'D5'), (3.0, 'C#5'), (3.3, 'B4')]),  # "we will see
    (3.9, 'G1', ['D2', 'G2', 'B2', 'D3', 'F#3', 'D3'], [(4.0, 'B4'), (4.6, 'D5')]),                   #  animal behaviour"
    (5.0, 'A1', ['E2', 'A2', 'D3', 'E3', 'A3', 'E3'], [(5.1, 'E5'), (5.7, 'C#5')]),                   # "we could scarcely"
    (5.9, 'A1', ['E2', 'A2', 'C#3', 'E3', 'A3', 'E3'], [(6.2, 'E5')]),
]
RISE = (6.55, 7.75, ['D3', 'F#3', 'A3', 'D4', 'F#4', 'A4', 'D5', 'F#5', 'A5', 'D6'])   # on "imagined": up and up
STEP = 0.3                                            # s between the broken-chord notes


@functools.lru_cache(None)
def piano():
    import deck_the_halls as D
    D.rng = np.random.default_rng(31)                 # fixed dice: the same piano every render
    n = int((CUT + 0.5) * D.SR)
    x = np.zeros(n)

    def note(t, name, vel, dur):
        s = D.piano_note(D.midi(name), vel, dur)
        i = int(t * D.SR)
        s = s[:max(0, n - i)]
        x[i:i + len(s)] += s

    ends = [p[0] for p in PIANO[1:]] + [RISE[0]]
    for (t0, bass, arp, tune), t1 in zip(PIANO, ends):
        note(t0, bass, 0.42, t1 - t0 + 0.4)
        k = 0
        while t0 + STEP * (k + 1) < t1 - 0.05:
            note(t0 + STEP * (k + 1), arp[k % len(arp)], 0.26 + 0.05 * (k % 2 == 0), STEP * 3)
            k += 1
        for tt, nm in tune:
            note(tt, nm, 0.4, 1.4)
    a, b, notes = RISE
    note(a, 'D2', 0.45, CUT - a)
    for j, nm in enumerate(notes):                    # quickening a little as it climbs
        u = j / (len(notes) - 1)
        note(a + (b - a) * (u ** 0.85), nm, 0.28 + 0.2 * u, 0.9)
    x = D.reverb(x)
    x = resample_poly(x, 160, 147)                    # 44.1 kHz -> the film's 48 kHz
    x = x[:int(CUT * SR)]
    k = int(0.35 * SR)                                # gone with the cut (a quick fade, not a click)
    x[-k:] *= np.linspace(1, 0, k) ** 2
    return x * 10 ** ((-27.0 - MA.lufs(x)) / 20)      # gentle: well under the voice (-20)


def rig(t):
    """Film time of rig-scene story time t (the freezes on the hits push later events back)."""
    return CUT + WR.real_of(t)


def cues():
    """[(film s, label, sound)]."""
    c = []
    # ---- under the sea (0 to the cut): the whales moving, two calls, muffled; nothing over the cut
    # (Sam, 2 Nov: lost under the dialogue, so up 5 dB; a whale sound in it at 7.0-7.4 s was cut off sharply at the
    # cut, so the bed now fades out over the last 0.6 s)
    bed = clip('underwater-whales', -25.0)[:int(CUT * SR)].copy()
    k = int(0.3 * SR)
    bed[:k] *= np.linspace(0, 1, k)
    k = int(0.6 * SR)
    bed[-k:] *= np.linspace(1, 0, k) ** 1.5
    c.append((0.0, 'under the sea: whales moving (Sam\'s first 10 s)', bed))
    # Sam, 2 Nov: "a loud whale noise at the beginning (beneath the dialogue)": the big call opens the film, under
    # "This series," (muffled: it is under water)
    c.append((0.0, 'whale call 1, LOUD, opening the film', clip('whale-call-1', -18.0, low=2200)))
    c.append((4.45, 'whale call 2, under water', clip('whale-call-2', -25.0, low=1800)))
    c.append((0.0, 'piano: gentle nature music under the sea (cut with the scene)', piano()))
    # ---- the rig scene: five whales burst out of the sea
    for k in PATHS.KEYS:
        c.append((rig(PATHS.SURFACE[k]), f'whale {k} bursts out of the sea', clip('splash-minor', -21.0 - k * 0.8)))
        a, b = PUFFS[k % len(PUFFS)]
        c.append((rig(PATHS.SURFACE[k] + BLOW_AFTER), f'whale {k} blowhole', clip('blowhole-raw', -27.0, a, b)))
    # angry calls as they come in (a little lower: grumpier)
    c.append((CUT + 1.0, 'whale call 1, angry', clip('whale-call-1', -23.0, rate=0.88)))
    c.append((CUT + 1.9, 'whale call 2, angry', clip('whale-call-2', -24.0, rate=0.85)))
    # ---- the hits: a crunch for each that has no fireball, an explosion for each fireball (graded by size)
    crunch = clip('building-collapse', -21.0, 0.0, 0.9)
    for t, label in ((2.56, 'Inky through the legs'), (3.71, 'Bib through the stair tower'),
                     (4.25, 'Freckle through the top deck'), (6.74, 'Blaze through the derrick')):
        c.append((rig(t), 'crunch: ' + label, crunch))
    for t0, _, size, _, _ in WR.FIREBALLS_AT:
        major = size >= 12
        c.append((rig(t0), f'explosion {"major" if major else "minor"} ({size:.0f} m fireball)',
                  clip('explosion-major', -17.0) if major else clip('explosion-minor', -20.0)))
    # ---- big pieces landing in the sea (not the braces at the waterline; not those under the crown splash)
    crown_t = next(s[0] for s in WR.SPLASHES if s[2] >= WR.CROWN[0])
    for n, f in WR.FALLS.items():
        if not f.entry or f.entry[1] is None or n.startswith('brace') or f.entry[0] > crown_t - 0.4:
            continue
        c.append((rig(f.entry[0]), f'{n} splashes into the sea', clip('splash-minor', -26.0)))
    # ---- the finale: the whole block goes over (Sam's building collapse), then the crown splash
    c.append((rig(WR.TF), 'the rig collapses and tips', clip('building-collapse', -17.0)))
    c.append((rig(crown_t), 'the crown splash (major)', clip('splash-major', -14.0)))
    return sorted(c, key=lambda q: q[0])


def track(n):
    """Every effect placed by when it really starts (filmkit.place), n samples long."""
    out = np.zeros(n)
    for at, _, s in cues():
        filmkit.place(out, s, at, SR)
    return out


if __name__ == '__main__':
    for at, label, s in cues():
        print(f'{at:6.2f} s  {len(s) / SR:4.1f} s  {label}')
