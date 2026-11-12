#!/usr/bin/env python3
"""MAP  checktests: every pre-flight check fed a deliberately broken film, to prove it can fail (system audit, 12 Nov,
question 4: "checks that can't fail"). Each case builds the smallest film that breaks one rule, runs only that check,
and passes only if the check names the fault. A check whose broken example it does not catch is a check that would
say "clean" over a real fault.

  CASES ........ (check, rule, how it is broken, the call) one per check; the honest-checker cases (NOT RUN, HAS)
  ELSEWHERE .... checks proven in kittests.py instead (a real film's old fault put back), by test name
  UNTESTED ..... checks with no broken example yet, listed every run (empty since audit item 11, 12 Nov)
  main() ....... runs them all; prints one line each and the untested list

    python3 source/checktests.py          (seconds; no drawing)
"""
import io
import os
import sys
import tempfile
import types
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def film(**kw):
    """A stand-in film module with just these settings."""
    m = types.ModuleType(kw.pop('name', 'brokenfilm'))
    m.__file__ = ''
    m.SHOTS, m.FPS, m.DUR = [('s', 0.0, 2.0)], 12, 2.0
    for k, v in kw.items():
        setattr(m, k, v)
    return m


def _plan(**kw):
    p = dict(CEIL=3.0, ROOMS={'a': (0.0, 0.0, 4.0, 4.0)}, OPENINGS={}, THINGS={}, PEOPLE={}, CAMS={}, GROUPS={})
    p.update(kw)
    return p


def _notes(text, archived=False):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, 'archive'))
    path = os.path.join(d, 'x.md')
    with open(os.path.join(d, 'archive', 'x.md') if archived else path, 'w') as fh:
        fh.write(text)
    return path


BRIEF_BLANK = '## The brief as a checklist\n| # | detail | done? |\n|---|---|---|\n| 1 | a red door | |\n'


# --- the cases ---------------------------------------------------------------------------------------------------
def c_plan():
    import plan
    return plan.faults(film(PLAN=_plan(ROOMS={'a': (0, 0, 4, 4), 'b': (2, 2, 6, 6)})))


def c_plan_missing():
    import plan
    return plan.faults(film())


def c_benchmark():
    import benchmark
    return benchmark.faults(film(BENCHMARK=[{'place': 'office', 'refs': [], 'items': []}]))


def c_hook_covers():
    import hookcheck
    return hookcheck.faults(film(HOOK=('A Hook Over His Face', {'y': 330, 'until': 1.0}),
                                 KEEP_CLEAR=[('his face', lambda t: (0, 0, 1080, 1920))]))


def c_hook_no_keep_clear():
    import hookcheck
    return hookcheck.faults(film(HOOK=('A Hook', {'y': 330})))


def c_shot_cast():
    import preflight as P
    return P.cast_faults(film(SHOT_CAST={'s': ['bob']}), {'s': {'amy'}})


def c_shot_length():
    import preflight as P
    out = []
    with contextlib.redirect_stdout(io.StringIO()):
        P._text_only(film(SHOTS=[('long', 0.0, 9.5)], DUR=9.5), out, 9.5, 12)
    return out


def c_brief_blank():
    import preflight as P
    return [x for x in P.gates(film(NOTES=_notes(BRIEF_BLANK)), 'x') if 'blank' in x]


def c_no_composition_sheet():
    import preflight as P
    return [x for x in P.gates(film(NOTES=_notes(BRIEF_BLANK)), 'x') if 'composition' in x]


def c_acting_list():
    import preflight as P
    return [x for x in P.gate_warnings(film(NOTES=_notes('## Notes\n')), 'x', {'voices'}) if 'acting' in x]


def c_rehearsal_line():
    import preflight as P
    return [x for x in P.gate_warnings(film(NOTES=_notes('## Notes\n')), 'x', set()) if 'Rehearsal' in x]


def c_head_life():
    import preflight as P
    return P.head_life_faults(film(LINES=[{'who': 'amy', 'n': 1, 'start': 0.0, 'end': 1.0}]))


def c_house_look():
    import film_engine
    return film_engine.look_faults(film(FPS=24))


