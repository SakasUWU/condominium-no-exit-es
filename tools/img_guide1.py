# guide1: barra de controles -> español
import os
from PIL import Image, ImageDraw
from imgtools import save, font, F_GAME, DEC

LIGHT = (169, 169, 169, 255)
clean = Image.open(os.path.join(DEC, 'pictures', '_guide_clean.png')).convert('RGBA')
src = Image.open(os.path.join(DEC, 'pictures', 'guide1.png')).convert('RGBA')

im = src.copy()
# borra solo las palabras, restaurando el fondo limpio
for box in [(518, 576, 608, 614), (713, 576, 850, 614), (956, 618, 1170, 664)]:
    im.paste(clean.crop(box), (box[0], box[1]))

d = ImageDraw.Draw(im)
f = font(F_GAME, 27)
d.text((526, 585), 'Mover', font=f, fill=LIGHT, anchor='lt')
d.text((721, 585), 'Correr', font=f, fill=LIGHT, anchor='lt')
d.text((964, 629), 'Menú, Cancelar', font=font(F_GAME, 25), fill=LIGHT, anchor='lt')
save(im, 'pictures', 'guide1')
print('guide1 ok')
