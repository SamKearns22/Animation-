import json,sys,re
from collections import defaultdict
e=json.load(open(sys.argv[1]))
g={m.split('.')[-1]:[d.split('*')[0] for d in ds if '*str' not in d] for m,ds in e.items()}
FILM=re.compile(r'^(ad_vanced_notice|bayeux|beaver_asteroid|blessed|burnham|channel_trailer|concept_mother|cryminister|daughter|mother|kitchen|shot$|s\d_|deck_the_halls|duel|ed$|ed_variants|elder_swindon|flying_whales|whale$|gta|halo|hutt|islamocommunism|maul|midterminal|milburn|mossad|netan|newsdesk|patriots|peepee|poker_mon|polanski|power_crime|prepper|press_secretary|professional|protest_tiers|rap|remakes|roadster|russiadent|salt|sam$|shocking|strictly|terfwarts|thepark|park$|traitors|trial_|walker$|wolf$|horror_|animation_test|satire_parts|series$|wolf)')
films=sorted(k for k in g if FILM.match(k))
kit=sorted(k for k in g if not FILM.match(k))
def closure(roots):
    seen=set(); st=list(roots)
    while st:
        x=st.pop()
        for d in g.get(x,[]):
            if d not in seen: seen.add(d); st.append(d)
    return seen
print('FILM FILES',len(films)); print('KIT/TOOL FILES',len(kit)); print(' '.join(kit)); print()
# direct: kit file -> film file
print('== kit files that load a film file DIRECTLY:')
n=0
for k in kit:
    fs=[d for d in g[k] if d in films]
    if fs: n+=1; print(f'  {k}: {" ".join(sorted(set(fs)))}')
print('count',n,'of',len(kit))
print()
for name,roots in [('PEOPLE KIT (people)',['people']),('PLACES KIT (places)',['places']),('figure',['figure']),('views',['views']),('GTA film (gta_*)',[k for k in g if k.startswith('gta')])]:
    c=closure(roots); fc=sorted(x for x in c if x in films and not x.startswith('gta'))
    print(f'== {name}: reaches {len(c)} files, {len(fc)} old-film files:'); print('   '+' '.join(fc))
