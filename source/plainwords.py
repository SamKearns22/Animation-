#!/usr/bin/env python3
"""plainwords: every message to Sam is read for plain words before it reaches him (Sam, 26 Nov: CLAUDE.md "Checked on
every message"; R8 chat 2). A Stop hook (a script the chat app runs each time a chat finishes a reply; it can send
the reply back once with a reason) reads the reply and sends it back ONCE to be rewritten when it holds a file name,
a label or code ("R8", "A1", "Q2"), or a project word without an everyday explanation in the same sentence. It never
loops: on the second try (stop_hook_active) it lets the reply through and logs it (LET_LOG). When Sam types "I don't
understand" / "explain" (and the like), the message he replied to is saved as a new example in notes/learn/plain-words/
and the project words it used go on the checker's list (WORDS), so the same words are caught next time.

MAP
  WORDS .............. notes/learn/plain-words/words.json: project words that need an everyday explanation where
                       they appear ({"words": [...], "learned": [{"word", "from", "t"}]})
  faults(text) ....... [(kind, what, sentence)]: kinds 'file' (file names, paths), 'code' (snake_case, CamelCase,
                       `backticks`), 'label' (R8, A1, Q2, N8 ...), 'word' (a listed project word, unexplained)
  explained(sent, w) . the sentence explains the word: brackets, a dash, "which/that/meaning/means/is a/: " after it
  skip_line(line) .... lines that may hold code names: "For Claude:" (the handover's line for them), quoted blocks
  hook() ............. Stop hook: block once with the faults; on stop_hook_active let through and log; Override skips
  learn() ............ UserPromptSubmit hook: Sam's "I don't understand"/"explain" saves the last reply as bad-N and
                       adds its flagged and quoted/bold terms to WORDS
  score() ............ the saved examples: bad-* must fail, good-* must pass (kittest plain_words_every_message)

    python3 source/plainwords.py check FILE|-     print the faults in a message (exit 1 if any)
    python3 source/plainwords.py score            run the saved examples
    python3 source/plainwords.py hook | learn     (hooks; read the hook's JSON on stdin)
"""
import glob
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, 'notes', 'learn', 'plain-words')
WORDS = os.path.join(EX, 'words.json')
LET_LOG = os.path.join(ROOT, 'notes', 'logs', 'plainwords.log')
STATE = os.path.join(ROOT, 'notes', 'logs', 'plainwords-blocks.jsonl')

FILE_RE = re.compile(r'(?<![\w@])(?:source|notes|guides|animations|story|story|assets|\.claude|~)/[\w./-]*'
                     r'|(?<![\w@])[\w.-]+/[\w.-]+/[\w./-]+'
                     r'|\b[\w-]+\.(?:py|md|json|jsonl|tsv|csv|sh|log|txt|html|yaml|yml)\b')
CODE_RE = re.compile(r'`[^`\n]+`|\b[a-z]+(?:_[a-z0-9]+)+\b|\b[a-z]+[A-Z][a-zA-Z]+\b|\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b')
LABEL_RE = re.compile(r'\b[A-Z]{1,2}\d{1,3}[a-z]?\b')
URL_RE = re.compile(r'https?://\S+')
# labels Sam uses himself, or that are everyday: TikTok, YouTube, iPhone, MP4, 3D ...
LABEL_OK = {'MP4', 'MP3', 'GIF', 'PNG', 'JPG', 'UK', 'US', 'TV', 'PM', 'AM', 'OK', '3D', '2D', 'MB', 'GB', 'KB', 'A4'}
CODE_OK = {'TikTok', 'YouTube', 'iPhone', 'iPad', 'GitHub', 'CranbriJoos', 'iOS', 'macOS', 'ChatGPT', 'OpenAI',
           'PowerPoint', 'WhatsApp', 'LinkedIn', 'McDonald', 'McDonalds', 'MacBook'}
EXPLAIN_RE = re.compile(r'\s*(?:\(|[-–—:]\s|,?\s*(?:which|that|meaning|means|is a|is an|are|is the|, a|, an|, the|i\.e\.))',
                        re.I)
