#!/usr/bin/env python3
"""MAP  Blessed: the jury (Sam's note 10, 12 Nov). "During the oath, 180 to the jury, staring at him. Some begin to show
crossed annoyed eyebrows or share glances with each other. Use elements from previous films to build the different
faces and body shapes, as long as no characters are repeated or identifiable."

  JURORS 20   twelve invented people, front only (Glimpses, rule 24): each face is the average face (patriots4)
              pushed its own way (the press pack's and the inmates' way), with the press pack's haircuts seen from
              the front, the inmates' stubble, beards and freckles, glasses; bodies from views.person in their own
              build and clothes. No face push, hair and colour set is repeated, and none is an earlier film's cast.
  acting 110  all stare at Brand (just right of the lens); on "the blessed evidence" brows knit one after another,
              one sceptical brow goes up, two pairs swap a sideways glance, then back to staring.
  draw 170    the back row, the box rail between the rows, the front row (blessed_sets.court_jury*).
"""
import math

import blessed_cast as BC
import burnham as B
import moves
import views as V

TC = BC.TC
# The faces: m = pushes on the average face; hair (blessed_cast: crop, bald, side, bob, long, curly, bun, pony,
# receding); stub (stubble shade), beard, freckles, glasses (frame colour).
FACES = {
    'juror1': dict(m=dict(face_wide=0.05, jaw_wide=0.08, nose_long=0.02, brow_high=-0.1, mouth_wide=0.03),
                   iris=(60, 44, 30), lip=(170, 110, 96), brow=(30, 26, 24), hair='crop', stub=0.86),
    'juror2': dict(m=dict(face_wide=-0.03, chin_long=0.02, eye_size=0.01, mouth_wide=-0.05, brow_slope=3.0),
                   iris=(90, 110, 130), lip=(200, 120, 120), brow=(150, 130, 100), hair='bob', glasses=(150, 60, 50)),
    'juror3': dict(m=dict(face_wide=0.08, jaw_wide=0.1, nose_wide=0.12, eye_size=-0.014, lip_low=0.02, chin_long=-0.02),
                   iris=(80, 96, 110), lip=(196, 128, 120), brow=(200, 196, 190), hair='receding', brow_thick=0.06),
    'juror4': dict(m=dict(face_wide=-0.06, jaw_wide=-0.06, eye_size=0.014, nose_wide=0.06, mouth_wide=0.06, lip_top=0.01),
                   iris=(48, 30, 22), lip=(120, 70, 66), brow=(26, 20, 18), hair='long'),
    'juror5': dict(m=dict(face_wide=0.02, jaw_wide=0.06, eyes_apart=-0.06, nose_long=0.04, brow_slope=-3.0),
                   iris=(70, 90, 70), lip=(186, 116, 104), brow=(70, 52, 38), hair='side', stub=0.8),
    'juror6': dict(m=dict(face_wide=-0.02, chin_long=0.03, eye_tilt=3.0, nose_wide=-0.04, mouth_wide=-0.02),
                   iris=(50, 36, 28), lip=(170, 100, 96), brow=(28, 22, 20), hair='bun'),
    'juror7': dict(m=dict(face_wide=0.04, eye_size=0.012, nose_long=-0.02, mouth_wide=0.04, chin_long=-0.03),
                   iris=(96, 120, 90), lip=(206, 130, 120), brow=(140, 70, 40), hair='curly', freckles=True),
    'juror8': dict(m=dict(face_wide=0.0, jaw_wide=0.04, nose_wide=0.08, eyes_apart=0.05, brow_high=0.1, lip_low=-0.01),
                   iris=(70, 80, 96), lip=(190, 120, 110), brow=(110, 106, 100), hair='crop', glasses=(30, 30, 34)),
    'juror9': dict(m=dict(face_wide=-0.05, jaw_wide=-0.08, eye_size=0.016, nose_long=-0.03, mouth_wide=-0.06),
                   iris=(80, 110, 140), lip=(212, 132, 128), brow=(170, 140, 90), hair='pony'),
    'juror10': dict(m=dict(face_wide=0.07, jaw_wide=0.12, nose_wide=0.18, eye_size=-0.01, mouth_wide=0.08, chin_long=0.01),
                    iris=(44, 30, 24), lip=(104, 62, 56), brow=(30, 26, 24), hair='bald', beard=(170, 166, 160)),
    'juror11': dict(m=dict(face_wide=-0.01, chin_long=0.04, nose_long=0.04, eye_size=-0.008, brow_slope=4.0),
                    iris=(110, 110, 120), lip=(190, 130, 130), brow=(170, 166, 160), hair='curly', glasses=(110, 60, 120)),
    'juror12': dict(m=dict(face_wide=0.03, eyes_apart=-0.03, eye_tilt=4.0, nose_wide=0.02, lip_low=0.01, brow_high=-0.08),
                    iris=(40, 30, 26), lip=(180, 116, 104), brow=(24, 20, 18), hair='side'),
}
# Bodies: skin, hair colour, clothes, build. Seated (the box covers them from the chest down).
_P = dict(hw=64, hh=94, head_dy=10, hair='bald', full=True, pose='custom', shoe=(30, 26, 24), trousers=(50, 50, 56))
JURORS = {
    'juror1': dict(_P, skin=B.OLIVE, hair_c=(34, 28, 24), outfit='suit', jacket=B.NAVY, tie=(120, 30, 40),
                   shoulders=162, height=1.80),
    'juror2': dict(_P, skin=B.PALE, hair_c=(196, 176, 140), outfit='jumper', jacket=(60, 120, 120), shoulders=136,
                   height=1.64, hw=60),
    'juror3': dict(_P, skin=B.PINK, hair_c=(196, 192, 186), outfit='suit', jacket=(120, 100, 70), tie=(40, 70, 50),
                   shoulders=170, height=1.76, hw=70),
    'juror4': dict(_P, skin=(120, 80, 58), hair_c=(62, 42, 32), outfit='blouse', jacket=(200, 150, 50),
                   shirt=(240, 236, 226), shoulders=134, height=1.66, hw=60),
    'juror5': dict(_P, skin=(150, 100, 70), hair_c=(50, 38, 30), outfit='jumper', jacket=(100, 116, 90), shoulders=158,
                   height=1.78),
    'juror6': dict(_P, skin=(214, 172, 136), hair_c=(24, 20, 20), outfit='dress', dress=(120, 40, 60), shoulders=132,
                   height=1.62, hw=60),
    'juror7': dict(_P, skin=B.PALE, hair_c=(150, 70, 40), outfit='jumper', jacket=(196, 160, 60), shoulders=138,
                   height=1.66, hw=60),
    'juror8': dict(_P, skin=(236, 196, 176), hair_c=(150, 148, 144), outfit='suit', jacket=B.CHARCOAL,
                   tie=(40, 60, 120), shoulders=154, height=1.74),
    'juror9': dict(_P, skin=B.PINK, hair_c=(214, 184, 120), outfit='blouse', jacket=(150, 180, 210),
                   shirt=(244, 244, 240), shoulders=132, height=1.64, hw=58),
    'juror10': dict(_P, skin=(96, 64, 48), hair_c=(30, 26, 24), outfit='suit', jacket=(150, 130, 100), tie=None,
                    shoulders=172, height=1.84, hw=70),
    'juror11': dict(_P, skin=(238, 204, 186), hair_c=(226, 224, 218), outfit='jumper', jacket=(110, 70, 120),
                    shoulders=136, height=1.62, hw=60),
    'juror12': dict(_P, skin=(222, 188, 150), hair_c=(22, 20, 20), outfit='jumper', jacket=(40, 50, 90), shoulders=150,
                    height=1.72),
}
for w, sp in JURORS.items():
    sp.update(who=w, name='Juror ' + w[5:], seed=700 + int(w[5:]))
