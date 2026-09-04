# message_into3-1 (mensajes distorsionados) y message_into4-1 (aviso PSA)
import random
import numpy as np
from PIL import Image, ImageDraw
from imgtools import load, save, font, F_GAME, text_w

BX0, BX1 = 354, 729
RED = (196, 22, 10, 255)
WHITE = (238, 238, 238, 255)
BLOCK = (110, 110, 110, 255)
HEAD_C = (71, 71, 71, 255)

random.seed(7)

# ---------- message_into3-1 : globos con texto distorsionado ----------
GLITCH = ['B¡envenida Ri0', 'P0r f1n nos vem0s', 'Est@ vez',
          'Pued0 recuperarl0', 'Ven a buscarm3', 'D0nde todo empez0']
BUBS3 = [(212, 257), (286, 331), (337, 382), (388, 433), (439, 484), (490, 535)]

im = load('pictures', 'message_into3-1')
d = ImageDraw.Draw(im)
for (y0, y1), txt in zip(BUBS3, GLITCH):
    im.paste((26, 26, 26, 255), (BX0 + 6, y0 + 5, BX1 - 6, y1 - 5))
    x = 368
    base = y0 + 12
    for ch in txt:
        s = random.choice([19, 21, 23, 25])
        f = font(F_GAME, s)
        dy = random.randint(-4, 4)
        d.text((x, base + dy), ch, font=f, fill=RED, anchor='lt')
        x += f.getlength(ch) + random.choice([-1, 0, 1, 2])
save(im, 'pictures', 'message_into3-1')
print('message_into3-1 ok')

# ---------- message_into4-1 : aviso de la estación ----------
im = load('pictures', 'message_into4-1')
d = ImageDraw.Draw(im)

# globo rojo superior
im.paste((26, 26, 26, 255), (BX0 + 6, 210, 749, 295))
f = font(F_GAME, 20)
d.text((366, 221), '[REVISADO] Normas de inspección', font=f, fill=RED, anchor='lt')
d.text((366, 243), 'Siga las instrucciones de abajo.', font=f, fill=RED, anchor='lt')

# globo inferior: se conservan las viñetas ❶❷❸ de la izquierda
im.paste((25, 25, 25, 255), (382, 317, 749, 529))
LINES = [
    (327, 'Conserve una sola pertenencia'),
    (348, 'personal y deseche la masa inútil.'),
    (385, 'Registre el █ que lo define en el'),
    (405, 'documento. Un █ sin rellenar'),
    (426, 'lo asentará aquí para siempre.'),
    (457, 'Incumplir lo clasifica como █.'),
    (478, 'Se procederá de inmediato a su'),
    (498, 'trituración y borrado.'),
]
f = font(F_GAME, 19)
for y, txt in LINES:
    x = 386
    parts = txt.split('█')
    for i, part in enumerate(parts):
        if part:
            d.text((x, y), part, font=f, fill=WHITE, anchor='lt')
            x += text_w(part, f)
        if i < len(parts) - 1:
            d.rectangle([x + 1, y + 3, x + 25, y + 17], fill=BLOCK)
            x += 28
save(im, 'pictures', 'message_into4-1')
print('message_into4-1 ok')
