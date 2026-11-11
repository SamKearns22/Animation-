#!/usr/bin/env python3
"""costbreak: where one chat's cost went, by kind of step (budget job, 11 Nov).

MAP
  kind() ....... names a step from its tool calls (look at a picture, read a guide, draw, edit code, helper...)
  breakdown() .. per kind: steps, cost of re-reading the history, cost of new material, cost of writing
  main() ....... python3 source/costbreak.py [TRANSCRIPT.jsonl ...]   (default: this chat's, plus its helpers')

A step's re-reading and writing cost go to its own kind; the new material it adds to the history (tool results)
is charged when the NEXT step stores it, so that cost goes to the kind of the step that produced it.
Prices and the week's allowance come from the cost watch (.claude/hooks/costwatch.py): good to about +-20%.
"""
import glob, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.claude', 'hooks'))
import costwatch as CW


def kind(tools):
    if not tools:
        return 'talk (reply or thinking, no tool)'
    ks = []
    for name, inp in tools:
        s = json.dumps(inp)
        p = inp.get('file_path', '') or ''
        if name == 'Read' and p.lower().endswith(('.jpg', '.jpeg', '.png')):
            ks.append('look at a picture')
        elif name == 'Read' and ('/guides/' in p or p.endswith('CLAUDE.md')):
            ks.append('read a guide')
        elif name == 'Read' and '/notes/' in p:
            ks.append('read notes')
        elif name in ('Read', 'Grep', 'Glob'):
            ks.append('read code or search')
        elif name in ('Edit', 'Write', 'NotebookEdit'):
            ks.append('write or edit code/notes')
        elif name in ('Agent', 'Task'):
            ks.append('helper (start and result)')
        elif name == 'Bash':
            if 'guides/' in s and ('cat ' in s or 'sed -n' in s or 'grep' in s):
                ks.append('read a guide')
            elif 'git ' in s:
                ks.append('git (merge, commit, push)')
            elif 'python3' in s:
                ks.append('run a tool (draw, check, critique)')
            else:
                ks.append('shell (other)')
        else:
            ks.append('other tool: ' + name.split('__')[-1])
    order = ['look at a picture', 'helper (start and result)', 'write or edit code/notes', 'read a guide', 'read notes',
             'read code or search', 'run a tool (draw, check, critique)', 'git (merge, commit, push)']
    for o in order:
        if o in ks:
            return o
    return ks[0]


def steps(path):
    seen, out = {}, []
    for raw in open(path, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(raw)
        except Exception:
            continue
        m = d.get('message')
        if d.get('type') != 'assistant' or not isinstance(m, dict) or not m.get('usage'):
            continue
        tools = [(c.get('name', ''), c.get('input') or {}) for c in m.get('content', []) if c.get('type') == 'tool_use']
        if m.get('id') in seen:                      # one reply is several lines with the same usage
            seen[m['id']]['tools'] += tools
            continue
        u = m['usage']
        st = {'tools': tools, 'fam': CW.fam(m.get('model')), 'rd': u.get('cache_read_input_tokens', 0),
              'wr': u.get('cache_creation_input_tokens', 0), 'in': u.get('input_tokens', 0),
              'out': u.get('output_tokens', 0)}
        seen[m['id']] = st
        out.append(st)
    return out


def breakdown(path):
    rows, prev, first = {}, 'start-up (the app, CLAUDE.md, the first message)', True
    tot = 0.0
    for st in steps(path):
        r, w, i, o = CW.PRICE[st['fam']]
        k = kind(st['tools'])
        a = rows.setdefault(k, [0, 0.0, 0.0, 0.0])
        b = rows.setdefault(prev, [0, 0.0, 0.0, 0.0])
        a[0] += 1
        a[1] += st['rd'] * r / 1e6                   # re-reading the history
        b[2] += (st['wr'] * w + st['in'] * i) / 1e6  # storing what the step before brought in
        a[3] += st['out'] * o / 1e6                  # what Claude wrote
        prev, first = k, False
    pc = lambda usd: 100 * usd / CW.WEEK_USD
    tot = sum(sum(v[1:]) for v in rows.values())
    print(f'{os.path.basename(path)[:8]}: {sum(v[0] for v in rows.values())} steps, {pc(tot):.2f}% of a week')
    print(f'  {"kind of step":46}{"steps":>6}{"re-read":>9}{"new":>8}{"written":>9}{"total":>8}')
    for k, v in sorted(rows.items(), key=lambda kv: -sum(kv[1][1:])):
        print(f'  {k:46}{v[0]:>6}{pc(v[1]):>9.2f}{pc(v[2]):>8.2f}{pc(v[3]):>9.2f}{pc(sum(v[1:])):>8.2f}')
    c = [sum(v[j] for v in rows.values()) for j in (1, 2, 3)]
    print(f'  {"ALL":46}{"":>6}{pc(c[0]):>9.2f}{pc(c[1]):>8.2f}{pc(c[2]):>9.2f}{pc(tot):>8.2f}')
    return tot


def main():
    paths = sys.argv[1:]
    if not paths:
        d = os.path.expanduser('~/.claude/projects')
        files = [os.path.join(r, f) for r, _, fs in os.walk(d) for f in fs if f.endswith('.jsonl')]
        main_t = max((f for f in files if '/subagents/' not in f), key=os.path.getmtime)
        paths = [main_t] + sorted(glob.glob(os.path.join(os.path.splitext(main_t)[0], '**', '*.jsonl'), recursive=True))
    usd = sum(breakdown(p) for p in paths)
    if len(paths) > 1:
        print(f'All {len(paths)} records (helpers included): {100 * usd / CW.WEEK_USD:.2f}% of a week')


if __name__ == '__main__':
    main()