CONFUSED_RE = re.compile(r"\b(?:i\s+don'?t\s+understand|i\s+do\s+not\s+understand|don'?t\s+follow|"
                         r"i'?m\s+lost|what\s+do(?:es)?\s+(?:you|that|this|it)\s+mean|explain|in\s+simple\s+language|"
                         r"simpler|plain\s+(?:words|english|language))\b", re.I)


def words():
    try:
        d = json.load(open(WORDS, encoding='utf-8'))
    except (OSError, ValueError):
        d = {'words': [], 'learned': []}
    return d


def _sentences(text):
    """Sentences, one per line piece; markdown marks dropped, so '**kit tests**' reads as 'kit tests'."""
    out = []
    for line in text.splitlines():
        if skip_line(line):
            continue
        line = re.sub(r'[*_]{2}', '', line)
        line = URL_RE.sub('', line)
        out += [s.strip() for s in re.split(r'(?<=[.!?])\s+', line) if s.strip()]
    return out


def skip_line(line):
    s = line.strip().lower()
    return s.startswith(('for claude', '>', 'checks:'))


def explained(sent, w):
    """True when the sentence explains the word right where it is used."""
    m = re.search(r'\b' + re.escape(w) + r's?\b', sent, re.I)
    if not m:
        return True
    return bool(EXPLAIN_RE.match(sent[m.end():]))


def faults(text, wordlist=None):
    wl = words()['words'] if wordlist is None else wordlist
    out, seen = [], set()

    def add(kind, what, sent):
        if (kind, what.lower()) not in seen:
            seen.add((kind, what.lower()))
            out.append((kind, what, sent))
    for sent in _sentences(text):
        for m in FILE_RE.finditer(sent):
            add('file', m.group(0), sent)
        for m in CODE_RE.finditer(sent):
            if m.group(0) not in CODE_OK and not FILE_RE.search(m.group(0)):
                add('code', m.group(0), sent)
        for m in LABEL_RE.finditer(sent):
            if m.group(0) not in LABEL_OK:
                add('label', m.group(0), sent)
        for w in wl:
            if re.search(r'\b' + re.escape(w) + r's?\b', sent, re.I) and not explained(sent, w):
                add('word', w, sent)
    return out


def say(fs, limit=12):
    kinds = {'file': 'a file or folder name', 'code': 'a code name', 'label': 'a label or code',
             'word': 'a project word with no everyday explanation in the same sentence'}
    return '\n'.join(f'- "{w}" ({kinds[k]}): "{s[:140]}"' for k, w, s in fs[:limit])


def block_reason(fs):
    return ('Plain-words check (Sam, 26 Nov: every message to him in everyday words, written for someone who has never '
            'seen the project). This reply holds:\n' + say(fs) +
            '\nRewrite only those sentences in everyday words: say what each thing is and what it does for the film, '
            'or leave it out. Code names may stay only on a "For Claude:" line. Send only the rewritten message, once '
            '(Sam must not get it twice).')


