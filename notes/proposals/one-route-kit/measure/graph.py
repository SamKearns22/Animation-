import ast, os, re, json, sys
ROOT='/home/user/Animation-/source'
mods={}
for dp,dn,fn in os.walk(ROOT):
    if '__pycache__' in dp: continue
    for f in fn:
        if f.endswith('.py'):
            p=os.path.join(dp,f); m=os.path.relpath(p,ROOT)[:-3].replace('/','.')
            mods[m]=p
top={m.split('.')[-1]:m for m in mods}
edges={}
for m,p in mods.items():
    src=open(p,errors='replace').read()
    deps=set()
    try: t=ast.parse(src)
    except Exception as e: print('PARSEFAIL',m,e,file=sys.stderr); continue
    for n in ast.walk(t):
        if isinstance(n,ast.Import):
            for a in n.names: deps.add(a.name.split('.')[0])
        elif isinstance(n,ast.ImportFrom) and n.module and n.level==0:
            deps.add(n.module.split('.')[0])
        elif isinstance(n,ast.Call):
            fn=getattr(n.func,'attr',None) or getattr(n.func,'id',None)
            if fn in ('import_module','__import__') and n.args and isinstance(n.args[0],ast.Constant):
                deps.add(str(n.args[0].value).split('.')[0]+'*dyn')
    # string mentions of module names used dynamically
    for s in re.findall(r"['\"]([a-z0-9_]+)['\"]",src):
        if s in top and s!=m.split('.')[-1]: deps.add(s+'*str')
    edges[m]=sorted(d for d in deps if d.rstrip('*dynstr').rstrip('*') in top or d.split('*')[0] in top)
json.dump(edges,open(sys.argv[1],'w'),indent=0)
print(len(mods),'modules')
