"""Test: chosen look (steps + paper) vs chosen look + paper-edge bevel + layered drop shadows. Pictures at 12/s, shown at 24."""
import os, sys
from multiprocessing import Process
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC='/home/user/Animation-/source'; sys.path.insert(0,SRC); os.chdir(SRC)
S=os.path.dirname(os.path.abspath(__file__)); FR=os.path.join(S,'frames2'); os.makedirs(FR,exist_ok=True)
FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',36)
sys.path.insert(0,S); import twostyles as T
def shift(a,dx,dy):
    return np.roll(np.roll(a,dy,0),dx,1)
def edges(img):
    a=np.asarray(img,np.float32)/255
    lum=a.mean(2)
    outline=(lum<0.22).astype(np.float32)           # the black house outline
    # drop shadow: outline shape pushed 4px right/down (light from upper left), softened, only where it lands on colour
    m=Image.fromarray((outline*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
    sh=shift(np.asarray(m,np.float32)/255,3,4)*(1-outline)
    a=a*(1-0.28*sh[...,None])
    # bevel: light on edges facing up-left, dark on edges facing down-right (2px so it survives the side-by-side)
    up=lum-shift(lum,0,2); lf=lum-shift(lum,2,0)
    b=np.clip((up+lf)*0.5,-0.2,0.2)*(1-outline)
    a=a+b[...,None]*0.9
    return Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))
def lab(d,x,t):
    w=d.textlength(t,font=FONT); d.rectangle([x-w/2-12,316,x+w/2+12,376],fill='white'); d.text((x-w/2,322),t,font=FONT,fill='black')
def work(i0,i1):
    import ad_vanced_notice as A
    P=np.asarray(Image.open(os.path.join(S,'paper.png')).convert('L'),np.float32)/255
    for i in range(i0,i1):
        out=os.path.join(FR,f'{i:05d}.jpg')
        if os.path.exists(out): continue
        t=i/24; j=i-i%2
        pic=A.picture(j/24).convert('RGB')
        base=T.paper(pic,P); fancy=T.paper(edges(pic),P)
        L=A.overlay(base.convert('RGBA'),t).convert('RGB').resize((540,960),Image.LANCZOS)
        R=A.overlay(fancy.convert('RGBA'),t).convert('RGB').resize((540,960),Image.LANCZOS)
        c=Image.new('RGB',(1080,1920),(32,32,32)); c.paste(L,(0,400)); c.paste(R,(540,400))
        d=ImageDraw.Draw(c); lab(d,270,'STEPS + PAPER'); lab(d,810,'+ EDGES + SHADOWS'); c.save(out,quality=90)
if __name__=='__main__':
    n=int(round(45.29*24)); k=4; b=[n*x//k for x in range(k+1)]
    # even frames only get drawn fresh; odd frames reuse the pair's picture (cheap: picture() is cached per call, so just run all)
    ps=[Process(target=work,args=(b[x],b[x+1])) for x in range(k)]
    [p.start() for p in ps]; [p.join() for p in ps]; print('frames',len(os.listdir(FR)))
