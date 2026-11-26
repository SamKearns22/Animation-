#!/usr/bin/env python3
"""Open Wounds note 15 (Sam, 26 Nov: "you might want to draw the room so that you have an understanding of where
everyone goes and when"): shot 3 from above, the room, the doors, the corridor and its cross passage, each guest and
wolf's path with the seconds into the shot. python3 source/ow_room_plan.py OUT.png"""
import sys; sys.path.insert(0,'source'); OUTP=sys.argv[1]; sys.argv=['x']
from PIL import Image, ImageDraw
import brexit_is_done_action as A, moves as MV
W,H=900,1300; img=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(img)
def P(x,dd): return (450+x*110, 1250-dd*75)
# room
d.rectangle([P(-5,7)[0],P(-5,7)[1],P(5,1)[0],P(5,1)[1]],outline='black',width=2)
d.line([P(-5,7),P(-1.9,7)],fill='saddlebrown',width=6); d.line([P(-0.1,7),P(5,7)],fill='saddlebrown',width=6)
for xw in (-1.9,-0.1):
    d.line([P(xw,7),P(xw,13.35)],fill='black',width=3); d.line([P(xw,14.95),P(xw,15.95)],fill='black',width=3)
d.line([P(-1.9,15.95),P(-0.1,15.95)],fill='steelblue',width=5)
d.line([P(-4,13.35),P(-1.9,13.35)],fill='black',width=2);d.line([P(-4,14.95),P(-1.9,14.95)],fill='black',width=2)
d.line([P(-0.1,13.35),P(3,13.35)],fill='black',width=2);d.line([P(-0.1,14.95),P(3,14.95)],fill='black',width=2)
d.ellipse([P(0.3,2.3)[0]-14,P(0.3,2.3)[1]-14,P(0.3,2.3)[0]+14,P(0.3,2.3)[1]+14],fill='darkred'); d.text((P(0.3,2.3)[0]+18,P(0.3,2.3)[1]),'BLAIR',fill='darkred')
d.text(P(-4.8,15.5),'cross passage',fill='black'); d.text(P(-1.8,16.3),'window',fill='steelblue')
d.line([(450,1250),P(-6,12)],fill=(200,200,200)); d.line([(450,1250),P(6,12)],fill=(200,200,200)); d.text((460,1230),'camera',fill='gray')
cols=['black','purple','green','orange']
mv=MV.chase_movers(A.PASSES,A.GUEST_V,A.WOLF_V)
for name,i,at in mv:
    if i>3: continue
    k=A.PASSES[i][0]; wolf=name.startswith('wolf')
    prev=None
    for n in range(0,60):
        t=-3+n*0.1; a=at(t)
        if a is None: continue
        q=P(a[0]+(0.12 if wolf else 0),a[1])
        if prev: d.line([prev,q],fill=cols[k],width=1 if wolf else 3)
        prev=q
        if abs(round(t,1)*2-round(t*2))<1e-6 and round(t,1)%0.5==0:
            d.text((q[0]+4,q[1]-6),('w' if wolf else 'g')+f'{t:.1f}',fill=cols[k])
d.text((10,10),'Shot 3 from above: guests (thick) and wolves (thin), seconds into the shot; doors open at 0.3',fill='black')
img.save(OUTP)
