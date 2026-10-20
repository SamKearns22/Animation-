#!/usr/bin/env python3
"""Sam's recordings, checked twice: as they arrive, and against the finished film's script, subtitles and mouths.

1. As they arrive (lesson of The Patriots 2, where two files carried the same take under different names, and a
   file's name did not match what was said in it). For each file: length, the stretches of speech and the pauses
   between them, an estimate of the syllables, and its loudness. Then:
   - DUPLICATES: any two files with the same sound (however they are named) are reported;
   - with --script: each script line's expected syllables and speaking time, to compare with the measurements.
     Files are identified by their names (numbered by script line, see guides/preflight.md).

2. The script and mouth audit (rule 7 of guides/film-quality-rules.md; Power Crime Action lost four notes to it: a
   whole sentence said but missing from the script and subtitles, "Shit" mouthed twice, the jaw hanging open after
   he spoke). For a film module, before any picture is shown to Sam:
   - SCRIPT v VOICE: each recording is cut into phrases at its pauses, the syllables in each phrase are counted from
     the sound (each syllable is a little burst of loudness), and the script's words are laid over the phrases in
     the way that fits best. A phrase left with no script words (something said that the script lacks), or with far
     more or fewer syllables than the voice, is flagged with its time.
   - SUBTITLES v SCRIPT: the subtitles actually shown (the film's caption_at(t), every 0.05 s) are compared word by
     word with each line's script (a starred word such as "Sh*t" matches its word); a subtitle up when no line is
     being spoken is flagged.
   - MOUTHS v VOICE: every frame, each speaker's face as drawn (on screen, facing us, big enough to read): the mouth
     must be shut in silence (allowed exceptions listed by the film), move while the voice speaks, and open about
     once per syllable (not twice for "Shit", not still through a sentence).
   There is no speech recognition here (the package sites are blocked), so the words themselves are never heard:
   a phrase flagged here means "listen to this bit and compare it with the script", not proof of a mistake.

A film joins in by giving LINES (dicts: who, text, audio = the file's name in source/audio without .m4a, start =
where the recording starts in the film), FPS, DUR, and optionally:
  caption_at(t)     the subtitle on screen at t (or None);
  mouths_seen(t)    [(name, mouth, yaw, head_px)] for every face drawn at t: its name, its mouth as drawn
                    ('v:AI', 'set', 'agape', ...), the view it is drawn in (degrees, 0 facing us) and its head's
                    height on screen in pixels. Without it the film's lip-sync TRACK is used, which cannot see a face
                    drawn over it (a horror jaw), so make one (power_crime.mouths_seen copies its scene(t));
  MOUTH_OPENNESS    {mouth: 0-1} for the film's own mouth drawings (how open each looks);
  ALLOWED_MOUTHS    [(who, t0, t1, why)]: a mouth meant to be open in silence (a jaw dropped in horror);
  SPEAKERS          {who: [name patterns]} when the drawn names differ from LINES' 'who' (default: the name itself,
                    or the name followed by a number, so CROWD covers CROWD17).

Usage:
    python3 voices.py FILE.m4a [FILE.m4a ...] [--script script.txt]
      script.txt: one line of dialogue per line, optionally "WHO: words".
    python3 voices.py --film FILM [--from T0] [--to T1] [--no-mouths]
      FILM is the module name in source/ (power_crime). The mouth part draws nothing but runs the film's picture
      code on every frame (about a minute for a 50 s film on 4 cores). Pre-flight runs it too (check()).
"""
import difflib
import fnmatch
import hashlib
import importlib
import os
import re
import sys

import numpy as np
from scipy.signal import butter, find_peaks, sosfilt

from burnham_film import load, SR
import mossad_audio as MA


# ================================================================================================= measuring
def syllables_in(text):
    """A rough count of spoken syllables (vowel groups per word, silent final e, numbers as words)."""
    n = 0
    for w in re.findall(r"[A-Za-z']+", text.lower()):
        w = w.replace("'", '')
        groups = re.findall(r'[aeiouy]+', w)
        k = len(groups)
        if w.endswith('e') and k > 1 and not w.endswith(('le', 'ee')):
            k -= 1
        n += max(1, k)
    return n


ENV_RATE = 200       # loudness readings a second


