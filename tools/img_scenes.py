# Fondos de las pantallas del menú (Scene_*_back) -> español
import numpy as np
from PIL import Image, ImageDraw
from imgtools import load, save, font, F_UI_B, F_UI, F_GAME, text_w

BG = (8, 8, 8, 255)
PILL = (171, 171, 171, 255)

def brightest_red(im, box):
    a = np.array(im.crop(box)).astype(int)
    m = (a[:, :, 3] > 200)
    if not m.sum():
        return (200, 30, 20, 255)
    px = a[m]
    return tuple(int(v) for v in px[px[:, 0].argmax()])

def tracked(d, xy, txt, f, fill, track):
    x, y = xy
    for ch in txt:
        d.text((x, y), ch, font=f, fill=fill, anchor='lt')
        x += f.getlength(ch) + track
    return x

# --- cabeceras y "Back" -------------------------------------------------
HEAD = {
    'Scene_item_back': 'LISTA',
    'Scene_gallery_back': 'GALERÍA',
    'Scene_message_back': 'MENSAJES',
    'Scene_save_back': 'GUARDAR',
    'Scene_Load_back': 'CARGAR',
    'Scene_Options_back': 'GENERAL',
}

results = {}
for name, head in HEAD.items():
    im = load('pictures', name)
    red = brightest_red(im, (200, 74, 620, 110))
    d = ImageDraw.Draw(im)
    im.paste(BG, (207, 74, 620, 110))
    f = font(F_UI_B, 27)
    tracked(d, (210, 78), head, f, red, 5)

    # "Back" -> "Atrás"
    box = (196, 632, 330, 666)
    im.paste(BG, box)
    d.text((198, 636), 'Atrás', font=font(F_UI, 24), fill=(235, 235, 235, 255), anchor='lt')
    results[name] = im

# --- Scene_item_back: "ITEM HELP" --------------------------------------
im = results['Scene_item_back']
d = ImageDraw.Draw(im)
red = brightest_red(load('pictures','Scene_item_back'), (200, 465, 620, 500))
im.paste(BG, (207, 465, 620, 500))
tracked(d, (210, 469), 'DESCRIPCIÓN', font(F_UI_B, 27), red, 5)

# --- Scene_Options_back: SOUND + etiquetas --------------------------------
im = results['Scene_Options_back']
d = ImageDraw.Draw(im)
red = brightest_red(load('pictures','Scene_Options_back'), (200, 351, 620, 387))
im.paste(BG, (207, 351, 620, 387))
tracked(d, (210, 355), 'SONIDO', font(F_UI_B, 27), red, 5)

PILLS = [((119, 175), 'Correr siempre'), ((190, 246), 'Velocidad de texto'), ((261, 317), 'Pantalla completa'),
         ((398, 454), 'Volumen BGM'), ((469, 525), 'Volumen BGS'), ((540, 596), 'Volumen SE')]
for (y0, y1), txt in PILLS:
    im.paste(PILL, (178, y0 + 5, 525, y1 - 5))
    cy = (y0 + y1) // 2
    f = font(F_UI, 30)
    while f.getlength(txt) > 330:
        f = font(F_UI, f.size - 1)
    d.text(((178 + 525) // 2, cy), txt, font=f, fill=(20, 20, 20, 255), anchor='mm')

for name, im in results.items():
    save(im, 'pictures', name)
    print(name, 'ok')
