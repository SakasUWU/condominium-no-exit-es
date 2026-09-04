# Pantallas del mensajero (message_into*) -> español
import numpy as np
from PIL import Image, ImageDraw
from imgtools import load, save, font, F_GAME, text_w

HEAD_C = (71, 71, 71, 255)
HEAD_CX, HEAD_TOP = 574, 151
WHITE = (238, 238, 238, 255)
GREY = (150, 150, 150, 255)
RED = (196, 22, 10, 255)
BX0, BX1 = 354, 729


def bubbles(a):
    """Bandas verticales que son globos de texto."""
    m = a[:, :, 3] > 100
    wide = (m[:, BX0:BX1].sum(1) > 150)
    out, s = [], None
    for i, v in enumerate(wide):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s > 30:
                out.append((s, i))
            s = None
    if s is not None:
        out.append((s, len(wide)))
    return out


def lines_in(a, y0, y1):
    sub = a[y0:y1, BX0 + 6:BX1 - 6]
    m = (sub[:, :, 3] > 150) & (np.abs(sub[:, :, :3] - 26).sum(2) > 90)
    rows = m.sum(1)
    out, s = [], None
    for i, v in enumerate(rows):
        if v > 0 and s is None:
            s = i
        elif v == 0 and s is not None:
            if i - s > 3:
                out.append(s + y0)
            s = None
    if s is not None:
        out.append(s + y0)
    return out


def draw_bubble(im, a, y0, y1, lines, size=20, x=367):
    """lines: lista de listas de (texto, color, negrita)"""
    from collections import Counter
    reg = a[y0 + 8:y1 - 8, BX0 + 8:BX1 - 8].reshape(-1, 4)
    col = Counter(map(tuple, reg.tolist())).most_common(1)[0][0]
    col = tuple(int(v) for v in col)
    im.paste(col, (BX0 + 6, y0 + 5, BX1 - 6, y1 - 5))
    tops = lines_in(a, y0, y1)
    if len(tops) != len(lines):        # reparte uniformemente si no coincide
        pitch = 25
        h = pitch * len(lines)
        start = y0 + (y1 - y0 - h) // 2 + 4
        tops = [start + i * pitch for i in range(len(lines))]
    d = ImageDraw.Draw(im)
    for top, segs in zip(tops, lines):
        top += 2
        cx = x
        for txt, c, bold in segs:
            f = font(F_GAME, size)
            d.text((cx, top), txt, font=f, fill=c, anchor='lt',
                   stroke_width=1 if bold else 0, stroke_fill=c)
            cx += text_w(txt, f) + (2 if bold else 0)


def header(im, txt, size=19):
    im.paste((0, 0, 0, 0), (430, 140, 720, 176))
    ImageDraw.Draw(im).text((HEAD_CX, HEAD_TOP), txt, font=font(F_GAME, size),
                            fill=HEAD_C, anchor='ma')


B = (RED, False)
W = (WHITE, False)
G = (GREY, False)

DATA = {
    'message_into1-1': ('Carta en cadena', [
        [[('[Mensaje web]', GREY[0], True)],
         [('Esta cadena empezó hace años.', GREY[0], False)],
         [('Reenvíala y tendrás suerte... ', GREY[0], False), ('(Más)', GREY[0], True)]],
        [[('• ', RED, False), ('Sal del tren.', WHITE, False)],
         [('• ', RED, False), ('Sube al andén.', WHITE, False)],
         [('• ', RED, False), ('Sal de la estación.', WHITE, False)]],
    ]),
    'message_into1-2': ('Carta en cadena', [
        [[('• ', RED, False), ('Encuentra la salida de la estación.', WHITE, False)]],
    ]),
    'message_into1-3': ('Carta en cadena', [
        [[('• ', RED, False), ('Encuentra el bolso perdido.', WHITE, False)],
         [('◆ ', GREY[0], False), ('Registra la estación a fondo.', GREY[0], False)]],
    ]),
    'message_into1-4': ('Carta en cadena', [
        [[('• ', RED, False), ('Descubre qué ', WHITE, False), ('exige este lugar', WHITE, True), ('.', WHITE, False)],
         [('• ', RED, False), ('Cuando estés lista, ve a la salida.', WHITE, False)]],
    ]),
    'message_into2-1': ('Jun', [
        [[('¿Por qué te fuiste así antes?', WHITE, False)],
         [('No tenías nada de buena cara.', WHITE, False)],
         [('Mira, sé que me pasé un poco.', WHITE, False)]],
        [[('Llámame cuando leas esto, ¿sí?', WHITE, False)]],
    ]),
}

for name, (head, bubs) in DATA.items():
    im = load('pictures', name)
    a = np.array(im).astype(int)
    bs = bubbles(a)
    header(im, head)
    for (y0, y1), lines in zip(bs, bubs):
        draw_bubble(im, a, y0, y1, lines)
    save(im, 'pictures', name)
    print(name, 'globos', bs)
