from PIL import Image, ImageDraw, ImageFont
import os
BASE=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-bikeways-brief-2026-11-15")
art=os.path.join(BASE,"hero_source","media-generation-hero-art-nashville-bikeways-0-ae751b2f-8737-491d-b003-b71a276a0e05.webp")
img=Image.open(art).convert("RGB"); W,H=img.size
d=ImageDraw.Draw(img,"RGBA")
for y in range(int(H*0.58)):
    a=int(215*(1-y/(H*0.58))+45); d.line([(0,y),(W,y)],fill=(18,18,18,min(a,240)))
def font(sz,bold=True):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,sz)
def wrap(text,f,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
d.text((60,60),"45.6 of 314.9",font=font(int(W*0.085)),fill=(232,163,61))
y=60+int(W*0.115); f2=font(int(W*0.036))
for line in wrap("Only 14.5% of Nashville's bikeway miles are protected lanes - 45.5% are signed shared routes",f2,W-120):
    d.text((60,y),line,font=f2,fill=(255,255,255)); y+=int(W*0.050)
source="Source: Nashville Bikeways layer, 510 segments (pulled Nov 15, 2026) - recorded miles, 499 length-carrying segments"
fs=font(int(W*0.019),False); sl=wrap(source,fs,W-120)
yy=H-int(W*0.026)*len(sl)-24
for line in sl: d.text((60,yy),line,font=fs,fill=(235,235,235)); yy+=int(W*0.026)
open(os.path.join(BASE,"hero-headline.txt"),"w").write("45.6 of 314.9 - only 14.5% of Nashville's recorded bikeway miles are protected lanes; 45.5% are signed shared routes\n"+source+"\n")
img.save(os.path.join(BASE,"hero.png")); print("hero saved", img.size)
