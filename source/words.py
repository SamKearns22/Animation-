#!/usr/bin/env python3
"""Word times from Sam's own recordings (speech-to-text), for every film (chat 29 of Open Wounds, 26 Nov; Sam: "Y install").

MAP
  times(path) ........ [(start, end, word)] seconds into the take; heard once by faster-whisper and saved beside the
                       take as NAME.words.json, so a later chat (or one without the tool) reads the saved times
  text(path) ......... the words heard, as one string (to check a take is the line, or which half of it)
  track(words, env) .. the lip track for one line from its word times: each word's shapes inside its own time, so the
                       mouth moves on the real moment each word is said (was: syllables spread evenly over the line)
  at_word(words, w) .. when the k-th word matching w starts (moves and beats land on it)

    python3 source/words.py hear TAKE.m4a [TAKE ...]        print each take's words and times (saves the .words.json)

The tool: faster-whisper (setup.sh installs it). The audio is decoded with the project's own ffmpeg, never PyAV's
reader (its newer versions refuse faster-whisper's call: chat 29). The model 'small.en' downloads once, on first use.
"""
import json
import os
import re
import subprocess
import sys

MODEL = 'small.en'
_M = []


def _model():
    if not _M:
        from faster_whisper import WhisperModel
        _M.append(WhisperModel(MODEL, device='cpu', compute_type='int8'))
    return _M[0]


def _pcm16k(path):
    import numpy as np
    import imageio_ffmpeg
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', '16000',
                          '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def _saved(path):
    return os.path.splitext(path)[0] + '.words.json'


def times(path):
    """[(start, end, word)] for one take, heard once and saved beside it."""
    sp = _saved(path)
    if os.path.exists(sp) and os.path.getmtime(sp) >= os.path.getmtime(path):
        return [tuple(w) for w in json.load(open(sp))['words']]
    segs, _ = _model().transcribe(_pcm16k(path), word_timestamps=True, language='en')
    out = [(round(w.start, 3), round(w.end, 3), w.word.strip()) for s in segs for w in s.words]
    json.dump({'take': os.path.basename(path), 'model': MODEL, 'words': out}, open(sp, 'w'), indent=0)
    return out


def text(path):
    return ' '.join(w for _, _, w in times(path))


def _bare(w):
    return re.sub(r"[^a-z0-9']", '', w.lower())


def at_word(words, w, k=1):
    """When the k-th word equal to w (punctuation and case ignored) starts; a phrase matches its first word in a run."""
    want = [_bare(x) for x in w.split()]
    n = 0
    for i in range(len(words)):
        if [_bare(x[2]) for x in words[i:i + len(want)]] == want:
            n += 1
            if n == k:
                return words[i][0]
    raise KeyError(f'{w!r} not heard in the take')


def track(words, env=None, env_rate=100, lead=1 / 12):
    """The lip track [(t0, t1, shape)] for one line: each word's shapes inside that word's own time."""
    import mouths
    out = []
    for a, b, w in words:
        b = max(b, a + 0.06)
        out += mouths.track(w, [(a, b)], env=env, env_rate=env_rate, lead=lead)
    out.sort()
    return out


def main(argv):
    if len(argv) >= 2 and argv[0] == 'hear':
        for p in argv[1:]:
            ws = times(p)
            print(f'{os.path.basename(p)}: {ws[0][0]:.2f}-{ws[-1][1]:.2f} s: ' + ' '.join(w for _, _, w in ws))
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
