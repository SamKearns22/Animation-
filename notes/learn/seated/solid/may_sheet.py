import sys, time; sys.path.insert(0,'source'); sys.path.insert(0,'notes/learn/seated/solid')
from PIL import Image
import sheet_solid as SH
SH.MODE = sys.argv[2] if len(sys.argv)>2 else 'whole'
tiles=[]
for yaw,pose,n in SH.VIEWS:
    t0=time.time(); im,chk=SH.tile('may',yaw,pose,full=True); print(n,chk,round(time.time()-t0,1))
    tiles.append(im.crop((240,620,840,1740)))
W=sum(t.width for t in tiles); page=Image.new('RGB',(W,tiles[0].height),'white')
x=0
for t in tiles: page.paste(t,(x,0)); x+=t.width
page.save(sys.argv[1])
