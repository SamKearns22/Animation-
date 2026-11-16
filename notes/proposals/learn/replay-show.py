import re,subprocess,sys,json
rows={}
for l in open('notes/archive/blessed-notes-animatics-1-2.md'):
    p=[x.strip() for x in l.split('|')]
    if len(p)>6 and p[1].isdigit(): rows[int(p[1])]=(p[4],p[7] if len(p)>7 else '')
# note -> tokens the fix text names (functions/constants/kit pieces), hand-read from the fix column
T={1:['HEAD_K'],2:['chin_long'],8:['gaze','turn'],9:['ears_hidden'],11:['camera','zoom'],12:['press_spots'],
13:['mouth','front'],14:['neck','bald'],16:['seat'],18:['cot_top'],19:['LINES'],20:['phone'],22:['chair'],
23:['zoom','neck'],24:['flash','photograph'],27:['music'],30:['gates2'],31:['gates2','zoom'],32:['G2_PART','gates2'],
35:['LINES','shall'],37:['dock','cy'],38:['music'],43:['pool','chair'],44:['tvroom','voice'],45:['checks','mouth'],
46:['gates2','gates']}
out=[]
for n,toks in sorted(T.items()):
    if n not in rows: continue
    note=re.sub(r'[^A-Za-z0-9\' ]',' ',rows[n][0])[:160]
    r=subprocess.run(['python3','source/page.py','blessed','show',note],capture_output=True,text=True)
    txt=r.stdout
    hits=[t for t in toks if re.search(re.escape(t),txt,re.I)]
    out.append((n,len(txt.splitlines()),len(txt)//4,hits,toks))
    print(n,len(txt.splitlines()),'lines',len(txt)//4,'tok','HIT' if hits else 'MISS',hits,'of',toks)
h=sum(1 for o in out if o[3]);print(h,len(out))