def envelope(a):
    """The voice's loudness (dB) in the band where vowels are loudest, 200 readings a second, lightly smoothed."""
    x = sosfilt(butter(2, [400, 2000], 'band', fs=SR, output='sos'), a)
    hop = SR // ENV_RATE
    n = len(x) // hop
    e = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1))
    k = np.hanning(7)
    e = np.convolve(e, k / k.sum(), 'same')
    return 20 * np.log10(e + 1e-7)


def nuclei(db, stretches):
    """The syllables' times (seconds): each a loudness peak at least 3 dB above the dips either side, 80 ms apart,
    within 25 dB of its phrase's loudest. Tuned on Power Crime Action's six recordings against their scripts:
    128 syllables counted as 131, every phrase within 3."""
    out = []
    for s, b in stretches:
        i0, i1 = int(s * ENV_RATE), int(b * ENV_RATE)
        seg = db[i0:i1]
        if len(seg) < 3:
            continue
        pk, _ = find_peaks(seg, prominence=3, distance=16)
        out += [(i0 + p) / ENV_RATE for p in pk if seg[p] > seg.max() - 25]
    return out


def phrases(a):
    """The recording's phrases: its stretches of speech joined across gaps under a quarter of a second."""
    return MA.pauses(a, 0.25)


def measure(path):
    a = load(path)
    pcm = np.round(a * 32767).astype(np.int16).tobytes()
    st = MA.pauses(a, 0.12)
    db = envelope(a)
    env = 10 ** (db[::2] / 20)
    return dict(path=path, dur=len(a) / SR, hash=hashlib.sha1(pcm).hexdigest()[:12], stretches=st,
                syll=len(nuclei(db, phrases(a))), lufs=MA.lufs(a), env=env / (env.max() + 1e-9))


def similar(a, b):
    n = min(len(a['env']), len(b['env']))
    if n < 20 or abs(len(a['env']) - len(b['env'])) > 0.05 * n:
        return 0.0
    return float(np.corrcoef(a['env'][:n], b['env'][:n])[0, 1])


# ================================================================================================= script v voice
def words_of(text):
    """The script's words with their syllables and whether a pause may follow (punctuation)."""
    ws = text.split()
    return [(w, syllables_in(w) if re.search('[A-Za-z]', w) else 0, bool(re.search(r'[,.?!;:—-]$', w)))
            for w in ws]


def fit(words, counts):
    """Lay the script's words (in order, every one) over the measured phrases so the syllables match best; a phrase
    may get no words (something said that the script lacks). A phrase ending mid-sentence costs a little. Returns
    [(first word, after last word)] per phrase."""
    n, m = len(counts), len(words)
    syl = np.concatenate([[0], np.cumsum([w[1] for w in words])])
    inf = 1e9
    cost = np.full((n + 1, m + 1), inf)
    back = np.zeros((n + 1, m + 1), int)
    cost[0, 0] = 0
    for p in range(n):
        for k in range(m + 1):
            if cost[p, k] >= inf:
                continue
            for k2 in range(k, m + 1):
                a = syl[k2] - syl[k]
                if k2 == k:
                    c = counts[p] + 1.0
                else:
                    c = abs(a - counts[p]) + (0.0 if (words[k2 - 1][2] or k2 == m) else 1.0)
                if cost[p, k] + c < cost[p + 1, k2]:
                    cost[p + 1, k2], back[p + 1, k2] = cost[p, k] + c, k
    out, k = [], m
    for p in range(n, 0, -1):
        out.append((back[p, k], k))
        k = back[p, k]
    return out[::-1]


