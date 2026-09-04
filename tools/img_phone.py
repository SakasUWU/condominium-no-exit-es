# Rótulos del teléfono en las pantallas de menú ("ITEM / MENU" -> "OBJETOS / MENÚ")
import numpy as np
from PIL import Image, ImageDraw
from imgtools import load_es, save, font, F_UI_B, F_DISPLAY

ANGLE = 17
RED = (196, 12, 4, 255)
WHITE = (205, 205, 205, 255)

import os
from imgtools import DEC
_names = ['Scene_item_back', 'Scene_save_back', 'Scene_gallery_back',
          'Scene_message_back', 'Scene_Load_back', 'Scene_Options_back']
_st = np.stack([np.array(Image.open(os.path.join(DEC, 'pictures', n + '.png')).convert('RGBA')).astype(np.int32)
                for n in _names])
_idx = np.argmin(_st[:, :, :, :3].sum(3), axis=0)
CLEAN = Image.fromarray(np.take_along_axis(_st, _idx[None, :, :, None], axis=0)[0].astype('uint8'), 'RGBA')

LABELS = {
    'Scene_item_back': 'OBJETOS',
    'Scene_save_back': 'GUARDAR',
    'Scene_gallery_back': 'GALERÍA',
    'Scene_message_back': 'MENSAJES',
    'Scene_Load_back': 'CARGAR',
    'Scene_Options_back': 'OPCIONES',
}


def rotated_text(txt, f, color, track=0, angle=ANGLE):
    pad = 30
    w = int(sum(f.getlength(c) + track for c in txt) - track) + 2 * pad
    h = f.size * 2 + 2 * pad
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = pad
    for c in txt:
        d.text((x, pad), c, font=f, fill=color, anchor='lt')
        x += f.getlength(c) + track
    return lay.rotate(angle, resample=Image.BICUBIC, expand=True)


def paste_center(im, lay, cx, cy):
    im.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))


for name, txt in LABELS.items():
    im = load_es('pictures', name)       # parte de la version ya traducida
    im.paste(CLEAN.crop((1040, 410, 1276, 592)), (1040, 410))   # quita el rótulo pequeño
    im.paste((9, 9, 9, 255), (1060, 492, 1252, 585))             # quita "MENU"

    # rótulo pequeño en rojo
    size = 22
    while True:
        f = font(F_UI_B, size)
        w = sum(f.getlength(c) + 6 for c in txt) - 6
        if w <= 138 or size <= 11:
            break
        size -= 1
    paste_center(im, rotated_text(txt, font(F_UI_B, size), RED, track=5), 1146, 494)

    # "MENÚ" grande en blanco
    paste_center(im, rotated_text('MENÚ', font(F_DISPLAY, 48), WHITE, track=1), 1152, 534)
    save(im, 'pictures', name)
    print(name, '->', txt)
