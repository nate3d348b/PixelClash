"""Deterministically draw original 48x64 pixel-art fighter animations.

96 frames: 32 per fighter, 8 columns per row, 4 rows per fighter.
The indexed PNG atlas is generated in memory for Streamlit.
"""
from PIL import Image, ImageDraw
from io import BytesIO
from pathlib import Path

W,H,COLS=48,64,8
ANIMS={'idle':(0,4),'walk':(4,6),'jump':(10,2),'punch':(12,4),
       'kick':(16,4),'special':(20,4),'hurt':(24,2),'block':(26,2),'ko':(28,4)}
THEMES=[
 dict(id='ember',skin='#f4bb89',shade='#b77360',dark='#37273c',cloth='#e85c41',cloth_hi='#ff9c57',trim='#ffdb72',hair='#7c3036',glow='#ffc75e',pant='#40344c'),
 dict(id='volt',skin='#b98268',shade='#825963',dark='#26344f',cloth='#386eda',cloth_hi='#5ce8ec',trim='#f3e078',hair='#d8e6ee',glow='#94f8ff',pant='#263b74'),
 dict(id='onyx',skin='#94684f',shade='#624656',dark='#262039',cloth='#684b9d',cloth_hi='#ad8fe5',trim='#bfc0db',hair='#29223e',glow='#d8b7ff',pant='#372c59'),
]

