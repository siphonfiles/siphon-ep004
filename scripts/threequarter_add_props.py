"""Free (CPU) fix of the three-quarter reference: paste the clipped paper stack and the loose sheets from the front reference
(cut out, scaled, sheared for the new angle, darkened/warmed to the local light, soft contact shadow) onto the mirrored image."""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import sys
f=Image.open('presenter/reference/thomas_ref_v1_source_1344x768.png').convert('RGB')
m=Image.open('presenter/reference/thomas_ref_threequarter_s55_mirrored.png').convert('RGB')
def cut(poly, box, thr=95, extra=None):
    mk=Image.new('L',f.size,0); ImageDraw.Draw(mk).polygon(poly,fill=255)
    lum=(f.split()[2] if thr>=120 else f.convert('L')).point(lambda v:255 if v>thr else 0).filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(5))
    from PIL import ImageChops
    mk=ImageChops.multiply(mk,lum)
    if extra: ImageDraw.Draw(mk).rectangle(extra,fill=255)
    mk=mk.filter(ImageFilter.GaussianBlur(1.2))
    mk=mk.point(lambda v: 0 if v<8 else v)
    return f.crop(box), mk.crop(box)
def place(img,mk,scale,bright,pos,shear=0.0):
    w,h=img.size; W,H=int(w*scale),int(h*scale)
    img=img.resize((W,H),Image.LANCZOS); mk=mk.resize((W,H),Image.LANCZOS)
    if shear:
        img=img.transform((W,H),Image.AFFINE,(1,shear,-shear*H/2,0,1,0),Image.BICUBIC)
        mk=mk.transform((W,H),Image.AFFINE,(1,shear,-shear*H/2,0,1,0),Image.BICUBIC)
    img=ImageEnhance.Brightness(img).enhance(bright)
    r,g,b=img.split(); img=Image.merge('RGB',(r.point(lambda v:min(255,int(v*1.0))),g.point(lambda v:int(v*0.86)),b.point(lambda v:int(v*0.72))))
    # soft contact shadow
    sh=Image.new('L',m.size,0); sm=mk.point(lambda v:int(v*0.35)).filter(ImageFilter.GaussianBlur(6))
    sh.paste(sm,(pos[0]+4,pos[1]+6))
    m.paste(Image.new('RGB',m.size,(0,0,0)),(0,0),sh)
    m.paste(img,pos,mk)
s_img,s_mk=cut([(240,608),(445,607),(476,628),(472,670),(200,673),(192,656)],(185,600,482,680),thr=90,extra=(268,652,362,676))
place(s_img,s_mk,1.25,0.5,(30,668),shear=0.12)
import numpy as np
def sheet(poly,col,off=(3,5)):
    sh=Image.new('L',m.size,0); ImageDraw.Draw(sh).polygon([(x+off[0],y+off[1]) for x,y in poly],fill=150)
    m.paste(Image.new('RGB',m.size,(0,0,0)),(0,0),sh.filter(ImageFilter.GaussianBlur(5)))
    mk=Image.new('L',m.size,0); ImageDraw.Draw(mk).polygon(poly,fill=255); mk=mk.filter(ImageFilter.GaussianBlur(0.7))
    xs=[p[0] for p in poly]; ys=[p[1] for p in poly]
    W,H=m.size; gx=np.linspace(0,1,W)[None,:]; gy=np.ones((H,1))
    # brighter toward the lamp (right)
    k=np.clip(0.80+0.25*((gx*W-min(xs))/(max(xs)-min(xs)+1)),0.75,1.05)*gy
    base=np.zeros((H,W,3)); base[...]=col; base=(base*k[...,None]).clip(0,255).astype('uint8')
    layer=Image.fromarray(base); d=ImageDraw.Draw(layer)
    # faint text lines
    for i in range(1,6):
        t=i/7; a=(poly[0][0]+(poly[3][0]-poly[0][0])*t, poly[0][1]+(poly[3][1]-poly[0][1])*t)
        b=(poly[1][0]+(poly[2][0]-poly[1][0])*t, poly[1][1]+(poly[2][1]-poly[1][1])*t)
        a=(a[0]+(b[0]-a[0])*0.1,a[1]+(b[1]-a[1])*0.1); b=(a[0]+(b[0]-a[0])*0.85,a[1]+(b[1]-a[1])*0.85)
        d.line([a,b],fill=tuple(int(c*0.94) for c in col),width=1)
    m.paste(layer,(0,0),mk)
m.save('presenter/reference/thomas_ref_threequarter_s55_mirrored_props.png')