def script_check(ln, voice):
    """One line: its phrases, the syllables heard in each, the script's words laid over them, and the faults."""
    ph = phrases(voice)
    db = envelope(voice)
    nuc = nuclei(db, ph)
    counts = [sum(1 for x in nuc if a <= x <= b) for a, b in ph]
    words = words_of(ln['text'])
    spans = fit(words, counts) if ph else []
    rows, faults = [], []
    for (a, b), c, (k0, k1) in zip(ph, counts, spans):
        said = ' '.join(w[0] for w in words[k0:k1])
        s = sum(w[1] for w in words[k0:k1])
        rows.append(dict(a=a, b=b, heard=c, script=s, words=said))
        tol = max(2.5, 0.3 * max(s, c))
        at = f"line {ln.get('n', '?')} ({ln['who']}), {a:.1f}-{b:.1f} s into the recording"
        if not said and c >= 2:
            whole = sum(w[1] for w in words)
            again = (' It is about the size of the whole line: the line said again? (fine if meant, a chant: then '
                     'write it out each time it is said)') if abs(c - whole) <= max(2, 0.3 * whole) else ''
            faults.append(f'{at}: about {c} syllables said that no script word covers (said but missing from the '
                          f'script and subtitles?).{again}')
        elif said and c - s > tol:
            faults.append(f'{at}: the voice says about {c} syllables, the script about {s} ("{said}"): words said '
                          f'that the script lacks?')
        elif said and s - c > tol:
            faults.append(f'{at}: the script has about {s} syllables ("{said}"), the voice about {c}: words in the '
                          f'script that were not said?')
    total = sum(w[1] for w in words)
    talk = sum(b - a for a, b in ph)
    if talk and not 1.8 <= total / talk <= 7.5:
        faults.append(f"line {ln.get('n', '?')} ({ln['who']}): {total} script syllables in {talk:.1f} s of speech "
                      f"({total / talk:.1f} a second; natural speech is 3-6): the script and recording don't match")
    return rows, faults


# ================================================================================================= subtitles
def _norm(w):
    return re.sub(r"[^a-z0-9*']", '', w.lower().replace('’', "'")).strip("'")


def _match(cap, scr):
    if '*' in cap:
        return re.fullmatch(cap.replace('*', '[a-z]*'), scr) is not None
    return cap == scr


def captions(film, step=0.05):
    """The subtitles as shown: [(t0, t1, text)]."""
    end = getattr(film, 'BLACK_AT', getattr(film, 'DUR'))
    out = []
    for i in range(int(end / step) + 1):
        t = i * step
        c = film.caption_at(t)
        if out and out[-1][2] == c and abs(out[-1][1] - t) < step * 1.5:
            out[-1][1] = t + step
        elif c:
            out.append([t, t + step, c])
    return [tuple(x) for x in out]


def caption_check(film, lines):
    faults = []
    caps = captions(film)
    per = {id(ln): [] for ln in lines}
    for t0, t1, c in caps:
        near = [ln for ln in lines if ln['start'] + ln['_speech'][0] - 0.4 <= t0 <= ln['start'] + ln['_speech'][1] + 0.7]
        if not near:
            faults.append(f'subtitle "{c}" at {t0:.2f}-{t1:.2f} s, when no line is being spoken')
            continue
        per[id(max(near, key=lambda ln: ln['start']))].append(c)
    for ln in lines:
        scr = [_norm(w) for w in ln['text'].split() if _norm(w)]
        cap = [_norm(w) for c in per[id(ln)] for w in c.split() if _norm(w)]
        cap = [next((s for s in scr if _match(w, s)), w) if '*' in w else w for w in cap]
        if not cap:
            faults.append(f"line {ln.get('n', '?')} ({ln['who']}): no subtitles while it is spoken")
            continue
        sm = difflib.SequenceMatcher(None, scr, cap, autojunk=False)
        for op, i0, i1, j0, j1 in sm.get_opcodes():
            if op == 'equal':
                continue
            a, b = ' '.join(scr[i0:i1]), ' '.join(cap[j0:j1])
            what = {'delete': f'in the script, not the subtitles: "{a}"',
                    'insert': f'in the subtitles, not the script: "{b}"',
                    'replace': f'script "{a}", subtitles "{b}"'}[op]
            faults.append(f"line {ln.get('n', '?')} ({ln['who']}): {what}")
    return faults


# ================================================================================================= mouths
OPENNESS = {'rest': 0.0, 'set': 0.0, 'line': 0.0, 'closed': 0.0, 'shut': 0.0, 'smile': 0.0, 'frown': 0.0,
            'MBP': 0.0, 'FV': 0.2, 'etc': 0.35, 'WQ': 0.35, 'U': 0.4, 'L': 0.5, 'E': 0.55, 'O': 0.75, 'AI': 1.0,
            'open': 0.7, 'shout': 1.0, 'agape': 0.8, 'oh': 0.7}
