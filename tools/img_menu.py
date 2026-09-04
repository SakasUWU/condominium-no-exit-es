# Etiquetas del menú del teléfono (Item/Save/Option/Messenger/Gallery/Quit)
import numpy as np
from PIL import Image
from imgtools import load, save, font, draw_text, F_DISPLAY

RED = (180, 5, 0, 255)
OUT = (13, 14, 14, 255)
GREY = (178, 178, 178, 255)

# nombre, banda del icono (y0,y1), banda de la etiqueta (y0,y1), texto
ITEMS = [
    ('menu_item',    (229, 308), (314, 334), 'Objetos'),
    ('menu_save',    (365, 444), (449, 469), 'Guardar'),
    ('menu_option',  (500, 578), (585, 605), 'Opciones'),
    ('menu_message', (365, 444), (448, 468), 'Mensajes'),
    ('menu_photo',   (229, 308), (314, 334), 'Galería'),
    ('menu_exit',    (500, 578), (585, 605), 'Salir'),
]
SIZE = 27

for name, icon_band, lab_band, txt in ITEMS:
    for suffix, col, outline, ow in [('', RED, OUT, 3), ('_quick', GREY, None, 0)]:
        src = load('pictures', name + suffix)
        a = np.array(src)
        m = a[:, :, 3] > 30
        # centro horizontal del icono
        icon = m[icon_band[0]:icon_band[1]]
        nz = np.nonzero(icon.sum(0))[0]
        cx = int((nz.min() + nz.max()) / 2)
        im = src.copy()
        im.paste((0, 0, 0, 0), (0, lab_band[0] - 8, src.width, lab_band[1] + 10))
        draw_text(im, (cx, lab_band[0] - 3), txt, font(F_DISPLAY, SIZE), col,
                  outline=outline, ow=ow, condense=0.88, anchor='ma')
        save(im, 'pictures', name + suffix)
    print(name, '->', txt)