def c_house_style():
    import burnham as B
    import housestyle
    return [x for x in housestyle.faults(film(), B, {'people'}) if 'OUTFIT' in x]


def c_set_feet_missing():
    import setcheck
    return setcheck.film_faults(film(SET_BOXES={}, HAS={'people', 'rooms'}))


def c_set_feet_half():
    import setcheck
    return setcheck.film_faults(film(SET_FEET={}, HAS={'people', 'rooms'}))


def c_door_without_angles():
    import sets
    return sets.solids_faults(film(PLAN=_plan(OPENINGS={'door': dict(wall=('x', 4.0), span=(1.0, 2.0), height=2.0,
                                                                     hinge=(1.0, 'in'))})))


def c_mark_in_mid_air():
    import kitchecks
    return kitchecks.marks(film(PLAN=_plan(), all_marks=lambda: [dict(at=(2.0, 1.5, 2.0), kind='bullet hole', t=0.5)]))


def c_pass_through():
    import clipcheck as CC
    return CC.solid_faults(film(solids=lambda t: [CC.sphere('amy', 'head', (0, 1.6, 2), 0.12),
                                                   CC.sphere('bob', 'head', (0.05, 1.6, 2), 0.12)]), [0.0, 0.5])


def c_teleport():
    import clipcheck as CC
    f = film(solids=lambda t: [CC.sphere('amy', 'head', (0 if t < 0.5 else 3.0, 1.6, 2), 0.12)])
    return CC.motion_faults(f, [i / 12 for i in range(12)], 12)


def c_draw_order_flip():
    import clipcheck as CC
    f = film(draw_order=lambda t: ['amy', 'bob'] if t < 1.0 else ['bob', 'amy'])
    return CC.flip_faults(f, [i / 12 for i in range(24)])


def c_collision():
    import audit
    f = film(scene=lambda t: [audit.Thing('amy', audit.simple('amy', 0.0, 3.0)),
                              audit.Thing('bob', audit.simple('bob', 0.05, 3.0))], cam_for=lambda t: None)
    with contextlib.redirect_stdout(io.StringIO()):
        return audit.check(f)


CAM = types.SimpleNamespace(pos=(0.0, 1.6, -2.0), f=(0.0, 0.0, 1.0), r=(1.0, 0.0, 0.0), u=(0.0, 1.0, 0.0), focal=1200)


def _popper(cam):
    import audit
    return film(scene=lambda t: [audit.Thing('amy', audit.simple('amy', 0.0, 3.0))] +
                ([audit.Thing('bob', audit.simple('bob', 1.0, 3.0))] if t >= 1.0 else []), cam_for=lambda t: cam)


def c_pop_in():
    import audit
    with contextlib.redirect_stdout(io.StringIO()):
        return [x for x in audit.check(_popper(CAM)) if 'POPS' in x]


def c_pop_in_blind():
    import audit
    with contextlib.redirect_stdout(io.StringIO()):
        return [x for x in audit.check(_popper(None)) if 'COULD NOT TEST' in x]


def c_not_run():
    import preflight as P
    f = film(SHOT_CAST={'s': ['kg']})
    return P.coverage_lines(f, P.coverage(f, {'voices'}))[0]


def c_not_run_off_without_yes():
    import preflight as P
    f = film(CHECKS_OFF={'hands': 'not needed'})
    return [x for x in P.coverage_lines(f, P.coverage(f, {'voices'}))[0] if x.startswith('NOT RUN: hands')
            and 'does not say Sam said yes' in x]


def c_has_claim():
    import preflight as P
    return P.claim_faults(film(SHOT_CAST={'s': ['kg']}), {'voices'})


def c_has_claim_drawn():
    import preflight as P
    return P.claim_faults(film(), {'voices'}, drawn_names=['vance'])


def c_never_clean_while_off():
    import report
    with contextlib.redirect_stdout(io.StringIO()):
        text = report.summarise('pre-flight (x)', [], off=["OFF (Sam's yes): hands: ..."])
    return [] if text.rstrip().endswith(': clean') or ': clean\n' in text else ['the summary did not say "clean"']


