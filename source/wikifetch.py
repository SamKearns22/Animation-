#!/usr/bin/env python3
"""MAP  wikifetch (Open Wounds chat 39, Sam, 26 Nov: "You have solved the Wikimedia problem before in this project, try
again with that fix implemented"). Wikimedia answers a bare request with an error page and a fast one with 429 (too
many requests): the fix found in Ad-vanced Notice (notes/archive/ad-vanced-notice-handovers.md) was the API with a
User-Agent, one request every ~6 s. Kept here so every film gets it instead of finding it again.

    python3 source/wikifetch.py search "WORDS" [N]          files on Commons matching WORDS (title, size, licence)
    python3 source/wikifetch.py get "File:NAME" OUT [WIDTH]  a WIDTH px thumbnail (default 500; the nearest size served) to OUT
"""
import json
import sys
import time
import urllib.parse
import urllib.error
import urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'AnimationReferenceFetcher/1.0 (reference photos for drawing; low volume)'   # generic: no personal details
GAP = 6.0                                       # seconds between requests (429s otherwise)
THUMBS = (250, 330, 500, 960, 1280)             # the thumbnail widths Wikimedia serves (w.wiki/GHai, chat 39: the
#                                                 full file got a 429 telling us to use these; a thumb always)
_last = [0.0]


def _open(url, retry=False):
    wait = GAP - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code != 429 or retry:
            raise
        time.sleep(30)                          # one slow retry, then stop (one failed try per source)
        return _open(url, retry=True)


def api(**q):
    q.update(format='json')
    return json.loads(_open(API + '?' + urllib.parse.urlencode(q)))


def search(words, n=10):
    r = api(action='query', list='search', srsearch=words, srnamespace=6, srlimit=n)
    return [x['title'] for x in r['query']['search']]


def info(title, width=None):
    q = dict(action='query', titles=title, prop='imageinfo', iiprop='url|size|extmetadata')
    if width:
        q['iiurlwidth'] = width
    p = list(api(**q)['query']['pages'].values())[0]['imageinfo'][0]
    m = p.get('extmetadata', {})
    return dict(url=p.get('thumburl') or p['url'], size=(p['width'], p['height']),
                licence=m.get('LicenseShortName', {}).get('value', '?'))


def get(title, out, width=500):
    width = min(THUMBS, key=lambda w: abs(w - (width or 500)))
    i = info(title, width)
    data = _open(i['url'])
    if data[:15].lstrip().lower().startswith((b'<!doctype', b'<html')):
        raise RuntimeError(f'{title}: Wikimedia sent an error page, not the file')
    open(out, 'wb').write(data)
    return i


if __name__ == '__main__':
    if sys.argv[1] == 'search':
        for t in search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 10):
            print(t)
    elif sys.argv[1] == 'get':
        i = get(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 500)
        print(sys.argv[3], i['size'], i['licence'])
