# Títulos de los créditos (ch1_end*) -> español
from PIL import Image, ImageDraw
from imgtools import load, save, font, F_GAME

BG = (4, 4, 4, 255)
RED = (160, 18, 4, 255)
CX = 640

HEADS = {
    'ch1_end1': [((304, 335), 'EDITORA')],
    'ch1_end2': [((211, 242), 'GUION / PRODUCCIÓN'), ((446, 477), 'ARTE / DISEÑO')],
    'ch1_end3': [((284, 315), 'MÚSICA')],
    'ch1_end4': [((252, 283), 'EFECTOS DE SONIDO')],
    'ch1_end5': [((251, 282), 'APOYO GRÁFICO')],
    'ch1_end6': [((201, 232), 'PLUGINS')],
    'ch1_end7': [((294, 325), 'TIPOGRAFÍA')],
    'ch1_end8': [((202, 233), 'PRUEBAS'), ((411, 442), 'AGRADECIMIENTOS')],
}

TRACK = 3
SIZE = 29

for name, heads in HEADS.items():
    im = load('pictures', name)
    d = ImageDraw.Draw(im)
    f = font(F_GAME, SIZE)
    for (y0, y1), txt in heads:
        im.paste(BG, (200, y0 - 8, 1080, y1 + 8))
        w = sum(f.getlength(c) + TRACK for c in txt) - TRACK
        x = CX - w / 2
        for c in txt:
            d.text((x, y0 - 2), c, font=f, fill=RED, anchor='lt')
            x += f.getlength(c) + TRACK
    save(im, 'pictures', name)
    print(name, [t for _, t in heads])