def c_lock_not_run():
    import film_engine as E
    real = E.PASSES
    E.PASSES = tempfile.mkdtemp()
    try:
        E.write_pass('x', 2, not_run=1)
        return [x for x in [E.lock_fault('x', faults_named=True)] if x]
    finally:
        E.PASSES = real


def c_audit_counts_guard():
    import figure as F
    import preflight as P
    n = len(F.LOG)
    F.LOG.append('s 1.00s: arm: forearm under half its length (allowed: audit of a finished film)')
    F.LOG.append('s 1.25s: arm: elbow folded (allowed: a stretchy gag)')
    try:
        out = P._audit_guard_faults()
    finally:
        del F.LOG[n:]
    return out if len(out) == 1 else []


def c_recheck_shot_tail():
    import preflight as P
    f = film(SHOTS=[('s', 0.0, 4.0), ('t', 4.0, 8.0)])
    todo = P._recheck(f, [46], 96, 12)                 # one frame changed 0.2 s before the cut at 4 s
    return ['the pose before the drop is redrawn'] if {36, 37, 38} <= todo and 50 not in todo else []


def c_recheck_check_files():
    import preflight as P
    files = P._check_files('brokenfilm')
    missing = [f for f in ('turnhead.py', 'setcheck.py') if f not in files]
    files = dict(files, **{'turnhead.py': 'old'})
    return ['a change to turnhead.py is seen'] if not missing and P._files_changed(files) == 'turnhead.py' else []


# --- the nine that had no broken example (audit item 11, Sam 12 Nov: "NOW"): drawn and recorded stand-ins ---------
def c_line_work():
    import linecheck
    from PIL import ImageDraw
    def draw(lay):                                    # a shape with no outline at all
        ImageDraw.Draw(lay).rectangle((300, 600, 780, 1300), fill=(200, 120, 90, 255))
    return linecheck.faults(film(LINE_SUBJECTS=lambda: [('box', draw)]))


def c_clothes():
    import landmarks
    return landmarks.faults(film(OUTFIT={'amy': {'skirt top': 560}}))    # a skirt starting below the hips


def c_real_sizes():
    import sizes
    return sizes.faults(film(PROP_SIZES=[('cup', 'mug', 0.4, 0.5, None)]))   # a mug half a metre tall


def c_effect_shape():
    import viewchecks
    import math
    from PIL import ImageDraw
    def star(img):                                    # a five-point cartoon star for a bang (rule S7: off-style)
        pts = [(540 + (300 if k % 2 == 0 else 110) * math.cos(math.pi * k / 5 - math.pi / 2),
                960 + (300 if k % 2 == 0 else 110) * math.sin(math.pi * k / 5 - math.pi / 2)) for k in range(10)]
        ImageDraw.Draw(img).polygon(pts, fill=(255, 220, 40, 255))
    return viewchecks.shape_faults(film(EFFECTS=[('bang', 'burst', star)]))


def c_body_audit():
    import filmkit
    from PIL import Image, ImageDraw
    def draw(t):                                      # a head drawn apart from its body
        im = Image.new('RGBA', (400, 800), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle((150, 300, 250, 700), fill=(80, 80, 200, 255))
        d.ellipse((160, 100, 240, 180), fill=(230, 190, 160, 255))
        return im
    return filmkit.silhouette_audit({'amy': ([0.0, 0.25], draw)})


def _bursts(n, sr, seed=1):
    import numpy as np
    rng = np.random.default_rng(seed)
    out = [np.zeros(int(0.3 * sr))]
    for _ in range(n):
        k = int(0.16 * sr)
        out += [rng.normal(0, 0.3, k) * np.hanning(k), np.zeros(int(0.22 * sr))]
    return np.concatenate(out + [np.zeros(int(0.3 * sr))])


def c_script_voice():
    import voices
    from burnham_film import SR
    ln = dict(n=1, who='amy', start=0.0, text='I absolutely never ever said anything like that in my whole life',
              _voice=_bursts(3, SR))                  # three syllables said; the script has about seventeen
    with contextlib.redirect_stdout(io.StringIO()):
        return voices.audit(film(LINES=[ln]), mouths=False)[0]


def c_song_join():
    import numpy as np
    import musiccheck
    import imageio_ffmpeg
    import subprocess
    d = tempfile.mkdtemp()
    sr, rng = 16000, np.random.default_rng(7)
    song = np.concatenate([np.sin(2 * np.pi * rng.uniform(200, 1500) * np.arange(int(0.25 * sr)) / sr) *
                           rng.uniform(0.2, 0.6) for _ in range(40)])   # 10 s of different notes, a quarter-second each
    path = os.path.join(d, 'song.wav')
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-f', 's16le', '-ar', str(sr), '-ac', '1', '-i',
                    '-', path], input=(song * 32767).astype(np.int16).tobytes(), check=True)
    return musiccheck.faults(film(SPLICE=((path, 0.0, 4.0), (path, 4.5, 8.0))))   # half a second of the song skipped


