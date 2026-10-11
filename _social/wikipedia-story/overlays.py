from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W,H=2160,3840
GOLD=(201,168,106); RED=(220,80,70); CREAM=(239,227,200); VOID=(11,8,6)
def font(path,size,wght=None):
    f=ImageFont.truetype(path,size)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception as e: print("var",e)
    return f
CIN=lambda s,w=700: font("cinzel.ttf",s,w)
GAR=lambda s,w=400: font("eb-garamond.ttf",s,w)
GARI=lambda s: font("eb-garamond-italic.ttf",s)
MONO=lambda s: font("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",s)
def layer(): return Image.new("RGBA",(W,H),(0,0,0,0))
def glow(im,r=18,a=0.55):
    g=im.filter(ImageFilter.GaussianBlur(r)); 
    al=g.getchannel("A").point(lambda v:int(v*a)); g.putalpha(al)
    out=layer(); out.alpha_composite(g); out.alpha_composite(im); return out
def ctext(d,y,txt,f,fill,spacing=0):
    w=d.textlength(txt,font=f) if not spacing else sum(d.textlength(c,font=f) for c in txt)+spacing*(len(txt)-1)
    x=(W-w)/2
    sw=max(4,f.size//14)
    if not spacing: d.text((x,y),txt,font=f,fill=fill,stroke_width=sw,stroke_fill=VOID+(230,)); return
    for c in txt: d.text((x,y),c,font=f,fill=fill,stroke_width=sw,stroke_fill=VOID+(230,)); x+=d.textlength(c,font=f)+spacing

# 1 Logo
src=Image.open("../../images/4.jpg").convert("L")
a=src.point(lambda v:max(0,min(255,int((v-150)*255/(225-150)))))
bbox=a.point(lambda v:255 if v>40 else 0).getbbox(); a=a.crop(bbox)
logo=Image.new("RGBA",a.size,CREAM+(255,)); logo.putalpha(a)
lw=1300; logo=logo.resize((lw,int(logo.height*lw/logo.width)),Image.LANCZOS)
L=layer(); L.alpha_composite(logo,((W-lw)//2,440)); glow(L,24,0.5).save("l1_logo.png")
logo_bottom=440+logo.height; print("logo bottom",logo_bottom)

# 2 Headline
L=layer(); d=ImageDraw.Draw(L); y=logo_bottom+70
ctext(d,y,"// NEUER EINTRAG",MONO(56),GOLD+(255,),spacing=14)
ctext(d,y+95,"JETZT AUF",CIN(130,700),CREAM+(255,),spacing=18)
ctext(d,y+250,"WIKIPEDIA",CIN(215,900),GOLD+(255,),spacing=10)
glow(L,20,0.6).save("l2_head.png"); head_bottom=y+250+250

# 3 Article card
L=layer(); d=ImageDraw.Draw(L)
cx0,cx1=200,W-200; cy0=head_bottom+50; cy1=cy0+640
d.rounded_rectangle((cx0,cy0,cx1,cy1),radius=28,fill=(15,11,8,225),outline=GOLD+(255,),width=4)
px=cx0+80; yy=cy0+55
d.text((px,yy),"Code Chaos",font=GAR(118,500),fill=(245,240,230,255)); yy+=150
d.line((px,yy,cx1-90,yy),fill=GOLD+(160,),width=3); yy+=30
d.text((px,yy),"aus Wikipedia, der freien Enzyklopädie",font=GARI(54),fill=(185,169,143,255)); yy+=95
body=["Code Chaos ist das Musikprojekt des deutschen","Musikproduzenten Tim Borchert aus Hamburg.","Er produziert seit 2016 Psytrance in den …"]
for line in body: d.text((px,yy),line,font=GAR(62),fill=(230,222,205,255)); yy+=80
print("card text bottom",yy,"card bottom",cy1)
L.save("l3_card.png"); card_bottom=cy1

# 4 Claim
L=layer(); d=ImageDraw.Draw(L); y=card_bottom+80
ctext(d,y,"EINZIGER HI-TECH- & PSYCORE-ACT",CIN(80,800),CREAM+(255,),spacing=4)
ctext(d,y+110,"IN DER DEUTSCHSPRACHIGEN",CIN(80,800),CREAM+(255,),spacing=4)
ctext(d,y+220,"WIKIPEDIA",CIN(104,900),RED+(255,),spacing=8)
glow(L,18,0.55).save("l4_claim.png"); claim_bottom=y+220+115

# 5 URL
L=layer(); d=ImageDraw.Draw(L); y=claim_bottom+60
ctext(d,y,"de.wikipedia.org/wiki/Code_Chaos",MONO(66),GOLD+(255,))
L.save("l5_url.png"); print("url bottom",y+80,"safe limit",H-680)