OPEN, SHUT, SWING = 0.3, 0.15, 0.25        # open enough to see; shut; how far it must move to count as a movement


def openness(film, mouth):
    table = dict(OPENNESS, **getattr(film, 'MOUTH_OPENNESS', {}))
    if isinstance(mouth, str) and mouth.startswith('v:'):
        mouth = mouth[2:]
    return table.get(mouth)


def movements(seq):
    """How many times a mouth opens and closes again (by at least SWING) over a run of openness values."""
    count, lo, hi = 0, (seq[0] if seq else 0.0), None
    for v in seq:
        if hi is None:
            lo = min(lo, v)
            if v - lo >= SWING:
                hi = v
        else:
            hi = max(hi, v)
            if hi - v >= SWING:
                count, hi, lo = count + 1, None, v
    return count + (hi is not None)


def speaker_of(film, name, whos):
    pats = getattr(film, 'SPEAKERS', {})
    for w in whos:
        for p in pats.get(w, [w]):
            if fnmatch.fnmatch(name, p) or (name.startswith(p) and name[len(p):].isdigit()):
                return w
    return None


_FILM = None


def _faces_at(t):
    return t, _FILM.mouths_seen(t)


def faces_over(film, t0, t1):
    """{name: {frame: mouth}} for the speakers' readable faces (on screen, not turned away, head 12 px or more)."""
    global _FILM
    fps = getattr(film, 'FPS', 12)
    whos = sorted({ln['who'] for ln in film.LINES})
    frames = range(int(round(t0 * fps)), int(t1 * fps))
    seen = {}
    if hasattr(film, 'mouths_seen'):
        _FILM = film
        from multiprocessing import Pool
        with Pool(os.cpu_count()) as pool:
            for t, faces in pool.imap(_faces_at, [i / fps for i in frames], chunksize=4):
                for name, mouth, yaw, px in faces:
                    w = speaker_of(film, name, whos)
                    if w and abs(yaw) <= 100 and px >= 12:
                        seen.setdefault((w, name), {})[round(t * fps)] = mouth
    else:                                   # only the lip-sync track: assumed always on screen
        import mouths
        for w, trk in getattr(film, 'TRACK', {}).items():
            seen[(w, w)] = {i: 'v:' + mouths.at(trk, i / fps) for i in frames}
    return seen


