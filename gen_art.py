import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math, random

BLACK = np.array([6,6,6])
BLACK2 = np.array([12,12,12])
GOLD = np.array([205,163,95])
GOLD_LIGHT = np.array([242,220,160])
GOLD_DEEP = np.array([138,106,52])
WHITE = np.array([245,244,239])

def lerp(a,b,t):
    return a + (b-a)*t

def radial_gradient(w,h,cx,cy,inner,outer,inner_col,outer_col,power=1.0):
    y,x = np.mgrid[0:h,0:w]
    cx_px, cy_px = cx*w, cy*h
    maxr = math.hypot(max(cx_px,w-cx_px), max(cy_px,h-cy_px))
    d = np.sqrt((x-cx_px)**2 + (y-cy_px)**2) / maxr
    d = np.clip(d, 0, 1) ** power
    out = np.zeros((h,w,3))
    for c in range(3):
        out[:,:,c] = lerp(inner_col[c], outer_col[c], d)
    return out

def add_noise(arr, amount=6):
    noise = np.random.normal(0, amount, arr.shape[:2])
    out = arr.copy()
    for c in range(3):
        out[:,:,c] += noise
    return out

def vignette(arr, strength=0.35):
    h,w = arr.shape[:2]
    y,x = np.mgrid[0:h,0:w]
    cx,cy = w/2,h/2
    maxr = math.hypot(cx,cy)
    d = np.sqrt((x-cx)**2+(y-cy)**2)/maxr
    v = 1 - strength*np.clip(d-0.4,0,1)
    out = arr.copy()
    for c in range(3):
        out[:,:,c] *= v
    return out

def to_img(arr):
    arr = np.clip(arr,0,255).astype(np.uint8)
    return Image.fromarray(arr, 'RGB')

def draw_arcs(draw, w, h, cx, cy, n, col, width=1, alpha=140, r0=0.15, r1=1.3):
    for i in range(n):
        t = i/max(1,n-1)
        r = (r0 + (r1-r0)*t) * min(w,h)
        bbox = [cx-r, cy-r, cx+r, cy+r]
        a = int(alpha * (1-t*0.7))
        draw.ellipse(bbox, outline=col+(a,), width=width)

def draw_radiating_lines(draw, w, h, cx, cy, n, length, col, alpha=90, width=1, start_r=40):
    for i in range(n):
        ang = (i/n) * 2*math.pi
        x0 = cx + math.cos(ang)*start_r
        y0 = cy + math.sin(ang)*start_r
        x1 = cx + math.cos(ang)*(start_r+length)
        y1 = cy + math.sin(ang)*(start_r+length)
        a = int(alpha * random.uniform(0.4,1))
        draw.line([x0,y0,x1,y1], fill=col+(a,), width=width)

def draw_diagonal_stripes(draw, w, h, n, col, alpha=60, width=2, angle=35):
    step = (w+h)/n
    for i in range(-n, n*2):
        x = i*step
        draw.line([x, 0, x - h/math.tan(math.radians(angle)), h], fill=col+(alpha,), width=width)

def draw_particles(draw, w, h, n, col_a, col_b, seed=0):
    random.seed(seed)
    for _ in range(n):
        x = random.uniform(0,w)
        y = random.uniform(0,h)
        r = random.uniform(0.6, 3.2)
        use_gold = random.random() < 0.6
        col = col_a if use_gold else col_b
        a = int(random.uniform(60,220))
        draw.ellipse([x-r,y-r,x+r,y+r], fill=col+(a,))

def compose(base_arr, overlay_img):
    base = to_img(base_arr).convert('RGBA')
    out = Image.alpha_composite(base, overlay_img)
    return out.convert('RGB')

def save(img, path, quality=88):
    img.save(path, quality=quality)
    print('saved', path, img.size)

random.seed(42)
np.random.seed(42)

OUT = '/home/claude/lr63-site/assets/img/generated'

# ---------------------------------------------------------------
# Showcase panels — 5 distinct abstract compositions, 4:5 ratio
# ---------------------------------------------------------------
SW, SH = 1200, 1500

