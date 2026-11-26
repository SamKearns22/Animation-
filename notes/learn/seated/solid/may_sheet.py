import sys, time; sys.path.insert(0,'source'); sys.path.insert(0,'notes/learn/seated/solid')
from PIL import Image
import sheet_solid as SH
SH.MODE = sys.argv[2] if len(sys.argv)>2 else 'whole'
tiles=[]
for yaw,pose,n in SH.VIEWS:
    t0=time.time(); im,chk=SH.tile('may',yaw,pose,full=True); print(n,chk,round(time.time()-t0,1))
    # chat 10 (Sam's side-view shoes, 26 Nov: the old crop 240-840 x 620-1740 cut her toes and soles off): the whole
    # person and chair in every tile, and the sheet stops if anything drawn touches the crop's edge
    import numpy as np
    a = np.asarray(im).astype(int); ys, xs = np.where(np.abs(a - np.array([232, 232, 226])).sum(-1) > 30)
    C = (200, 600, 940, 1780)
    if xs.min() <= C[0] or xs.max() >= C[2] - 1 or ys.min() <= C[1] or ys.max() >= C[3] - 1:
        sys.exit(f'FAULT: {n} runs off the sheet tile ({xs.min()}-{xs.max()}, {ys.min()}-{ys.max()}; crop {C})')
    tiles.append(im.crop(C))
W=sum(t.width for t in tiles); page=Image.new('RGB',(W,tiles[0].height),'white')
x=0
for t in tiles: page.paste(t,(x,0)); x+=t.width
page.save(sys.argv[1])