def mouth_check(film, lines, t0, t1):
    fps = getattr(film, 'FPS', 12)
    allowed = getattr(film, 'ALLOWED_MOUTHS', [])
    seen = faces_over(film, t0, t1)
    faults, unknown, used = [], set(), {}
    speech = {}                                      # each speaker's stretches of voice, in film time
    for ln in lines:
        speech.setdefault(ln['who'], []).extend((ln['start'] + a, ln['start'] + b) for a, b in ln['_stretches'])
    groups = {}
    for (who, name) in seen:
        groups.setdefault(who, []).append(name)
    series = {}                                      # (who, name) -> {frame: openness}; a crowd also as one face
    for (who, name), fr in sorted(seen.items()):
        op = {}
        for i, m in fr.items():
            v = openness(film, m)
            if v is None:
                unknown.add(m)
            else:
                op[i] = v
        series[(who, name)] = op
    for who, names in groups.items():
        if len(names) > 1 or names[0] != who:        # a group (CROWD17, CROWD240...): its loudest mouth each frame
            op = {}
            for n in names:
                for i, v in series[(who, n)].items():
                    op[i] = max(op.get(i, 0.0), v)
            series[(who, f'{who} (any of {len(names)} faces)')] = op
    silent = {}                                      # mouth open in silence: (who, span) -> [names]
    for (who, name), op in sorted(series.items()):
        group = name.startswith(f'{who} (any')
        member = not group and (len(groups[who]) > 1 or name != who)
        st = speech.get(who, [])

        def talking(t):
            return any(a - 0.13 <= t <= b + 0.17 for a, b in st)

        def ok(t):
            for e in allowed:
                if fnmatch.fnmatch(name, e[0]) or e[0] == who:
                    if (e[1] is None or t >= e[1]) and (e[2] is None or t <= e[2]):
                        used[e[3]] = used.get(e[3], 0) + 1
                        return True
            return False
        if not group:                                # each face shuts when the voice stops
            bad = [i for i in sorted(op) if op[i] >= OPEN and not talking(i / fps) and not ok(i / fps)]
            for a, b in _runs(bad):
                if b - a + 1 >= 2:
                    silent.setdefault((who, a, b), []).append(name)
            if member:                               # one face of a crowd: some may be silent; the group is tested
                continue
        # still while the voice speaks
        for a, b in st:
            idx = [i for i in range(int(np.ceil(a * fps)), int(b * fps) + 1) if i in op]
            shut = [i for i in idx if op[i] < SHUT]
            for r0, r1 in _runs(shut):
                if (r1 - r0 + 1) / fps >= 0.4:
                    faults.append(f'{name}: mouth still and shut at {r0 / fps:.2f}-{(r1 + 1) / fps:.2f} s while '
                                  f'the voice speaks')
        # movements per syllable, phrase by phrase: no more open-and-shut movements than about one a syllable, and
        # the drawing changing often enough to read as speech (at 12 frames a second a mouth can't shut between
        # every syllable of quick speech, so the low test counts changes of shape)
        fr = seen.get((who, name), {})
        for ln in lines:
            if ln['who'] != who:
                continue
            for r in ln['_rows']:
                a, b = ln['start'] + r['a'], ln['start'] + r['b']
                idx = list(range(int(np.floor((a - 0.1) * fps)), int(np.ceil((b + 0.1) * fps)) + 1))
                vis = [i for i in idx if i in op]
                if len(vis) < 0.8 * len(idx):
                    continue
                n = movements([op[i] for i in vis])
                changes = sum(1 for i, j in zip(vis, vis[1:]) if abs(op[i] - op[j]) > 0.01
                              or (fr and fr.get(i) != fr.get(j)))
                ref = r['script'] or r['heard']
                what = f"{name}: \"{r['words'] or '(no script words)'}\" at {a:.2f}-{b:.2f} s"
                if ref and n > ref * 1.5:
                    faults.append(f'{what}: the mouth opens and shuts {n} times for about {ref} syllable'
                                  f"{'s' if ref > 1 else ''}")
                elif ref >= 3 and changes < ref * 0.4:
                    faults.append(f'{what}: the mouth changes only {changes} times for about {ref} syllables')
    for (who, a, b), names in sorted(silent.items(), key=lambda x: x[0][1]):
        face = names[0] if len(names) == 1 else f'{who} ({len(names)} faces: {", ".join(names[:4])}...)'
        faults.append(f'{face}: mouth open in silence at {a / fps:.2f}-{(b + 1) / fps:.2f} s; it should shut when '
                      f'the voice stops')
    notes = [f'{n} frame(s) of "{why}" allowed' for why, n in used.items()]
    if unknown:
        notes.append('mouths not read (add them to MOUTH_OPENNESS): ' + ', '.join(sorted(map(str, unknown))))
    if not hasattr(film, 'mouths_seen'):
        notes.append('read from the lip-sync TRACK only (the film has no mouths_seen(t)): mouths drawn over it '
                     '(a horror jaw, a gasp) are not seen')
    return faults, notes, seen


def _runs(idx):
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return out


# ================================================================================================= the audit
def prepared(film):
    """The film's lines with their recordings measured (their own voices, as the film places them). A line with no
    recording yet keeps the film's placeholder timing (its 'end', or its _stretches) and gets no script check."""
    out = []
    for ln in film.LINES:
        ln = dict(ln)
        v = ln.get('_voice')
        path = os.path.join(MA.HERE, 'audio', f"{ln.get('audio')}.m4a")
        if v is None and ln.get('audio') and os.path.exists(path):
            v = MA.line(ln['audio'])
        if v is None:
            ln['_stretches'] = ln.get('_stretches') or ([(0.0, ln['end'] - ln['start'])] if ln.get('end') else [])
            ln['_rows'], ln['_faults'], ln['_placeholder'] = [], [], True
        else:
            ln['_stretches'] = ln.get('_stretches') or MA.pauses(v, 0.12)
            ln['_rows'], ln['_faults'] = script_check(ln, v)
        if not ln['_stretches']:
            continue
        ln['_speech'] = (ln['_stretches'][0][0], ln['_stretches'][-1][1])
        out.append(ln)
    return out