def showcase_1():
    base = radial_gradient(SW,SH, 0.25,0.2, 0,1, GOLD_DEEP*0.5, BLACK, power=1.6)
    base = vignette(base, 0.4)
    base = add_noise(base, 4)
    img = to_img(base).convert('RGBA')
    ov = Image.new('RGBA', (SW,SH), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    draw_arcs(d, SW, SH, SW*0.22, SH*0.18, 10, tuple(GOLD.astype(int)), width=1, alpha=130, r0=0.05, r1=0.9)
    draw_particles(d, SW, SH, 220, tuple(GOLD_LIGHT.astype(int)), tuple(WHITE.astype(int)), seed=1)
    ov = ov.filter(ImageFilter.GaussianBlur(0.4))
    return compose(base, ov)

def showcase_2():
    base = radial_gradient(SW,SH, 0.8,0.75, 0,1, GOLD*0.55, BLACK2, power=1.4)
    base = vignette(base, 0.42)
    base = add_noise(base, 4)
    img = to_img(base).convert('RGBA')
    ov = Image.new('RGBA', (SW,SH), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    draw_diagonal_stripes(d, SW, SH, 26, tuple(GOLD_LIGHT.astype(int)), alpha=45, width=2, angle=28)
    draw_arcs(d, SW, SH, SW*0.8, SH*0.78, 6, tuple(WHITE.astype(int)), width=1, alpha=90, r0=0.05, r1=0.5)
    ov = ov.filter(ImageFilter.GaussianBlur(0.3))
    return compose(base, ov)

def showcase_3():
    base = radial_gradient(SW,SH, 0.5,0.15, 0,1, GOLD_LIGHT*0.5, BLACK, power=2.0)
    base = vignette(base, 0.45)
    base = add_noise(base, 4)
    img = to_img(base).convert('RGBA')
    ov = Image.new('RGBA', (SW,SH), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    draw_radiating_lines(d, SW, SH, SW*0.5, SH*0.14, 60, SH*0.9, tuple(GOLD.astype(int)), alpha=55, width=1, start_r=20)
    ov = ov.filter(ImageFilter.GaussianBlur(0.4))
    return compose(base, ov)

def showcase_4():
    base = radial_gradient(SW,SH, 0.15,0.85, 0,1, GOLD_DEEP*0.6, BLACK2, power=1.5)
    base = vignette(base, 0.4)
    base = add_noise(base, 4)
    img = to_img(base).convert('RGBA')
    ov = Image.new('RGBA', (SW,SH), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    draw_particles(d, SW, SH, 320, tuple(GOLD.astype(int)), tuple(GOLD_LIGHT.astype(int)), seed=4)
    draw_arcs(d, SW, SH, SW*0.15, SH*0.88, 8, tuple(GOLD_LIGHT.astype(int)), width=1, alpha=110, r0=0.05, r1=0.7)
    ov = ov.filter(ImageFilter.GaussianBlur(0.3))
    return compose(base, ov)

def showcase_5():
    base = radial_gradient(SW,SH, 0.6,0.4, 0,1, GOLD*0.5, BLACK, power=1.7)
    base = vignette(base, 0.42)
    base = add_noise(base, 4)
    img = to_img(base).convert('RGBA')
    ov = Image.new('RGBA', (SW,SH), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    draw_diagonal_stripes(d, SW, SH, 18, tuple(WHITE.astype(int)), alpha=25, width=1, angle=-32)
    draw_arcs(d, SW, SH, SW*0.6, SH*0.42, 12, tuple(GOLD_LIGHT.astype(int)), width=1, alpha=120, r0=0.03, r1=1.1)
    ov = ov.filter(ImageFilter.GaussianBlur(0.35))
    return compose(base, ov)

for i, fn in enumerate([showcase_1, showcase_2, showcase_3, showcase_4, showcase_5], start=1):
    img = fn()
    save(img, f'{OUT}/showcase-{i}.jpg')

# ---------------------------------------------------------------
# Hero background — wide abstract linework, sits behind headline
# ---------------------------------------------------------------
HW, HH = 2400, 1400
base = radial_gradient(HW,HH, 0.78,0.15, 0,1, GOLD_DEEP*0.55, BLACK, power=1.8)
base2 = radial_gradient(HW,HH, 0.05,0.9, 0,1, GOLD_DEEP*0.3, BLACK, power=2.0)
base = np.minimum(255, base*0.7 + base2*0.5)
base = vignette(base, 0.5)
base = add_noise(base, 3)
ov = Image.new('RGBA', (HW,HH), (0,0,0,0))
d = ImageDraw.Draw(ov)
draw_arcs(d, HW, HH, HW*0.82, HH*0.1, 14, tuple(GOLD.astype(int)), width=1, alpha=90, r0=0.03, r1=1.4)
draw_particles(d, HW, HH, 260, tuple(GOLD_LIGHT.astype(int)), tuple(WHITE.astype(int)), seed=7)
ov = ov.filter(ImageFilter.GaussianBlur(0.5))
img = compose(base, ov)
save(img, f'{OUT}/hero-bg.jpg', quality=85)

# ---------------------------------------------------------------
# Growth section frame panels — 2 small abstract textures
# ---------------------------------------------------------------
def growth_panel(w,h,cx,cy,seed):
    base = radial_gradient(w,h,cx,cy,0,1, GOLD_DEEP*0.5, BLACK, power=1.6)
    base = add_noise(base, 4)
    ov = Image.new('RGBA', (w,h), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    draw_radiating_lines(d, w, h, w*cx, h*cy, 34, max(w,h)*0.7, tuple(GOLD.astype(int)), alpha=70, width=1, start_r=10)
    ov = ov.filter(ImageFilter.GaussianBlur(0.3))
    return compose(base, ov)

save(growth_panel(700,900,0.3,0.3,11), f'{OUT}/growth-panel-1.jpg')
save(growth_panel(500,700,0.7,0.6,12), f'{OUT}/growth-panel-2.jpg')

# ---------------------------------------------------------------
# About section side texture — tall soft gradient with fine lines
# ---------------------------------------------------------------
AW, AH = 1000, 1400
base = radial_gradient(AW,AH,0.5,0.0,0,1, WHITE*0.96, np.array([230,228,220]), power=1.2)
ov = Image.new('RGBA', (AW,AH), (0,0,0,0))
d = ImageDraw.Draw(ov)
draw_arcs(d, AW, AH, AW*0.5, AH*0.05, 16, tuple(GOLD_DEEP.astype(int)), width=1, alpha=50, r0=0.02, r1=1.3)
ov = ov.filter(ImageFilter.GaussianBlur(0.3))
img = compose(base, ov)
save(img, f'{OUT}/about-texture.jpg', quality=85)

# ---------------------------------------------------------------
# Service panel background art — 5 subtle full-bleed textures
# ---------------------------------------------------------------
PW, PH = 1000, 1200
service_specs = [
    ('social', 0.25, 0.1, GOLD_DEEP),
    ('meta', 0.9, 0.05, GOLD_DEEP),
    ('google', 0.05, 0.95, GOLD_DEEP),
    ('growth', 0.85, 0.9, GOLD_DEEP),
    ('digital', 0.5, 0.05, GOLD_DEEP),
]
for name, cx, cy, col in service_specs:
    base = radial_gradient(PW,PH,cx,cy,0,1, col*0.55, BLACK, power=1.7)
    base = add_noise(base,3)
    ov = Image.new('RGBA', (PW,PH), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    draw_particles(d, PW, PH, 90, tuple(GOLD.astype(int)), tuple(GOLD_LIGHT.astype(int)), seed=hash(name)%1000)
    ov = ov.filter(ImageFilter.GaussianBlur(0.3))
    img = compose(base, ov)
    save(img, f'{OUT}/service-{name}.jpg')

print('DONE')
