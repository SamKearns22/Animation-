import ast,os,sys,re
R='/home/user/Animation-/source'
out={}
for f in sorted(os.listdir(R)):
    if not f.endswith('.py'): continue
    t=ast.parse(open(os.path.join(R,f),errors='replace').read())
    alias={}
    for n in ast.walk(t):
        if isinstance(n,ast.Import):
            for a in n.names: alias[a.asname or a.name]=a.name
    hits=set()
    for n in ast.walk(t):
        tg=[]
        if isinstance(n,ast.Assign): tg=n.targets
        elif isinstance(n,(ast.AugAssign,ast.AnnAssign)): tg=[n.target]
        for x in tg:
            if isinstance(x,ast.Attribute) and isinstance(x.value,ast.Name) and x.value.id in alias:
                hits.add(f'{alias[x.value.id]}.{x.attr}')
        if isinstance(n,ast.Call) and getattr(n.func,'id',None)=='setattr' and n.args and isinstance(n.args[0],ast.Name) and n.args[0].id in alias:
            hits.add(f'{alias[n.args[0].id]}.(setattr)')
    if hits: out[f[:-3]]=sorted(hits)
for k,v in out.items(): print(f'{k} [{len(v)}]: {" ".join(v[:12])}{" ..." if len(v)>12 else ""}')
print('files that rewrite another file\'s parts:',len(out),' total rewrites:',sum(len(v) for v in out.values()))