def _log(rec):
    os.makedirs(os.path.dirname(LET_LOG), exist_ok=True)
    rec = dict(rec, t=time.strftime('%Y-%m-%d %H:%M'))
    with open(LET_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')


def _last_reply(path):
    """The chat's last reply text (all text blocks of the last assistant turn, after Sam's last real message)."""
    if not path or not os.path.exists(path):
        return ''
    texts = []
    for line in open(path, encoding='utf-8', errors='replace'):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        msg = e.get('message') or {}
        if e.get('type') == 'user' and isinstance(msg.get('content'), str):
            texts = []
        elif e.get('type') == 'assistant':
            for c in msg.get('content') or []:
                if isinstance(c, dict) and c.get('type') == 'text':
                    texts.append(c['text'])
    return texts[-1] if texts else ''


def hook(stdin=None):
    try:
        data = json.loads(stdin if stdin is not None else sys.stdin.read() or '{}')
    except ValueError:
        return 0
    reply = data.get('last_assistant_message') or _last_reply(data.get('transcript_path'))
    fs = faults(reply)
    chat = os.path.basename(data.get('transcript_path') or 'unknown')[:8]
    if not fs:
        return 0
    if data.get('stop_hook_active'):          # the second try (or another hook blocked first): never loop; leave a trace
        _log({'chat': chat, 'event': 'let-through', 'faults': [list(f[:2]) for f in fs], 'reply': reply[:3000]})
        return 0
    try:
        sys.path.insert(0, os.path.join(ROOT, 'source'))
        if __import__('override').skip('plain-words check: ' + ', '.join(f[1] for f in fs), data.get('transcript_path'),
                                       sys.stderr):
            return 0
    except Exception:
        pass
    _log({'chat': chat, 'event': 'block', 'faults': [list(f[:2]) for f in fs]})
    print(json.dumps({'decision': 'block', 'reason': block_reason(fs)}))
    return 0


def _terms(text):
    """Terms a confusing message leaned on: its flagged project words and labels, and quoted or bold phrases."""
    out = [w for k, w, _ in faults(text) if k in ('word',)]
    for m in re.finditer(r'\*\*([^*\n]{3,40})\*\*|"([^"\n]{3,30})"|“([^”\n]{3,30})”', text):
        t = (m.group(1) or m.group(2) or m.group(3)).strip().strip('.:').lower()
        if 1 <= len(t.split()) <= 3 and not re.search(r'\d|[?!]', t):
            out.append(t)
    return out


def learn(stdin=None, sam_text=None, reply=None):
    """Sam's "I don't understand" / "explain": save the message he replied to, and add its terms to the list."""
    if sam_text is None:
        try:
            data = json.loads(stdin if stdin is not None else sys.stdin.read() or '{}')
        except ValueError:
            return 0
        sam_text = data.get('prompt') or ''
        reply = _last_reply(data.get('transcript_path'))
    if not CONFUSED_RE.search(sam_text or '') or not (reply or '').strip():
        return 0
    n = 1 + max([int(m.group(1)) for f in glob.glob(os.path.join(EX, 'bad-*.md'))
                 for m in [re.match(r'bad-(\d+)', os.path.basename(f))] if m] or [0])
    path = os.path.join(EX, f'bad-{n}-auto-{time.strftime("%d%b").lower()}.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'# Saved example (auto, {time.strftime("%d %b %H:%M")})\nSam\'s reply: "{sam_text.strip()[:300]}"\n\n'
                f'## The message as sent\n\n{reply.strip()}\n')
    d = words()
    for t in _terms(reply):
        if t not in [w.lower() for w in d['words']]:
            d['words'].append(t)
            d['learned'].append({'word': t, 'from': os.path.basename(path), 't': time.strftime('%Y-%m-%d %H:%M')})
    json.dump(d, open(WORDS, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(f'plainwords: saved the message Sam did not follow as {os.path.relpath(path, ROOT)}; its words are on the list')
    return 0


def example_text(path):
    t = open(path, encoding='utf-8').read()
    return t.split('## The message as sent', 1)[-1]


def score():
    """{name: (expected, faults)} over the saved examples: bad-* must fail, good-* must pass."""
    res = {}
    for f in sorted(glob.glob(os.path.join(EX, '*.md'))):
        b = os.path.basename(f)
        if b.startswith(('bad-', 'good-')):
            res[b] = ('fail' if b.startswith('bad-') else 'pass', faults(example_text(f)))
    return res


def main(argv):
    cmd = argv[0] if argv else '-h'
    if cmd in ('hook', 'learn'):
        try:
            sys.path.insert(0, os.path.join(ROOT, 'source'))
            __import__('hookran').ran('plainwords.py ' + cmd)     # the watcher's "seen running" mark
        except Exception:
            pass
        return hook() if cmd == 'hook' else learn()
    if cmd == 'check':
        text = sys.stdin.read() if len(argv) < 2 or argv[1] == '-' else open(argv[1], encoding='utf-8').read()
        fs = faults(text)
        print(say(fs, 99) or 'plain: no faults')
        return 1 if fs else 0
    if cmd == 'score':
        bad = 0
        for b, (want, fs) in score().items():
            ok = bool(fs) == (want == 'fail')
            bad += not ok
            print(f"{'ok ' if ok else 'BAD'} {b}: must {want}; {len(fs)} faults "
                  + ', '.join(f'"{w}"' for _, w, _ in fs[:8]))
        return 1 if bad else 0
    print(__doc__)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
