# Pantalla de fin de demo: botones y texto de agradecimiento
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from imgtools import load, save, font, draw_text, F_UI_B, F_GAME

WHITE = (232, 232, 232, 255)
RED = (195, 7, 0, 255)
SHADOW = (0, 0, 0, 160)

# (nombre, texto, relleno, color, centro x, caja a borrar, y del texto)
BTN = [
    ('demoON_button1', 'Lista de deseos', (11, 11, 11, 255), WHITE, 645, (476, 630, 817, 667), 632),
    ('demoON_button2', 'Lista de deseos', (17, 17, 17, 255), RED,   640, (506, 630, 774, 669), 632),
    ('demoON_button3', 'Síguenos',        (11, 11, 11, 255), WHITE, 1044, (875, 630, 1216, 667), 632),
    ('demoON_button4', 'Síguenos',        (17, 17, 17, 255), RED,   1040, (905, 630, 1173, 669), 632),
]
for name, txt, fillc, col, cx, box, ty in BTN:
    im = load('pictures', name)
    im.paste(fillc, box)
    draw_text(im, (cx, ty), txt, font(F_UI_B, 30), col, shadow=SHADOW, soff=(2, 2), sblur=1,
              condense=0.95, anchor='ma')
    save(im, 'pictures', name)
    print(name, '->', txt)

# ---- demoON_1: velo oscuro sobre el texto y reescritura ----
im = load('pictures', 'demoON_1')
veil = Image.new('RGBA', (1210, 275), (8, 8, 10, 255))
vd = ImageDraw.Draw(veil)
for i in range(10):
    al = int(255 * i / 10)
    vd.line([(0, i), (1210, i)], fill=(8, 8, 10, al))
    vd.line([(0, 274 - i), (1210, 274 - i)], fill=(8, 8, 10, al))
im.alpha_composite(veil, (45, 332))

d = ImageDraw.Draw(im)
draw_text(im, (66, 340), '¡Completada!', font(F_UI_B, 52), (196, 12, 4, 255), condense=0.95, anchor='la')
LINES = [
    (424, 'Gracias por jugar la demo y acompañarnos hasta el final.'),
    (455, 'Tu apoyo y tu interés significan muchísimo para nosotros.'),
    (486, 'Para no perderte las novedades ni la fecha de lanzamiento,'),
    (517, 'añade el juego a tu lista de deseos de Steam y síguenos.'),
]
for y, t in LINES:
    d.text((66, y), t, font=font(F_GAME, 23), fill=(238, 238, 238, 255), anchor='lt')
save(im, 'pictures', 'demoON_1')
print('demoON_1 ok')
