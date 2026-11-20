import math

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def rgb2lab(rgb):
    r, g, b = [lin(x) for x in rgb]
    X = r * 0.4124 + g * 0.3576 + b * 0.1805
    Y = r * 0.2126 + g * 0.7152 + b * 0.0722
    Z = r * 0.0193 + g * 0.1192 + b * 0.9505
    Xn, Yn, Zn = 0.95047, 1.0, 1.08883
    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(X / Xn), f(Y / Yn), f(Z / Zn)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))

def de(a, b):
    la, lb = rgb2lab(hex2rgb(a)), rgb2lab(hex2rgb(b))
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(la, lb)))

light = {'ems': '#0284c7', 'fire': '#b91c1c', 'admin': '#475569', 'util': '#78716c'}
dark = {'ems': '#38bdf8', 'fire': '#f87171', 'admin': '#94a3b8', 'util': '#a8a29e'}
for name, cols in (('light', light), ('dark', dark)):
    print('---', name)
    for n, c in cols.items():
        print(f"{n:5s} {c}  dE-vs-admin {de(c, cols['admin']):5.2f}  "
              f"dE-vs-ems {de(c, cols['ems']):5.2f}  dE-vs-fire {de(c, cols['fire']):5.2f}")
