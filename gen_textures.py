from PIL import Image, ImageDraw, ImageFilter
import math, random

S = 4  # supersampling

def ss(size):
    return Image.new("RGBA", (size*S, size*S), (0,0,0,0))

def finish(img, size):
    return img.resize((size, size), Image.LANCZOS)

def lerp(a, b, t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(len(a)))

GOLD_L = (255, 236, 160, 255)
GOLD   = (222, 170, 60, 255)
GOLD_D = (128, 82, 22, 255)
DARK   = (28, 22, 18, 255)

# ---------- wheel.png (256) : rueda de 8 radios (dharma wheel) ----------
def make_wheel(size=256):
    im = ss(size); d = ImageDraw.Draw(im)
    c = size*S/2
    def R(v): return v*S
    # glow
    glow = Image.new("RGBA", im.size, (0,0,0,0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([c-R(120), c-R(120), c+R(120), c+R(120)], outline=(255,200,80,160), width=R(10))
    glow = glow.filter(ImageFilter.GaussianBlur(R(6)))
    im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    # aro exterior con degradado radial
    for i in range(18):
        t = i/17
        col = lerp(GOLD_L, GOLD_D, t)
        r = R(112) - i*R(0.9)
        d.ellipse([c-r, c-r, c+r, c+r], outline=col, width=R(1)+1)
    # aro grueso
    d.ellipse([c-R(112), c-R(112), c+R(112), c+R(112)], outline=GOLD_D, width=R(3))
    d.ellipse([c-R(98), c-R(98), c+R(98), c+R(98)], outline=GOLD_D, width=R(2))
    d.ellipse([c-R(80), c-R(80), c+R(80), c+R(80)], outline=GOLD, width=R(7))
    # radios
    for k in range(8):
        a = k*math.pi/4
        ca, sa = math.cos(a), math.sin(a)
        # radio principal
        px, py = -sa, ca
        for w, col in ((R(9), GOLD_D), (R(6), GOLD), (R(2.4), GOLD_L)):
            d.line([c+ca*R(26), c+sa*R(26), c+ca*R(110), c+sa*R(110)], fill=col, width=int(w))
        # mango/empuñadura exterior
        ex, ey = c+ca*R(118), c+sa*R(118)
        d.ellipse([ex-R(9), ey-R(9), ex+R(9), ey+R(9)], fill=GOLD_D)
        d.ellipse([ex-R(7), ey-R(7), ex+R(7), ey+R(7)], fill=GOLD)
        d.ellipse([ex-R(3), ey-R(3), ex+R(3), ey+R(3)], fill=GOLD_L)
    # moyú
    d.ellipse([c-R(30), c-R(30), c+R(30), c+R(30)], fill=GOLD_D)
    d.ellipse([c-R(26), c-R(26), c+R(26), c+R(26)], fill=GOLD)
    d.ellipse([c-R(18), c-R(18), c+R(18), c+R(18)], fill=DARK)
    d.ellipse([c-R(12), c-R(12), c+R(12), c+R(12)], fill=(255,120,30,255))
    d.ellipse([c-R(6), c-R(6), c+R(6), c+R(6)], fill=(255,230,150,255))
    return finish(im, size)

# ---------- node.png (32): aro circular blanco (se tiñe en código) ----------
def make_node(size=32):
    im = ss(size); d = ImageDraw.Draw(im); c = size*S/2
    d.ellipse([c-14*S, c-14*S, c+14*S, c+14*S], fill=(255,255,255,70))
    d.ellipse([c-14*S, c-14*S, c+14*S, c+14*S], outline=(255,255,255,255), width=2*S)
    d.ellipse([c-11*S, c-11*S, c+11*S, c+11*S], outline=(255,255,255,120), width=1*S)
    return finish(im, size)

# ---------- glow.png (64): halo radial ----------
def make_glow(size=64):
    im = Image.new("RGBA", (size, size), (0,0,0,0)); px = im.load(); c = (size-1)/2
    for y in range(size):
        for x in range(size):
            r = math.hypot(x-c, y-c)/c
            a = max(0.0, 1-r); a = a**2.2
            px[x,y] = (255,255,255,int(255*a))
    return im

# ---------- entity/wheel.png (64): atlas para el modelo 3D ----------
# (0..32,0..32)=oro con bisel  (32..64,0..32)=oro oscuro  (0..32,32..64)=cara con grabado  (32..64,32..64)=gema brillante
def make_atlas():
    im = Image.new("RGBA", (64,64), (0,0,0,255)); px = im.load(); rnd = random.Random(7)
    def fillq(x0,y0,base_l,base_d):
        for y in range(32):
            for x in range(32):
                t = (x+y)/62
                n = rnd.randint(-6,6)
                col = lerp(base_l, base_d, t)
                px[x0+x, y0+y] = tuple(max(0,min(255,col[i]+n)) for i in range(3))+(255,)
        for i in range(32):  # borde biselado
            for (x,y) in ((i,0),(i,31),(0,i),(31,i)):
                px[x0+x,y0+y] = lerp(base_l,(255,255,255,255),0.35)
    fillq(0,0,(255,222,120,255),(200,140,40,255))
    fillq(32,0,(170,110,30,255),(90,55,15,255))
    fillq(0,32,(240,200,100,255),(170,115,35,255))
    d = ImageDraw.Draw(im)
    d.rectangle([4,36,27,59], outline=(110,70,20,255))
    d.line([6,47,25,47], fill=(110,70,20,255)); d.line([16,38,16,57], fill=(110,70,20,255))
    for y in range(32):
        for x in range(32):
            r = math.hypot(x-15.5,y-15.5)/16
            col = lerp((255,255,255,255),(150,150,150,255),min(1,r))
            px[32+x,32+y] = col
    return im

base = "src/main/resources/assets/mahoraga/textures/"
make_wheel().save(base+"gui/wheel.png")
make_node().save(base+"gui/node.png")
make_glow().save(base+"gui/glow.png")
make_atlas().save(base+"entity/wheel.png")
print("ok")
