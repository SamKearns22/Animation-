import csv, collections, sys
rows = list(csv.DictReader(open(sys.argv[1]), delimiter='\t'))
FIX = {
 'P-same': ('people','Crowds and groups varied by default (city mix, clothes, hats, faces)','ON: change 1 (16 Nov)',0),
 'P-pose': ('people','Poses checked at phone size in their own shot before Sam sees them','YES: change 2 (16 Nov)',0),
 'P-motion': ('people','Group moves varied by default: each person their own timing, style, direction','not built; the next step of change 1',1.0),
 'P-alive': ('people','Nobody in shot is still: idle life and reactions (hits, blinks, glances) by default','partly (headlife); no check',1.0),
 'P-contact': ('people','Contact and eyeline check: hands reach what they hold or hit, feet on ground, eyes on whom they address','partly (rule 83 by hand, LOOKS_AT)',1.0),
 'P-face': ('people','House face everywhere: every person has a mouth and a front face','DONE (Blessed: mouth check)',0),
 'P-extras': ('people','Extras built with the main cast: jobs, clothes, scale, seen from behind','partly (people kit)',1.0),
 'P-like': ('people','Likeness pack and check before a famous face is shown','DONE (rule 49)',0),
 'P-draw': ('people','Drawing faults (glints, floating pockets, arms in hair, broken heads)','no single fix: each its own engine fault, fixed when found',0),
 'P-stage': ('people','Small staging of who stands where','taste',0),
 'E-size': ('effects','Effect sizes checked in metres against the nearest person','not built',0.5),
 'E-place': ('effects','Effects tied to what makes them: fire from windows, cracks inside the pane, hits where things land, glow lights what is near','not built',1.0),
 'E-life': ('effects','Effects that live over time: smoke drifts, debris settles still, blasts build over frames','not built',0.75),
 'E-var': ('effects','Thrown things and fireworks varied by default','not built',0.25),
 'F-plan': ('framing','A composition for each shot, agreed before building (who is where, what fills the frame)','Sam declined a moving rough (16 Nov); framing lessons F1-F12 not in the rulebook',1.0),
 'F-frame': ('framing','Frame check: focus near the centre of the safe area, no empty half-frame, clear of the app buttons','rule 10 has no check; lessons F1, F10',0.5),
 'F-cont': ('framing','Continuity across cuts: same set pieces, same places, nothing pops in','not built',0.5),
 'C-height': ('cameras','Camera height and distance chosen first, for what the shot must read as (lesson F2)','lesson F2 not in the rulebook',0.5),
 'C-move': ('cameras','Camera moves eased and landing on the face','rule 72 (camfeel) exists',0),
 'S-ref': ('sets','Sets and kit built against their reference photos, ticked item by item','partly (reference checklists, rule 89 A2)',0.5),
 'S-clip': ('sets','No one walks through walls or pops out of sight: automatic set clipping check','rule 83, by hand on stills',1.0),
 'S-text': ('sets','Words on signs: fitted, hand-lettered, on a real board in perspective','DONE in EPR (fit_lines, marker font); not in the kit',0.25),
}
by = collections.defaultdict(list)
for r in rows: by[r['fix']].append(r)
W={'S':1,'M':2,'L':3}
out=['# Craft census: what each fix would have saved','',
 'Status: done (craft chat 4, 16 Nov). Sources: European Protests, Ranked (notes/archive/protest-tiers.md), Blessed (notes/archive/blessed-notes-animatics-1-2.md, blessed.md), Remakes (notes/remakes.md, notes/archive/remakes-handovers.md). Craft notes only: no lines, sound, brief changes or questions. Every note with its tags: craft-census/notes.tsv.',
 '','How to read: **saved** = Sam\'s notes the fix would have stopped; **repeats** = of those, notes that came back after a first fix; **weight** = each note counted by its fix cost (small 1, medium 2, large 3), so a fix that saves costly rounds ranks higher. Ranked by weight per % of a week the fix costs to build. Already-made fixes are listed last in each area, to show what is covered.','']
tot=collections.Counter(r['area'] for r in rows); causes=collections.Counter(r['cause'] for r in rows)
out.append(f"**Totals:** {len(rows)} craft notes: "+', '.join(f'{a} {n}' for a,n in tot.most_common())+'. Causes: '+', '.join(f'{c} {n}' for c,n in causes.most_common())+f". Repeats: {sum(r['repeat']=='Y' for r in rows)}.")
out.append('')
for area in ['people','effects','framing','cameras','sets']:
    out.append(f'## {area.capitalize()}'); out.append('')
    out.append('| rank | fix | saved (EPR/Blessed/Remakes) | repeats | weight | cost to build (% week) | where it stands | notes it would have saved |')
    out.append('|---|---|---|---|---|---|---|---|')
    items=[]
    for k,(a,desc,st,cost) in FIX.items():
        rs=[r for r in by.get(k,[]) if r['area']==area or (a==area and r['area']!=area and False)]
        rs=[r for r in by.get(k,[]) if FIX[k][0]==area]
        if not rs: continue
        w=sum(W[r['cost']] for r in rs); rep=sum(r['repeat']=='Y' for r in rs)
        f=collections.Counter(r['film'] for r in rs)
        score = w/cost if cost else -1
        items.append((score,k,desc,st,cost,rs,w,rep,f))
    items.sort(key=lambda x:(x[0]<0,-x[0],-x[6]))
    for i,(score,k,desc,st,cost,rs,w,rep,f) in enumerate(items,1):
        notes='; '.join(f"{r['film'][0]} {r['note']} {r['what']}" for r in rs)
        out.append(f"| {i if score>=0 else '-'} | {desc} | {len(rs)} ({f['EPR']}/{f['Blessed']}/{f['Remakes']}) | {rep} | {w} | {cost or '-'} | {st} | {notes} |")
    out.append('')
left=[r for r in rows if r['fix']=='-']
out.append(f"## Taste calls no fix would have saved ({len(left)})"); out.append('')
out.append('; '.join(f"{r['film'][0]} {r['note']} {r['what']}" for r in left)+'.'); out.append('')
open(sys.argv[2],'w').write('\n'.join(out)+'\n')
allx=[]
for k,(a,desc,st,cost) in FIX.items():
    rs=by.get(k,[])
    if cost and rs: allx.append((sum(W[r['cost']] for r in rs)/cost, sum(W[r['cost']] for r in rs), len(rs), sum(r['repeat']=='Y' for r in rs), a, desc, cost))
allx.sort(reverse=True)
o=['## Across all areas (not yet built, by weight per % of a week)','','| # | area | fix | notes saved | repeats | weight | cost |','|---|---|---|---|---|---|---|']
for i,x in enumerate(allx,1): o.append(f'| {i} | {x[4]} | {x[5]} | {x[2]} | {x[3]} | {x[1]} | {x[6]} |')
o+=['','**Caution (Sam, 16 Nov):** EPR was built with no composition in mind, so its 9 "no composition" framing notes partly record his own late choices; Blessed and Remakes had a script and still gave 10. A moving rough before building was declined on 16 Nov (notes/proposals/epr-lessons.md). The tagging is one chat\'s reading: cause and cost are judgments, counts are exact.','']
t=open(sys.argv[2]).read().split('\n## People',1)
open(sys.argv[2],'w').write(t[0]+'\n'.join(o)+'\n## People'+t[1])