def audit(film, t0=None, t1=None, mouths=True):
    """Every fault (lines of text), plus notes and the tables behind them."""
    lines = prepared(film)
    faults = [f for ln in lines for f in ln['_faults']]
    if hasattr(film, 'caption_at'):
        faults += caption_check(film, lines)
    notes, seen = [], {}
    if any(ln.get('_placeholder') for ln in lines):
        notes.append('no recording yet for line(s) ' + ', '.join(str(ln.get('n', ln['text'][:20])) for ln in lines
                                                            if ln.get('_placeholder')) + ': placeholder timing, no '
                     'script check; run this again when they arrive')
    if mouths:
        end = getattr(film, 'BLACK_AT', getattr(film, 'DUR'))
        mf, mn, seen = mouth_check(film, lines, t0 or 0.0, t1 or end)
        faults += mf
        notes += mn
    return faults, notes, lines, seen


def check(film):
    """For pre-flight: the faults as lines (no LINES: nothing to check)."""
    if not hasattr(film, 'LINES'):
        return []
    faults, notes, _, _ = audit(film)
    return ['script/mouth: ' + f for f in faults]


def report(film, t0=None, t1=None, mouths=True):
    faults, notes, lines, seen = audit(film, t0, t1, mouths)
    print('SCRIPT v VOICE (syllables heard / in the script, phrase by phrase):')
    for ln in lines:
        print(f"  line {ln.get('n', '?')} {ln['who']}:")
        for r in ln['_rows']:
            print(f"    {r['a']:5.2f}-{r['b']:5.2f} s  {r['heard']:2d} / {r['script']:2d}  {r['words'] or '(no script words)'}")
    if mouths:
        print('MOUTHS: faces read', ', '.join(f'{n} ({len(f)} frames)' for (w, n), f in sorted(seen.items())
                                              if not n.startswith('CROWD')) or 'none',
              f"+ {sum(1 for w, n in seen if n.startswith('CROWD'))} crowd faces")
    for n in notes:
        print('  note:', n)
    print()
    print(f'{len(faults)} fault(s)' + (':' if faults else ''))
    for f in faults:
        print('  -', f)
    return faults


def main():
    args = sys.argv[1:]
    if '--film' in args:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        film = importlib.import_module(args[args.index('--film') + 1])
        t0 = float(args[args.index('--from') + 1]) if '--from' in args else None
        t1 = float(args[args.index('--to') + 1]) if '--to' in args else None
        report(film, t0, t1, '--no-mouths' not in args)
        return
    script = []
    if '--script' in args:
        k = args.index('--script')
        script = [l.strip() for l in open(args[k + 1]) if l.strip()]
        args = args[:k] + args[k + 2:]
    ms = [measure(p) for p in args]
    for m in ms:
        sts = ', '.join(f'{a:.2f}-{b:.2f}' for a, b in m['stretches'])
        print(f"{os.path.basename(m['path'])}: {m['dur']:.1f} s, ~{m['syll']} syllables, {len(m['stretches'])} phrases "
              f"[{sts}], {m['lufs']:.1f} LUFS")
    print()
    dup = False
    for i, a in enumerate(ms):
        for b in ms[i + 1:]:
            if a['hash'] == b['hash'] or similar(a, b) > 0.97:
                dup = True
                print(f"DUPLICATE: {os.path.basename(a['path'])} and {os.path.basename(b['path'])} are the same take")
    if not dup:
        print('No duplicates.')
    if script:
        # Expected size of each script line, to compare with the measurements above. (Matching files to lines by
        # measurement alone was tried on The Patriots 2 and got 2 of 7 right: the file name, numbered by script line,
        # is what identifies a take; when a name and a measurement disagree, ask Sam. Once the film's LINES exist,
        # `--film FILM` checks each take phrase by phrase.)
        print()
        print('Script lines (expected syllables, and speech at a natural 3-4 syllables a second):')
        for j, l in enumerate(script, 1):
            syl = syllables_in(l.split(':', 1)[-1])
            print(f'  {j}. ~{syl} syllables, {syl / 4.2:.1f}-{syl / 3.0:.1f} s: {l[:70]}')


if __name__ == '__main__':
    main()