def c_resting_arm():
    import kitchecks
    import sitting as SK
    top = 500.0
    line = top - SK.SLEEVE
    rec = dict(_rest=dict(t=1.0, posed={'L': True, 'R': False}, floor=900.0, bob=0.0, tops={'desk': top},
                          arms={'L': ((0.0, line + 40), (60.0, line + 40)), 'R': ((0.0, line), (60.0, line))},
                          on_desk={'L': True}))      # the forearm 40 units (about 10 cm) inside the desk
    return kitchecks.rests(film(RESTS=[('amy', 'desk', 0.0, 2.0, 'leaning on the desk, note 3')]),
                           [('1.00 s', 'amy', rec)])


def c_portal_flat():
    import sets
    from PIL import Image
    cam = types.SimpleNamespace(pos=(2.0, 1.4, -1.0), f=(0.0, 0.0, 1.0), r=(1.0, 0.0, 0.0), u=(0.0, 1.0, 0.0),
                                focal=900)
    f = film(PLAN=_plan(OPENINGS={'window': dict(wall=('z', 4.0), span=(1.0, 3.0), height=(0.8, 2.2))}),
             cam_for=lambda t: cam, frame_image=lambda t: Image.new('RGB', (1080, 1920), (90, 90, 95)))
    return sets.portal_faults(f)                      # the window shows one flat grey


CASES = [   # (check, rule, how it is broken, the case)
    ('plan', '1', 'two rooms overlap', c_plan),
    ('plan', '1', 'no PLAN at all', c_plan_missing),
    ('benchmark', '3', 'a place with no references', c_benchmark),
    ('hook text', '75', 'the Hook Text covers a face', c_hook_covers),
    ('hook text', '75', 'HOOK with no KEEP_CLEAR', c_hook_no_keep_clear),
    ('shot cast', '14', 'someone the brief puts in a shot is never there', c_shot_cast),
    ('shot lengths', '-', 'a 9.5 s shot', c_shot_length),
    ('brief checklist', '14', 'a blank "done?" row', c_brief_blank),
    ('composition sheet', '11', 'no record of the sheet being sent', c_no_composition_sheet),
    ('acting list', '74', 'no acting list', c_acting_list),
    ('rehearsal clips', '8', 'no "Rehearsal clips sent" line', c_rehearsal_line),
    ('head life', '74', 'a speaker with a still head', c_head_life),
    ('house look', 'S7', 'drawn at 24 a second, no reason', c_house_look),
    ('house style', '-', 'a film with people and no OUTFIT', c_house_style),
    ('set feet', '13', 'SET_BOXES but no SET_FEET', c_set_feet_missing),
    ('set feet', '13', 'SET_FEET but no SET_CAM, MOVE_SPAN', c_set_feet_half),
    ('set solids', '5', 'a hinged door with no door_angles', c_door_without_angles),
    ('marks', '13', 'a bullet hole in mid-air', c_mark_in_mid_air),
    ('clip: pass-through', '5', 'two heads in one place', c_pass_through),
    ('clip: teleport', '6', 'a head jumps 3 m in a frame', c_teleport),
    ('clip: draw order', '57', 'two people swap in front mid-shot', c_draw_order_flip),
    ('collisions', '5', 'two people standing in each other', c_collision),
    ('pop-ins', '6', 'someone appears mid-frame', c_pop_in),
    ('pop-ins', '6', 'a camera the test cannot read (it used to go quiet)', c_pop_in_blind),
    ('honest: NOT RUN', '59', 'HAS leaves out people', c_not_run),
    ('honest: NOT RUN', '59', 'CHECKS_OFF with no Sam yes or date', c_not_run_off_without_yes),
    ('honest: HAS', '58', 'HAS says no people, SHOT_CAST has some', c_has_claim),
    ('honest: HAS', '58', 'HAS says no people, the drawing has some', c_has_claim_drawn),
    ('honest: summary', '59', '"clean" while a check is off', c_never_clean_while_off),
    ('honest: render lock', '59', 'a render past a check that never ran, "named"', c_lock_not_run),
    ('honest: --audit', '19', "the arm guard's stops only in the small print", c_audit_counts_guard),
    ('incremental', '59', 'a drop to rest just before a cut', c_recheck_shot_tail),
    ('incremental', '59', 'a check file not in CHECK_FILES changes', c_recheck_check_files),
    ('line work', '-', 'a shape with no outline', c_line_work),
    ('clothes', '-', 'a skirt starting below the hips', c_clothes),
    ('real sizes', '-', 'a mug half a metre tall', c_real_sizes),
    ('effect shapes', 'S7', 'a cartoon star for a bang', c_effect_shape),
    ('body audit', '-', 'a head drawn apart from its body', c_body_audit),
    ('script v voice', '7', 'three syllables said, a 21-syllable script', c_script_voice),
    ('song joins', '-', 'half a second of the song skipped at a join', c_song_join),
    ('resting arms', '78', 'a resting forearm 6 cm inside the desk', c_resting_arm),
    ('openings', '2', 'a window showing one flat grey', c_portal_flat),
]