BC.FRONT_FACES.update(FACES)
TC.HEADS.update({w: BC.inmate_head for w in JURORS})
BACK_ROW = ['juror7', 'juror8', 'juror9', 'juror10', 'juror11', 'juror12']     # left to right on screen
FRONT_ROW = ['juror1', 'juror2', 'juror3', 'juror4', 'juror5', 'juror6']

# ---------------------------------------------------------------------------------------------- acting
# Times are seconds after "the blessed evidence" (k). Roles: knit (brows down and in, lids lower, mouth flattens),
# sceptic (one brow up), glance (eyes snap to the neighbour and back, the head tips towards them).
ACT = {
    'juror1': dict(knit=0.55),
    'juror2': dict(knit=0.15),
    'juror3': dict(glance=(1.0, 2.0, +1), knit=0.4),
    'juror4': dict(glance=(1.1, 2.0, -1)),
    'juror5': dict(knit=0.3, hard=True),
    'juror6': dict(sceptic=0.5),
    'juror7': dict(knit=0.7),
    'juror8': dict(sceptic=0.2),
    'juror9': dict(glance=(1.4, 2.3, +1)),
    'juror10': dict(glance=(1.5, 2.3, -1), knit=0.25, hard=True),
    'juror11': dict(knit=0.45),
    'juror12': dict(),                                   # one keeps the blank stare all through
}
LOOK_AT_HIM = 0.3                                        # Brand is just right of the lens


