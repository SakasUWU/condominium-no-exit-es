# Menú del título: New Game / Load Game / Option / Exit  ->  español
import os
from PIL import Image
from imgtools import load, save, font, draw_text, text_w, F_DISPLAY

W, H = 300, 110          # ancho ampliado (se compensa en Command Pos de plugins.js)
FRAME = 55
RED = (209, 23, 7, 255)
WHITE = (255, 255, 255, 255)
OUTL = (110, 110, 110, 255)
SHADOW = (0, 0, 0, 90)

# (archivo, [(texto, tamaño)])  primera palabra pequeña, segunda grande, como el original
ITEMS = [
    ('Command_0', [('Nueva', 26), ('Partida', 34)]),
    ('Command_1', [('Cargar', 26), ('Partida', 34)]),
    ('Command_2', [('Opciones', 34)]),
    ('Command_3', [('Salir', 34)]),
]

for name, parts in ITEMS:
    src = load('titles2', name)
    badge = src.crop((0, 0, 20, FRAME))          # la insignia numerada ❶❷❸❹
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    im.alpha_composite(badge, (0, 0))

    for row, (col, outline, ow) in enumerate([(RED, None, 0), (WHITE, OUTL, 2)]):
        x = 30
        base = row * FRAME
        for txt, size in parts:
            f = font(F_DISPLAY, size)
            y = base + 42 - int(0.70 * size)
            draw_text(im, (x, y), txt, f, col, outline=outline, ow=ow,
                      shadow=SHADOW, soff=(3, 3), sblur=2, anchor='ls', condense=0.92)
            x += int(text_w(txt, f) * 0.92) + 8
    save(im, 'titles2', name)
    print(name, '->', [p[0] for p in parts])