ELSEWHERE = {   # check: the kittests.py tests that put a real film's old fault back and see it caught
    'hands (rule 41)': 'hands_round_the_head, hands_in_sleeves, point_hand_shows_a_finger, shoulder_seam_caught',
    'held props (rules 13, 20)': 'held_prop_through_the_camera, held_prop_touches, grips_contacts_and_carry',
    'facing and turned heads (rule 13)': 'head_turns_its_own_way, looks_at_the_shot_camera, turned_heads_for_anyone',
    'poses and lying bodies (rule 42)': 'pose_gallery, lying_and_pose_checks, lying_shirt_and_nape',
    'copies (Job K)': 'copies_in_a_group', 'cut rests (rule 72)': 'cut_before_the_return',
    'famous faces (rule 50)': 'famous_face_size', 'eyes (S5)': 'eyes_cut_to_the_outline',
    'subtitles (rule 62)': 'subtitles_readable, caption_check_at_delivered_speed, subtitle_starts_on_its_word',
    'bleeps': 'bleeps_every_swear', 'hook planned (rule 75)': 'hook_text_planned',
    'moving figures in the set (rule 13)': 'moving_figures_against_the_set, moving_figures_per_shot',
    'render lock (rule 59)': 'render_lock', 'house look pairs (S7)': 'house_look_once_in_pairs',
    'sounds with their thing (rule 13)': 'sounds_and_references_kept',
}

UNTESTED = []   # every check has a broken example (audit item 11, 12 Nov); a new check adds its case to CASES


def main():
    bad = 0
    for check, rule, how, fn in CASES:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                found = fn()
            ok, detail = bool(found), (found[0] if found else 'NOT CAUGHT: the check said nothing')
        except Exception as e:                      # a check that crashes on a broken film has not caught it
            ok, detail = False, f'crashed: {type(e).__name__}: {e}'
        bad += not ok
        print(f"{'CAUGHT' if ok else 'MISSED'} {check} (rule {rule}): {how} -> {str(detail)[:110]}")
    print(f'checktests: {len(CASES) - bad} of {len(CASES)} broken films caught'
          f'{"" if not bad else f"; {bad} MISSED"}; {len(ELSEWHERE)} more checks proven in kittests.py; '
          + (f'{len(UNTESTED)} with no broken example yet:' if UNTESTED else 'every check has a broken example'))
    for x in UNTESTED:
        print('  -', x)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