def art_frame(d,motion,phase):
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    q=ImageDraw.Draw(im)
    outline=d['dark']
    def box(x0,y0,x1,y1,c):q.rectangle((round(x0),round(y0),round(x1),round(y1)),fill=c)
    def poly(points,col):q.polygon([(round(x),round(y)) for x,y in points],fill=col)
    idle=(motion=='idle'); bob=[0,0,-1,0][phase%4] if idle else 0
    walk=(motion=='walk'); stride=[-4,-2,2,4,2,-2][phase%6] if walk else 0
    air=(motion=='jump'); rise=(2 if phase==0 else -1) if air else 0
    stagger=(motion=='hurt'); recoil=-3 if stagger else 0
    guard=(motion=='block'); punch=(motion=='punch'); kick=(motion=='kick'); cast=(motion=='special'); dead=(motion=='ko')
    if dead:
        q.rectangle((13,52,40,56),fill=outline)
        box(11,51,41,53,d['pant']);box(9,45,23,53,d['cloth'])
        box(24,44,34,51,d['skin']);box(34,43,40,45,d['hair'])
        if phase<2:box(14,38,21,46,d['cloth_hi'])
        return im
    dy=bob-rise
    if air:
        legs=[((16,40),(13,47),(19,51),(23,46)),((26,40),(30,47),(35,48),(30,43))]
    elif kick:
        extension=[3,10,14,4][phase%4]
        legs=[((15,40),(13,53),(21,55),(23,42)),
              ((25,40),(28,44),(35+extension,43),(36+extension,47),(25,49))]
    else:
        legs=[((15,40),(14+stride,54),(22+stride,56),(23,41)),
              ((25,40),(28-stride,54),(36-stride,56),(33,40))]
    for n,pts in enumerate(legs):
        poly(pts,outline)
        poly([(x,y-1) for x,y in pts[:3]],d['pant'])
        sh=(-stride if n else stride)//2
        box((16 if n==0 else 28)+sh,48+dy,(21 if n==0 else 33)+sh,51+dy,d['cloth'])
    if not air and not kick:
        box(12+stride,53+dy,22+stride,57+dy,outline)
        box(13+stride,53+dy,21+stride,55+dy,d['trim'])
        box(27-stride,53+dy,37-stride,57+dy,outline)
        box(28-stride,53+dy,36-stride,55+dy,d['trim'])
    if kick:
        extension=[3,10,14,4][phase%4]
        box(35+extension,42+dy,41+extension,48+dy,outline)
        box(36+extension,43+dy,40+extension,45+dy,d['trim'])
    cx=23+recoil
    if d['id']=='onyx':
        poly([(cx-13,24+dy),(cx+13,24+dy),(cx+15,36+dy),(cx+9,44+dy),(cx-12,44+dy),(cx-16,35+dy)],outline)
        box(cx-12,27+dy,cx+11,40+dy,d['cloth'])
        box(cx-8,30+dy,cx+5,33+dy,d['cloth_hi'])
        box(cx-15,25+dy,cx-9,34+dy,d['trim'])
        box(cx+9,25+dy,cx+15,35+dy,d['trim'])
        box(cx-4,34+dy,cx+3,38+dy,d['dark'])
        box(cx-1,34+dy,cx+1,37+dy,d['glow'])
    elif d['id']=='volt':
        poly([(cx-10,25+dy),(cx+10,25+dy),(cx+12,37+dy),(cx+8,44+dy),(cx-9,44+dy),(cx-11,35+dy)],outline)
        box(cx-9,27+dy,cx+9,41+dy,d['cloth'])
        box(cx-7,28+dy,cx+7,29+dy,d['cloth_hi'])
        box(cx-3,31+dy,cx+3,37+dy,d['trim'])
        box(cx-1,32+dy,cx+1,34+dy,d['glow'])
        box(cx-10,41+dy,cx+10,43+dy,d['trim'])
    else:
        poly([(cx-10,25+dy),(cx+9,24+dy),(cx+12,37+dy),(cx+8,44+dy),(cx-9,44+dy),(cx-12,35+dy)],outline)
        box(cx-9,27+dy,cx+9,41+dy,d['cloth'])
        box(cx-8,29+dy,cx+4,30+dy,d['cloth_hi'])
        poly([(cx+2,29+dy),(cx+8,30+dy),(cx-2,42+dy),(cx-6,42+dy)],d['trim'])
        box(cx-8,41+dy,cx+8,43+dy,d['dark'])
    box(cx-4,23+dy,cx+3,28+dy,d['shade'])
    box(cx-8,10+dy,cx+9,26+dy,outline)
    box(cx-6,12+dy,cx+7,24+dy,d['skin'])
    box(cx-6,22+dy,cx+6,24+dy,d['shade'])
    box(cx+4,17+dy,cx+7,18+dy,outline)
    box(cx+6,18+dy,cx+7,18+dy,'#fff3ce')
    if d['id']=='ember':
        poly([(cx-9,12+dy),(cx-12,9+dy),(cx-6,11+dy),(cx-5,4+dy),(cx,9+dy),(cx+4,2+dy),(cx+8,9+dy),(cx+10,12+dy),(cx+9,16+dy),(cx-9,16+dy)],outline)
        poly([(cx-8,11+dy),(cx-4,6+dy),(cx,10+dy),(cx+4,5+dy),(cx+8,12+dy),(cx+6,15+dy),(cx-7,15+dy)],d['hair'])
        box(cx-3,10+dy,cx+3,11+dy,d['cloth_hi'])
    elif d['id']=='volt':
        poly([(cx-9,14+dy),(cx-9,8+dy),(cx-3,5+dy),(cx+3,8+dy),(cx+10,5+dy),(cx+8,15+dy)],outline)
        box(cx-7,8+dy,cx+6,13+dy,d['hair'])
        box(cx-3,6+dy,cx+3,10+dy,'#fef0ad')
        box(cx-10,17+dy,cx-7,21+dy,d['cloth_hi'])
        box(cx+8,17+dy,cx+11,21+dy,d['glow'])
    else:
        poly([(cx-10,10+dy),(cx-6,5+dy),(cx+5,5+dy),(cx+10,10+dy),(cx+11,18+dy),(cx-10,18+dy)],outline)
        box(cx-8,9+dy,cx+8,15+dy,d['cloth'])
        box(cx-6,11+dy,cx+7,12+dy,d['cloth_hi'])
        box(cx+7,15+dy,cx+10,23+dy,d['trim'])
        box(cx-10,15+dy,cx-7,22+dy,d['trim'])
    poly([(cx-11,27+dy),(cx-16,31+dy),(cx-14,43+dy),(cx-11,44+dy),(cx-8,35+dy)],outline)
    box(cx-16,40+dy,cx-10,46+dy,d['trim'])
    box(cx-14,32+dy,cx-12,39+dy,d['shade'])
    if guard:
        box(cx+5,26+dy,cx+11,32+dy,outline)
        box(cx+8,19+dy,cx+13,32+dy,d['skin'])
        box(cx+7,18+dy,cx+14,23+dy,outline)
        box(cx+8,19+dy,cx+13,21+dy,d['trim'])
        box(cx-12,19+dy,cx-5,32+dy,d['skin'])
        box(cx-13,17+dy,cx-6,22+dy,d['trim'])
    elif punch:
        extend=[5,17,24,9][phase%4]
        box(cx+8,27+dy,cx+14+extend,34+dy,outline)
        box(cx+10,28+dy,cx+14+extend,32+dy,d['skin'])
        box(cx+13+extend,25+dy,cx+21+extend,35+dy,outline)
        box(cx+15+extend,27+dy,cx+19+extend,32+dy,d['trim'])
    elif cast:
        lift=[0,-3,-5,-2][phase%4]
        box(cx+8,24+dy+lift,cx+17,31+dy+lift,outline)
        box(cx+12,26+dy+lift,cx+18,29+dy+lift,d['skin'])
        box(cx+17,21+dy+lift,cx+24,30+dy+lift,d['trim'])
        if phase>0:
            box(cx+24,19+dy+lift,cx+31,26+dy+lift,d['glow'])
            box(cx+26,17+dy+lift,cx+29,28+dy+lift,'#fff7ce')
    else:
        box(cx+9,28+dy,cx+15,42+dy,outline)
        box(cx+10,30+dy,cx+13,40+dy,d['skin'])
        box(cx+8,40+dy,cx+16,47+dy,d['trim'])
    if d['id']=='ember':
        box(cx-11,38+dy,cx-7,45+dy,d['trim'])
        if motion=='idle' and phase%4==2:box(cx+8,24+dy,cx+11,26+dy,'#fff0ab')
    elif d['id']=='volt':
        box(cx-10,30+dy,cx-7,34+dy,d['glow'])
        box(cx+7,37+dy,cx+10,40+dy,d['trim'])
    else:
        box(cx-10,41+dy,cx+10,43+dy,d['trim'])
        box(cx-16,35+dy,cx-12,39+dy,d['cloth_hi'])
    if stagger:box(cx+10,12+dy,cx+12,14+dy,'#fff0aa')
    return im

def build_atlas_png() -> bytes:
    atlas=Image.new('RGBA',(W*COLS,H*12),(0,0,0,0))
    for char_idx,d in enumerate(THEMES):
        for motion,(start,count) in ANIMS.items():
            for phase in range(count):
                n=start+phase
                atlas.alpha_composite(art_frame(d,motion,phase),((n%COLS)*W,(char_idx*4+n//COLS)*H))
    rgb=Image.new('RGB',atlas.size,(255,0,255))
    rgb.paste(atlas,mask=atlas.getchannel('A'))
    out=rgb.quantize(colors=48,method=Image.Quantize.FASTOCTREE)
    transparent_idx=out.getpixel((0,0))
    buf=BytesIO()
    out.save(buf,format='PNG',optimize=True,transparency=transparent_idx)
    return buf.getvalue()

if __name__=='__main__':
    path=Path(__file__).parent/'assets'/'fighters.png'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(build_atlas_png())
    print(f'Wrote {path} ({path.stat().st_size} bytes), 96 animation frames')
