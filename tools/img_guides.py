# Pantallas de GUIA (guide2..guide6) -> español
import os
from PIL import Image
from imgtools import save, font, fit_font, text_w, F_GAME, DEC

RED = (179, 3, 0, 255)
LIGHT = (169, 169, 169, 255)
DIM = (93, 93, 93, 255)

X = 542
TITLE_TOP = 571
BODY_TOP = [612, 641, 670]
MAXW = 1128 - X
TITLE_SIZE = 38
BODY_SIZE = 24

clean = Image.open(os.path.join(DEC, 'pictures', '_guide_clean.png')).convert('RGBA')

# (nombre, titulo, [ (linea, color) | [(trozo,color),...] ])
DATA = [
    ('guide2', 'Guardar', [
        [('Pulsa X ante una expendedora → GUARDAR', RED)],
        [('No puedes guardar en máquinas vacías.', LIGHT)],
        [('( Este juego no tiene guardado automático. )', DIM)],
    ]),
    ('guide3', 'Objetivo', [
        [('Recibirás una notificación cada vez', LIGHT)],
        [('que se actualice tu objetivo.', LIGHT)],
        [('Pulsa X → Mensajes → "Carta en cadena"', RED), (' para verlo.', LIGHT)],
    ]),
    ('guide4', 'HP', [
        [('Tu HP se ve en el icono de batería del menú.', LIGHT)],
        [('Si se agota por completo, será Game Over.', RED)],
    ]),
    ('guide5', 'OBJETOS', [
        [('Los objetos no se consumen automáticamente.', RED)],
        [('Tienes que usarlos tú manualmente.', RED)],
        [('Puedes volver a examinar algunos objetos en la pestaña.', LIGHT)],
    ]),
    ('guide6', '???', [
        [('Este valor aumenta durante ciertos eventos.', RED)],
        [('Es una estadística oculta, invisible para el jugador.', LIGHT)],
        [('Ten en cuenta que afecta al ánimo de Rio.', LIGHT)],
    ]),
]

from PIL import ImageDraw

for name, title, lines in DATA:
    src = Image.open(os.path.join(DEC, 'pictures', name + '.png')).convert('RGBA')
    im = clean.copy()
    # el recuadro del icono se conserva del original
    im.paste(src.crop((340, 555, 515, 690)), (340, 555))
    d = ImageDraw.Draw(im)

    ft = fit_font(F_GAME, title, MAXW, TITLE_SIZE)
    d.text((X, TITLE_TOP), title, font=ft, fill=RED, anchor='lt', stroke_width=1, stroke_fill=RED)

    for i, segs in enumerate(lines):
        total = ''.join(s for s, _ in segs)
        fb = fit_font(F_GAME, total, MAXW, BODY_SIZE, 20)
        x = X
        for s, col in segs:
            d.text((x, BODY_TOP[i]), s, font=fb, fill=col, anchor='lt')
            x += text_w(s, fb)
    save(im, 'pictures', name)
    print(name, 'ok  (tamaño cuerpo', fb.size, ')')