def _ramp(t, a, b):
    return min(1.0, max(0.0, (t - a) / max(1e-6, b - a)))


def _ease(u):
    return u * u * (3 - 2 * u)


def state(w, t, k):
    """The face and head of juror w at film time t; k is the film time of "the blessed evidence"."""
    a = ACT[w]
    d = dict(look=LOOK_AT_HIM, frown=0.0, brow_up=0.0, lid4=0.16, smile=-0.25)
    roll = 0.0
    if 'knit' in a:
        u = _ease(_ramp(t, k + a['knit'], k + a['knit'] + 0.4))
        hard = 1.4 if a.get('hard') else 1.0
        d.update(frown=0.07 * hard * u, brow_up=-0.014 * hard * u, lid4=0.16 + 0.14 * u, smile=-0.25 - 0.45 * u)
    if 'sceptic' in a:
        u = _ease(_ramp(t, k + a['sceptic'], k + a['sceptic'] + 0.35))
        d.update(brow_up=(-0.006 * u, 0.05 * u), frown=0.02 * u, smile=-0.25 - 0.3 * u)
    if 'glance' in a:
        g0, g1, side = a['glance']
        snap = _ramp(t, k + g0, k + g0 + 0.08) * (1 - _ramp(t, k + g1, k + g1 + 0.08))     # eyes snap
        d['look'] = LOOK_AT_HIM + (side - LOOK_AT_HIM) * snap
        roll = 5.0 * side * _ease(_ramp(t, k + g0, k + g0 + 0.3)) * (1 - _ease(_ramp(t, k + g1, k + g1 + 0.35)))
        if snap > 0.5:
            d['smile'] = min(d['smile'], -0.5)
    return d, roll


# ---------------------------------------------------------------------------------------------- draw
def draw(img, cam, t, k, put_seated, face, ST):
    """Both rows on court_jury: the back row, its box rail (ST.mid), the front row; the front box is ST.front."""
    st = ST.STAGE['court_jury']
    for row, marks in ((BACK_ROW, st['back']), (FRONT_ROW, st['front'])):
        if row is FRONT_ROW:
            ST.mid('court_jury', img, cam, t)
        for w, mark in zip(row, marks):
            d, roll = state(w, t, k)
            sp = dict(JURORS[w], **face(w, t, 'neutral', **d))
            j = moves.seated(sp)
            j['head_roll'] = roll
            put_seated(img, cam, sp, mark, t, j=j)
